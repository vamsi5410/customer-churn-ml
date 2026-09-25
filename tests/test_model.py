from src.ml import risk_level

def test_risk_levels():
    assert risk_level(0.80) == "HIGH"
    assert risk_level(0.50) == "MEDIUM"
    assert risk_level(0.10) == "LOW"
