import json
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_logo_page():
    response = client.get("/tools/logo-studio")
    assert response.status_code == 200
    assert "Logo Studio" in response.text


def test_post_logo_page_free_variant():
    payload = {
        "business_name": "AURA PEAK",
        "business_activity": "Premium fashion accessories",
        "founder_dob": "1990-05-15",
    }
    response = client.post("/tools/logo-studio", data=payload)
    assert response.status_code == 200
    # The free variant should contain the lock‑CTA when not aligned
    assert "Unlock Full Brand Insights" in response.text
    # Ensure report JSON fields are present
    assert "Chaldean Compound" in response.text or "chaldean" in response.text.lower()

def test_post_logo_page_aligned_variant(monkeypatch):
    # Monkeypatch the deterministic engine to force alignment = True
    from app.services.brand_report import generate_brand_report as original
    def fake_report(*args, **kwargs):
        report = original(*args, **kwargs)
        report["aligned"] = True
        return report
    monkeypatch.setattr("app.services.brand_report.generate_brand_report", fake_report)
    payload = {
        "business_name": "NUMEROS VISION",
        "business_activity": "Numerology SaaS platform",
        "founder_dob": "1985-01-01",
    }
    response = client.post("/tools/logo-studio", data=payload)
    assert response.status_code == 200
    # Aligned variant should show download button instead of lock CTA
    assert "Download SVG Logo" in response.text

    # Monkeypatch the deterministic engine to force alignment = True
    from app.services.brand_report import generate_brand_report
    def fake_report(*args, **kwargs):
        report = generate_brand_report(*args, **kwargs)
        report["aligned"] = True
        return report
    monkeypatch.setattr("app.services.brand_report.generate_brand_report", fake_report)
    payload = {
        "business_name": "NUMEROS VISION",
        "business_activity": "Numerology SaaS platform",
        "founder_dob": "1985-01-01",
    }
    response = client.post("/tools/logo-studio", data=payload)
    assert response.status_code == 200
    # Aligned variant should show download button instead of lock CTA
    assert "Download SVG Logo" in response.text
