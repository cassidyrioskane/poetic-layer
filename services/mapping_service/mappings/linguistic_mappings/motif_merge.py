import random

def motif_merge(motif, params=None):
    other = params.get("other_text", "")
    a = motif.get("content", "").split()
    b = other.split()
    merged = []
    while a or b:
        if random.random() < 0.5 and a:
            merged.append(a.pop(0))
        elif b:
            merged.append(b.pop(0))
    return " ".join(merged)
