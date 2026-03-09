from src.alertmanager_feishu.config import settings
from src.alertmanager_feishu.formatter import format_alertmanager_payload


def test_format_text():
    settings.message_type = "text"
    payload = {
        "status": "firing",
        "alerts": [
            {
                "status": "firing",
                "annotations": {
                    "summary": "High CPU",
                    "description": "CPU usage > 90%",
                },
                "startsAt": "2026-03-09T12:00:00Z",
            }
        ],
        "commonLabels": {"alertname": "CPUAlert"},
    }
    result = format_alertmanager_payload(payload)
    assert result["msg_type"] == "text"
    assert "High CPU" in result["content"]["text"]
    assert "CPU usage > 90%" in result["content"]["text"]
    assert "FIRING" in result["content"]["text"]


def test_format_card():
    settings.message_type = "interactive"
    payload = {
        "status": "firing",
        "alerts": [
            {
                "status": "firing",
                "labels": {"severity": "critical"},
                "annotations": {
                    "summary": "High CPU",
                    "description": "CPU usage > 90%",
                },
                "startsAt": "2026-03-09T12:00:00Z",
                "generatorURL": "http://prometheus:9090",
            }
        ],
        "commonLabels": {"alertname": "CPUAlert"},
    }
    result = format_alertmanager_payload(payload)
    assert result["msg_type"] == "interactive"
    assert "card" in result
    assert result["card"]["schema"] == "2.0"
    header = result["card"]["header"]
    assert "FIRING" in header["title"]["content"]
    assert "CPUAlert" in header["title"]["content"]
    assert header["template"] == "red"

    body = result["card"]["body"]
    assert body["direction"] == "vertical"
    elements = body["elements"]
    assert any("High CPU" in e.get("content", "") for e in elements)
    assert any("<font color='red'>critical</font>" in e.get("content", "") for e in elements)
    assert any(e.get("tag") == "button" for e in elements)

    assert "config" in result["card"]
    assert result["card"]["config"]["update_multi"] is True
    assert "CPUAlert" in result["card"]["config"]["summary"]["content"]

