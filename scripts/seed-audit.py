#!/usr/bin/env python3
"""Seed the LusakaRide AUDIT database with dense, realistic sample data.

Talking to the live API (not the DB) so every write flows through the same
business rules as production:

  1. Admin login (email/password)              → admin token
  2. Driver identity: admin-create (+ OTP login), admin-approve
  3. Driver vehicle: make/model, create, admin-approve, equip
  4. Itineraries: named runs (idempotent by Name), published to Open
  5. Passenger login (mock OTP)                 → passenger token
  6. Bookings on the seeded itineraries (per-segment seats via SlotEngine)

Rerun-safe: identities/plates/itinerary names are deterministic and looked up
before creating. Env overrides:

  LR_API       default http://localhost:5287
  LR_ADMIN_EMAIL / LR_ADMIN_PASSWORD   dev admin creds
  LR_PASSENGER_PHONE   default 260971234567 (audit tester)
  LR_DRIVER_PHONE      default 260971234568 (audit driver)
  LR_OTP               default 123456 (mock)

Usage: python3 scripts/seed-audit.py
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

BASE = os.environ.get('LR_API', 'http://localhost:5287').rstrip('/')
ADMIN_EMAIL = os.environ.get('LR_ADMIN_EMAIL', 'admin@lusaka-ride.co.zm')
ADMIN_PASSWORD = os.environ.get('LR_ADMIN_PASSWORD', 'Admin@1234')
PASSENGER_PHONE = os.environ.get('LR_PASSENGER_PHONE', '260971234567')
DRIVER_PHONE = os.environ.get('LR_DRIVER_PHONE', '260971234568')
OTP = os.environ.get('LR_OTP', '123456')

created: dict[str, str] = {}


def call(method: str, path: str, token: Optional[str] = None, body: Any = None) -> tuple[int, Any]:
    url = BASE + path
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header('Content-Type', 'application/json')
    if token:
        req.add_header('Authorization', f'Bearer {token}')
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read()
            payload = json.loads(raw) if raw else {}
            return resp.status, payload
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            payload = json.loads(raw) if raw else {}
        except Exception:
            payload = {'raw': raw.decode(errors='replace')}
        return e.code, payload


def step(label: str) -> None:
    print(f'— {label}')


def admin_login() -> str:
    step('admin login')
    code, payload = call('POST', '/api/auth/admin/login', body={
        'email': ADMIN_EMAIL, 'password': ADMIN_PASSWORD,
    })
    if code != 200:
        raise SystemExit(f'admin login failed {code}: {payload}')
    return payload['accessToken']


def passenger_login() -> str:
    step('passenger login (mock OTP)')
    call('POST', '/api/auth/passenger/send-otp', body={'phone': PASSENGER_PHONE})
    code, payload = call('POST', '/api/auth/passenger/verify-otp', body={
        'phone': PASSENGER_PHONE, 'code': OTP,
    })
    if code not in (200, 201):
        raise SystemExit(f'passenger verify failed {code}: {payload}')
    return payload['accessToken']


def driver_signup(admin: str) -> tuple[str, str]:
    step('driver identity (create/lookup + login + approve)')
    code, created_driver = call('POST', '/api/drivers', token=admin, body={
        'name': 'Audit Driver',
        'phone': f'+{DRIVER_PHONE}',
        'licenseNumber': f'AUDIT-{DRIVER_PHONE[-4:]}',
    })
    # 201 create / 409 already-exists both fine — pull the id either way.
    driver_id = None
    if code == 201 and isinstance(created_driver, dict):
        driver_id = created_driver.get('id') or created_driver.get('Id')
    if not driver_id:
        # Look him up from the admin list.
        code_l, listing = call('GET', '/api/drivers', token=admin)
        rows = listing.get('items', listing) if isinstance(listing, dict) else listing
        for row in rows:
            phones = {row.get('phone'), row.get('maskedPhone')}
            if any(f'{DRIVER_PHONE}' in str(ph) for ph in phones):
                driver_id = row.get('id')
                break
    if not driver_id:
        raise SystemExit(f'driver lookup failed (create={code}): {created_driver}')

    call('POST', '/api/auth/driver/send-otp', body={'phone': f'+{DRIVER_PHONE}'})
    code_v, verify = call('POST', '/api/auth/driver/verify-otp', body={
        'phone': f'+{DRIVER_PHONE}', 'code': OTP,
    })
    if code_v != 200:
        raise SystemExit(f'driver OTP verify failed {code_v}: {verify}')
    token = verify['accessToken']

    code_a, _ = call('POST', f'/api/drivers/{driver_id}/approve', token=admin)
    if code_a not in (200, 204):
        print(f'   approve -> {code_a} (may already be approved)')
    return driver_id, token


def seed_vehicle(admin: str, driver_token: str) -> str:
    step('vehicle (make/model + create + approve + equip)')
    code, makes = call('GET', '/api/vehicle-makes', token=admin)
    make = (makes[0] if isinstance(makes, list) and makes else None)
    if make is None:
        raise SystemExit(f'no vehicle makes: {makes}')
    code, models = call('GET', f'/api/vehicle-makes/{make["id"]}/models', token=admin)
    model = (models[0] if isinstance(models, list) and models else None)
    if model is None and isinstance(models, dict):
        # Some endpoints return {items: [...]}; remember shape on rerun.
        model = (models.get('items') or [None])[0]
    if model is None:
        raise SystemExit(f'no models for make {make["id"]}: {models}')

    plate = f'AUD-{DRIVER_PHONE[-4:]}'
    code_d, drivers_list = call('GET', '/api/vehicles', token=driver_token)
    # Generic ListingService items returned under `items` when PagedResult.
    candidates = []
    for response in (drivers_list,):
        rows = response.get('items') if isinstance(response, dict) else response
        if isinstance(rows, list):
            candidates = rows
    vehicle_id = next((v['id'] for v in candidates if v.get('plateNumber') == plate), None)

    if not vehicle_id:
        code_c, vehicle = call('POST', '/api/vehicles', token=driver_token, body={
            'makeId': make['id'],
            'modelId': model['id'],
            'year': 2021,
            'plateNumber': plate,
            'seatCount': 14,
            'color': '#1A6634',
        })
        if code_c not in (200, 201):
            raise SystemExit(f'vehicle create failed {code_c}: {vehicle}')
        vehicle_id = vehicle['id']

    code_a, _ = call('POST', f'/api/vehicles/{vehicle_id}/approve', token=admin)
    if code_a not in (200, 204):
        print(f'   vehicle approve -> {code_a} (may already be approved)')

    code_e, equip = call('POST', f'/api/vehicles/{vehicle_id}/equip', token=driver_token)
    if code_e not in (200, 204):
        print(f'   equip -> {code_e}: {equip} (may already be equipped)')
    return vehicle_id


def seed_itineraries(admin: str) -> list[dict]:
    step('itineraries (idempotent by name) + publish')
    code, locations = call('GET', '/api/locations')
    rows = locations.get('items') if isinstance(locations, dict) else locations
    if not rows:
        raise SystemExit(f'no locations: {locations}')
    # Expect the auto-seeded Lusaka hub set; take a chain of stops in id order
    # as stored, minimum 2.
    stops = [r['id'] for r in rows][:5]
    names = {r['id']: r.get('name', '?') for r in rows}

    plans = [
        ('AUDIT Zed Audit AM 07:30 Arcades→Ibex', 1, stops[:3]),
        ('AUDIT Zed Audit Midday 12:10 Town Loop', 4, stops[:4]),
        ('AUDIT Zed Audit Evening 17:45 Libala→Makeni', 8, stops[2:5]),
    ]
    now = datetime.now(timezone.utc)
    seeded = []
    for name, hours_ahead, chain in plans:
        # Idempotency: admin list then name match.
        code_l, existing = call('GET', '/api/itineraries?includeDrafts=true', token=admin)
        rows_e = existing.get('items') if isinstance(existing, dict) else existing
        if isinstance(rows_e, list) and any(r.get('name') == name for r in rows_e):
            match = next(r for r in rows_e if r.get('name') == name)
            seeded.append(match)
            print(f'   exists: {name} ({match.get("status", "?")})')
            continue

        departure = now + timedelta(hours=hours_ahead, minutes=0)
        code_c, itin = call('POST', '/api/itineraries', token=admin, body={
            'name': name,
            'stopIds': chain,
            'departureTime': departure.isoformat(),
            'autoCloseMinutes': 10,
        })
        if code_c not in (200, 201):
            raise SystemExit(f'itinerary create failed {code_c}: {itin}')
        code_p, pub = call('POST', f'/api/itineraries/{itin["id"]}/publish', token=admin)
        if code_p not in (200, 204):
            print(f'   publish -> {code_p}: {pub}')
        chain_names = ' → '.join(names.get(s, s[:6]) for s in chain)
        print(f'   created: {name} [{chain_names}]')
        itin['status'] = 'Open'
        seeded.append(itin)
    return seeded


def seed_assignments(admin: str, driver_token: str, vehicle_id: str, itineraries: list[dict]) -> int:
    step('driver self-assignments (sets per-segment capacity)')
    done = 0
    for it in itineraries:
        itin_id = it['id']
        # Idempotency: the driver's own assignment list.
        code_l, my_assignments = call('GET', '/api/itinerary-assignments', token=driver_token)
        rows = my_assignments.get('items') if isinstance(my_assignments, dict) else my_assignments
        if isinstance(rows, list) and any(r.get('itineraryId') == itin_id for r in rows):
            print(f'   assignment exists: {it["name"][:34]}')
            done += 1
            continue
        code_c, assign = call('POST', '/api/itinerary-assignments', token=driver_token, body={
            'itineraryId': itin_id,
            'vehicleId': vehicle_id,
            'offeredSeatCount': 14,
        })
        if code_c in (200, 201):
            done += 1
            print(f'   assigned: {it["name"][:34]}')
        else:
            print(f'   assign {code_c}: {json.dumps(assign)[:140] if isinstance(assign, dict) else assign}')
    return done


def seed_bookings(passenger_token: str, admin: str, itineraries: list[dict]) -> int:
    step('bookings for the audit passenger')
    if not itineraries:
        print('   nothing to book on')
        return 0
    found = 0
    for itin in itineraries:
        stops = (itin.get('stopIds') if itin.get('stopIds') is not None else None)
        if not stops:
            # List rows carry stopCount only — pull the detail for location ids.
            code_d, detail = call('GET', f'/api/itineraries/{itin["id"]}', token=admin)
            stops = []
            if code_d == 200 and isinstance(detail, dict):
                for s in (detail.get('stops') or []):
                    loc = s.get('locationId') or s.get('id')
                    if loc:
                        stops.append(loc)
        if len(stops) < 2:
            print(f'   skip (no stop ids): {itin["name"][:34]}')
            continue
        code_b, booking = call('POST', '/api/bookings', token=passenger_token, body={
            'itineraryId': itin['id'],
            'boardingLocationId': stops[0],
            'alightingLocationId': stops[-1],
        })
        if code_b in (200, 201):
            found += 1
            seats = (booking.get('seatCount') if isinstance(booking, dict) else None)
            print(f'   booked OK {itin["name"][:34]} (status={booking.get("status", "?")}, seats={seats})')
        else:
            body = json.dumps(booking)[:160] if isinstance(booking, dict) else booking
            print(f'   booking {code_b} on {itin["name"][:34]}: {body}')
    return found


def main() -> None:
    started = time.time()
    admin = admin_login()
    passenger = passenger_login()
    driver_id, driver_token = driver_signup(admin)
    vehicle_id = seed_vehicle(admin, driver_token)
    itineraries = seed_itineraries(admin)
    seed_assignments(admin, driver_token, vehicle_id, itineraries)
    bookings = seed_bookings(passenger, admin, itineraries)

    print('\n=== SEED SUMMARY ===')
    print(f'driver  : {driver_id}')
    print(f'vehicle : {vehicle_id}')
    print(f'itins   : {[i.get("name", "?")[:40] for i in itineraries]}')
    print(f'bookings: {bookings} confirmed')
    print(f'seconds : {time.time() - started:.1f}')


if __name__ == '__main__':
    main()
