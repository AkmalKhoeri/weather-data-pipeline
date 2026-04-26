import requests
import os
from datetime import datetime
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
PROJECT_ID = "sinuous-vortex-494509-v4"

CITIES = [
    "Jakarta",
    "Surabaya",
    "Bandung",
    "Medan",
    "Semarang",
    "Makassar",
    "Palembang"
]

URL = "https://api.openweathermap.org/data/2.5/weather"

client = bigquery.Client(project=PROJECT_ID)

TABLE_REF = f"{PROJECT_ID}.weather_data.daily_weather"


def extract(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(URL, params=params)
    response.raise_for_status()
    return response.json()


def transform(data):
    return {
        "city": data["name"],
        "country": data["sys"].get("country"),
        "lat": data["coord"].get("lat"),
        "lon": data["coord"].get("lon"),
        "temp_c": data["main"].get("temp"),
        "feels_like_c": data["main"].get("feels_like"),
        "temp_min_c": data["main"].get("temp_min"),
        "temp_max_c": data["main"].get("temp_max"),
        "humidity_pct": data["main"].get("humidity"),
        "pressure_hpa": data["main"].get("pressure"),
        "visibility_m": data.get("visibility"),
        "cloudiness_pct": data["clouds"].get("all"),
        "wind_speed_ms": data["wind"].get("speed"),
        "wind_deg": data["wind"].get("deg"),
        "wind_gust_ms": data["wind"].get("gust"),
        "weather_main": data["weather"][0].get("main"),
        "weather_desc": data["weather"][0].get("description"),
        "sunrise_utc": str(data["sys"].get("sunrise")),
        "sunset_utc": str(data["sys"].get("sunset")),
        "fetched_at": datetime.utcnow().isoformat()
    }


def load(rows):
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_APPEND",
        source_format="NEWLINE_DELIMITED_JSON"
    )

    job = client.load_table_from_json(rows, TABLE_REF, job_config=job_config)
    job.result()


def main():
    all_rows = []

    for city in CITIES:
        print(f"Fetching {city}...")
        raw = extract(city)
        cleaned = transform(raw)
        all_rows.append(cleaned)

    load(all_rows)

    print("ETL DONE")


if __name__ == "__main__":
    main()