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
                if name.startswith("_"):
                    continue
                MAPPING_REGISTRY[name] = obj
                doc = inspect.getdoc(obj)
                summary = doc.split("\n")[0] if doc else "No description available."
                MAPPING_META[name] = {
                    "module": module_path,
                    "description": summary,
                }
                discovered.append(f"{module_path}.{name}")

    print(f"[mappings] Registered {len(MAPPING_REGISTRY)} mapping functions:")
    for k in sorted(MAPPING_REGISTRY.keys()):
        desc = MAPPING_META[k]["description"]
        print(f"  • {k} – {desc}")
    return MAPPING_REGISTRY
