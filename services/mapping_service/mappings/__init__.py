# services/mapping_service/mappings/__init__.py
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

# --- Shared helpers (NOT mappings) -------------------------------------------
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
    # unified "content" for text motifs, legacy "text" fallback
    return motif.get("text") or motif.get("content") or ""

# Any names we NEVER want to register as mappings:
_IGNORE_NAMES = {
    "get_text", "discover_mappings",
    "MAPPING_REGISTRY", "MAPPING_META",
}

def _looks_like_mapping(func):
    """Heuristic: mapping functions are (motif, params=None)."""
    sig = inspect.signature(func)
    params = list(sig.parameters.values())
    if not (1 <= len(params) <= 2):
        return False
    # first arg can be called anything, we don't enforce its name
    if len(params) == 2:
        # second is typically params=None
        p2 = params[1]
        if p2.default is inspect._empty:
            return False
    return True

def discover_mappings(base_package: str = __name__):
    """Recursively import mapping modules and store metadata."""
    root = Path(__file__).parent
    subpackages = [p for p in root.iterdir() if p.is_dir() and not p.name.startswith("__")]
    discovered = []

    for subpkg in subpackages:
        package_name = f"{base_package}.{subpkg.name}"
        for _, mod_name, _ in pkgutil.iter_modules([str(subpkg)]):
            module_path = f"{package_name}.{mod_name}"
            try:
                module = importlib.import_module(module_path)
            except Exception as e:
                print(f"[mappings] ⚠️  Failed to import {module_path}: {e}")
                continue

            for name, obj in inspect.getmembers(module, inspect.isfunction):
                # 1) skip private/dunder and hard-ignored names
                if name.startswith("_") or name in _IGNORE_NAMES:
                    continue
                # 2) skip functions imported into the module (not defined there)
                if getattr(obj, "__module__", None) != module.__name__:
                    continue
                # 3) ensure it looks like a mapping
                if not _looks_like_mapping(obj):
                    continue

                MAPPING_REGISTRY[name] = obj
                doc = inspect.getdoc(obj)
                summary = doc.split("\n")[0] if doc else "No description available."
                # Optional: domain inference by package path
                domain = "image" if ".visual_mappings." in module_path else "text"
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
