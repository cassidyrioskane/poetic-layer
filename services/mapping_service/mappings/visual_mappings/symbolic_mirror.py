from PIL import Image, ImageOps
import io, base64

def symbol_mirror(motif, params=None):
    """Reflects an image horizontally to reveal hidden symmetry and invert its compositional ethics."""

    data = base64.b64decode(motif["content"])
    img = Image.open(io.BytesIO(data)).convert("RGB")
    mirrored = ImageOps.mirror(img)
    buf = io.BytesIO()
    mirrored.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()
