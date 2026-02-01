# Homework 2: Workflow Orchestrator for Data Engineering Zoomcamp 2026
This directory records my codes and answers of homework 2.

## **Question 1.** Within the execution for `Yellow` Taxi data for the year `2020` and month `12`: what is the uncompressed file size (i.e. the output file `yellow_tripdata_2020-12.csv` of the `extract` task)?
💡Answer: 128.3 MiB
This question can be solved using the flow `04-postgres-taxi.yaml` from the lecture.
We can see the uncompress file by comment out the `purge_files` task (near the end of flow)
```
# - id: purge_files
#    type: io.kestra.plugin.core.storage.PurgeCurrentExecutionFiles
```
Then, we can execute the flow for the yellow taxi data of December, 2020 and see the file from extract task in the output.

## **Question 2.** What is the rendered value of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04` during execution?
💡Answer: green_tripdata_2020-04.csv

Run the same flow with the first question; but, replace the `taxt`, `year`, and `month` accordingly.

## **Question 3.** How many rows are there for the `Yellow` Taxi data for all CSV files in the year 2020?



## **Question 4.** How many rows are there for the `Green` Taxi data for all CSV files in the year 2020?



## **Question 5.** How many rows are there for the `Yellow` Taxi data for the March 2021 CSV file?



## **Question 6.** How would you configure the timezone to New York in a Schedule trigger?

