import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64",
    "airport_fee": "float64",
    "cbd_congestion_fee": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
@click.option('--pg-host', default='localhost', help='PostgreSQL host')
@click.option('--pg-port', default=5432, type=int, help='PostgreSQL port')
@click.option('--pg-db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--year', default=2025, type=int, help='Year of the data')
@click.option('--month', default=1, type=int, help='Month of the data')
@click.option('--target-table', default='yellow_taxi_data_2025', help='Target table name')
@click.option('--chunksize', default=100000, type=int, help='Chunk size for reading parquet')
def run(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_table, chunksize):
    """Ingest NYC taxi data into PostgreSQL database."""
    # Official NYC TLC data URL for parquet files
    prefix = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
    url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.parquet'

    print(f"Downloading data from: {url}")

    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # Read parquet file
    df = pd.read_parquet(url)
    
    # Apply dtype conversions (parquet may have different types)
    for col, col_dtype in dtype.items():
        if col in df.columns:
            df[col] = df[col].astype(col_dtype)
    
    # Ensure datetime columns are parsed correctly
    for col in parse_dates:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col])

    # Process in chunks
    total_rows = len(df)
    num_chunks = (total_rows // chunksize) + (1 if total_rows % chunksize else 0)
    
    print(f"Total rows: {total_rows}")
    print(f"Processing in {num_chunks} chunks of {chunksize} rows")

    first = True

    for i in tqdm(range(0, total_rows, chunksize), total=num_chunks):
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

    print(f"Successfully ingested {total_rows} rows into {target_table}")

if __name__ == '__main__':
    run()