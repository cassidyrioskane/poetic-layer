from PIL import Image, ImageEnhance
import io, base64, random

def color_drift(motif, params=None):
    """Shifts an image’s emotional tone by subtly altering color balance and saturation."""

    data = base64.b64decode(motif["content"])
    img = Image.open(io.BytesIO(data)).convert("RGB")
    hue_shift = random.uniform(0.8, 1.2)
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(hue_shift)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()
