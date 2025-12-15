## Setup

### Virtual Environment

This project uses a Python virtual environment to manage dependencies. To set up:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Checks and Formatting

Run all checks (linting, type checking, tests):

```bash
make check
```

Format code and fix linting issues:

```bash
make format
```

View available commands:

```bash
make help
```
