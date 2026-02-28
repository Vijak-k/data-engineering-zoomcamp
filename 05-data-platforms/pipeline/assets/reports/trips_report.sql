/* @bruin

name: reports.trips_report
type: duckdb.sql

depends:
  - staging.trips_summary

materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_month
  time_granularity: date

columns:
  - name: taxi_type
    type: string
    description: The type of taxi (e.g. yellow, green)
    primary_key: true
  - name: pickup_month
    type: date
    description: The start of the month for the reported trips
    primary_key: true
  - name: trip_count
    type: bigint
    description: Total number of trips in the month
    checks:
      - name: non_negative
  - name: total_fare
    type: double
    description: Total fare amount collected
    checks:
      - name: non_negative
  - name: total_amount
    type: double
    description: Total amount collected (including tips, surcharges, etc)
    checks:
      - name: non_negative
  - name: average_trip_distance
    type: double
    description: Average trip distance in miles
    checks:
      - name: non_negative

@bruin */

-- Purpose: Monthly aggregation of taxi trips by type
-- This report uses the time_interval strategy to allow for efficient updates
-- as new data is processed in the staging layer.

SELECT
    taxi_type,
    date_trunc('month', pickup_time)::DATE AS pickup_month,
    COUNT(*) AS trip_count,
    SUM(fare_amount) AS total_fare,
    SUM(total_amount) AS total_amount,
    AVG(trip_distance) AS average_trip_distance
FROM staging.trips_summary
WHERE pickup_time >= '{{ start_datetime }}'
  AND pickup_time < '{{ end_datetime }}'
GROUP BY ALL
