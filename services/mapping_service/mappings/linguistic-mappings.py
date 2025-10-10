# services/mapping-service/mappings/linguistic_mappings.py
"""
Linguistic mappings for Poetic Layer.
These handle basic language-level transformations — case, structure, mutation, etc.
"""

from . import register_mapping
import random


@register_mapping("uppercase")
def uppercase(motif, params):
    """Convert all text to uppercase."""
    return motif["text"].upper()


@register_mapping("append")
def append(motif, params):
    """Append additional text from parameters."""
    return motif["text"] + str(params.get("append_text", ""))


@register_mapping("echo")
def echo(motif, params):
    """Return the same text unmodified."""
    return motif["text"]


@register_mapping("reverse")
def reverse(motif, params):
    """Reverse all characters in the motif text."""
    return motif["text"][::-1]


@register_mapping("mirror")
def mirror(motif, params):
    """Mirror the text against itself."""
    t = motif["text"]
    return f"{t} / {t[::-1]}"


@register_mapping("titlecase")
def titlecase(motif, params):
    """Capitalize every word in the text."""
    return motif["text"].title()


@register_mapping("mutate")
def mutate(motif, params):
    """Randomly mutate vowels for generative variation."""
    vowels = "aeiou"
    def mutate_word(w):
        if len(w) < 3 or random.random() > 0.3:
            return w
        return "".join(random.choice(vowels) if c.lower() in vowels else c for c in w)
    return " ".join(mutate_word(w) for w in motif["text"].split())


@register_mapping("summarize")
def summarize(motif, params):
    """Truncate the motif to its first few words."""
    words = motif["text"].split()
    if len(words) <= 8:
        return motif["text"]
    return " ".join(words[:8]) + "..."


@register_mapping("invert_case")
def invert_case(motif, params):
    """Invert case of every character."""
    return "".join(c.lower() if c.isupper() else c.upper() for c in motif["text"])
