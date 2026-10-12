---
name: skill-creator
description: Guide for creating agent skills. Use when asked to create, write, or add a new skill, or when packaging domain knowledge as a reusable skill for AI agents.
---

# Creating a Skill
Skills live in `.github/skills/<skill-name>/SKILL.md`. Each skill is a folder containing at minimum a `SKILL.md` file.

## SKILL.md structure
```markdown
---
name: skill-name          # lowercase, hyphens only, max 64 chars
description: What this skill does and when to use it in third person. Use when [specific triggers]. Max 1024 chars.
---

# Skill Body and Placement

```

## Placement rules

- **Project skills**: `.../.agents/skills/<name>/SKILL.md` (this repo)
- **Global skills**: `~/.agents/skills/<name>/SKILL.md`

## Writing good descriptions

The description is how Copilot decides whether to load the skill. Include:

- What the skill does
- When to use it (trigger words, task types)
- Write in **third person** — never "I can..." or "You can..."

```yaml

# Good

description: Analyzes Excel spreadsheets and generates pivot tables. Use when working with .xlsx files, spreadsheets, or tabular data analysis.

```

```yaml

# Bad

description: Helps with documents

```

## Writing the body

- Keep under 200 lines
- Only include what the agent doesn't already know
- Match specificity to how fragile the task is:
  - **High freedom**: text instructions for flexible tasks
  - **Low freedom**: exact scripts/commands for fragile operations
- Split large content into linked reference files loaded on demand with progressive disclosure

## Progressive disclosure

For large skills, reference additional files instead of including everything:

```text

skill-name/
├── SKILL.md          # overview + links
└── references/       # loaded only when needed
|   └── reference-name.md
└── scripts/          # invoked when needed
|   └── helper.py
└── assets/
    └── icon.svg

```

In SKILL.md, link to them:

```markdown

For advanced usage, see [reference.md](reference.md).

```

### When to Add Scripts

Add utility scripts when:

- Operation is deterministic (validation, formatting)
- Same code would be generated repeatedly
- Errors need explicit handling
- Scripts save tokens and improve reliability vs generated code.

### When to Split Files

Split into separate files when:

- SKILL.md exceeds 200 lines
- Content has distinct domains (finance vs sales schemas)
- Advanced features are rarely needed

## Checklist

1. **Gather requirements** - ask user about:
   - What task/domain does the skill cover?
   - What specific use cases should it handle?
   - Does it need executable scripts or just instructions?
   - Any reference materials to include?

2. **Create folder `.agents/skills/<name>/`**

3. **Write `SKILL.md` with valid frontmatter** (`name`, `description`)
   - Keep body concise — assume the agent is capable
   - Additional reference files if content exceeds 200 lines

4. **Review with user** - present draft and ask:
   - Does this cover your use cases?
   - Anything missing or unclear?
   - Should any section be more/less detailed?

After drafting, verify:

- Description includes triggers ("Use when...")
- SKILL.md under 200 lines
- No time-sensitive info
- Consistent terminology
- Concrete examples included
- References one level deep

