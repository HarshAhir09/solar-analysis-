import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Solar Analytics", layout="wide")

st.title("☀️ Solar Plant Underperformance Investigation")

@st.cache_data(ttl=300)
def load_data():
    url = st.secrets["DATABASE_URL"]
    url = url.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )
    engine = create_engine(url)
    with engine.connect() as conn:
        df = pd.read_sql(
            text("SELECT * FROM solar_readings"), conn
        )
    df["DATE_TIME"] = pd.to_datetime(df["DATE_TIME"])
    return df

try:
    df = load_data()
except Exception:
    st.error("Database connection failed. Check Neon credentials.")
    st.stop()

st.sidebar.header("Filters")

inverter = st.sidebar.selectbox(
    "Select Inverter", sorted(df["SOURCE_KEY"].unique())
)

data = df[df["SOURCE_KEY"] == inverter].sort_values("DATE_TIME")

c1, c2, c3 = st.columns(3)
c1.metric("Total Readings", len(data))
c2.metric("Low Output", int(data["underperforming"].sum()))
c3.metric("Missing Weather", int(data["missing_weather"].sum()))

st.subheader("Actual vs Expected Power")
fig = px.line(
    data,
    x="DATE_TIME",
    y=["AC_POWER", "expected_power"],
    labels={"value": "AC Power", "DATE_TIME": "Time"}
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Solar Irradiation")
fig2 = px.line(data, x="DATE_TIME", y="IRRADIATION")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Underperformance Report")
low = data[data["underperforming"]]
st.dataframe(low, use_container_width=True)

st.download_button(
    "Download CSV Report",
    low.to_csv(index=False),
    "solar_report.csv",
    "text/csv"
)

st.info(
    "Low-output flags indicate periods for investigation, "
    "not confirmed equipment faults."
)
