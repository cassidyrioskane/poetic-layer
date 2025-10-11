"""
Symbolic Mirror Mapping
-----------------------
Reflects an image into a symmetrical composition and overlays
it with a translucent echo of itself, creating a ghostlike mirror
intended to evoke duality and introspection.
"""

import io, base64
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

def symbolic_mirror(src, params=None):
    """Creates a mirrored composition with faint overlay."""
    b64 = src.get("content")
    if not b64:
        return src.get("text", "")

    img = Image.open(io.BytesIO(base64.b64decode(b64))).convert("RGBA")

    mirrored = ImageOps.mirror(img)
    combined = Image.blend(img, mirrored, alpha=0.5)
    blurred = combined.filter(ImageFilter.GaussianBlur(radius=2))
    enhancer = ImageEnhance.Brightness(blurred)
    out = enhancer.enhance(1.05)

    buf = io.BytesIO()
    out.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()
