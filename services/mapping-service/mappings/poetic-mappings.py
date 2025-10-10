# services/mapping-service/mappings/poetic_mappings.py
"""
Poetic mappings — unique to Poetic Layer.
Operate on meaning, provenance, and motif relationships.
"""

from . import register_mapping
from datetime import datetime
import random


@register_mapping("resonance")
def resonance(motif, params):
    """Amplify emotionally charged words."""
    import re
    text = motif["text"]
    keywords = ["love", "death", "hope", "fear", "light", "dark", "time"]
    def amplify(word):
        if word.lower().strip(".,!?") in keywords:
            return f"{word.upper()} — {word.lower()}"
        return word
    return " ".join(amplify(w) for w in re.split(r"(\W+)", text))


@register_mapping("echo_chamber")
def echo_chamber(motif, params):
    """Reflect the motif through its provenance."""
    prov = motif.get("provenance", {})
    who = prov.get("who", "unknown")
    when = prov.get("when")
    if when:
        when_str = datetime.utcfromtimestamp(int(when)).strftime("%Y")
    else:
        when_str = "timeless"
    return f"{motif['text']} ({who}, {when_str})"


@register_mapping("ethical_mirror")
def ethical_mirror(motif, params):
    """Invert ethical tone based on metadata."""
    ethics = motif.get("ethics", {})
    tone = ethics.get("tone", [])
    inverse = {"hopeful": "despairing", "calm": "chaotic", "joyful": "melancholic"}
    new_tone = [inverse.get(t, t) for t in tone]
    if tone:
        tone_str = ", ".join(new_tone)
        return f"{motif['text']} [refracted through {tone_str} light]"
    return motif["text"] + " [ethically mirrored]"


@register_mapping("motif_merge")
def motif_merge(motif, params):
    """Blend two motifs into one hybrid phrase."""
    from services.mapping_service.app import MOTIFS
    other_id = params.get("other_motif_id")
    if not other_id:
        return motif["text"] + " [no second motif]"
    other = MOTIFS.get(other_id)
    if not other:
        return motif["text"] + " [missing second motif]"
    words1 = motif["text"].split()
    words2 = other["text"].split()
    if len(words1) == 0 or len(words2) == 0:
        return motif["text"]
    return f"{words1[0].capitalize()} {' '.join(words2[1:])}. {words2[0].capitalize()} {' '.join(words1[1:])}."


@register_mapping("temporal_distortion")
def temporal_distortion(motif, params):
    """Shift motif into a different temporal voice."""
    text = motif["text"]
    return f"{text} Once spoken, now remembered, soon to be repeated."


@register_mapping("dream_sequence")
def dream_sequence(motif, params):
    """
    Apply a random sequence of 2–3 other mappings to a motif.
    Creates a layered transformation — the motif dreaming itself.
    """
    from services.mapping_service import mappings

    available = list(mappings.MAPPING_REGISTRY.keys())
    exclude = {"dream_sequence"}  # avoid recursion
    choices = [t for t in available if t not in exclude]

    if not choices:
        return motif["text"] + " [no other mappings available]"

    chain_length = params.get("chain_length", random.choice([2, 3]))
    selected = random.sample(choices, min(chain_length, len(choices)))

    text = motif["text"]
    current = {"text": text, "id": motif.get("id", "unknown")}

    history = []
    for t in selected:
        func = mappings.MAPPING_REGISTRY.get(t)
        if not func:
            continue
        try:
            new_text = func(current, params)
            current = {"text": new_text, "id": motif.get("id", "unknown")}
            history.append(t)
        except Exception as e:
            history.append(f"{t}:error")

    hist_str = " → ".join(history) if history else "none"
    return f"{current['text']} [dream sequence: {hist_str}]"
