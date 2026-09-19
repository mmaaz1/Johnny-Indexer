.PHONY: install check format test

PYTHON := venv/bin/python

install:
	python3 -m venv venv
	$(PYTHON) -m pip install -e ".[dev]"

check:
	$(PYTHON) -m ruff format --check .
	$(PYTHON) -m ruff check .
	$(PYTHON) -m pyright

format:
	$(PYTHON) -m ruff format .
	$(PYTHON) -m ruff check . --fix

test:
	$(PYTHON) -m pytest tests/ -v
