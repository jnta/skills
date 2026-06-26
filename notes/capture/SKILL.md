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

- If user specified a category (Projects/Areas/Resources/Archives), set folder accordingly
- If not, infer category from qmd results (pick the PARA folder most related notes are in; fallback to Resources)

### 2. Decision Matrix

Parse scores from qmd JSON. Let `max_score` be the highest score found:

| Score | Action |
|-------|--------|
| `>= 0.85` AND intent is continuation/update | **Append** to existing file |
| `0.65` to `< 0.85` | **Create new** + link to matched notes |
| `< 0.65` | **Create new** (no links) |

### 3. Create new file

Name: `YYYYMMDDHHMM-lowercase-slug.md` under the appropriate PARA folder.

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

* [[timestamp-slug-of-related-note]]
```

Rules:
- `type`: `fleeting` for raw capture, `literature` for summarized source, `permanent` for distilled thought
- PARA category is folder-based only — do NOT put in frontmatter
- Links go under `## Relationships` in the body (Obsidian graph view needs them there)

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
