import random
from services.mapping_service.mappings import get_text

def dream_sequence(motif, params=None):
    """Inserts surreal fragments into a motif, turning it into a drifting narrative of associative imagery."""

    text = get_text(motif)
    fragments = text.split(". ")
    inserts = [
        "The air ripples.",
        "Time folds inward.",
        "Someone hums a forgotten song.",
        "The world looks back."
    ]
    for _ in range(random.randint(1, 2)):
        pos = random.randint(0, len(fragments))
        fragments.insert(pos, random.choice(inserts))
    return ". ".join(fragments)
