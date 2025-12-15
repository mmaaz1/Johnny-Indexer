.PHONY: check format help

check:
	python -m ruff format --check .
	python -m ruff check .
	python -m pyright
	python -m pytest tests/ -v

format:
	python -m ruff format .
	python -m ruff check . --fix

help:
	@echo "Available commands:"
	@echo "  make check    - Run all checks (ruff format, ruff lint, pyright, pytest)"
	@echo "  make format   - Format code and fix issues"
	@echo "  make help     - Show this help message"
