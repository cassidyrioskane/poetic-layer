"""
Temporal Echo (image)
---------------------
Creates the sensation of time layered into a single frame by compositing
offset, fading copies—like motion trails or memory afterimages.

Domain: image
"""

import io, base64, math
from PIL import Image, ImageEnhance

def _to_img(b64):
    return Image.open(io.BytesIO(base64.b64decode(b64)))

def _to_b64(img, fmt="PNG"):
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return base64.b64encode(buf.getvalue()).decode("utf-8")

def temporal_echo(src, params=None):
    """
    Parameters (all optional):
      echoes: int = number of echoes (default 4)
      dx: int = per-echo x offset in pixels (default 6)
      dy: int = per-echo y offset in pixels (default 3)
      fade: float = per-echo alpha multiplier (0..1, default 0.8)
      tint: float = optional color shift toward warm/cool (−0.1..0.1)
    """
    params = params or {}
    b64 = src.get("content")
    if not b64:
        return src.get("text", "")

    base = _to_img(b64).convert("RGBA")
    w, h = base.size

    echoes = max(1, int(params.get("echoes", 4)))
    dx = int(params.get("dx", 6))
    dy = int(params.get("dy", 3))
    fade = float(params.get("fade", 0.8))
    tint = float(params.get("tint", 0.0))  # simple brightness bias

    # Start from a slightly dimmer base so echoes pop
    canvas = ImageEnhance.Brightness(base).enhance(0.95)

    # Composite echoes from oldest to newest
    alpha = 0.6
    for i in range(echoes, 0, -1):
        offset = (dx * i, dy * i)
        layer = base.copy()

        # subtle brightness drift per echo
        b_mult = 1.0 + (tint * (i / echoes))
        layer = ImageEnhance.Brightness(layer).enhance(b_mult)

        # alpha for this echo
        a = max(0.05, alpha * (fade ** (echoes - i)))
        # apply alpha by converting to RGBA and setting uniform alpha
        r, g, b, _ = layer.split()
        layer = Image.merge("RGBA", (r, g, b, Image.new("L", (w, h), int(255 * a))))

        # paste with offset, clipped to canvas
        tmp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        tmp.paste(layer, offset)
        canvas = Image.alpha_composite(canvas, tmp)

    # Gentle final pop
    canvas = ImageEnhance.Contrast(canvas).enhance(1.03)
    canvas = ImageEnhance.Sharpness(canvas).enhance(1.04)

    return _to_b64(canvas)
