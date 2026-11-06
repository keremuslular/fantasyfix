#!/usr/bin/env python3
"""Draws the FantasyFix icon (red rounded square with two white swap arrows) as PNGs.
Pure standard library. Usage: make_icons.py OUT_DIR SIZE [SIZE ...] [--square]
--square fills the whole canvas (for the iOS app icon, which iOS rounds itself)."""

import struct
import sys
import zlib

RED_TOP = (226, 35, 26)
RED_BOTTOM = (176, 18, 14)
WHITE = (255, 255, 255)
SS = 4  # subsamples per axis


def rounded_rect(x, y, r):
    # unit square [0,1]; r = corner radius
    cx = min(max(x, r), 1 - r)
    cy = min(max(y, r), 1 - r)
    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r and 0 <= x <= 1 and 0 <= y <= 1


def in_poly(x, y, pts):
    inside = False
    j = len(pts) - 1
    for i in range(len(pts)):
        xi, yi = pts[i]
        xj, yj = pts[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def arrow(y, right):
    # horizontal arrow centred on y, shaft from 0.24 to 0.76
    t = 0.055  # half shaft thickness
    h = 0.13  # half head height
    head = 0.16  # head length
    if right:
        tip, base, tail = 0.78, 0.78 - head, 0.22
        return [(tail, y - t), (base, y - t), (base, y - h), (tip, y), (base, y + h), (base, y + t), (tail, y + t)]
    tip, base, tail = 0.22, 0.22 + head, 0.78
    return [(tail, y - t), (base, y - t), (base, y - h), (tip, y), (base, y + h), (base, y + t), (tail, y + t)]


ARROWS = [arrow(0.37, True), arrow(0.63, False)]


def pixel(px, py, n, square):
    bg = arrows = 0
    for sy in range(SS):
        for sx in range(SS):
            x = (px + (sx + 0.5) / SS) / n
            y = (py + (sy + 0.5) / SS) / n
            if square or rounded_rect(x, y, 0.22):
                bg += 1
                if any(in_poly(x, y, a) for a in ARROWS):
                    arrows += 1
    total = SS * SS
    if bg == 0:
        return (0, 0, 0, 0)
    t = py / max(n - 1, 1)
    base = [RED_TOP[i] * (1 - t) + RED_BOTTOM[i] * t for i in range(3)]
    a = arrows / bg
    rgb = [round(base[i] * (1 - a) + WHITE[i] * a) for i in range(3)]
    return (*rgb, round(255 * bg / total))


def write_png(path, n, square):
    rows = bytearray()
    for py in range(n):
        rows.append(0)
        for px in range(n):
            rows.extend(pixel(px, py, n, square))

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    color_type = 2 if square else 6
    if square:  # drop alpha: iOS app icons must be opaque
        rgb = bytearray()
        for i in range(0, len(rows), 1 + 4 * n):
            rgb.append(0)
            row = rows[i + 1:i + 1 + 4 * n]
            for j in range(0, len(row), 4):
                rgb.extend(row[j:j + 3])
        rows = rgb
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", n, n, 8, color_type, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(rows), 9)) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--square"]
    square = "--square" in sys.argv
    out, sizes = args[0], [int(s) for s in args[1:]]
    for s in sizes:
        name = f"{out}/icon-{s}.png"
        write_png(name, s, square)
        print(name)
