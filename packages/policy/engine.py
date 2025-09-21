import yaml
from typing import Dict

class OmegaPolicyEngine:
    def __init__(self, path: str):
        with open(path, "r") as f:
            self.rules = yaml.safe_load(f)["rules"]

    def govern(self, metrics: Dict) -> Dict:
        for rule in self.rules:
            if eval(rule["when"], {}, {"metrics": metrics}):
                return {
                    "action": rule["then"],
                    "rule": rule["name"]
                }
        return {"action": "allow", "rule": "default"}
