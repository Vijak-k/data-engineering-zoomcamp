import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

# Data types for green taxi data based on official data dictionary
green_dtype = {
    "VendorID": "Int64",
    "store_and_fwd_flag": "string",
    "RatecodeID": "Int64",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "payment_type": "Int64",
    "trip_type": "Int64",
    "congestion_surcharge": "float64",
    "cbd_congestion_fee": "float64"
}

# Parse dates for green taxi
parse_dates = [
    "lpep_pickup_datetime",
    "lpep_dropoff_datetime"
]


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2025, type=int, help='Year of the data')
@click.option('--month', default=11, type=int, help='Month of the data')
@click.option('--target-table', default='green_taxi_data', help='Target table name')
@click.option('--zones-table', default='taxi_zones', help='Zones table name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading parquet')
@click.option('--ingest-zones/--no-ingest-zones', default=True, help='Also ingest taxi zones lookup data')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_table, zones_table, chunksize, ingest_zones):
    """Ingest NYC Green Taxi data into PostgreSQL database."""
    
    # Green taxi data URL
    prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
    url = f'{prefix}/green_tripdata_{year}-{month:02d}.parquet'
    
    # Taxi zones lookup URL
    zones_url = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv'

    print(f"Downloading green taxi data from: {url}")

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # Ingest taxi zones lookup data first (if enabled)
    if ingest_zones:
        print(f"\nIngesting taxi zones lookup data from: {zones_url}")
        df_zones = pd.read_csv(zones_url)
        df_zones.to_sql(
            name=zones_table,
            con=engine,
            if_exists='replace',
            index=False
        )
        print(f"Successfully ingested {len(df_zones)} zones into {zones_table}")

    # Read green taxi parquet file
    print(f"\nReading green taxi parquet file...")
    df = pd.read_parquet(url)
    
    # Ensure datetime columns are parsed first
    for col in parse_dates:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])
    
    # Apply dtype conversions (skip datetime columns as they're already converted)
    for col, col_dtype in green_dtype.items():
        if col in df.columns and col not in parse_dates:
            try:
                df[col] = df[col].astype(col_dtype)
            except Exception as e:
                print(f"Warning: Could not convert {col} to {col_dtype}: {e}")

    # Process in chunks
    total_rows = len(df)
    num_chunks = (total_rows // chunksize) + (1 if total_rows % chunksize else 0)
    
    print(f"Total rows: {total_rows}")
    print(f"Total columns: {len(df.columns)}")
    print(f"Columns: {list(df.columns)}")
    print(f"Processing in {num_chunks} chunks of {chunksize} rows")

    first = True

    for i in tqdm(range(0, total_rows, chunksize), total=num_chunks, desc="Ingesting"):
        df_chunk = df.iloc[i:i+chunksize]
        
        if first:
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists='replace',
                index=False
            )
            first = False

        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists='append',
            index=False
        )

    print(f"\nSuccessfully ingested {total_rows} rows into {target_table}")
    print("Done!")

if __name__ == '__main__':
    run()