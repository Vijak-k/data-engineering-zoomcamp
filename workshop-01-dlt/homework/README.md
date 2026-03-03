# Homework 6: Ingestion with dlt

This folder contain [ingestion pipeline](https://github.com/Vijak-k/data-engineering-zoomcamp/blob/main/workshop-01-dlt/homework/taxi-pipeline/taxi_pipeline.py) and answer to homework in the workshop [From APIs to Warehouses: AI-Assisted Data Ingestion with dlt](https://www.youtube.com/embed/5eMytPBgmVs?si=CE-RlumCejgWPRDi).



## Question 1: What is the start date and end date of the dataset?

💡Ans: 2009-06-01 to 2009-07-01
```
select
  min(trip_pickup_date_time) as first_date,
  max(trip_pickup_date_time) as last_date
from taxi_pipeline.taxi_data.taxi_data;
```

## Question 2: What proportion of trips are paid with credit card?

💡Ans: 26.66%


```
select
  payment_type,
  count(*) AS total_trip,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS percentage
from taxi_pipeline.taxi_data.taxi_data
group by payment_type;
```

## Question 3: What is the total amount of money generated in tips?

💡Ans: $6,063.41

```
SELECT
  sum(tip_amt) AS total_tip_amt
from taxi_pipeline_pipeline.taxi_data.taxi_data;
```