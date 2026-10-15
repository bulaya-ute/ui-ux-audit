# Free stock-image sources — verified 2026-10-15

Reference for audits/creative work when a site needs real imagery without
legal encumbrance. Verified against their license pages this session.

## Verified license terms (session-fetched from their pages)

- **[Pexels](https://www.pexels.com/license/)** — free for any use, no
  attribution required. Forbidden: selling unaltered copies as stock/prints;
  implying product endorsement by the subjects; redistribution on other stock
  platforms; using uploads inside service marks.
- **[Pixabay](https://pixabay.com/service/license-summary/)** — free use, no
  attribution required, modifications allowed. Forbidden: standalone resale,
  prints on merchandise when recognizable trademarks/logos appear, immoral
  use with recognizable people, mark usage.
- **[Unsplash](https://unsplash.com/license)** — free for commercial and
  personal use, no attribution required, modifications allowed. Forbidden:
  selling unaltered copies, compiling a competing stock service. NOTE: their
  license page 401s some automated fetchers — re-verify manually when citing
  exact terms.
- **Wikimedia Commons** — per-file licenses (CC0/Public-domain/CC BY/CC BY-SA).
  Attribution REQUIRED for CC BY/BY-SA (artist + license + link). BY-SA also
  binds scaled/edited derivatives to the same license.
- **[Openverse](https://api.openverse.org/v1/images/)** — CC-licensed search
  index (Flickr/Wikimedia + more). REST: `GET /v1/images/?license=cc0,pdm&q=…`
  anonymously (rate-limited: ~20 req/min); responses include a ready-to-paste
  `attribution` string, `foreign_landing_url`, and thumbnail URL.

## Practical access patterns this session

1. **Place-honest photos of real cities** (e.g. Lusaka): Commons has genuine
   local imagery search engines lack. QA the burning question — does the file
   carry burned-in ad/magazine text? (The Lusaka "Bus Terminus" original did;
   rejected.) API: `commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category:X&gcmtype=file&prop=imageinfo&iiprop=url%7Cextmetadata…`
   — filter on width/height + LicenseShortName.
2. **Direct file URLs** via `commons.wikimedia.org/wiki/Special:FilePath/<FileName>`
   (redirects to the raw file; send a User-Agent — Commons rejects empty agents).
   Confirm content-type with `file` before trusting a download.
3. **Thumbnails at target width**: `iiprop=url&iiurlwidth=1600` returns
   `thumburl` for CDN-resized versions (smaller than originals).
4. **Attribution string** every CC file's `extmetadata.Artist` +
   `LicenseShortName` + `LicenseUrl` — copy into `docs/IMAGE-CREDITS.md`
   with: source file page, author, license link, where used, and the exact
   required credit line.

## Honesty rules (audit context)

- **Place-honesty**: never style a photo of another city as the audited
  place (trust anti-pattern — W-family). Every image should genuinely depict
  the place/product claim it supports.
- Check for burned-in third-party claims (magazine typography, promo text)
  before wiring — those make claims our page can't stand behind.
- People in photos must not appear in a way that would embarrass them
  (Pexels clause); incidental street crowds on public roads are standard
  acceptably, focal-point strangers less so.
- Prefer images over text-heavy explanations ONLY where a photo genuinely
  supports comprehension; our marketing page needed two grounded strips, not
  a photo gallery.
