"""Generate static/bg.jpg — dark blue gradient background."""

import os

try:
    from PIL import Image, ImageDraw  # pyright: ignore[reportMissingImports]
except ImportError:
    print("Install Pillow: pip install Pillow")
    raise

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(BASE_DIR, "static", "bg.jpg")

w, h = 1920, 1080
img = Image.new("RGB", (w, h))
draw = ImageDraw.Draw(img)

for y in range(h):
    t = y / h
    r = int(10 + t * 8)
    g = int(14 + t * 20)
    b = int(26 + t * 40)
    draw.line([(0, y), (w, y)], fill=(r, g, b))

img.save(OUT_PATH, "JPEG", quality=85)
print(f"Saved {OUT_PATH}")
