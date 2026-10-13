#!/usr/bin/env python3
"""Render an ASCII wireframe from DOM rect JSON (see references/wireframe.md).

Input: JSON list of {"tag","cls","x","y","w","h"} (y in page coordinates).
Output: ASCII grid drawing, boxes scaled to --width columns.

Usage:
    python3 wireframe.py boxes.json --width 90 [--height 60]
    cat boxes.json | python3 wireframe.py --width 90
"""
import argparse
import json
import sys

TL, TR, BL, BR = "┌", "┐", "└", "┘"
H, V = "─", "│"


def scale(boxes, cols, rows_cap=None, pad=1):
    xs = [b["x"] for b in boxes] + [b["x"] + b["w"] for b in boxes]
    ys = [b["y"] for b in boxes] + [b["y"] + b["h"] for b in boxes]
    x0, x1 = min(xs), max(xs)
    y0, y1 = min(ys), max(ys)
    sx = (cols - pad * 2) / max(1, x1 - x0)
    sy = min(sx / 2, (rows_cap if rows_cap else y1 - y0 or 1) / max(1, y1 - y0))
    return [{
        **b,
        "cx": int((b["x"] - x0) * sx) + pad,
        "cw": max(2, int(b["w"] * sx)),
        "cy": int((b["y"] - y0) * sy) + pad,
        "ch": max(1, int(b["h"] * sy)),
    } for b in boxes]


def draw(boxes, cols, rows_cap):
    rows = (rows_cap or max(b["cy"] + b["ch"] + 2 for b in boxes)) + 2
    canvas = [[" "] * cols for _ in range(rows)]
    drawn = []
    for b in sorted(boxes, key=lambda k: (k["cy"], k["cx"])):
        x, y, w, h = b["cx"], b["cy"], b["cw"], b["ch"]
        x2, y2 = min(x + w, cols - 1), min(y + h, rows - 1)
        if any(px <= x and x2 <= px2 and py <= y and y2 <= py2
               for px, px2, py, py2 in drawn):
            continue
        for cx in range(x, x2 + 1):
            if cx < cols:
                canvas[y][cx] = H
                canvas[y2][cx] = H
        for cy in range(y, y2 + 1):
            canvas[cy][x] = V
            canvas[cy][x2] = V
        canvas[y][x], canvas[y][x2] = TL, TR
        canvas[y2][x], canvas[y2][x2] = BL, BR
        room = (x2 - x) - 1
        if room > 2:
            label = b.get("tag", "")
            cls = (b.get("cls") or "").split()[0] if b.get("cls") else ""
            if cls:
                label += "." + cls
            text = label[:room - 2]
            for j, ch in enumerate(text):
                if y + 1 < rows and x + 1 + j < x2 and canvas[y + 1][x + 1 + j] == " ":
                    canvas[y + 1][x + 1 + j] = ch
        drawn.append((x, x2, y, y2))
    return "\n".join("".join(row) for row in canvas)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file", nargs="?", help="JSON file of rect boxes; stdin if omitted")
    ap.add_argument("--width", type=int, default=90)
    ap.add_argument("--height", type=int, default=None)
    args = ap.parse_args()

    with open(args.file) if args.file else sys.stdin as f:
        boxes = json.load(f)
    boxes = [b for b in boxes if b.get("w", 0) > 8 and b.get("h", 0) > 8]
    if not boxes:
        sys.exit("no boxes above the 8px noise floor")
    print(draw(scale(boxes, args.width, args.height), args.width, args.height))


if __name__ == "__main__":
    main()
