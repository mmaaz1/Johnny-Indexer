.PHONY: check format help

check:
	python -m ruff format --check .
	python -m ruff check .
	python -m pyright
# 	python -m pytest tests/ -v

format:
	python -m ruff format .
	python -m ruff check . --fix
