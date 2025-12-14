## Development Experience 
- [ ] Code Formatting and Linting
- [ ] Static Type Checking
- [ ] Doc Generation
- [ ] Unit tests and coverage

## Features
- [ ] Slow traversal - For each file rename, scans entire tree for references.
- [ ] Validations - Validate 10-area, 10-category, 100 topic limits. Validte no file exists past the bound.
        If validation fails, report in a file
- [ ] Dry Run Mode - Users cannot preview all changes without applying them. Current workflow is to commit changes through git then run script.
- [ ] Obsidian weblink fixer doesn't Doesn't handle inline references like `[link text](filename.md)`. Check if this should be handled
- [ ] No conflict detection when renaming. We can accidentally lose a file.
- [ ] Summary report for when unexpected things happen

### Daily Committer
- [ ] Make AI create a commit comment

## Tech Debt
- [ ] update_index_from_portions is failing silently. Figure out why. Either don't do this or add logging somehow.