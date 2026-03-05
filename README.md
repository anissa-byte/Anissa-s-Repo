# Anissa's Skills

A Claude Code plugin repository containing custom skills, commands, and agents.

## Structure

```
├── .claude-plugin/
│   └── plugin.json      # Plugin manifest
├── skills/              # Auto-activating skills (subdirectories with SKILL.md)
├── commands/            # Slash commands (.md files)
├── agents/              # Subagent definitions (.md files)
└── scripts/             # Helper scripts and utilities
```

## Adding a Skill

Create a new subdirectory under `skills/` with a `SKILL.md` file:

```
skills/my-skill/
├── SKILL.md             # Required: skill definition with YAML frontmatter
└── references/          # Optional: supporting files
```

## Installation

Add this plugin to Claude Code:

```
claude plugin add /path/to/this/repo
```
