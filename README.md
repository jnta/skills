# skills

A personal collection of AI agent skills — structured Markdown workflows that guide LLM-based coding agents through software development and knowledge management tasks.

## Structure

```
development/      Core dev pipeline: setup, design, plan, modify, verify
notes/            Second-brain and capture workflows
```

### development/

| Skill | Purpose |
|---|---|
| `setup-skills` | Bootstrap a project for AI agent workflows |
| `quality-gate-architect` | Auto-detect linters/formatters/tests and generate verification scripts |
| `write-a-skill` | Template for creating new skills |
| `adr-architect` | Interview-driven Architecture Decision Records |
| `task-manager` | Decompose ADRs into ordered JSON task pipelines |
| `code-modifier` | Execute tasks with scoped edits and quality gates |

### notes/

| Skill | Purpose |
|---|---|
| `second-brain-setup` | Initialize a PARA knowledge base with semantic search |
| `capture` | Classify and store information into the second brain |

## Philosophy

High-friction cognitive design (human + adr-architect) → low-friction automated execution (task-manager + code-modifier).

## Usage

Skills are loaded by an AI agent at runtime. Each skill is a `SKILL.md` file with YAML frontmatter that the agent uses to discover and invoke the right workflow.
