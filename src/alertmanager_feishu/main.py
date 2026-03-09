import asyncio

import typer
import uvicorn
from fastapi import FastAPI, Request

from .config import settings
from .feishu import send_feishu_message
from .formatter import format_alertmanager_payload

app = FastAPI(title="Alertmanager Feishu Service")
cli = typer.Typer()


@app.post("/webhook")
async def webhook_receiver(request: Request):
    payload = await request.json()
    formatted = format_alertmanager_payload(payload)

    msg_type = formatted["msg_type"]
    if msg_type == "interactive":
        await send_feishu_message(msg_type=msg_type, card=formatted["card"])
    else:
        await send_feishu_message(msg_type=msg_type, content=formatted["content"])

    return {"status": "ok"}


@cli.command()
def serve():
    """
    Start the Alertmanager Feishu service.
    """
    uvicorn.run(app, host=settings.app_host, port=settings.app_port)


@cli.command()
def test():
    """
    Send a test message to Feishu.
    """
    print("Sending test message...")
    test_payload = {
        "status": "firing",
        "alerts": [
            {
                "status": "firing",
                "labels": {"alertname": "TestAlert", "severity": "critical"},
                "annotations": {
                    "summary": "This is a test alert",
                    "description": "If you see this, the alertmanager-feishu service is working!",
                },
                "startsAt": "2026-03-09T12:00:00Z",
                "generatorURL": "http://prometheus:9090",
            }
        ],
        "commonLabels": {"alertname": "TestAlert"},
    }

    formatted = format_alertmanager_payload(test_payload)

    async def _send():
        msg_type = formatted["msg_type"]
        if msg_type == "interactive":
            return await send_feishu_message(msg_type=msg_type, card=formatted["card"])
        else:
            return await send_feishu_message(
                msg_type=msg_type, content=formatted["content"]
            )

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    result = loop.run_until_complete(_send())
    print(f"Result: {result}")


if __name__ == "__main__":
    cli()
