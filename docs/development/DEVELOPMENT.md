## Setup

### Virtual Environment

This project uses a Python virtual environment to manage dependencies. To set up:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Type Checking

The project uses **pyright** for static type checking with strict enforcement. All Python modules are fully type-annotated.

To run the type checker:

```bash
source venv/bin/activate
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
