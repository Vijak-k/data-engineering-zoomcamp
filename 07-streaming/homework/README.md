# Homework: Streaming

In this homework, we'll practice streaming with Kafka (Redpanda) and PyFlink.

We use Redpanda, a drop-in replacement for Kafka. It implements the same
protocol, so any Kafka client library works with it unchanged.

For this homework we will be using Green Taxi Trip data from October 2025:

- [green_tripdata_2025-10.parquet](https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-10.parquet)


## Setup

We'll use the same infrastructure from the [workshop](../../../07-streaming/workshop/).

Follow the setup instructions: build the Docker image, start the services:

```bash
cd 07-streaming/workshop/
docker compose build
docker compose up -d
```

This gives us:

- Redpanda (Kafka-compatible broker) on `localhost:9092`
- Flink Job Manager at http://localhost:8081
- Flink Task Manager
- PostgreSQL on `localhost:5432` (user: `postgres`, password: `postgres`)

If you previously ran the workshop and have old containers/volumes,
do a clean start:

```bash
docker compose down -v
docker compose build
docker compose up -d
```

Note: the container names (like `workshop-redpanda-1`) assume the
directory is called `workshop`. If you renamed it, adjust accordingly.


## Question 1. Redpanda version

Run `rpk version` inside the Redpanda container:

```bash
docker exec -it workshop-redpanda-1 rpk version
```

What version of Redpanda are you running?
💡Ans: v25.3.9


## Question 2. Sending data to Redpanda

Create a topic called `green-trips`:

```bash
docker exec -it workshop-redpanda-1 rpk topic create green-trips
```

Now write a producer to send the green taxi data to this topic.

Read the parquet file and keep only these columns:

- `lpep_pickup_datetime`
- `lpep_dropoff_datetime`
- `PULocationID`
- `DOLocationID`
- `passenger_count`
- `trip_distance`
- `tip_amount`
- `total_amount`

Convert each row to a dictionary and send it to the `green-trips` topic.
You'll need to handle the datetime columns - convert them to strings
before serializing to JSON.

Measure the time it takes to send the entire dataset and flush:

```python
from time import time

t0 = time()
topic_name = 'green-trips'
for _, row in df.iterrows():
    ride = ride_from_row(row)
    producer.send(topic_name, value=ride)
    print(f"Sent: {ride}")
    time.sleep(0.01)

producer.flush()

t1 = time()
print(f'took {(t1 - t0):.2f} seconds')
```

How long did it take to send the data?

💡Ans: 10 seconds

Actually, I've got 15.28 seconds see https://github.com/Vijak-k/data-engineering-zoomcamp/blob/main/07-streaming/homework/notebooks/hw-producer.ipynb

## Question 3. Consumer - trip distance

Write a Kafka consumer that reads all messages from the `green-trips` topic
(set `auto_offset_reset='earliest'`).

Count how many trips have a `trip_distance` greater than 5.0 kilometers.

How many trips have `trip_distance` > 5?

💡Ans:  8506
Note book for this question: https://github.com/Vijak-k/data-engineering-zoomcamp/blob/main/07-streaming/homework/notebooks/hw-consumer.ipynb

## Part 2: PyFlink (Questions 4-6)
Producer : https://github.com/Vijak-k/data-engineering-zoomcamp/blob/main/07-streaming/src/producers/producer_hw.py

## Question 4. Tumbling window - pickup location

Create a Flink job that reads from `green-trips` and uses a 5-minute
tumbling window to count trips per `PULocationID`.

Write the results to a PostgreSQL table with columns:
`window_start`, `PULocationID`, `num_trips`.

After the job processes all data, query the results:

```sql
SELECT PULocationID, num_trips
FROM <your_table>
ORDER BY num_trips DESC
LIMIT 3;
```

Which `PULocationID` had the most trips in a single 5-minute window?

💡Ans: 74

Job file for this question: https://github.com/Vijak-k/data-engineering-zoomcamp/blob/main/07-streaming/src/job/hw_q4_job.py

## Question 5. Session window - longest streak

Create another Flink job that uses a session window with a 5-minute gap
on `PULocationID`, using `lpep_pickup_datetime` as the event time
with a 5-second watermark tolerance.

A session window groups events that arrive within 5 minutes of each other.
When there's a gap of more than 5 minutes, the window closes.

Write the results to a PostgreSQL table and find the `PULocationID`
with the longest session (most trips in a single session).

How many trips were in the longest session?

💡Ans: 81

Job file: https://github.com/Vijak-k/data-engineering-zoomcamp/blob/main/07-streaming/src/job/hw_q5_job.py

SQL for result
```
SELECT num_trips
FROM green_taxi_session_stats
ORDER BY num_trips DESC
LIMIT 1;
```


## Question 6. Tumbling window - largest tip

Create a Flink job that uses a 1-hour tumbling window to compute the
total `tip_amount` per hour (across all locations).

Which hour had the highest total tip amount?

💡Ans: 2025-10-16 18:00:00

Job file: https://github.com/Vijak-k/data-engineering-zoomcamp/blob/main/07-streaming/src/job/hw_q6_job.py

SQL for result
```
SELECT window_start, window_end, total_tip
FROM green_taxi_tips_hourly
ORDER BY total_tip DESC
LIMIT 3;
```


## Submitting the solutions

- Form for submitting: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw7


## Learning in public

We encourage everyone to share what they learned.
Read more about the benefits [here](https://alexeyondata.substack.com/p/benefits-of-learning-in-public-and).

## Example post for LinkedIn

```
Week 7 of Data Engineering Zoomcamp by @DataTalksClub complete!

Just finished Module 7 - Streaming with PyFlink. Learned how to:

- Set up Redpanda as a Kafka replacement
- Build Kafka producers and consumers in Python
- Create tumbling and session windows in Flink
- Analyze real-time taxi trip data with stream processing

Here's my homework solution: <LINK>

You can sign up here: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```

## Example post for Twitter/X

```
Module 7 of Data Engineering Zoomcamp done!

- Kafka producers and consumers
- PyFlink tumbling and session windows
- Real-time taxi data analysis
- Redpanda as Kafka replacement

My solution: <LINK>

Free course by @DataTalksClub: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```
