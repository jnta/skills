---
name: setup-skills
description: Initializes the workspace for AI agent assembly lines. It creates doc/AGENTS.md and chains into quality-gate-architect if needed. Use when initializing a new repository or onboarding agents.
---

# Setup Skills

## Purpose
Idempotently bootstraps the project repository rules, folders, and quality hooks for autonomous development agents.

## Workflows

### 1. Guardrail Check
Check if `doc/AGENTS.md` exists. 
*   **If it exists:** Terminate immediately. Print: `"Workspace already initialized."`
*   **If it does not exist:** Proceed.

### 2. Write doc/AGENTS.md
Create the `doc/` directory if missing and write the following minimal guide directly to `doc/AGENTS.md`:

```markdown
# Repository Agent Guidelines
This project enforces a phased, automated assembly line for code changes.

## 📁 Paths
*   `doc/adr/` : Architecture Decision Records (*.md)
*   `doc/tasks/` : Phased execution pipelines (*_pipeline.json)

## 🛑 Hard Rules
1. Never edit files outside a task's defined `scope.target_files`.
2. Update task states to `in_progress` and `completed` on disk as you work.
3. You cannot advance to the next phase until the `quality-checker` skill passes.
```

### 3. Chain to Quality Gate Architect
After creating `doc/AGENTS.md`, invoke the `quality-gate-architect` skill to auto-discover the project's quality tools and generate the `quality-checker` skill.
