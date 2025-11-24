import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Pakistan COVID-19 Dashboard", layout="wide")
st.title("Pakistan COVID-19 Interactive Dashboard")
st.markdown("Historical & latest data from Our World in Data")

@st.cache_data(ttl=3600)
def load_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    pak = df[df['location'] == 'Pakistan'].copy()
    pak['date'] = pd.to_datetime(pak['date'])
    return pak

df = load_data()

metric = st.sidebar.selectbox("Choose metric",
    ["New Cases", "New Deaths", "Total Cases", "Total Deaths", "Total Vaccinations"])

col = {"New Cases":"new_cases", "New Deaths":"new_deaths",
       "Total Cases":"total_cases", "Total Deaths":"total_deaths",
       "Total Vaccinations":"total_vaccinations"}[metric]

fig = px.area(df, x='date', y=col, title=f"Pakistan {metric} Over Time")
st.plotly_chart(fig, use_container_width=True)

latest = df.iloc[-1]
st.metric("Latest Date", latest['date'].strftime('%Y-%m-%d'))
st.metric("Total Cases", f"{latest['total_cases']:,.0f}")
st.metric("Total Deaths", f"{latest['total_deaths']:,.0f}")