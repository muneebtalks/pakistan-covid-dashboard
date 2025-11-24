import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Pakistan COVID-19 Dashboard", layout="wide")
st.title("Pakistan COVID-19 Interactive Dashboard")
st.markdown("Historical & latest data from Johns Hopkins")


@st.cache_data(ttl=3600)
def load_data():
    # JHU Confirmed cases time-series (global, filter Pakistan)
    confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    df_conf = pd.read_csv(confirmed_url)

    # JHU Deaths
    deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    df_deaths = pd.read_csv(deaths_url)

    # Filter Pakistan rows
    pak_conf = df_conf[df_conf['Country/Region'] == 'Pakistan'].iloc[0].drop(['Province/State', 'Lat', 'Long'])
    pak_deaths = df_deaths[df_deaths['Country/Region'] == 'Pakistan'].iloc[0].drop(['Province/State', 'Lat', 'Long'])

    # Create date index
    dates = pd.to_datetime(pak_conf.index)
    df = pd.DataFrame({
        'date': dates,
        'total_cases': pak_conf.values,
        'total_deaths': pak_deaths.values
    })

    # Calculate new_ from total (diff)
    df['new_cases'] = df['total_cases'].diff().fillna(0).astype(int)
    df['new_deaths'] = df['total_deaths'].diff().fillna(0).astype(int)

    # Note: No vacc data in JHU; we can add later if needed
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