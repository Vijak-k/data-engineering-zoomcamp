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
