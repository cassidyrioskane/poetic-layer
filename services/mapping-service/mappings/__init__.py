# services/mapping-service/mappings/__init__.py
"""
Mapping registry system for the Poetic Layer mapping-service.

This file defines:
- MAPPING_REGISTRY: global dictionary of all registered mapping functions
- register_mapping(name): decorator to register a mapping
- discover_mappings(): auto-imports all mapping modules under this package

Every file in this folder (e.g. linguistic_mappings.py, poetic_mappings.py)
can simply import the decorator:

    from . import register_mapping

and define new mappings like:

    @register_mapping("uppercase")
    def uppercase(motif, params):
        return motif["text"].upper()
"""

import importlib
import os
import pkgutil

# Global registry of mapping name → function
MAPPING_REGISTRY: dict[str, callable] = {}


def register_mapping(name: str):
    """Decorator to register a mapping function by name."""
    def decorator(func):
        if name in MAPPING_REGISTRY:
            raise ValueError(f"Duplicate mapping name: {name}")
        MAPPING_REGISTRY[name] = func
        return func
    return decorator


def discover_mappings():
    """
    Auto-import all mapping modules in this package and print a summary.

    This allows the mapping-service to find every mapping definition
    without having to modify app.py manually.
    """
    pkg_dir = os.path.dirname(__file__)
    pkg_name = __name__
    discovered = []

    for _, module_name, is_pkg in pkgutil.iter_modules([pkg_dir]):
        if is_pkg:
            continue
        full_name = f"{pkg_name}.{module_name}"
        importlib.import_module(full_name)
        discovered.append(module_name)

    if discovered:
        print(f"[mappings] Loaded modules: {', '.join(discovered)}")
        print(f"[mappings] Registered mapping types: {', '.join(MAPPING_REGISTRY.keys())}")
    else:
        print("[mappings] No mapping modules discovered.")
