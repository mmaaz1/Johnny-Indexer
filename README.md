# Johnny Indexer

The Johnny Indexer is a Python-based tool designed to automate the indexing of files in a hierarchical directory structure using the [Johnny Decimal system](https://johnnydecimal.com/). This script removes all maintaining overhead required to ensure a consistent indexing format. It also auto-generates [JDex files](https://johnnydecimal.com/10-19-concepts/11-core/11.05-the-index/). 

---

## Features

- **Automatic Indexing**: Analyzes and updates file indexes based on their hierarchical position.
- **Interactive Index Correction**: Prompts users to confirm changes for file names that are incorrectly indexed.
- **Jdex Generation**: Produces a Markdown file summarizing the directory structure and indexing status.
---

## Usage

To fix and generate indexes for files in a directory, run:
```bash
python fix_indexes.py <path_to_directory>
```

**Note:** You need to manually create the Area indexes with the format `X0-X9` for the script to work. All files and directories within the areas will be indexed by this script.

## Johnny Index System

ToDo: Define the system

## Testing

ToDo: Put testing command here.
