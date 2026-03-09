# alertmanager-feishu Instructions

## Overview
`alertmanager-feishu` is a resident service designed to receive alerts from Prometheus Alertmanager and forward them to a Feishu (Lark) webhook bot.

## Functional Requirements
- **Commands**:
    - `serve`: Start the long-running HTTP service to listen for Alertmanager webhooks.
    - `test`: Send a single test message to the configured Feishu webhook to verify connectivity and formatting.
- **Message Styles**:
    - Support both **Interactive Cards** (Rich text, colors, buttons) and **Plain Text**.
- **Configuration**:
    - Follows **12-factor app** principles: configuration via environment variables (e.g., `FEISHU_WEBHOOK_URL`, `MESSAGE_TYPE`).

## Technical Standards (per GEMINI.md)
- **Language**: Modern Python with Type Hinting.
- **Dependency Management**: `uv`.
- **Formatting**: PEP 8, sorted imports, strict linting.
- **Ops**: 
    - `Makefile` for build/test/run entry points.
    - Systemd unit file for service management.
    - (Optional) Podman containerization.
    - (Optional) PKGBUILD for Arch Linux integration.

## Reference
- Feishu Webhook Documentation: Use `feishu-docs` skill.
