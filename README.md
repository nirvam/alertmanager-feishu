# alertmanager-feishu

Alertmanager to Feishu webhook service.

## Usage

### Commands
- `serve`: Start the webhook service.
- `test`: Send a test alert message.

### Configuration
Set the following environment variables (or in `.env`):
- `FEISHU_WEBHOOK_URL`: The Feishu webhook URL.
- `FEISHU_SECRET`: (Optional) Feishu webhook secret.
- `MESSAGE_TYPE`: `interactive` (default) or `text`.

### Development
```bash
make sync
make test
make lint
```
