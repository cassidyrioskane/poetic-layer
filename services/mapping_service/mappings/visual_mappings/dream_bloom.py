"""
Dream Bloom (image)
-------------------
A painterly, luminous bloom that lifts highlights, softens edges, and
adds a subtle halation—evoking dreamlike memory rather than a simple blur.

Domain: image
"""

import io, base64
from PIL import Image, ImageFilter, ImageEnhance

def _to_img(b64):
    return Image.open(io.BytesIO(base64.b64decode(b64)))

def _to_b64(img, fmt="PNG"):
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def dream_bloom(src, params=None):
    """
    Creates a luminous, dreamy bloom:
      1) duplicate image → heavy Gaussian blur
      2) brighten & slightly color-warm the blurred layer
      3) screen-like composite over original
      4) gentle local contrast to keep forms readable
    Returns base64 image string.
    """
    params = params or {}
    b64 = src.get("content")
    if not b64:
        # Fallback for non-image motifs
        return src.get("text", "")

    img = _to_img(b64).convert("RGBA")

    # 1) Soft halo from highlights
    blur_radius = float(params.get("blur_radius", 8.0))
    glow = img.filter(ImageFilter.GaussianBlur(blur_radius))

    # 2) brighten & slight warmth
    glow = ImageEnhance.Brightness(glow).enhance(1.2)
    glow = ImageEnhance.Color(glow).enhance(1.05)

    # 3) screen composite (approx) via lighten blend
    # Convert to RGB for some ops, then back to RGBA
    base = img.convert("RGB")
    glow_rgb = glow.convert("RGB")
    blended = Image.blend(base, glow_rgb, alpha=0.5)

    # 4) subtle clarity
    blended = ImageEnhance.Contrast(blended).enhance(1.05)
    blended = ImageEnhance.Sharpness(blended).enhance(1.05)

    out = blended.convert("RGBA")
    return _to_b64(out)
