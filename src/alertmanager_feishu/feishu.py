import base64
import hashlib
import hmac
import time
from typing import Any, Dict, Optional

import httpx

from .config import settings


def gen_sign(timestamp: int, secret: str) -> str:
    # 拼接timestamp和secret
    string_to_sign = f"{timestamp}\n{secret}"
    hmac_code = hmac.new(
        string_to_sign.encode("utf-8"), digestmod=hashlib.sha256
    ).digest()

    # 对结果进行base64处理
    sign = base64.b64encode(hmac_code).decode("utf-8")
    return sign


async def send_feishu_message(
    msg_type: str,
    content: Optional[Dict[str, Any]] = None,
    card: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"msg_type": msg_type}

    if msg_type == "interactive":
        if card:
            payload["card"] = card
    else:
        if content:
            payload["content"] = content

    if settings.feishu_secret:
        timestamp = int(time.time())
        payload["timestamp"] = str(timestamp)
        payload["sign"] = gen_sign(timestamp, settings.feishu_secret)

    async with httpx.AsyncClient() as client:
        response = await client.post(
            settings.feishu_webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()
