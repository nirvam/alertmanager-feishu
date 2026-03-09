from typing import Any, Dict, List

from .config import settings


def format_alertmanager_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format Alertmanager payload into Feishu message.
    """
    status = payload.get("status", "unknown")
    alerts: List[Dict[str, Any]] = payload.get("alerts", [])

    if settings.message_type == "interactive":
        return format_card(status, alerts, payload)
    else:
        return format_text(status, alerts, payload)


def format_text(
    status: str, alerts: List[Dict[str, Any]], payload: Dict[str, Any]
) -> Dict[str, Any]:
    common_labels = payload.get("commonLabels", {})
    alertname = common_labels.get("alertname", "Alert")

    lines = [f"Status: {status.upper()}", f"Alert: {alertname}"]

    for alert in alerts:
        summary = alert.get("annotations", {}).get("summary", "No summary")
        description = alert.get("annotations", {}).get("description", "No description")
        lines.append("\n--- Alert ---")
        lines.append(f"Summary: {summary}")
        lines.append(f"Description: {description}")
        lines.append(f"Starts At: {alert.get('startsAt')}")

    return {"msg_type": "text", "content": {"text": "\n".join(lines)}}


def format_card(
    status: str, alerts: List[Dict[str, Any]], payload: Dict[str, Any]
) -> Dict[str, Any]:
    common_labels = payload.get("commonLabels", {})
    alertname = common_labels.get("alertname", "Alert")

    # Header color based on status
    header_template = "red" if status == "firing" else "green"

    elements = []

    for alert in alerts:
        summary = alert.get("annotations", {}).get("summary", "No summary")
        description = alert.get("annotations", {}).get("description", "No description")
        severity = alert.get("labels", {}).get("severity", "unknown")

        # Color coded severity
        severity_color = "red" if severity.lower() == "critical" else "orange" if severity.lower() == "warning" else "grey"

        elements.append(
            {
                "tag": "markdown",
                "content": f"**Summary:** {summary}\n**Description:** {description}\n**Severity:** <font color='{severity_color}'>{severity}</font>\n**Starts At:** {alert.get('startsAt')}",
            }
        )

        if alert.get("generatorURL"):
            elements.append(
                {
                    "tag": "button",
                    "text": {"tag": "plain_text", "content": "View in Prometheus"},
                    "type": "default",
                    "behaviors": [
                        {"type": "open_url", "default_url": alert.get("generatorURL")}
                    ],
                }
            )

        elements.append({"tag": "hr"})

    # Remove the last hr
    if elements and elements[-1]["tag"] == "hr":
        elements.pop()

    card = {
        "schema": "2.0",
        "config": {
            "update_multi": True,
            "summary": {"content": f"[{status.upper()}] {alertname}"},
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": f"[{status.upper()}] {alertname}",
            },
            "template": header_template,
        },
        "body": {
            "direction": "vertical",
            "elements": elements,
        },
    }

    return {"msg_type": "interactive", "card": card}
