/* @bruin

name: staging.trips_summary
type: duckdb.sql

materialization:
  type: table

depends:
  - ingestion.raw_trips
  - ingestion.payment_lookup
  - ingestion.taxi_zone_lookup

custom_checks:
  - name: all_rows_unique
    description: Ensures that each row is unique based on the primary key columns (pickup_time, dropoff_time, pickup_location_id, dropoff_location_id, taxi_type)
    value: 0
    query: |
      SELECT COUNT(*)
      FROM (
        SELECT
          pickup_time,
          dropoff_time,
          pickup_zone,
          pickup_borough,
          dropoff_zone,
          dropoff_borough,
          taxi_type,
          trip_distance,
          passenger_count,
          fare_amount,
          tip_amount,
          total_amount,
          payment_type
        FROM staging.trips_summary
        GROUP BY ALL
        HAVING COUNT(*) > 1
      )

@bruin */

-- normalize columns title and data typse
-- enrich the normalized data
-- normalization raw_trips
WITH normalized_trips AS (
  SELECT
    vendorid AS vendor_id,
    ratecodeid AS rate_code_id, -- Note: Check if your ingestion standardized this name!
    -- pickup and dropoff information
    CAST(COALESCE(tpep_pickup_datetime, lpep_pickup_datetime) AS TIMESTAMP) AS pickup_time,
    CAST(COALESCE(tpep_dropoff_datetime, lpep_dropoff_datetime) AS TIMESTAMP) AS dropoff_time,
    pulocationid as pickup_location_id,
    dolocationid as dropoff_location_id,
    -- trip information
    store_and_fwd_flag,
    trip_distance,
    passenger_count,
    -- payment information
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    total_amount,
    payment_type,
    -- table information
    taxi_type,
    CAST(extracted_at AS TIMESTAMP) AS extracted_at
  FROM ingestion.raw_trips
  -- THE CRITICAL FILTER:
  WHERE 1=1
    AND CAST(COALESCE(tpep_pickup_datetime, lpep_pickup_datetime) AS TIMESTAMP) >= '{{ start_datetime }}'
    AND CAST(COALESCE(tpep_pickup_datetime, lpep_pickup_datetime) AS TIMESTAMP) <  '{{ end_datetime }}'
    AND COALESCE(tpep_pickup_datetime, lpep_pickup_datetime) IS NOT NULL
    AND COALESCE(tpep_dropoff_datetime, lpep_dropoff_datetime) IS NOT NULL
    AND pulocationid IS NOT NULL
    AND dolocationid IS NOT NULL
    AND taxi_type IS NOT NULL
),
enriched_trips AS (
  SELECT
    nt.vendor_id,
    nt.rate_code_id,
    nt.pickup_time,
    nt.dropoff_time,
    EXTRACT(EPOCH FROM (nt.dropoff_time - nt.pickup_time)) AS trip_duration_seconds,
    nt.pickup_location_id,
    zp.borough AS pickup_borough,
    zp.zone AS pickup_zone,
    nt.dropoff_location_id,
    zd.borough AS dropoff_borough,
    zd.zone AS dropoff_zone,
    nt.store_and_fwd_flag,
    nt.trip_distance,
    nt.passenger_count,
    nt.fare_amount,
    nt.extra,
    nt.mta_tax,
    nt.tip_amount,
    nt.tolls_amount,
    nt.improvement_surcharge,
    nt.total_amount,
    nt.payment_type,
    pl.payment_type_name,
    nt.taxi_type,
    nt.extracted_at
  FROM normalized_trips nt
  -- joining pickup location
  LEFT JOIN ingestion.taxi_zone_lookup zp
    ON nt.pickup_location_id = zp.location_id
  -- joining dropoff location
  LEFT JOIN ingestion.taxi_zone_lookup zd
    ON nt.pickup_location_id = zd.location_id
  LEFT JOIN ingestion.payment_lookup pl
    ON nt.payment_type = pl.payment_type_id
  
  WHERE 1=1
    -- filter only trip with passenger, payment, distance, duration
    AND nt.passenger_count > 0
    AND nt.total_amount >= 0
    AND nt.trip_distance >= 0
    AND EXTRACT(EPOCH FROM (nt.dropoff_time - nt.pickup_time)) > 0
    AND nt.payment_type IN (0,1,2)
  -- deduplication
  QUALIFY ROW_NUMBER() OVER (
    PARTITION BY
      nt.pickup_time,
      nt.dropoff_time,
      nt.pickup_location_id,
      nt.dropoff_location_id,
      nt.taxi_type,
      nt.trip_distance,
      nt.passenger_count,
      nt.fare_amount,
      nt.tip_amount,
      nt.total_amount,
      nt.payment_type
    ORDER BY nt.extracted_at DESC
  ) = 1
)
SELECT
  vendor_id,
  rate_code_id,
  trip_duration_seconds,
  pickup_time,
  pickup_borough,
  pickup_zone,
  dropoff_time,
  dropoff_borough,
  dropoff_zone,
  trip_distance,
  passenger_count,
  fare_amount,
  extra,
  mta_tax,
  tip_amount,
  tolls_amount,
  improvement_surcharge,
  total_amount,
  payment_type_name AS payment_type,
  taxi_type,
  extracted_at,
  CAST(CURRENT_TIMESTAMP AS TIMESTAMP) AS updated_at,
FROM enriched_trips


/*
SELECT *
FROM ingestion.trips
WHERE pickup_datetime >= '{{ start_datetime }}'
  AND pickup_datetime < '{{ end_datetime }}'
*/
