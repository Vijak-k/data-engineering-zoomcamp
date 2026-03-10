# Module 6: Batch Processing with Apache Spark

This directory contains the code and notebooks for the Batch Processing module of the Data Engineering Zoomcamp. The focus is on using **Apache Spark** (PySpark) to process large-scale datasets, specifically NYC Taxi and For-Hire Vehicle (FHV) data.

## 📂 Directory Structure

* `codes/`: Contains all the scripts and Jupyter notebooks used for learning and practicing Spark.
* `homework/`: Contains the module's homework assignments.
* `data/`: (Local) Storage for raw CSV and processed Parquet files.

---

## 📜 Code Summaries

Each file in the `codes/` directory focuses on a specific aspect of Spark's functionality:

### 1. Basic Setup & Testing

* **`01_test_spark.py`**: A simple diagnostic script to verify the Spark installation. It initializes a local Spark session, creates a basic range DataFrame, and prints the Spark version.

### 2. Data Ingestion & Partitioning

* **`02_pyspark.ipynb`**: Demonstrates the basics of reading CSV data (FHVHV), enforcing schemas, and the importance of **repartitioning** for optimizing parallel processing. It concludes by saving the data in the efficient **Parquet** format.
* **`download_data.sh`**: A shell script to automate the downloading of NYC Taxi CSV data for specific years and taxi types from the public repository.

### 3. Schema Management & Batch Conversion

* **`03_taxi_schema.ipynb`**: Detailed examples of defining `StructType` schemas for Green and Yellow taxi data. It includes an automated loop to process and convert raw CSVs into a structured Parquet lake across multiple years and months.

### 4. Spark SQL & Transformations

* **`04_spark_sql.ipynb`**: Shows how to use Spark's SQL engine. It covers renaming columns, performing a `unionAll` on Green and Yellow taxi data, registering temporary views, and running complex SQL queries to calculate monthly revenue and trip metrics.

### 5. Joins & Aggregations

* **`05_groupby_join.ipynb`**: Explores advanced transformations including `groupBy` and various `join` strategies (e.g., outer joins). It calculates hourly revenue per zone and joins the results with a taxi zone lookup table.

### 6. Deep Dive into RDDs

* **`06_rdd.ipynb`**: An "under the hood" look at **Resilient Distributed Datasets (RDDs)**. It demonstrates how to manually implement filters, maps, and reduces. It also introduces `mapPartitions` for performance-heavy tasks like batch model inference.

---

## 🚀 Getting Started

1. **Environment**: Ensure you have Spark and PySpark installed (this project uses `pyspark` via `uv`).
2. **Download Data**: Use `bash download_data.sh yellow 2021` to fetch raw datasets.
3. **Execution**: Run the notebooks sequentially to understand the flow from ingestion to complex analytics.
