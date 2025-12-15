# Guidelines for Claude Code

1. NEVER make git commits or git pushes. All git operations must be done by the user manually.
1. NEVER use `# type: ignore` exceptions unless absolutely necessary. Usually this indicates that there are issues with design/implementation.
1. After making changes to the codebase, ALWAYS update the relevant documentation files. Most notably, README.md and DEVELOPMENT.md.
1. When asked to create a task doc, look at existing files in `docs/tasks` for inspiration and create one for your task