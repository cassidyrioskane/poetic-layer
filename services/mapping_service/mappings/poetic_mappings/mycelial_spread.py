import random

def mycelial_spread(motif, params=None):
    others = params.get("other_text", "")
    a, b = motif.get("content", "").split(), others.split()
    merged = []
    while a or b:
        if random.random() < 0.5 and a:
            merged.append(a.pop(0))
        elif b:
            merged.append(b.pop(0))
    return " ".join(merged)
