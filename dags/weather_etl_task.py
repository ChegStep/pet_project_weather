from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import os
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

OPENWEATHER_API_KEY = "265b5e0f8b9bc036fbfa0a327fc169b1"
def fetch_weather_data(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()

def transform_weather_data(raw_data):
    df = pd.DataFrame([{
        'city':raw_data['name'],
        'temp':raw_data['main']['temp'],
        'humidity':raw_data['main']['humidity'],
        'pressure':raw_data['main']['pressure'],
        'wind_speed':raw_data['wind']['speed'],
        'time':pd.to_datetime('now').floor('s') + timedelta(hours=5),

    }])
    return df

def save_weather_data_to_postgres(df):
    df.to_sql(schema='weather',
              name='weather_data',
              con="postgresql://postgres:postgres@postgres_wthr:5432/weather_db",
              if_exists='append',
              index=False)

def run_etl():
    raw_data = fetch_weather_data(city='Yekaterinburg', api_key=OPENWEATHER_API_KEY)
    transformed_data = transform_weather_data(raw_data)
    save_weather_data_to_postgres(transformed_data)

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'weather_etl_task',
    default_args=default_args,
    schedule=timedelta(minutes=5),
    start_date=datetime(2025, 1, 1),
)

etl_task = PythonOperator(
    task_id='weather_etl_task',
    python_callable=run_etl,
    dag=dag,
)