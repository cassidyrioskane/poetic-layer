import random, re
from services.mapping_service.mappings import get_text

def echo_gradient(motif, params=None):
    """Creates recursive echoes of the motif, repeating and mutating phrases like an evolving memory."""

    text = motif.get("content", "")
    sentences = re.split(r'(?<=[.!?]) +', text)
    echoes = []
    for s in sentences:
        if not s.strip(): continue
        mut = re.sub(r'\b(\w{4,})\b', lambda m: m.group(1).upper() if random.random() < 0.15 else m.group(1), s)
        echoes.append(mut)
        if random.random() < 0.3:
            echoes.append(random.choice(sentences))
    return " ".join(echoes)
