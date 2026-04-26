from google.cloud import bigquery

PROJECT_ID = "sinuous-vortex-494509-v4"
DATASET_ID = "weather_data"
TABLE_ID = "daily_weather"

client = bigquery.Client(project=PROJECT_ID)

dataset_ref = f"{PROJECT_ID}.{DATASET_ID}"
table_ref = f"{dataset_ref}.{TABLE_ID}"



# create dataset
dataset = bigquery.Dataset(dataset_ref)
dataset.location = "asia-southeast2"

client.create_dataset(dataset, exists_ok=True)
print("Creating dataset...")
client.create_dataset(dataset, exists_ok=True)
# schema
schema = [
    bigquery.SchemaField("city", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("country", "STRING"),
    bigquery.SchemaField("lat", "FLOAT64"),
    bigquery.SchemaField("lon", "FLOAT64"),
    bigquery.SchemaField("temp_c", "FLOAT64"),
    bigquery.SchemaField("feels_like_c", "FLOAT64"),
    bigquery.SchemaField("temp_min_c", "FLOAT64"),
    bigquery.SchemaField("temp_max_c", "FLOAT64"),
    bigquery.SchemaField("humidity_pct", "INT64"),
    bigquery.SchemaField("pressure_hpa", "INT64"),
    bigquery.SchemaField("visibility_m", "INT64"),
    bigquery.SchemaField("cloudiness_pct", "INT64"),
    bigquery.SchemaField("wind_speed_ms", "FLOAT64"),
    bigquery.SchemaField("wind_deg", "INT64"),
    bigquery.SchemaField("wind_gust_ms", "FLOAT64"),
    bigquery.SchemaField("weather_main", "STRING"),
    bigquery.SchemaField("weather_desc", "STRING"),
    bigquery.SchemaField("sunrise_utc", "STRING"),
    bigquery.SchemaField("sunset_utc", "STRING"),
    bigquery.SchemaField("fetched_at", "TIMESTAMP", mode="REQUIRED"),
]


table = bigquery.Table(table_ref, schema=schema)
print("Creating table...")
client.create_table(table, exists_ok=True)


client.create_table(table, exists_ok=True)
print("SETUP DONE")