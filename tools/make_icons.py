#!/usr/bin/env python3
"""Draws the FantasyFix icon (orange basketball on a navy rounded square) as PNGs.
Pure standard library. Usage: make_icons.py OUT_DIR SIZE [SIZE ...] [--square | --mac] [--style=hardwood|court|teal]
--square fills the whole canvas and drops transparency (iOS app icon; iOS rounds it itself).
--mac draws the macOS app icon: body inset on Apple's icon grid, with a soft shadow."""

import math
import struct
import sys
import zlib

STYLE = "hardwood"  # background style: "court", "hardwood" or "teal"
BACKGROUNDS = {
    # (top-left colour, bottom-right colour, court line colour)
    "court": ((122, 58, 230), (36, 18, 96), (255, 255, 255)),
    "teal": ((0, 168, 160), (6, 58, 92), (255, 255, 255)),
}
BALL_LIGHT = (255, 160, 64)
BALL_DARK = (214, 92, 18)
SEAM = (40, 18, 6)

CX, CY, R = 0.5, 0.5, 0.33  # ball centre and radius (unit square)
SEAM_W = 0.026
LINE_W = 0.02


def mix(a, b, t):
    return tuple(a[i] * (1 - t) + b[i] * t for i in range(3))


def in_rounded_rect(x, y, r=0.22):
    if not (0 <= x <= 1 and 0 <= y <= 1):
        return False
    cx = min(max(x, r), 1 - r)
    cy = min(max(y, r), 1 - r)
    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r


def background(x, y):
    if STYLE == "hardwood":
        plank = int(x * 7)
        shade = (0.08 if plank % 2 else 0.0) + 0.05 * math.sin(y * 40 + plank * 2.3)
        wood = mix((222, 170, 110), (176, 118, 64), min(1, y * 0.7 + shade))
        if (x * 7) % 1 < 0.03:  # gaps between planks
            wood = mix(wood, (90, 56, 28), 0.5)
        return mix(wood, (250, 250, 250), 0.85) if court_line(x, y) else wood
    top, bottom, line = BACKGROUNDS[STYLE]
    bg = mix(top, bottom, (x + y) / 2)
    return mix(bg, line, 0.28) if court_line(x, y) else bg


def court_line(x, y):
    """Centre circle and half-court line behind the ball (hidden at tiny sizes)."""
    if LINE_W == 0:
        return False
    d = math.hypot(x - CX, y - CY)
    return abs(d - 0.43) < LINE_W / 2 or abs(y - CY) < LINE_W / 2


MAC = False  # macOS style: icon body inset with a transparent margin and soft shadow
MAC_MARGIN = 100 / 1024  # Apple's macOS icon grid: 824px body on a 1024px canvas


def rounded_rect_sdf(x, y, r=0.225):
    """Signed distance to a rounded unit square (negative inside)."""
    qx = abs(x - 0.5) - (0.5 - r)
    qy = abs(y - 0.5) - (0.5 - r)
    outside = math.hypot(max(qx, 0), max(qy, 0))
    return outside + min(max(qx, qy), 0) - r


def sample(x, y, square):
    """Colour (r, g, b, a) at one point of the unit square."""
    if MAC:
        scale = 1 - 2 * MAC_MARGIN
        u, v = (x - MAC_MARGIN) / scale, (y - MAC_MARGIN) / scale
        if rounded_rect_sdf(u, v) > 0:
            # soft drop shadow, slightly below the body
            d = rounded_rect_sdf(u, v - 0.02)
            alpha = 0.32 * max(0.0, 1 - d / 0.045) if d > 0 else 0.32
            return (0, 0, 0, round(255 * alpha))
        return sample_body(u, v)
    if not square and not in_rounded_rect(x, y):
        return (0, 0, 0, 0)
    return sample_body(x, y)


def sample_body(x, y):
    """Colour of the icon body (background + ball) at a point of the unit square."""
    bg = background(x, y)

    dx, dy = x - CX, y - CY
    d = math.hypot(dx, dy)
    if d > R:
        return (*bg, 255)

    # seams: outline, vertical, horizontal, and two side curves
    half = SEAM_W / 2
    side_offset, side_r = R * 1.18, R * 0.82
    seam = (
        R - d < half * 1.4
        or abs(dx) < half
        or abs(dy) < half
        or abs(math.hypot(x - (CX - side_offset), dy) - side_r) < half
        or abs(math.hypot(x - (CX + side_offset), dy) - side_r) < half
    )
    if seam:
        return (*SEAM, 255)

    # simple lighting from the top left
    light = max(0.0, min(1.0, 0.35 + (dx + dy) / (2 * R) * 0.55 + (d / R) ** 2 * 0.3))
    return (*mix(BALL_LIGHT, BALL_DARK, light), 255)


def pixel(px, py, n, square, ss):
    acc = [0.0, 0.0, 0.0, 0.0]
    for sy in range(ss):
        for sx in range(ss):
            r, g, b, a = sample((px + (sx + 0.5) / ss) / n, (py + (sy + 0.5) / ss) / n, square)
            acc[0] += r * a
            acc[1] += g * a
            acc[2] += b * a
            acc[3] += a
    if acc[3] == 0:
        return (0, 0, 0, 0)
    return (round(acc[0] / acc[3]), round(acc[1] / acc[3]), round(acc[2] / acc[3]), round(acc[3] / (ss * ss)))


def write_png(path, n, square):
    global R, SEAM_W, LINE_W
    # small toolbar sizes: bigger ball, thicker seams and no court lines so it stays readable
    R, SEAM_W, LINE_W = (0.42, 0.06, 0) if n <= 16 else (0.40, 0.045, 0) if n <= 48 else (0.33, 0.026, 0.02)
    ss = 4 if n <= 256 else 2
    channels = 3 if square else 4
    rows = bytearray()
    for py in range(n):
        rows.append(0)
        for px in range(n):
            rows.extend(pixel(px, py, n, square, ss)[:channels])

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    color_type = 2 if square else 6
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", n, n, 8, color_type, 0, 0, 0))
    png += chunk(b"IDAT", zlib.compress(bytes(rows), 9)) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(png)


if __name__ == "__main__":
    MAC = "--mac" in sys.argv
    for a in sys.argv[1:]:
        if a.startswith("--style="):
            STYLE = a.split("=", 1)[1]
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    square = "--square" in sys.argv
    out, sizes = args[0], [int(s) for s in args[1:]]
    for s in sizes:
        name = f"{out}/icon-{s}.png"
        write_png(name, s, square)
        print(name)
