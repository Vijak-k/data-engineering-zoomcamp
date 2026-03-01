# NYC Taxi Data Platform (Bruin)

This directory contains an end-to-end ELT pipeline for NYC Taxi data built with **Bruin**. The pipeline handles data ingestion from public APIs, transformation/deduplication in a staging layer, and final aggregation for reporting.

## 📂 Project Structure

```text
05-data-platforms/
├── homework/                # Homework questions and answers
│   └── README.md
└── pipeline/                # Bruin pipeline definition
    ├── pipeline.yml         # Global pipeline configuration (schedule, variables, etc.)
    └── assets/              # Data assets (Python, SQL, Seed)
        ├── ingestion/       # RAW LAYER: Data extraction
        │   ├── trips.py             # Python ingestion fetching TLC parquet files
        │   ├── taxi_zone_lookup.sql # SQL ingestion for zone mapping via HTTP
        │   ├── payment_lookup.asset.yml # Seed asset for static payment types
        │   └── requirements.txt     # Dependencies for Python assets
        ├── staging/         # STAGING LAYER: Cleaning & Normalization
        │   └── trips.sql            # Deduplication, enrichment, and schema alignment
        └── reports/         # REPORTING LAYER: Analytics
            └── trips_report.sql     # Aggregated monthly metrics (trip count, fares)
```

## 🛠️ Pipeline Assets

### 1. Ingestion Layer (`ingestion.`)
- **`raw_trips` (Python)**: Dynamically fetches parquet files from the NYC TLC endpoint based on the pipeline's date range. Uses an `append` strategy.
- **`taxi_zone_lookup` (SQL)**: Fetches the latest taxi zone mappings directly from a CSV URL using DuckDB's `read_csv`.
- **`payment_lookup` (Seed)**: A static lookup table for payment types loaded from a local CSV.

### 2. Staging Layer (`staging.`)
- **`trips_summary` (SQL)**: The "workhorse" of the pipeline. It:
    - Normalizes column names and types.
    - Joins ingestion assets (trips + zones + payments).
    - Deduplicates records using a composite key and `QUALIFY ROW_NUMBER()`.
    - Filters for valid records (e.g., passenger count > 0).

### 3. Reports Layer (`reports.`)
- **`trips_report` (SQL)**: Aggregates staging data into monthly summaries by taxi type. It uses the `time_interval` materialization strategy for efficient incremental updates.

## 🚀 Quick Start

Ensure you have the [Bruin CLI](https://getbruin.com/docs/bruin/getting-started/installation) installed.

### Validate the Pipeline
Check for syntax errors, missing dependencies, or configuration issues:
```bash
bruin validate pipeline/pipeline.yml
```

### Run the Pipeline
Execute the entire pipeline (requires a `duckdb-default` connection in your `.bruin.yml`):
```bash
# Full refresh (recreates tables)
bruin run pipeline/pipeline.yml --full-refresh

# Run with specific date range
bruin run pipeline/pipeline.yml --start-date 2022-01-01 --end-date 2022-02-01

# Run only yellow taxis
bruin run pipeline/pipeline.yml --var 'taxi_types=["yellow"]'
```

### Targeted Execution
```bash
# Run a specific asset and all its downstream dependencies
bruin run pipeline/assets/ingestion/trips.py --downstream
```

## 📝 Homework
Detailed answers to the module's quiz questions—covering materialization strategies, quality checks, and Bruin CLI usage—can be found in [homework/README.md](./homework/README.md).
