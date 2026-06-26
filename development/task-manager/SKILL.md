---
name: task-manager
description: Reads an Architecture Decision Record (ADR) from doc/adr/ and outputs a structured, machine-readable JSON pipeline of sequential, phased execution tasks into doc/tasks/.
---

# Task Manager

## Purpose
Converts a text-based ADR document into a strictly ordered, multi-phase atomic execution graph for an AI Agent. This skill prevents context drift, maintains global task traceability, and enforces modular state boundaries.

## File System Architecture

This skill operates within a standardized `doc/` directory structure at the root of the project:
*   **Inputs:** Read from `doc/adr/{ADR_ID}_{slug}.md` (e.g., `doc/adr/ADR-004_postgres_rls.md`).
*   **Outputs:** Written to `doc/tasks/{ADR_ID}_pipeline.json` (e.g., `doc/tasks/ADR-004_pipeline.json`).

## Workflows

1. **Analyze ADR:** Read the target Markdown file inside `doc/adr/` to extract architectural context, core decisions, and technical consequences.
2. **Generate Task Pipeline:** Output a single, valid JSON object following the strict schema below and save it to the designated path in `doc/tasks/`.

### Mandatory Execution Logic

*   **Global Uniqueness (Id Schema):** To prevent collisions across multiple architectural documents, every single task ID must be globally unique and prefixed with the ADR identity. Follow the rigid pattern: `{ADR_ID}-PH{phase_number}-TSK{task_number}` (e.g., `ADR-004-PH1-TSK1`). 
*   **Traceable Dependencies:** All strings listed within a task's `scope.dependencies` array must use the fully namespaced ID format (e.g., `["ADR-004-PH1-TSK1"]`).
*   **Atomicity:** Every item in the `tasks` array must represent a micro-action (e.g., creating one file, editing one module). Never group disparate structural changes into a single task.
*   **Target Scoping:** `scope.target_files` must strictly list explicit file paths relative to the project root directory.
*   **Phase Gates:** Every phase object must culminate in a `phase_gate` defining the automated testing, validation, or linting requirements required to unlock the subsequent phase loop.
*   **Test-Driven Acceptance:** The `acceptance_criteria` for any code-related task MUST explicitly include the creation and passing of relevant automated tests. If the task involves non-code changes (e.g., Docker configuration), testing requirements may be omitted.

### Expected JSON Output Schema

```json
{
  "adr_id": "string (e.g., ADR-004)",
  "title": "string (Title of the ADR)",
  "global_context": "string (High-level architectural constraints or patterns from the ADR that apply universally across all tasks)",
  "total_phases": "integer",
  "pipeline": [
    {
      "phase_number": "integer",
      "phase_name": "string (e.g., Database Schema & Migration)",
      "status": "pending" | "in_progress" | "completed" | "failed",
      "tasks": [
        {
          "task_id": "string (Pattern: {ADR_ID}-PH{phase_number}-TSK{task_number})",
          "title": "string (Clear, short action statement)",
          "execution_order": "integer (sequential starting at 1)",
          "status": "pending" | "in_progress" | "completed" | "failed",
          "scope": {
            "target_files": ["string (array of project-root relative file paths)"],
            "dependencies": ["string (array of prerequisite namespaced task_ids)"]
          },
          "instructions": "string (Detailed step-by-step implementation instructions. Markdown formatting may be used inside this string field)",
          "acceptance_criteria": [
            "string (Binary, testable verification conditions. MUST include writing/passing tests if the task involves code changes)"
          ],
          "output_format": {
            "type": "file_creation" | "file_modification" | "dependency_installation",
            "schema_or_template": "string (optional layout reference or template structural guide)"
          }
        }
      ],
      "phase_gate": {
        "trigger_skill": "string (Name of the verification skill, e.g., code_verification_agent)",
        "params": {
          "run_migrations": "boolean",
          "run_unit_tests": "boolean",
          "test_path": "string"
        }
      }
    }
  ]
}