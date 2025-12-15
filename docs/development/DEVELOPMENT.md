## Setup

### Virtual Environment

This project uses a Python virtual environment to manage dependencies. To set up:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Linting and Formatting

The project uses **Ruff** for fast linting and code formatting. Ruff checks for style issues, import ordering, naming conventions, and performance anti-patterns.

To check for linting issues:

```bash
ruff check .
```

To auto-fix linting issues:

```bash
ruff check . --fix
```

To check formatting compliance:

```bash
ruff format --check .
```

To apply formatting:

```bash
ruff format .
```

## Type Checking

The project uses **pyright** for static type checking with strict enforcement. All Python modules are fully type-annotated.

To run the type checker:

```bash
pyright
```

### Handling Circular Imports

When a return type would create a circular import, use `TYPE_CHECKING` to import it only for type annotations:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from some_module import SomeType

def some_method(self) -> "SomeType":
    # Implementation that imports SomeType at runtime through another module
    return get_some_type()
```

### Testing

ToDo: Put testing command here.
