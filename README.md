# Pakistan COVID-19 Interactive Dashboard  

Live App: https://pakistan-covid-dashboard.streamlit.app/  

A clean, fast, and fully interactive dashboard showing the complete COVID-19 timeline for Pakistan (2020–2023) using official Johns Hopkins CSSE data.

### Features
- Interactive line charts (Total Cases, New Cases, Total Deaths, New Deaths)  
- Real-time latest statistics  
- Responsive sidebar to switch metrics  
- Beautiful Plotly graphics  
- 100% free & publicly hosted on Streamlit Community Cloud  

### Data Source
Johns Hopkins University Center for Systems Science and Engineering (CSSE)  

- Confirmed Cases:  
  https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv  
- Deaths:  
  https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv  

(Note: JHU stopped daily updates in March 2023 after the global emergency ended.)

### Tech Stack
- Python  
- Streamlit 
- Pandas – data processing  
- Plotly Express – interactive & beautiful charts  

### How to Run Locally
```bash
git clone https://github.com/muneebtalks/pakistan-covid-dashboard.git
cd pakistan-covid-dashboard
pip install -r requirements.txt
streamlit run app.py