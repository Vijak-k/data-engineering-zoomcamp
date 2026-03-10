# Homework: Batch Processing

## Question 1: Install Spark and PySpark

- Install Spark
- Run PySpark
- Create a local spark session
- Execute spark.version.

What's the output?

💡Ans: `'4.1.1'`


## Question 2: Yellow November 2025

Read the November 2025 Yellow into a Spark Dataframe.

Repartition the Dataframe to 4 partitions and save it to parquet.

What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.

💡Ans: 25MB
Actually, I've got ~24.42 MB
```Python
# Read the downloaded yellow taxi data
df = spark.read.parquet('yellow_tripdata_2025-11.parquet')
# Repartition to 4 partitions and save as parquet files
df.repartition(4).write.parquet('yellow_tripdata_2025-11')
import os

path = 'yellow_tripdata_2025-11'
# Filter for actual parquet data files, excluding metadata like _SUCCESS
files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.parquet')]

if files:
    # Get sizes in bytes, convert to MB (1024 * 1024)
    sizes = [os.path.getsize(f) / (1024 * 1024) for f in files]
    print(f"partition sizes in MB {sizes}")
    avg_size = sum(sizes) / len(sizes)
    print(f"Average Parquet file size: {avg_size:.2f} MB")
else:
    print("No Parquet files found in the directory.")
```


## Question 3: Count records

How many taxi trips were there on the 15th of November?

Consider only trips that started on the 15th of November.

💡Ans: 162,604
```Python
# First materialize the dataframe
df.registerTempTable('trips_data')
spark.sql("""
SELECT
    count(*) AS count
FROM
    trips_data
WHERE
    tpep_pickup_datetime >= '2025-11-15 00:00:00' AND
    tpep_pickup_datetime < '2025-11-16 00:00:00'
""").show()
```


## Question 4: Longest trip

What is the length of the longest trip in the dataset in hours?

💡Ans: 90.6
```Python
spark.sql("""
SELECT
    tpep_pickup_datetime AS pickup_datetime,
    tpep_dropoff_datetime AS dropoff_datetime,
    (unix_timestamp(tpep_dropoff_datetime) - unix_timestamp(tpep_pickup_datetime)) / 3600.0 AS duration_hours
FROM
    trips_data
ORDER BY
    duration_hours DESC
LIMIT
    1
""").show()
```

## Question 5: User Interface

Spark's User Interface which shows the application's dashboard runs on which local port?

💡Ans:  4040

## Question 6: Least frequent pickup location zone

Load the zone lookup data into a temp view in Spark:

```bash
wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
```

Using the zone lookup data and the Yellow November 2025 data, what is the name of the LEAST frequent pickup location Zone?

- Governor's Island/Ellis Island/Liberty Island
- Arden Heights

If multiple answers are correct, select any
```Python
# Read the data
df_zone = spark.read \
    .option("header", "true") \
    .csv('taxi_zone_lookup.csv')
# join with the working dataframe
df_join = df_4.join(df_zone, df_4.PULocationID == df_zone.LocationID)
# materialize
df_join.registerTempTable('trips_data_with_zones')
# Check the result to least 10 for sure
spark.sql("""
SELECT
    Zone,
    COUNT(*) AS count
FROM
    trips_data_with_zones
GROUP BY
    ZONE
ORDER BY
    2 ASC
LIMIT
    10
""").show()
```