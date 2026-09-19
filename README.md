# Johnny Indexer

The Johnny Indexer is a Python tool designed to automate the indexing of files using the [Johnny Decimal system](https://johnnydecimal.com/).

It also comes with some additional goodies:
1. **Obsidian integration**: Updates wiki links (`[[filename]]`) to renamed files, and generates JDex index files with wiki links
1. **Git integration**: Commits and pushes your notes before each run, so every run has a restore point


## Setup

1. Install Python 3.12 or newer.
1. From this repo's directory, create the virtual environment and install the `johnny-indexer` command:
   ```bash
   python3 -m venv venv
   venv/bin/pip install -e .
   ```
1. Optionally, override the default config in `config.override.yaml` (see [Additional Configuration](#additional-configuration)). Eg:
   ```yaml
   auto_commit: true
   auto_push: true
   ```

### Knowledge Base Setup

In your knowledge base, manually create the Area indexes with the format `X0-X9`. All files and directories within the areas will be indexed by this script.

## Usage

### One-time
Run:
```bash
venv/bin/johnny-indexer fix "/path/to/notes"
```

### Recurring (Linux and macOS)
Schedule the indexer to run every few hours, anchored at 12 pm local time. Logs are written in `logs/fix_indexes_<notes directory name>.log`

0. On macOS, notes in iCloud Drive, Documents or Desktop need `/usr/sbin/cron` to have Full Disk Access (System Settings > Privacy & Security).
1. Schedule the indexer:
   ```bash
   venv/bin/johnny-indexer schedule install "/path/to/notes"
   ```
   - `--hours N` sets the hours between runs: `1`, `2`, `3`, `4`, `6`, `8`, `12` or `24` (default). Eg: `--hours 6`.
   - `--skip-test` skips the setup check that runs the indexer once during install.

Manage scheduled runs:
```bash
venv/bin/johnny-indexer schedule status
venv/bin/johnny-indexer schedule uninstall "/path/to/notes"
```

## Additional Configuration
Defaults are in `config.defaults.yaml`. To change an option, set it in `config.override.yaml`, which only needs the options you change.

### Exclude Files
Excluded files are never renamed, aren't marked **(NOT INDEXED)** in JDex files, and aren't scanned for links.
- `prefixes_excluded_from_indexing`: File name prefixes to exclude (eg: `.` for hidden files)
- `patterns_excluded_from_indexing`: File name regex patterns to exclude (eg: `^\d{4}-\d{2}-\d{2}` for dated notes)

### Fix Obsidian Wiki Links
- `fix_wikilinks`: When `true`, updates Obsidian wiki links (`[[filename]]`) in Markdown files to point to renamed files

### Prompt User Before Acting
- `prompt_for_approval`: When `true`, asks for confirmation before each rename. Answering `n` stops the run.
  Only applies when running in a terminal. Scheduled and other non-interactive runs apply renames without prompting.

### Generate JDex
- `generate_jdex`: When `true`, regenerates the [JDex files](docs/DEVELOPMENT.md#jdex-file-generation) after fixing indexes

To generate JDex files without fixing indexes, run `venv/bin/johnny-indexer jdex "/path/to/notes"`.

### Auto Commit
The notes directory must be in a git repository. Failures are reported in the output but never stop the indexer.
- `auto_commit`: When `true`, commits the notes directory to git before fixing indexes, so every run has a restore point
- `auto_push`: When `true`, pushes to the notes repository's remote. Commits from an earlier failed push are retried on the next run.
  - Scheduled runs can't use the macOS keychain, so use an SSH remote (eg: `git@github.com:user/notes.git`) with a key that has no passphrase.

## Documentation

- **[JOHNNY_INDEX_SPECIFICATION.md](docs/JOHNNY_INDEX_SPECIFICATION.md)** - Specification of the index formats at each hierarchy level
- **[DEVELOPMENT.md](docs/DEVELOPMENT.md)** - Instructions for developing the code, and its design and implementation
- **[TODO.md](docs/TODO.md)** - List of outstanding tasks and future work items
- **[CLAUDE.md](CLAUDE.md)** - Instructions for the AI agent on how to develop this codebase
- **[ai-brainstorming](docs/ai-brainstorming)** - Directory used to keep a log of brainstorm sessions with an AI agent
- **[projects](docs/projects)** - Plans for in-progress projects
- **[projects/completed](docs/projects/completed)** - Plans for projects that are done