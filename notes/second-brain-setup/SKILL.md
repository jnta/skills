---
name: second-brain-setup
description: Initialize the current directory as a second brain repository using the PARA system and qmd for semantic search. Checks for qmd (installs if missing), creates Projects/Areas/Resources/Archives folders, writes AGENTS.md with PARA context and qmd usage docs, and initializes qmd indexing. Use when user wants to set up a new second brain, initialize a PARA repository, or bootstrap a knowledge base.
---

# Second Brain Setup

## Quick Start

Run from the target directory:

```
qmd --version || npm install -g @tobilu/qmd
mkdir -p Projects Areas Resources Archives
qmd init
qmd collection add . --name second-brain --mask "**/*.md"
qmd context add qmd://second-brain "Second brain knowledge base using PARA system"
qmd embed
```

Then write `AGENTS.md` with PARA structure, collection info, and qmd usage (see [Writing AGENTS.md](#writing-agentsmd)).

## Workflows

### Setup a new second brain

1. Verify/install qmd: `qmd --version` or `npm install -g @tobilu/qmd`
2. Create PARA folders: `mkdir -p Projects Areas Resources Archives`
3. Initialize qmd: `qmd init`
4. Add collection: `qmd collection add . --name second-brain --mask "**/*.md"`
5. Add context: `qmd context add qmd://second-brain "Second brain knowledge base using PARA system"`
6. Add contexts per PARA category (optional but recommended):

   ```
   qmd context add qmd://second-brain/Projects "Active projects with deadlines"
   qmd context add qmd://second-brain/Areas "Ongoing responsibilities to maintain"
   qmd context add qmd://second-brain/Resources "Topics of interest for future reference"
   qmd context add qmd://second-brain/Archives "Inactive items from other categories"
   ```

7. Generate embeddings: `qmd embed`
8. Write `AGENTS.md` (see template below)

### Writing AGENTS.md

Write an `AGENTS.md` at the repo root with:

- **Identity**: This repo is a second brain using the PARA system. The agent is the mediator and organizer of this structure.
- **PARA structure**: Explain Projects (short-term, deadline-driven), Areas (ongoing responsibilities), Resources (reference topics), Archives (inactive items). Notes go into the appropriate folder based on actionability.
- **qmd usage**: Document key commands the agent should use:
  - `qmd search "query"` — BM25 keyword search
  - `qmd vsearch "query"` — semantic vector search
  - `qmd query "query"` — hybrid search with re-ranking (best quality)
  - `qmd search "query" --all --files --min-score 0.3` — export all matches for agent processing
  - `qmd get "path/to/file.md"` — retrieve a specific document
  - `qmd multi-get "Projects/**/*.md"` — batch retrieve by glob
  - `qmd update` — re-index collections after adding/changing files
  - `qmd embed` — regenerate embeddings after updates
  - `qmd status` — check index health
- **Maintenance**: Run `qmd update && qmd embed` after adding or modifying notes to keep the index current.
- **Conventions**: One idea per note (atomic), link between notes, use your own words, organize by actionability not topic.

## Advanced: Re-indexing after changes

```
qmd update       # re-scan filesystem for new/changed files
qmd embed        # regenerate vector embeddings
qmd status       # verify everything is healthy
```

## How to Request

Tell me you want to set up a second brain in a repo, and I'll run through the checklist above.
