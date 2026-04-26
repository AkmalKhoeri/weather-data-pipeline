# 🌦️ Weather Data Pipeline (End-to-End)

## 🚀 Overview

This project demonstrates an end-to-end **Data Engineering pipeline** that ingests real-time weather data from an external API, processes it, and stores it in a cloud data warehouse for analytics and visualization.

---

## 🧱 Architecture

```
OpenWeather API → Python ETL → BigQuery (Raw → Clean) → GitHub Actions → Power BI
```

---

## ⚙️ Tech Stack

* **Python** – ETL scripting
* **Google BigQuery** – Data warehouse
* **OpenWeatherMap API** – Data source
* **GitHub Actions** – Automation / scheduling
* **Power BI** – Visualization

---

## 📊 Data Pipeline Flow

### 1. Extract

* Fetch weather data from OpenWeatherMap API
* Cities:

  * Jakarta
  * Surabaya
  * Bandung
  * Medan
  * Semarang
  * Makassar
  * Palembang

### 2. Transform

* Normalize JSON response
* Handle missing fields safely
* Convert timestamps to proper format

### 3. Load

* Load data into **BigQuery (append-only)**
* Use `load_table_from_json` (free-tier friendly)

---

## 🧠 Data Modeling

### Raw Table

`weather_data.daily_weather`

* Append-only
* Partitioned by `fetched_at`

### Clean Table (Deduplicated)

`weather_data.daily_weather_clean`

* Removes duplicate records
* Uses window function:

```
ROW_NUMBER() OVER (
  PARTITION BY city, TIMESTAMP_TRUNC(fetched_at, HOUR)
  ORDER BY fetched_at DESC
)
```

### Mart / View

`weather_data.weather_mart`

* Aggregated for BI
* Daily metrics per city

---

## ⚡ Automation

Pipeline runs automatically using **GitHub Actions**:

* Schedule: Daily (08:00 WIB)
* Also supports manual trigger

Workflow:

```
GitHub Actions → Auth → Run Python → BigQuery
```

---

## 🔐 Authentication Strategy

| Environment    | Method                             |
| -------------- | ---------------------------------- |
| Local          | ADC (gcloud CLI)                   |
| GitHub Actions | Service Account (JSON via secrets) |

---

## 📦 Project Structure

```
weather-data-pipeline/
├── main.py
├── setup_bigquery.py
├── requirements.txt
├── .env
├── .gitignore
└── .github/
    └── workflows/
        └── daily_etl.yml
```

---

## 🧪 How to Run Locally

### 1. Activate environment

```
venv\Scripts\activate
```

### 2. Install dependencies

```
pip install -r requirements.txt
```

### 3. Authenticate BigQuery (ADC)

```
gcloud auth application-default login
```

### 4. Setup dataset & table

```
python setup_bigquery.py
```

### 5. Run pipeline

```
python main.py
```

---

## 📈 Key Features

* Automated data ingestion
* Append-only time series design
* Partitioned BigQuery table
* Deduplication logic (idempotent pipeline)
* Cloud-native automation

---

## 🧠 Key Insights

* Designed for **scalability & cost efficiency**
* Avoids streaming insert limitations in BigQuery free tier
* Implements **data quality control via deduplication**
* Separates raw vs clean vs mart layers

---

## 📊 Future Improvements

* Add Airflow orchestration
* Integrate dbt for transformation
* Add anomaly detection (weather spikes)
* Expand to more cities / historical data

---

## 💡 Summary

This project showcases a production-style data pipeline with:

* Automated ingestion
* Cloud data warehousing
* Data modeling best practices
* End-to-end workflow from API to dashboard

---

## 👨‍💻 Author

Akmal Khoeri
