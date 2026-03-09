.PHONY: all sync install run test lint clean

all: sync

sync:
	uv sync

install: sync

run:
	uv run alertmanager-feishu serve

test:
	uv run pytest tests/

lint:
	uv run black .
	uv run isort .
	uv run ruff check .

clean:
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
