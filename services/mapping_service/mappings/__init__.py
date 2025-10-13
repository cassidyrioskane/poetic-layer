"""
Dynamic mapping registry for Poetic Layer.
Auto-discovers mapping functions and their conceptual docstrings.
"""

import importlib
import pkgutil
import inspect
from pathlib import Path

MAPPING_REGISTRY = {}
MAPPING_META = {}

def get_text(motif):
    """
    Safely extracts the text content of a motif.
    Supports both legacy ('text') and unified ('content') field names.
    Returns an empty string if the motif has no textual content.
    """
    if not motif:
        return ""
    if isinstance(motif, str):
        return motif
    return motif.get("text") or motif.get("content") or ""


def discover_mappings(base_package: str = __name__):
    """Recursively import mapping modules and store metadata."""
    root = Path(__file__).parent
    discovered = []

    for module_info in pkgutil.walk_packages([str(root)], prefix=f"{base_package}."):
        module_path = module_info.name
        try:
            module = importlib.import_module(module_path)
        except Exception as e:
            print(f"[mappings] ⚠️  Failed to import {module_path}: {e}")
            continue

        for name, obj in inspect.getmembers(module, inspect.isfunction):
            if name.startswith("_"):
                continue

            # --- Determine mapping domain automatically ---
            module_path_lower = module_path.lower()
            if "visual" in module_path_lower:
                domain = "image"
            else:
                domain = "text"

            MAPPING_REGISTRY[name] = obj
            doc = inspect.getdoc(obj)
            summary = doc.split("\n")[0] if doc else "No description available."
            MAPPING_META[name] = {
                "module": module_path,
                "description": summary,
                "domain": domain,
            }
            discovered.append(f"{module_path}.{name}")

    print(f"[mappings] Registered {len(MAPPING_REGISTRY)} mapping functions:")
    for k in sorted(MAPPING_REGISTRY.keys()):
        desc = MAPPING_META[k]["description"]
        print(f"  • {k} – {desc}")
    return MAPPING_REGISTRY


