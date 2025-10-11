import importlib
import pkgutil

MAPPING_REGISTRY = {}

def discover_mappings():
    """Dynamically import all mapping modules in subpackages."""
    packages = ["linguistic_mappings", "poetic_mappings", "visual_mappings"]
    for pkg in packages:
        package = f"services.mapping_service.mappings.{pkg}"
        for _, mod_name, _ in pkgutil.iter_modules([pkg.replace('.', '/')]):
            module_path = f"{package}.{mod_name}"
            module = importlib.import_module(module_path)
            for name, obj in vars(module).items():
                if callable(obj) and not name.startswith("_"):
                    MAPPING_REGISTRY[name] = obj
    print(f"[mappings] Registered {len(MAPPING_REGISTRY)} mappings:")
    for k in MAPPING_REGISTRY:
        print("  -", k)
