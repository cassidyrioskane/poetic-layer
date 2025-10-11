import random

imagery = ["moonlight", "glass", "smoke", "mirrors", "roots", "static", "light", "memory"]

def lucid_dream(motif, params=None):
    """Infuses a motif with dreamlike sensory imagery, weaving symbols and sensations into the text."""

    text = motif.get("content", "")
    words = text.split()
    for i in range(0, len(words), max(1, len(words)//5)):
        words.insert(i, random.choice(imagery))
    return " ".join(words)
