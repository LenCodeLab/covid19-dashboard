import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit page settings
st.set_page_config(page_title="COVID-19 Dashboard", layout="wide")

# Load and cache data
@st.cache_data
def load_data():
    cases_url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/new_cases.csv"
    deaths_url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/new_deaths.csv"
    total_cases_url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/total_cases.csv"
    total_deaths_url = "https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/total_deaths.csv"

    # Load all data
    new_cases = pd.read_csv(cases_url)
    new_deaths = pd.read_csv(deaths_url)
    total_cases = pd.read_csv(total_cases_url)
    total_deaths = pd.read_csv(total_deaths_url)

    # Melt for daily data
    new_cases = new_cases.melt(id_vars=["date"], var_name="country", value_name="new_cases")
    new_deaths = new_deaths.melt(id_vars=["date"], var_name="country", value_name="new_deaths")

    # Merge daily data
    daily_df = pd.merge(new_cases, new_deaths, on=["date", "country"])
    daily_df["date"] = pd.to_datetime(daily_df["date"])
    daily_df = daily_df.dropna()

    # Latest totals
    latest_total_cases = total_cases.iloc[-1].drop("date")
    latest_total_deaths = total_deaths.iloc[-1].drop("date")

    return daily_df, latest_total_cases, latest_total_deaths

# Sidebar
st.sidebar.title("COVID-19 Dashboard 🌍")
refresh = st.sidebar.button("🔄 Refresh Data", on_click=lambda: [st.cache_data.clear(), st.rerun()])

# Show loading spinner while loading data
with st.spinner("Loading data..."):
    df, total_cases_dict, total_deaths_dict = load_data()

# Main Title
st.title("📊 COVID-19 Cases Dashboard")
st.markdown("Data sourced from [Our World In Data](https://github.com/owid/covid-19-data).")

# Country selection
country = st.selectbox("Select a country to view its daily new cases and deaths", df["country"].unique())

# Filter data for selected country
country_data = df[df["country"] == country].sort_values("date")

# Total metrics
st.subheader(f"📌 Latest COVID-19 Stats for {country}")

total_cases = total_cases_dict.get(country, float("nan"))
total_deaths = total_deaths_dict.get(country, float("nan"))
death_rate = (total_deaths / total_cases * 100) if pd.notna(total_cases) and total_cases > 0 else float("nan")

col1, col2, col3 = st.columns(3)
col1.metric("🧮 Total Cases", f"{int(total_cases):,}" if pd.notna(total_cases) else "N/A")
col2.metric("💀 Total Deaths", f"{int(total_deaths):,}" if pd.notna(total_deaths) else "N/A")
col3.metric("📉 Death Rate", f"{death_rate:.2f}%" if pd.notna(death_rate) else "N/A")

# Country plot
st.subheader(f"📈 Daily New COVID-19 Cases and Deaths in {country}")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(country_data["date"], country_data["new_cases"], color="blue", label="New Daily Cases")
ax.plot(country_data["date"], country_data["new_deaths"], color="red", label="New Daily Deaths", linestyle="--")
ax.set_xlabel("Date")
ax.set_ylabel("Count")
ax.set_title(f"COVID-19 Daily New Cases and Deaths - {country}")
ax.legend()
st.pyplot(fig)

# Country comparison chart
st.subheader("🌍 Compare Countries (New Cases Only)")
selected_countries = st.multiselect(
    "Select countries to compare",
    df["country"].unique(),
    default=["Kenya", "Nigeria", "South Africa"]
)

if selected_countries:
    comparison_df = df[df["country"].isin(selected_countries)]
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=comparison_df, x="date", y="new_cases", hue="country", ax=ax2)
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Cases")
    ax2.set_title("Daily New Cases Comparison")
    st.pyplot(fig2)

# Footer
st.markdown("---")
st.markdown("Created by **Lenix Owino** | Data from [OWID](https://github.com/owid/covid-19-data)")
