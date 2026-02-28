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

### Data Platforms: Bruin
- Context: Bruin is used to orchestrate end-to-end pipelines, bridging the gap between raw data ingestion and validated analytics. More details at @./05-data-platforms/README.md
- Rule: Use `.bruin.yaml` files to define tasks and metadata.
- Implementation strategies:
    1. Ingestion Pattern (EL)
        - Method: Use the ingestr type for direct source-to-destination sync.
        - Implementation: 
            - Define a `pipeline.yml` file in the `pipeline/` directory.
            - Set type: `ingestr`.
            - Strategy: Always land data into a `raw` or `staging` schema first. Do not transform during this step.
            - Metadata: Include `source_connection` and `destination` explicitly.
    2. Transformation Pattern (T)
        - SQL Assets:
            - File Header: Use the /`* @bruin ... @bruin */` block for metadata.
            - Materialization: Use `type: table` for final outputs and type: view for intermediate logic.
            - Incremental: Use `incremental: true` with a where clause referencing `{{ last_run_date }}` to process only new data.
        - Python Assets:
            - Method: Use `bruin-python` for complex logic (API enrichment, PII masking).
            - Implementation: Must include a `materialize()` function that returns a Pandas/Polars DataFrame. Bruin handles the loading to the destination via uv.
    3. Data Quality (DQ) Strategy
    Blocking Gates: Quality checks are blocking by default. If a check fails, downstream assets will not run.
        - Built-in Column Checks: Define these inside the `columns` list of any asset:
            - `not_null`: Fails if any nulls are found.
            - `unique`: Fails if duplicate values exist.
            - `accepted_values`: Fails if values fall outside a provided list
            - `positive`: Fails if numeric values are less than 0.
        - Custom SQL Checks: For business logic, use the custom_checks block:
            - Pattern: Write a query that should return 0 rows (or a specific value).
            - Example: Verify that total_order_amount equals the sum of line_item_prices.

- 🤖 Helper Prompts for Bruin Data Management
    - For ELT: "Create an ELT flow: Ingest raw 'orders' data to DuckDB, then create a SQL transformation that joins it with 'customers', adding a unique check on the order_id."
    - For Data Quality: "Review my @bruin-asset.sql and suggest three custom SQL quality checks to ensure the total tax amount is never negative and always less than the subtotal."
    - For Incremental Processing: "Modify this Bruin SQL task to be incremental. Use a high-water mark pattern based on the updated_at column."

### dlt
- Context: dlt or data load tool is an open-source Python library designed to simplify and automate the process of building data ingestion pipelines (Extract, Load, Transform - ELT). It allows data professionals to load data from various sources into well-structured datasets without requiring complex infrastructure like backends or containers.
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