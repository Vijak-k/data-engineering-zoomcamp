# Data Engineering Zoomcamp 2026

## Context
- Objective: Mastering end-to-end data pipelines from ingestion to analytics.
- Role: Coding assistant for data engineering workflow.

---

## Tools
- Rule and description of data engineering tools used in this course

### Package Manager: uv
- Rule: Always use `uv run` to execute scripts.
- Rule: Use `uv add` for new dependencies to maintain `pyproject.toml`.

### dlt
- Rules Directory: @./workshop-01-dlt/.cursor/rules/
- Implementation Strategy:
    1. Primary Logic: Follow the rules defined in the `@` directory above for naming conventions and resource structure.
    2. Write Disposition: Default to `merge` using a `primary_key` to avoid duplicates unless `replace` is needed for testing.
    3. Environment: Assume the project is located in the `./workshop-01-dlt/` subdirectory, otherwise specified.
    4. State Management: Use `dlt` state to handle incremental loading; do not hardcode offsets.
- Helper Prompts:
    - "Check the @./workshop-01-dlt/.cursor/rules/ and explain the naming convention for new resources."
    - "Generate a new dlt resource for the OpenLibrary API in @./workshop-01-dlt/open_library_pipeline.py following the project rules."

---

## 🗒️ Global Memory & Shortcuts
- Refresh Command: `/memory refresh` (Run this after updating this file).
- Verify Tools: `/mcp list`.