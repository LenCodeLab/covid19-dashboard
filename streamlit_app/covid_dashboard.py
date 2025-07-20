import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import sys
import os

# Add project root directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Now imports will work
from utils.db import fetch_covid_data

# Config
st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")

# Title
st.markdown("<h1 style='text-align: center;'>🦠 COVID-19 Dashboard - Africa & Global Insights</h1>", unsafe_allow_html=True)

# Load Data
df = fetch_covid_data()
df['date'] = pd.to_datetime(df['date'])

# Rename columns to standard names
df.rename(columns={
    "location": "Country",
    "continent": "Continent",
    "total_cases": "Total Cases",
    "new_cases": "New Cases",
    "total_deaths": "Total Deaths",
    "new_deaths": "New Deaths"
}, inplace=True)

# Sidebar: Filter
st.sidebar.header("Filter Options")
country_list = sorted(df['Country'].dropna().unique())
default_index = country_list.index("Kenya") if "Kenya" in country_list else 0
country = st.sidebar.selectbox("Choose a Country", country_list, index=default_index)

# Filtered Data
filtered_df = df[df["Country"] == country].sort_values("date")

# Latest row
latest = filtered_df.iloc[-1]

# ==================== METRICS ====================
st.subheader(f"📍 Summary for {country}")
col1, col2, col3 = st.columns(3)
col1.metric("🦠 Total Cases", f"{int(latest['Total Cases']):,}")
col2.metric("☠️ Total Deaths", f"{int(latest['Total Deaths']):,}")
col3.metric("➕ New Cases", f"{int(latest['New Cases']):,}")

st.markdown("---")

# ==================== EXPORT SECTION ====================
st.sidebar.markdown("### Download Data")
csv = filtered_df.to_csv(index=False).encode("utf-8")
excel_buffer = BytesIO()
with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
    filtered_df.to_excel(writer, index=False, sheet_name='Data')
st.sidebar.download_button("⬇️ Download CSV", csv, f"{country}_covid_data.csv", "text/csv")
st.sidebar.download_button("⬇️ Download Excel", excel_buffer.getvalue(), f"{country}_covid_data.xlsx", "application/vnd.ms-excel")

# ==================== VISUALIZATIONS ====================
tab1, tab2, tab3 = st.tabs(["📈 Trends", "📊 Bar Chart", "🧩 Pie Chart"])

with tab1:
    st.markdown("#### 📈 COVID-19 Trends Over Time")
    fig_line = px.line(
        filtered_df,
        x="date",
        y=["Total Cases", "New Cases", "Total Deaths", "New Deaths"],
        labels={"value": "Count", "variable": "Metric"},
        template="plotly_dark"
    )
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    st.markdown("#### 📊 Bar Chart - Latest Case Stats")
    latest_data = pd.DataFrame({
        "Metric": ["Total Deaths", "New Deaths", "New Cases"],
        "Value": [latest["Total Deaths"], latest["New Deaths"], latest["New Cases"]]
    })
    fig_bar = px.bar(latest_data, x="Metric", y="Value", color="Metric", text_auto=True, template="simple_white")
    st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    st.markdown("#### 🧩 Pie Chart - Total Cases by Continent")
    latest_global = df[df["date"] == df["date"].max()]
    continent_data = latest_global.groupby("Continent")["Total Cases"].sum().reset_index()
    fig_pie = px.pie(continent_data, values="Total Cases", names="Continent", title="Share of Total Cases by Continent")
    st.plotly_chart(fig_pie, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center;'>Built with ❤️ by Lenix Owino · Powered by Streamlit & PostgreSQL</p>", unsafe_allow_html=True)
