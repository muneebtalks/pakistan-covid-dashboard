import streamlit as st
import pandas as pd
import plotly.express as px
import requests

st.set_page_config(page_title="Pakistan COVID-19 Dashboard", layout="wide")
st.title("Pakistan COVID-19 Interactive Dashboard")
st.markdown("Historical & latest data from National Command & Operation Center (ncp.gov.pk)")

@st.cache_data(ttl=3600)
def load_data():
    url = "https://ncp.gov.pk/ncp/api"
    response = requests.get(url)
    data = response.json()

    # Parse historical data (assumes structure: list of daily records)
    # Adjust keys based on actual JSON (common: 'date', 'cases', 'deaths', etc.)
    timeline = []
    for item in data.get('data', []):  # Or 'timeline' key if different
        timeline.append({
            'date': pd.to_datetime(item.get('date', item.get('reportDate'))),
            'new_cases': item.get('newCases', 0),
            'total_cases': item.get('totalCases', 0),
            'new_deaths': item.get('newDeaths', 0),
            'total_deaths': item.get('totalDeaths', 0)
        })

    df = pd.DataFrame(timeline)
    df = df.sort_values('date').reset_index(drop=True)

    # Fill missing totals with cumulative sum if needed
    if df['total_cases'].isna().any():
        df['total_cases'] = df['new_cases'].cumsum()
    if df['total_deaths'].isna().any():
        df['total_deaths'] = df['new_deaths'].cumsum()

    return df

metric = st.sidebar.selectbox("Choose metric",
    ["New Cases", "New Deaths", "Total Cases", "Total Deaths"])

col = {"New Cases":"new_cases", "New Deaths":"new_deaths",
       "Total Cases":"total_cases", "Total Deaths":"total_deaths"}[metric]

fig = px.line(df, x='date', y=col, title=f"Pakistan {metric} Over Time")

latest = df.iloc[-1]
st.metric("Latest Date", latest['date'].strftime('%Y-%m-%d'))
st.metric("Total Cases", f"{int(latest['total_cases']):,.0f}")
st.metric("Total Deaths", f"{int(latest['total_deaths']):,.0f}")