# 🌍 Covid-19 Data Dashboard (Africa & Global)

An interactive web-based dashboard built with **Streamlit**, visualizing the spread and impact of COVID-19 across Africa and globally. This project leverages data from a PostgreSQL database hosted on **Render**, updated via a custom Python ETL pipeline.

## 📊 Live Demo

🚀 [Launch the Dashboard](https://covid19-dashboard-lenix.onrender.com)

---

## 🔍 Features

- 📈 **Trends & Comparisons:** Track daily confirmed cases, deaths, and recoveries across African countries and globally.
- 🌍 **Geographic Breakdown:** Visual analysis by region or country.
- 🔄 **Automated ETL:** Data is periodically fetched from a local or external source and migrated to a live PostgreSQL DB on Render.
- 💾 **Persistent Backend:** PostgreSQL database hosted on Render retains historical data for analysis.

---

## 🛠️ Tools & Technologies

| Area              | Stack                                 |
|-------------------|----------------------------------------|
| Backend           | Python, Pandas, SQLAlchemy, psycopg2   |
| Web Framework     | Streamlit                              |
| Database          | PostgreSQL (Render Cloud DB)           |
| Deployment        | Render (Streamlit App + PostgreSQL)    |
| Data Source       | COVID-19 CSVs / API (custom ETL)       |
| Version Control   | Git, GitHub                            |

---

## 📂 Project Structure

├── cron.log
├── dashboard
├── data
│   └── latest.csv
├── migrate_to_render.py
├── notebooks
├── README.md
├── render.yaml
├── requirements.txt
├── schema.sql
├── scripts
│   └── load_covid_data.py
├── streamlit_app
│   └── covid_dashboard.py
├── utils
│   ├── db.py
│   └── __pycache__
└── visuals
