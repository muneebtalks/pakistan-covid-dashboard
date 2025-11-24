import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Pakistan COVID-19 Dashboard", layout="wide")
st.title("Pakistan COVID-19 Interactive Dashboard")
st.markdown("**Made by Muneeb**")
st.markdown("Historical data from Johns Hopkins CSSE (2020–2023)")


@st.cache_data(ttl=3600)
def load_data():
    confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"

    df_conf = pd.read_csv(confirmed_url)
    df_deaths = pd.read_csv(deaths_url)

    pak_conf = df_conf[df_conf['Country/Region'] == 'Pakistan'].iloc[0, 4:]  # from column 4 onward (dates)
    pak_deaths = df_deaths[df_deaths['Country/Region'] == 'Pakistan'].iloc[0, 4:]

    dates = pd.to_datetime(pak_conf.index)

    df = pd.DataFrame({
        'date': dates,
        'total_cases': pak_conf.values.astype(int),
        'total_deaths': pak_deaths.values.astype(int)
    })

    df['new_cases'] = df['total_cases'].diff().fillna(0).astype(int)
    df['new_deaths'] = df['total_deaths'].diff().fillna(0).astype(int)

    return df


# ← THIS LINE WAS MISSING BEFORE ←
df = load_data()
# ← NOW IT WORKS ←

metric = st.sidebar.selectbox("Choose metric",
                              ["New Cases", "New Deaths", "Total Cases", "Total Deaths"])

col = {"New Cases": "new_cases", "New Deaths": "new_deaths",
       "Total Cases": "total_cases", "Total Deaths": "total_deaths"}[metric]

fig = px.line(df, x='date', y=col, title=f"Pakistan {metric} Over Time")
st.plotly_chart(fig, use_container_width=True)

latest = df.iloc[-1]
st.metric("Latest Update", latest['date'].strftime('%Y-%m-%d'))
st.metric("Total Cases", f"{int(latest['total_cases']):,}")
st.metric("Total Deaths", f"{int(latest['total_deaths']):,}")