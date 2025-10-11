"""
Color Drift Mapping
-------------------
Shifts an image's chromatic mood by gently rotating its hue space,
altering contrast, and introducing organic noise.
Intended to evoke emotional drift rather than harsh recoloring.
"""

import io, random, base64
from PIL import Image, ImageEnhance, ImageOps
import numpy as np

def color_drift(src, params=None):
    """Applies perceptible, mood-based color drift to a base64-encoded image."""
    params = params or {}
    b64 = src.get("content")
    if not b64:
        return src.get("text", "")

    # Decode base64 → Pillow image
    img = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGB")

    # 1. Hue drift via numpy transform
    arr = np.array(img).astype(np.float32)
    shift = random.uniform(-20, 20)  # hue drift degrees
    hsv = Image.fromarray(arr.astype(np.uint8)).convert("HSV")
    h, s, v = hsv.split()
    np_h = (np.array(h, dtype=np.uint16) + int(shift)) % 255
    h = Image.fromarray(np_h.astype(np.uint8))
    drifted = Image.merge("HSV", (h, s, v)).convert("RGB")

    # 2. Contrast + brightness variation
    enhancer = ImageEnhance.Contrast(drifted)
    drifted = enhancer.enhance(random.uniform(0.85, 1.25))
    enhancer = ImageEnhance.Brightness(drifted)
    drifted = enhancer.enhance(random.uniform(0.9, 1.1))

    # 3. Subtle vignette
    w, h = drifted.size
    vignette = Image.new("L", (w, h))
    for x in range(w):
        for y in range(h):
            dx = (x - w / 2) / (w / 2)
            dy = (y - h / 2) / (h / 2)
            vignette.putpixel((x, y), int(255 * (1 - 0.5 * (dx * dx + dy * dy))))
    drifted = Image.composite(drifted, ImageOps.colorize(vignette, "black", "white"), vignette)

    # Encode back to base64
    buf = io.BytesIO()
    drifted.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()
