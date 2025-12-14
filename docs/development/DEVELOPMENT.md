## Setup

### Virtual Environment

This project uses a Python virtual environment to manage dependencies. To set up:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Type Checking

The project uses **pyright** for static type checking. Type hints have been added to the core modules:
- `utils/file/file.py` - File class with full type annotations
- `utils/config/config_helper.py` - Configuration helper with type annotations

To run the type checker:

```bash
# Activate virtual environment first
source venv/bin/activate
pyright utils/file/file.py utils/config/config_helper.py
```

Or check all Python files:

```bash
pyright
```

#### Type Checking Configuration

Type checking is configured in `pyproject.toml` with `typeCheckingMode: basic`. This provides a good balance between catching real errors and avoiding overly strict checks.

#### Handling Circular Imports

When a return type would create a circular import, use `TYPE_CHECKING` to import it only for type annotations:

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from some_module import SomeType

def some_method(self) -> "SomeType":
    # Implementation that imports SomeType at runtime through another module
    return get_some_type()
```

## Development Guidelines

### Adding Type Hints

When adding new code or modifying existing code:
1. Always add type hints to function parameters and return types
2. Use `Optional[T]` for values that can be `None`
3. Use `List[T]`, `Dict[K, V]`, etc. from the `typing` module
4. Run pyright to verify your changes have no type errors

### Testing

ToDo: Put testing command here.
