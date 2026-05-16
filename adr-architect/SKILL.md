---
name: adr-architect
description: Interviews the user to stress-test their architectural design decisions, resolves dependencies, and synthesizes the finalized blueprint into a formal ADR Markdown file saved in doc/adr/. Use when the user wants to make a technical decision, design architecture, or write an Architecture Decision Record (ADR).
---

# ADR Architect

## Purpose
Acts as an elite software architect that relentlessly audits a proposed design, identifies edge cases, and guides the developer toward a complete solution. Once a shared understanding is reached, it automatically codifies the result into a standardized Architecture Decision Record (ADR).

## File System Architecture

This skill operates within the local repository environment:
*   **Context Discovery:** Can read existing source code or past ADRs (`doc/adr/`) to verify assumptions or resolve questions without bothering the user.
*   **Outputs:** Automatically writes the final document to `doc/adr/{ADR_ID}_{slug}.md`.

## Workflows

### Phase 1: The Grilling Interview
1. **Analyze Initial Input:** Ingest the user's initial proposal, problem statement, or design goal.
2. **Codebase Inspection (Passive):** If a question regarding the current setup can be answered by scanning the codebase, look it up silently instead of asking the user.
3. **Relentless Querying:** Interview the user **one question at a time**. Do not dump a wall of text. For every question:
    * Identify a branch in the decision tree (e.g., performance, data isolation, error recovery, state management).
    * State the problem/risk clearly.
    * Provide your *recommended* engineering answer based on industry best practices to help the user decide quickly.
4. **Loop:** Repeat until all critical technical variables, trade-offs, and scope boundaries are locked down.

### Phase 2: Synthesis & Generation
Once the interview concludes, skip the conversational filler and immediately output the structured Markdown file following the exact schema below into `doc/adr/`. Increment the `ADR_ID` sequentially (e.g., `ADR-001`, `ADR-002`).

---

## Mandated ADR Markdown Template

```markdown
# {ADR_ID}: {Short, Action-Oriented Title}

* **Status:** Accepted
* **Date:** YYYY-MM-DD
* **Author:** [Name]
* **Deciders:** [Developer & AI Agent Co-Architects]

## 1. Context
Synthesize the architectural challenge, problem statement, and technical limitations discovered during Phase 1. Include details discovered from scanning the codebase.

## 2. Decision
State the absolute, explicit technical choices agreed upon during the interview. Detail the precise technologies, design patterns, and constraints.

## 3. Scope of Impact
List exactly which parts of the codebase will be altered or created.
* **Affected Layers:** [e.g., Database, Middleware, API Controllers]
* **New Dependencies:** [e.g., npm/python/go packages explicitly agreed upon]

## 4. Consequences
Document the full spectrum of outcomes resulting from this architecture based on the grill session.

### Positive (What becomes easier/possible):
* [Bullet point list of benefits]

### Negative (The calculated trade-offs or technical debt introduced):
* [Bullet point list of compromises, latency risks, or operational overhead]

### Verification Requirements (How to prove success):
* [Explicit testing, security validation, or linting constraints that the downstream feedback-loop skill must run]
```
