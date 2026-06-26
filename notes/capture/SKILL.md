---
name: capture
description: Capture information into a second brain repository using the CODE framework. Interprets `capture` commands, categorizes into PARA via qmd semantic search, creates/updates atomic Markdown notes with Obsidian wikilinks, and maintains qmd index. Use when user says "capture" followed by text or a PARA category.
---

# Capture

## Quick Start

User says `capture <text>` or `capture <category> <text>`.
Agent runs: `qmd query "<text>" --json --all` -> classify -> create/append -> re-index.

## Ingestion Pipeline

### 1. Search & Classify

- If user explicitly specified a category (e.g. `capture Projects <text>`), set `OVERRIDE_CATEGORY` and **skip all algorithmic routing** — the file goes directly to that folder with no PARA link injection.
- Otherwise, run qmd search and proceed to algorithmic routing below.

### 2. Decision Matrix (Intent Matching)

Parse scores from qmd JSON. Let `max_score` be the highest score found:

| Score | Action |
|-------|--------|
| `>= 0.85` AND intent is continuation/update | **Append** to existing file → skip creation, go to re-index |
| `0.65` to `< 0.85` | **Create new** — proceed to PARA Routing |
| `< 0.65` | **Create new** (no links) — proceed to PARA Routing |

### 3. Create new file (with PARA Routing substep)

Name: `YYYYMMDDHHMM-lowercase-slug.md` under the appropriate PARA folder.

#### Substep: PARA Routing Rules

Evaluate the **same** qmd JSON array against metadata dimensions:

1. **Project Match** — Is there a note where `type == "project"` and `score >= 0.75`?
   - `SAVE_PATH = ./vault/Projects/`
   - `PRIMARY_LINK = [[Project-Name]]`
   - `ACTIVE_PROJECT = Project-Name`
   - STOP — do not evaluate Area.

2. **Area Match** — (if no Project matched) Is there a note where `type == "area"` and `score >= 0.75`?
   - `SAVE_PATH = ./vault/Areas/`
   - `PRIMARY_LINK = [[Area-Name]]`

3. **Default** — Neither matched:
   - `SAVE_PATH = ./vault/Resources/`
   - `PRIMARY_LINK = null`

4. **Displacement Check** — Only if `ACTIVE_PROJECT` is defined (Step 1 succeeded):
   - Scrutinize all existing notes in results.
   - IF any existing note currently in `/Areas/` or `/Resources/` scores `>= 0.88`:
     - Execute physical `mv` to `./vault/Projects/`
     - Append `* [[ACTIVE_PROJECT]]` to that existing note's `## Relationships`
     - Force this new capture's `SAVE_PATH` to `./vault/Projects/`

#### Template

```markdown
---
title: "<Clean Title>"
created: YYYY-MM-DD HH:MM
type: fleeting | literature | permanent
tags: []
---

# <Clean Title>

## Core Concepts

Content body.

## Relationships
* [[PRIMARY_LINK]]
* [[secondary-matches-between-065-and-074]] (Tangential Reference)
```

Rules:
- `type`: `fleeting` for raw capture, `literature` for summarized source, `permanent` for distilled thought
- PARA category is folder-based only — do NOT put in frontmatter
- PRIMARY_LINK (from PARA routing) gets the top bullet; secondary matches (0.65–0.74) go below
- Soft link (0.75–0.87): leave existing note in place, cross-reference only

### 4. Append (score >= 0.85, continuation)

- Read existing file
- Add entry under `## Updates` (create section if missing) with timestamp
- Update/insert `modified` field in frontmatter

### 5. Re-index

```
qmd update && qmd embed
```

## Examples

```
User:  capture just read about RAG in LLMs
Agent: [qmd scores all < 0.65, creates Resources/202606261830-retrieval-augmented-generation.md]

User:  capture Projects working on db migration
Agent: [saves to Projects/202606261835-database-migration-script.md]

User:  capture the migration script needs Python 3.11
Agent: [qmd finds existing note at 0.91, appends under ## Updates]
```
