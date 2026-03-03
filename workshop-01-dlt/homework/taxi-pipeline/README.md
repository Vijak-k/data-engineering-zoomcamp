# NYC Taxi Data Ingestion with dlt

This directory contains a `dlt` pipeline designed to ingest NYC Taxi data from a REST API and load it into a local DuckDB database. This is part of the Data Engineering Zoomcamp (Workshop 01 - dlt).

## 🚀 Overview

The pipeline extracts data from a cloud function endpoint, handles pagination automatically using `dlt`'s REST API source, and stores the results in a structured format within DuckDB.

- **Source:** [NYC Taxi Data API](https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api)
- **Destination:** DuckDB
- **Dataset Name:** `taxi_data`
- **Tooling:** [dlt (data load tool)](https://dlthub.com/)

## 📂 Project Structure

```text
taxi-pipeline/
├── .cursor/rules/       # dlt-specific AI rules for code generation
├── .dlt/                # dlt configuration and secrets
├── .gitignore           # Git ignore rules for dlt (secrets, db files)
├── taxi_pipeline.py     # Main dlt pipeline script
└── requirements.txt     # Python dependencies
```

## 🛠️ Setup

1. **Install Dependencies:**
   Ensure you have `dlt` with DuckDB support installed.
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration:**
   The pipeline configuration is managed via `.dlt/config.toml`. Secrets (if any were required) would be in `.dlt/secrets.toml`.

## 🏃 Usage

Run the pipeline script to start the ingestion:

```bash
python taxi_pipeline.py
```

By default, the script is configured with `refresh="drop_sources"`, which clears existing data and state before each run. This is useful for development and testing.

## 📊 Homework Analysis

Once the data is loaded into `taxi_data.duckdb`, you can run SQL queries to analyze the dataset. The homework questions and answers related to this pipeline can be found in the parent directory's [README.md](../README.md).

Example query to check the date range:
```sql
SELECT
  MIN(trip_pickup_date_time) AS first_date,
  MAX(trip_pickup_date_time) AS last_date
FROM taxi_data;
```
