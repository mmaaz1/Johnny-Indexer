# Johnny Indexer

The Johnny Indexer is a Python-based tool designed to automate the indexing of files in a hierarchical directory structure using the [Johnny Decimal system](https://johnnydecimal.com/). This script removes all maintaining overhead required to ensure a consistent indexing format. It also auto-generates [JDex files](https://johnnydecimal.com/10-19-concepts/11-core/11.05-the-index/). 


## Features

- **Automatic Indexing**: Analyzes and updates file indexes based on their hierarchical position.
- **Jdex Generation**: Produces a Markdown file summarizing the directory structure and indexing status.
- **File Exclusion**: Allows users to exclude files
- **Interactive Index Correction**: Prompts users to confirm changes for file names that are incorrectly indexed.
- **Automatic File Link Fixing**: Fixes all the file content

### Additional Scripts
- **Daily Committer**: Script that can be used to commmit changes to your documentation daily

### Configuration
- `prefixes_excluded_from_indexing`: File prefixes that are ignored by the indexer
- `patterns_excluded_from_indexing`: File regex patterns that are ignored by the indexer
- `fix_weblinks`: Whether the script should fix file weblinks at the end of indexing fixes
- `prompt_for_approval`: Whether the should should prompt user for approval before each fix

## Knowledge Base Setup

In your knowledge base, manually create the Area indexes with the format `X0-X9`. All files and directories within the areas will be indexed by this script.

## Usage

To fix and generate indexes for files in a directory, run:
```bash
python fix_indexes.py <path_to_directory>
```

### Cron Usage
Here is a sample cron job to fix indexes and create commit:
```bash
*/30 * * * * SCRIPT_DIR_PATH/.venv/bin/python3 SCRIPT_DIR_PATH/fix_indexes.py NOTES_PATH >> SCRIPT_DIR_PATH/logs/fix_indexes_MaazWorkNotes.log 2>&1
*/5 * * * * SCRIPT_DIR_PATH/.venv/bin/python3 SCRIPT_DIR_PATH/related_scripts/commit_daily.py NOTES_PATH >> SCRIPT_DIR_PATH/logs/commit_daily.py.log 2>&1
```

## Johnny Index System Specification

The Johnny Indexer implements a hierarchical indexing system based on the Johnny Decimal methodology. Files are organized into a nested directory structure with specific index formats at each level.

### Hierarchy Format Strategy

The system defines seven types of organization across 4 levels:

1. **Area** (Level 0) - Groups broad organizational divisions of your life or expertise.
    - Format: `X0-X9` (e.g., `10-19`, `20-29`)
    - Parent: System Root
    - Max: 10 areas per system

1. **Category** (Level 1) - Groups related items within an area by a subject matter.
    - Format: `XY` (e.g., `11`, `12`, `23`)
    - Parent: Area
    - Max: 10 categories per area

1. **Topic** (Level 2) - Main unit of a note in which you keep your actual materials (documents, notes, files). These are topical containers with descriptive names (e.g., `12.21 Electricity, gas, & water`)
    - Format: `XX.YY` (e.g., `11.01`, `11.05`, `12.03`)
    - Parent: Category
    - Max: 100 topics per category

1. **Extension** (Level 3) - Groups Topics further into specialized subdivisions
    - Format: `XX.XX+SUFF` (e.g., `11.05+DOCS`, `12.03+CODE`)
    - Parent: Topic
    - Max: Unlimited, but < 5 is preferred

1. **Subtopic Type 1** (Level 3) - Splits up a topic into smaller pieces of notes
    - Format: `XX.XX-Y*` (e.g., `11.05-1`, `11.05-10`, `12.03-5`)
    - Parent: Topic
    - Max: 100 subtopics per topic

1. **Subtopic Type 2** (Level 4) - Splits up a topic into smaller pieces of notes
    - Format: `XX.XX+SUFF-Y*` (e.g., `11.05+DOCS-1`, `12.03+CODE-15`)
    - Parent: Extension
    - Max: 100 subtopics per extension

1. **The Rest** (Level 4+) - The system has given up. Existence of these files indicates you need to re-organize
    - Format: `Y*` (e.g., `1`, `25`, `100`)
    - Parent: Subtopic Type 1 or Subtopic Type 2
    - Max: Unlimited

## Design and Implementation

### Glossary

1. **Proper Index**: A file that is indexed according to the format specifications for its hierarchy level
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

1. **Initialize**: Start with all Area directories at Level 0
1. **Collect Changes**: For each directory level:
   - Scan all non-excluded files in current level
   - Sort files alphabetically by filename
   - Assign main indexes based on position in sorted list (0, 1, 2, ...) with zero-padding to match directory width
   - For Topics, ensure main indexes always have 2 digits (e.g., `01`, `02`, `10`)
   - For Extensions, preserve their alphabetic suffix (e.g., `+DOCS`, `+CODE`)
   - Combine parent index + separator + main index to create expected full index
   - Identify files where actual index doesn't match expected index
1. **Sort & Present**: Sort proposed changes alphabetically by new filename
1. **User Confirmation** (if enabled): Prompt user to accept (`y`) or reject (`n`) changes
1. **Update Links** (if enabled):
   - Search all files in the directory tree for references to the old filename
   - Update any found links to point to the new filename
1. **Apply Rename**: Rename the file on disk
1. **Recurse**: Move to the next directory level and repeat from step 2
1. **Generate JDex**: After all renames complete, regenerate index files

### JDex File Generation

The system automatically generates Markdown index files (`Index of [DirectoryName].md`) at the root and in each Area. These files:

- Document the directory structure in a hierarchical format
- Mark files that are not properly indexed with **(NOT INDEXED)**
- Are automatically updated after each fix operation
- Support Obsidian-style wiki links for markdown files (`[[filename]]`)


## Resources
- For development, check out `docs/development/DEVELOPMENT.md`