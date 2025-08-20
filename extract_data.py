import binary
import requests
import os
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

from dotenv import load_dotenv
load_dotenv()

def fetch_weather_data(city='Yekaterinburg', api_key=os.getenv('OPENWEATHER_API_KEY')):
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
        'time':pd.to_datetime('now').floor('s'),

    }])
    return df

def save_weather_data_to_postgres(df):
    df.to_sql(schema='weather',
              name='weather_data',
              con="postgresql://postgres:postgres@localhost:5432/weather_db",
              if_exists='append',
              index=False)

raw_data = fetch_weather_data()
df = transform_weather_data(raw_data)
save_weather_data_to_postgres(df)


