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
💡postgres:5432


## **Question 3.** For the trips in November 2025, how many trips had a trip_distance of less than or equal to 1 mile?

💡


## **Question 4.** Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles. 


## **Question 5.** Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?


## Question 6. For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip? (1 point)

# Reference
NYC Taxi & Limousine Comission, _TLC Trip Record Data_
https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page