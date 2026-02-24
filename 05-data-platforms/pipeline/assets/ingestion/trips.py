"""@bruin
name: ingestion.trips
type: python
image: python:3.11
connection: duckdb-default
materialization:
  type: table
  strategy: append
@bruin"""

import os
import json
from datetime import datetime
from io import BytesIO
from typing import List, Dict

import pandas as pd
import requests

def get_date_range() -> tuple[str, str]:
    start_date = os.getenv('BRUIN_START_DATE')
    end_date = os.getenv('BRUIN_END_DATE')
    if not start_date or not end_date:
        raise ValueError("BRUIN_START_DATE and BRUIN_END_DATE must be set")
    return start_date, end_date

def get_pipeline_variables() -> Dict:
    bruin_vars = os.getenv('BRUIN_VARS', '{}')
    return json.loads(bruin_vars)

def generate_download_tasks(start_date: str, end_date: str, taxi_types: List[str]) -> List[Dict]:
    from dateutil.rrule import rrule, MONTHLY
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    tasks = []
    for dt in rrule(MONTHLY, dtstart=start, until=end):
        for taxi_type in taxi_types:
            tasks.append({
                'year': dt.year,
                'month': dt.month,
                'taxi_type': taxi_type,
                'date_key': dt.strftime('%Y-%m')
            })
    return tasks

def download_nyc_taxi_data(year: int, month: int, taxi_type: str) -> pd.DataFrame:
    base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"
    filename = f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"
    url = f"{base_url}/{filename}"
    print(f"Downloading: {filename}")
    try:
        response = requests.get(url, timeout=300)
        response.raise_for_status()
        df = pd.read_parquet(BytesIO(response.content))
        print(f"  [OK] Downloaded {len(df):,} records")
        return df
    except Exception as e:
        print(f"  [X] Error downloading {filename}: {e}")
        return pd.DataFrame()

def materialize():
    print("=" * 70)
    print("NYC Taxi Data Ingestion (Windows Compatibility Mode)")
    print("=" * 70)
    
    start_date, end_date = get_date_range()
    pipeline_vars = get_pipeline_variables()
    taxi_types = pipeline_vars.get('taxi_types', ['yellow'])
    
    tasks = generate_download_tasks(start_date, end_date, taxi_types)
    dataframes = []
    
    for task in tasks:
        df = download_nyc_taxi_data(task['year'], task['month'], task['taxi_type'])
        if not df.empty:
            # Add basic metadata
            df['extracted_at'] = datetime.now()
            dataframes.append(df)
    
    if not dataframes:
        return pd.DataFrame()

    final_df = pd.concat(dataframes, ignore_index=True)

    # --- THE "STRING FIRST" STRATEGY ---
    # Convert all datetime columns to strings. 
    # This prevents PyArrow from looking for a timezone database.
    # DuckDB will automatically parse these strings back into dates upon ingestion.
    for col in final_df.columns:
        if pd.api.types.is_datetime64_any_dtype(final_df[col]):
            print(f"  [Fix] Converting {col} to string for safe transit")
            final_df[col] = final_df[col].astype(str)
    # -----------------------------------

    return final_df


# This block is for local testing only - Bruin will call materialize() directly
if __name__ == "__main__":
    # Set test environment variables
    os.environ['BRUIN_START_DATE'] = '2024-01-01'
    os.environ['BRUIN_END_DATE'] = '2024-01-31'
    os.environ['BRUIN_VARS'] = json.dumps({'taxi_types': ['yellow']})
    
    # Run materialize
    result = materialize()
    print("\nTest run completed!")
    print(f"Shape: {result.shape}")
    if not result.empty:
        print("\nFirst few rows:")
        print(result.head())