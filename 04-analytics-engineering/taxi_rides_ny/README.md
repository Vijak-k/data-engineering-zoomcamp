### NYC Taxi Rides

This project transforms raw NYC Taxi and Limousine Commission (TLC) data into clean, analysis-ready models.

#### Model Structure
* **Staging (`models/staging/`):** Initial cleanup, renaming, and type casting of raw source data.
* **Intermediate (`models/intermediate/`):** Complex logic, joining green/yellow datasets, and creating surrogate keys.
* **Marts (`models/marts/`):** Business-level dimensions and fact tables used for BI and reporting.

```text
models/
├── staging/
│   ├── schema.yml
│   ├── stg_green_tripdata.sql
│   ├── stg_yellow_tripdata.sql
│   └── stg_fhv_tripdata.sql
├── intermediate/
│   ├── schema.yml
│   ├── int_trips_unioned.sql
│   └── int_trips.sql
└── marts/
    ├── schema.yml
    ├── dim_vendors.sql
    ├── dim_zones.sql
    ├── fct_trips.sql
    └── fct_monthly_zone_revenue.sql