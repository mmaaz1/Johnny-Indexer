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

## Design and Implementation

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
- Support Obsidian-style wiki links for markdown files (`[[filename]]`)
