from packages.policy.engine import OmegaPolicyEngine

def test_policy_block():
    engine = OmegaPolicyEngine("packages/policy/policies.yaml")
    metrics = {"coherence_tech": 0.5, "nli_contradiction": 0.0, "ethics_risk": 0.0}
    result = engine.govern(metrics)
    assert result["action"] == "block"

def test_policy_allow():
    engine = OmegaPolicyEngine("packages/policy/policies.yaml")
    metrics = {"coherence_tech": 0.9, "nli_contradiction": 0.0, "ethics_risk": 0.0}
    result = engine.govern(metrics)
    assert result["action"] == "allow"
