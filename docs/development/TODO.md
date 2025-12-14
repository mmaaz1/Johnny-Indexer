## Development Experience 
- [f] Static Type Checking
- [!] Code Formatting and Linting
- [ ] Doc Generation
- [ ] Unit tests and coverage

## Features
- [f] Slow traversal - For each file rename, scans entire tree for references.
- [!] Validations - Validate 10-area, 10-category, 100 topic limits. Suffix is 4 lettered max. Validte no file exists past the bound.
        If validation fails, report in a file
- [!] Obsidian weblink fixer doesn't Doesn't handle inline references like `[link text](filename.md)`. Check if this should be handled
- [!] No conflict detection when renaming. We can accidentally lose a file.
- [!] Summary report for when unexpected things happen
- [ ] Dry Run Mode - Users cannot preview all changes without applying them. Current workflow is to commit changes through git then run script.

### Daily Committer
- [!] Make AI create a commit comment

## Tech Debt
- [ ] update_index_from_portions is failing silently. Figure out why. Either don't do this or add logging somehow.