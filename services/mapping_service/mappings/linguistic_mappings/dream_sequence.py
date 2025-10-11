import random

def dream_sequence(motif, params=None):
    text = motif.get("content", "")
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
