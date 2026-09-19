# Development

## Development Commands

Install [uv](https://docs.astral.sh/uv/) and [just](https://just.systems/) first (eg: `brew install uv just`).

| Command | Description |
| --- | --- |
| `uv sync` | Create the virtual environment (`.venv/`) and install the package in editable mode, with dev tools |
| `just check` | Run all checks (formatting, linting, type checking) |
| `just format` | Format code and fix linting issues |
| `just test` | Run tests |
| `just` | List all recipes |
| `uv add <package>` | Add a runtime dependency |
| `uv add --dev <package>` | Add a dev tool |

Dependencies are declared in `pyproject.toml` and locked in `uv.lock`. Commit `uv.lock` with any dependency change.

## Tech Stack

- **Python 3.12+**, packaged with setuptools and a `src/` layout
- **uv** - Virtual environment, dependencies and lockfile
- **just** - Task runner for the development commands
- **Ruff** - Formatting and linting
- **Pyright** - Type checking, in strict mode
- **pytest** - Tests
- **PyYAML** - Reading the config files. The only runtime dependency.
- **cron** - Scheduled runs

## Project Layout

- `src/johnny_indexer/` - The package
  - `__main__.py` - The `johnny-indexer` CLI (`fix`, `jdex`, `schedule`)
  - `fix_indexes.py`, `create_jdex.py`, `schedule.py` - One module per command
  - `file.py` - A file or directory. Knows nothing about indexes.
  - `index/` - Index formats, parsing, sorting and fixing. Depends on `file.py`, never the reverse.
  - `paths.py` - Paths to the config files and `logs/`, relative to the repo root
  - `log.py` - Logging setup for a run
- `tests/` - Tests
- `config.defaults.yaml` - Every option and its default. New options must be added here.
- `config.override.yaml` - The user's optional overrides of the defaults. Gitignored.
- `logs/` - Log files of runs.

The package is installed in editable mode and reads the config files and `logs/` from the repo root, so it's run from its repo checkout.

## Design and Implementation

### Logging

- `print` is only for the interactive UI (the approval prompt and the `schedule` commands' results). Everything else is logged.
- Log levels:
    - `DEBUG`: Details for troubleshooting, like exceptions that are expected and handled
    - `INFO`: Changes made to the notes, like renames, link updates and commits
    - `WARNING`: Something was skipped, but the run continued
    - `ERROR`: The run stopped

### Glossary

1. **Proper Index**: A file that is indexed according to the [format specifications](JOHNNY_INDEX_SPECIFICATION.md) for its hierarchy level
    - Matches the exact regex pattern for its index type
    - Has the correct separator between parent and main indexes
    - Example: `12.01 My Topic` is a proper Topic index; `12.01.01 My Topic` is not

1. **Improper Index**: A file with an index that exists but doesn't strictly follow the format specification
    - Still uses a valid index structure, but may have extra suffixes or non-standard patterns
    - Will be automatically corrected by the indexer to a proper format
    - Example: `12.01.01 My Topic` is an improper Topic index (has extra `.01`); it will be corrected to `12.01 My Topic`

1. **Parent Index**: The left-section of a file's index that determines under which section the file belongs to
    - Usually is either the index of the parent's directory, but for Areas its only a part of it

1. **Main Index**: The right-section of a file's index that determines the ordering of the file among its siblings 

1. **Separator**: The set of characters used to separate the parent index and the main index
    - Generally, these are '-', '.' or ''.

1. **Final Index**: Constructed by combining parent and main indexes with the appropriate separator

**Example**: In a Topic `12.34`, `12` is the parent index, `34` is the main index, and `.` is the separator

### Index Fixing Workflow

Files are processed using a breadth-first search (BFS) algorithm:

1. **Auto Commit** (if enabled): Commit the notes directory to git as a restore point, then push (if enabled)
1. **Initialize**: Start with all Area directories at Level 0
1. **Collect Changes**: For each directory level:
   - Scan all non-excluded files in current level
   - Sort files by their current index, so existing order is kept. Files without an index go last, oldest (by creation time) first
   - Assign main indexes based on position in sorted list (0, 1, 2, ...) with zero-padding to match directory width
   - For Topics, ensure main indexes always have 2 digits (e.g., `01`, `02`, `10`)
   - For Extensions, preserve their alphabetic suffix (e.g., `+DOCS`, `+CODE`)
   - Combine parent index + separator + main index to create expected full index
   - Identify files where actual index doesn't match expected index
1. **Sort & Present**: Sort proposed changes by their new index
1. **User Confirmation** (if enabled): Prompt user to approve each rename (`y`) or stop the run (`n`)
1. **Apply Renames**: Rename each file on disk, stopping the run if the new filename already exists
1. **Update Links** (if enabled): In a single pass over the directory tree, update links to any of the renamed files so they point to the new filenames
1. **Recurse**: Move to the next directory level and repeat from step 3
1. **Generate JDex** (if enabled): After all renames complete, regenerate index files

### JDex File Generation

The system automatically generates Markdown index files (`Index of [DirectoryName].md`) at the root and in each Area. These files:

- Document the directory structure in a hierarchical format
- Mark files that are not properly indexed with **(NOT INDEXED)**
- Are automatically updated after each fix operation when `generate_jdex` is enabled
- Are only rewritten when their content changes, and have no timestamp, so runs that change nothing leave nothing for auto-commit
- Are generated for Areas before the root, so the root lists each Area's current index file. Index files left behind by a renamed directory are deleted
- Support Obsidian-style wiki links for markdown files (`[[filename]]`)
