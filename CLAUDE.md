# Guidelines for Claude Code

1. NEVER use `# type: ignore` exceptions without confirming with the user first. Usually this indicates that there are issues with design/implementation.
1. After making changes to the codebase, ALWAYS update the relevant documentation files. Most notably, README.md and DEVELOPMENT.md.
1. Run `just check` and `just format` after your tasks to ensure things are working.