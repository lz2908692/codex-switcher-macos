#!/usr/bin/env python3
"""Generate macOS .icns icon from scratch (no SVG dependency)."""
import os
from PIL import Image, ImageDraw, ImageFont

iconset_dir = "icon.iconset"
os.makedirs(iconset_dir, exist_ok=True)

sizes = [16, 32, 64, 128, 256, 512]
for sz in sizes:
    img = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Blue circle background (#2860E1)
    margin = int(sz * 0.05)
    draw.ellipse([margin, margin, sz - margin, sz - margin], fill=(0x28, 0x60, 0xE1, 255))
    # White "SS" text
    font_size = int(sz * 0.48)
    font = None
    for fp in ["/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/SFNS.ttf"]:
        try:
            font = ImageFont.truetype(fp, font_size)
            break
        except Exception:
            continue
    if font is None:
        font = ImageFont.load_default()
    text = "SS"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    x = (sz - tw) // 2 - bbox[0]
    y = int(sz * 0.66) - th - bbox[1]
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    # Save normal and @2x
    img.save(os.path.join(iconset_dir, "icon_%dx%d.png" % (sz, sz)))
    if sz <= 256:
        img2 = img.resize((sz * 2, sz * 2), Image.LANCZOS)
        img2.save(os.path.join(iconset_dir, "icon_%dx%d@2x.png" % (sz, sz)))

print("Icon PNGs generated in %s" % iconset_dir)
