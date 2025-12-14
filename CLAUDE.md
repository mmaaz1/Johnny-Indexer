# Guidelines for Claude Code

## Git Operations

**NEVER make git commits or git pushes.**

All git operations must be done by the user manually. This includes:
- `git add`
- `git commit`
- `git push`
- `git pull`
- Any other git commands

If changes need to be committed, notify the user and let them handle it.

---

## Documentation Updates

After making changes to the codebase, **always update the relevant documentation files**.

### Critical Documentation Files

These files must be kept in sync with code changes:

- **README.md** - Project overview, features, usage instructions, and Johnny Decimal system specification
- **DEVELOPMENT.md** - Setup instructions, type checking configuration, development guidelines, and testing procedures

### When to Update Documentation

Update documentation whenever you:

- Add or remove features
- Change configuration (e.g., pyproject.toml, type checking rules)
- Modify setup or installation procedures
- Update development guidelines or best practices
- Change testing approaches or add new test suites
- Complete significant implementation phases or milestones

### Documentation Update Checklist

- [ ] README.md - Update if features, usage, or system specification changed
- [ ] DEVELOPMENT.md - Update if setup, configuration, or development guidelines changed
- [ ] Task files in docs/tasks/ - Mark completed items and summarize changes
- [ ] Code comments - Add clarifying comments for complex logic
- [ ] Type annotations - Ensure all new functions have complete type hints

### Examples

**Type Checking Work:**
- Updated pyproject.toml → Update DEVELOPMENT.md with new settings
- Added type hints to modules → Update DEVELOPMENT.md with list of typed modules
- Changed type checking mode → Update DEVELOPMENT.md with new configuration

**Feature Implementation:**
- Added new CLI flag → Update README.md usage section
- Changed error handling → Update DEVELOPMENT.md guidelines
- Modified file indexing algorithm → Update README.md system specification

### How to Update

1. Read the current documentation file
2. Identify what needs to change based on code modifications
3. Update the relevant sections with accurate information
4. Include current status, new features, or changes made
5. Verify the documentation is clear and complete

---

**Remember:** Good documentation helps future developers (including future you) understand the project quickly and accurately.
