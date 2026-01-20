# Homework 1: Docker, SQL and Terraform for Data Engineering Zoomcamp 2026




## **Question 1.** What's the version of pip in the python:3.13 image?
Run the docker image of python:3.13
```
docker run -it --rm python:3.13
```
Then check the pip version using
```
print(pip.__version__)
```
💡The pip version in python:3.13 image is 25.3.


## **Question 2.** Given the docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?
```
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

💡Answer: postgres:5432


## **Question 3.** For the trips in November 2025, how many trips had a trip_distance of less than or equal to 1 mile?
```
SELECT 
	COUNT(*)
FROM 
    public.green_taxi_data
WHERE 
    trip_distance <= 1
	AND (lpep_pickup_datetime between '2025-11-01' and '2025-12-01')
```

💡Answer: 8,007 trips


## **Question 4.** Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles.
```
SELECT 
    lpep_pickup_datetime::date AS pickup_day,
    MAX(trip_distance) AS max_distance
FROM 
    public.green_taxi_data
WHERE 
    trip_distance < 100
GROUP BY 
    pickup_day
ORDER BY 
    max_distance DESC
LIMIT 1;
```
💡The answer is `2025-11-14`

## **Question 5.** Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?
```
WITH max_pickup_location_id AS (
	SELECT
		"PULocationID",
		COUNT(*) as pickup_count
	FROM green_taxi_data
	WHERE lpep_pickup_datetime::date = '2025-11-08'
	GROUP BY "PULocationID"
	ORDER BY pickup_count DESC
	LIMIT 1)
SELECT z."Zone"
FROM max_pickup_location_id m
	JOIN taxi_zones z ON m."PULocationID" = z."LocationID";
```
💡Answer: The most pick up location on November 18th, 2025 is East Harlem North



## Question 6. For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip? (1 point)
```
WITH biggest_tip AS (
SELECT
		"DOLocationID",
		MAX(tip_amount) as largest_tip
	FROM green_taxi_data
	WHERE "PULocationID" =
		(SELECT "LocationID" FROM taxi_zones WHERE "Zone" = 'East Harlem North')
	GROUP BY "DOLocationID"
	ORDER BY largest_tip DESC LIMIT 1)

SELECT z."Zone"
FROM biggest_tip b
	JOIN taxi_zones z ON b."DOLocationID" = z."LocationID";
```
💡Answer: The largest tip was paid in Yorkville West

## **Question 7.** Which of the following sequences describes the Terraform workflow for: 1) Downloading plugins and setting up backend, 2) Generating and executing changes, 3) Removing all resources?

💡 `terraform init`, `terraform apply -auto-approve`, `terraform destroy`

- `terraform init` perform downloading plugins and setting up backend.
- `terraform apply -auto-approve` will generating and executing changes. `terraform apply` will generate change and ask for an approval. With the addition of `-auto-approve`, it will generate and execute the changes immediately (Note that `terraform plan` generates the changes, _not execute then_)<br>
- `terraform destroy` BAAMM !! Remove everything.

# Reference
NYC Taxi & Limousine Comission, _TLC Trip Record Data_
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page