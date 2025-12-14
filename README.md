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

## Setup

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

### Hierarchy Levels

The system defines seven types of organization across 4 levels:

1. **Area** (Level 0) - Represents the broadest category of information
    - Format: `X0-X9` (e.g., `10-19`, `20-29`)
    - Parent: Area
    - Max: 10 areas per system

2. **Category** (Level 1) - Provides subdivision within an area
    - Format: `XY` (e.g., `11`, `12`, `23`)
    - Parent: Area
    - Max: 10 categories per area

3. **Topic** (Level 2) - ToDo
    - Format: `XX.YY` (e.g., `11.01`, `11.05`, `12.03`)
    - Parent: Category
    - Max: 100 topics per category

4. **Extension** (Level 3) - Allows organizing related content under a single topic
    - Format: `XX.XX+SUFF` (e.g., `11.05+DOCS`, `12.03+CODE`)
    - Parent: Topic
    - Max: Unlimited, but < 5 is preferred

5. **Subtopic Type 1** (Level 3) - Creates numbered subdivisions within a topic
    - Format: `XX.XX-Y*` (e.g., `11.05-1`, `11.05-10`, `12.03-5`)
    - Parent: Topic
    - Max: 100 subtopics per topic

6. **Subtopic Type 2** (Level 4) - Creates numbered subdivisions within an extension
    - Format: `XX.XX+SUFF-Y*` (e.g., `11.05+DOCS-1`, `12.03+CODE-15`)
    - Parent: Extension
    - Max: 100 subtopics per extension

7. **The Rest** (Level 4+)
    - Format: `Y*` (e.g., `1`, `25`, `100`)
    - Parent: Subtopic Type 1 or Subtopic Type 2
    - Max: Unlimited

### Index Format Rules

- **Proper vs. Improper**: The system distinguishes between properly formatted indexes (as defined above) and improperly formatted indexes. Files with improper indexes are still recognized but marked for correction.
- **Padding**: Main indexes are padded with leading zeros to maintain uniform length within a directory (e.g., `01`, `02`, `10`).
- **Topic Padding**: Topics always use two-digit main indexes regardless of count (e.g., `11.01`, `11.02`).

### Index Computation Algorithm

When fixing indexes, the system computes two portions:

1. **Parent Index**: Extracted from the parent directory's index
   - For files under an Area, parent index is the area's main index
   - For files under a Subtopic, parent index is empty
   - For files under other indexed items, parent index is the parent's full index

2. **Main Index**: Assigned sequentially to siblings
   - Files in a directory are sorted alphabetically
   - Each file receives an index based on its position (0, 1, 2, ...)
   - The index is padded to match the number of siblings in the directory

3. **Final Index**: Constructed by combining parent and main indexes with the appropriate separator

### Directory Processing

Files are processed using a breadth-first search (BFS) algorithm:

1. Start with all Area directories
2. For each directory level, collect all files and proposed changes
3. Sort proposed changes alphabetically by new file name
4. Prompt user for confirmation of each change (if enabled)
5. Update weblinks in other files if linking is enabled (if enabled)
6. Apply the file rename
7. Process the next level of directories

### JDex File Genration

The system automatically generates Markdown index files (`Index of [DirectoryName].md`) at the root and in each Area. These files:

- Document the directory structure in a hierarchical format
- Mark files that are not properly indexed with **(NOT INDEXED)**
- Are automatically updated after each fix operation
- Support Obsidian-style wiki links for markdown files (`[[filename]]`)

## Testing

ToDo: Put testing command here.
