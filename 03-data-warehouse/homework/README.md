# Homework 3: Workflow Orchestrator for Data Engineering Zoomcamp 2026
This directory records my codes and answers of homework 3.
Load data into Google Cloud Storage (GCP) bucket using python script
```
uv run load_yellow_taxi_data.py
```
BigQuery setup:
- Create external table
```
CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-487008.de_zoomcamp.de-zoomcamp-hw-03`
(
  `VendorID` INT64,
  tpep_pickup_datetime TIMESTAMP,
  `tpep_dropoff_datetime` TIMESTAMP,
  passenger_count FLOAT64,
  trip_distance FLOAT64,
  RatecodeID FLOAT64,
  store_and_fwd_flag STRING,
  `PULocationID` INT64,
  `DOLocationID` INT64,
  payment_type INT64,
  fare_amount FLOAT64,
  extra FLOAT64,
  mta_tax FLOAT64,
  tip_amount FLOAT64,
  tolls_amount FLOAT64,
  improvement_surcharge FLOAT64,
  total_amount FLOAT64,
  congestion_surcharge FLOAT64
)
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://de-zoomcamp-vijak/yellow_tripdata_2024-*.parquet']
);
```
- Create a materialize view
```
CREATE OR REPLACE TABLE `de-zoomcamp-487008.de_zoomcamp.yellow_tripdata_non_partitioned` AS
SELECT * FROM `de-zoomcamp-487008.de_zoomcamp.de-zoomcamp-hw-03`;
```
# Question 1. Counting Records
What is count of records for the 2024 Yellow Taxi Data?<br>
💡Ans: 20,332,093
SQL for the answer
```
SELECT count(*) FROM `de-zoomcamp-487008.de_zoomcamp.de-zoomcamp-hw-03`
```
# Question 2. Data Estimation
Write a query to count the distinct number of `PULocationID`s for the entire dataset on both the tables.
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?<br>
💡Ans: 0 MB for the External Table and 155.12 MB for the Materialized Table
For the external table, this query will process 0 MB when run.
```
SELECT count(distinct `PULocationID`) FROM `de-zoomcamp-487008.de_zoomcamp.de-zoomcamp-hw-03`
```

For the table, this query will process 155.12 MB when run.
```
SELECT count(distinct `PULocationID`) FROM `de-zoomcamp-487008.de_zoomcamp.yellow_tripdata_non_partitioned`
```

# Question 3. Understanding columnar storage
Write a query to retrieve the `PULocationID` from the table (not the external table) in BigQuery. Now write a query to retrieve the `PULocationID` and `DOLocationID` on the same table.<br>
💡Ans: BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.
Retrieve only `PULocationID`
```
SELECT PULocationID FROM `de-zoomcamp-487008.de_zoomcamp.yellow_tripdata_non_partitioned`
```
This query will process 155.12 MB when run.

Retrieve both `PULocationID` and `DOLocationID`
```
SELECT PULocationID, DOLocationID FROM `de-zoomcamp-487008.de_zoomcamp.yellow_tripdata_non_partitioned`
```
This query will process 310.24 MB when run.

# Question 4. Counting zero fare trips
How many records have a `fare_amount` of 0?<br>
💡Ans: 8,333
```
SELECT count(*) FROM `de-zoomcamp-487008.de_zoomcamp.de-zoomcamp-hw-03` WHERE fare_amount = 0;
```

# Question 5. Partitioning and clustering
 What is the best strategy to make an optimized table in Big Query if your query will always filter based on `tpep_dropoff_datetime` and order the results by `VendorID` (Create a new table with this strategy)<br>
💡Ans: Partitioning and clustering
To create the table
```
CREATE OR REPLACE TABLE `de-zoomcamp-487008.de_zoomcamp.yellow_tripdata_partitioned_clustered`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM `de-zoomcamp-487008.de_zoomcamp.de-zoomcamp-hw-03`;
```

# Question 6. Partition benefits
Write a query to retrieve the distinct `VendorID`s between `tpep_dropoff_datetime` 2024-03-01 and 2024-03-15 (inclusive). Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?<br>
💡Ans: 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table
SQL for non-partitioned and non-clustered table
```
SELECT DISTINCT VendorID
FROM `de-zoomcamp-487008.de_zoomcamp.yellow_tripdata_non_partitioned`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15'
```
This query will process 310.24 MB when run.

SQL for partitioned and clustered table
```
SELECT DISTINCT VendorID
FROM `de-zoomcamp-487008.de_zoomcamp.yellow_tripdata_partitioned_clustered`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15'
```
This query will process 26.84 MB when run.


# Question 7. External table storage
Where is the data stored in the External Table you created?<br>
💡Ans: GCP Bucket

# Question 8. Clustering best practices
It is best practice in Big Query to always cluster your data:<br>
💡Ans: False 
Small tables usually don't get benifit from clustering.

# Question 9. Understanding table scans
No Points: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?<br>
💡Ans:
```
SELECT COUNT(*) FROM `de-zoomcamp-487008.de_zoomcamp.yellow_tripdata_non_partitioned`
```
This query will process 0 B when run. BigQuery do not read any data because the total number of rows is stored in the table's metadata.
