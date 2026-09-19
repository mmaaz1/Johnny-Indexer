# List available recipes
default:
    @just --list

# Check formatting, linting and types
check:
    uv run ruff format --check .
    uv run ruff check .
    uv run pyright

# Format code and fix linting issues
format:
    uv run ruff format .
    uv run ruff check . --fix

# Run tests
test:
    uv run pytest -v
