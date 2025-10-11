import re

antonyms = {
    "light": "dark", "bright": "dim", "open": "closed", "rise": "fall",
    "create": "destroy", "hope": "despair", "build": "ruin", "dream": "forget"
}

def ethical_mirror(motif, params=None):
    text = motif.get("content", "")
    for k, v in antonyms.items():
        text = re.sub(rf"\b{k}\b", v, text, flags=re.IGNORECASE)
    return text
