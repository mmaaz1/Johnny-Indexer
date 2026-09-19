## Development Experience 
- [f] Class docs for all classes and automatic doc generation.
- [ ] Unit tests and coverage

## Features
- [!] Validations - Validate 10-area, 10-category, 100 topic limits. Suffix is 4 lettered max. Validte no file exists past the bound.
        If validation fails, report in a file
- [!] Obsidian wiki link fixer doesn't handle inline references like `[link text](filename.md)`. Check if this should be handled
- [ ] Dry Run Mode - Users cannot preview all changes without applying them. Current workflow is to commit changes through git then run script.

### Auto Commit
- [f] Make AI create a commit comment

## Tech Debt
- [ ] update_index_from_portions is failing silently. Figure out why. Its errors are now logged at `DEBUG`.