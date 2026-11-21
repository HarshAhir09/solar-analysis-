
import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text

# Page settings
st.set_page_config(
    page_title="Solar Plant Analytics",
    page_icon="☀️",
    layout="wide"
)

st.title("☀️ Solar Plant Underperformance Investigation")
st.write("Solar Power Generation Monitoring Dashboard")

# Connect to Neon PostgreSQL
@st.cache_data(ttl=300)
def load_data():
    url = st.secrets["DATABASE_URL"]

    url = url.replace(
        "postgresql://",
        "postgresql+psycopg://",
        1
    )

    engine = create_engine(url, pool_pre_ping=True)

    with engine.connect() as conn:
        df = pd.read_sql(
            text("SELECT * FROM solar_readings"),
            conn
        )

    df["DATE_TIME"] = pd.to_datetime(df["DATE_TIME"])

    return df


try:
    df = load_data()
except Exception:
    st.error("Database connection failed. Check Neon credentials.")
    st.stop()


# Sidebar
st.sidebar.header("Dashboard Filters")

# Convert inverter IDs to simple names
inverter_ids = sorted(df["SOURCE_KEY"].dropna().unique())

inverter_names = {
    inv_id: f"Inverter {i + 1}"
    for i, inv_id in enumerate(inverter_ids)
}

# Dropdown showing Inverter 1, 2, 3...
selected_inverter = st.sidebar.selectbox(
    "Select Inverter",
    inverter_ids,
    format_func=lambda x: inverter_names[x]
)

# Filter selected inverter
data = df[
    df["SOURCE_KEY"] == selected_inverter
].copy()

data = data.sort_values("DATE_TIME")

# Date filter
min_date = data["DATE_TIME"].min().date()
max_date = data["DATE_TIME"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range

    data = data[
        (data["DATE_TIME"].dt.date >= start_date) &
        (data["DATE_TIME"].dt.date <= end_date)
    ]

if data.empty:
    st.warning("No data available for selected dates.")
    st.stop()


# Dashboard metrics
st.subheader("📊 Performance Overview")

c1, c2, c3, c4 = st.columns(4)

total_readings = len(data)
low_output = int(data["underperforming"].sum())
missing_power = int(data["missing_power"].sum())
missing_weather = int(data["missing_weather"].sum())

c1.metric("Total Readings", total_readings)
c2.metric("Low Output Periods", low_output)
c3.metric("Missing Power", missing_power)
c4.metric("Missing Weather", missing_weather)

st.divider()

# Actual vs Expected Power
st.subheader("⚡ Actual vs Expected Power")

fig1 = px.line(
    data,
    x="DATE_TIME",
    y=["AC_POWER", "expected_power"],
    title="Solar Power Performance Comparison",
    labels={
        "DATE_TIME": "Date and Time",
        "value": "AC Power",
        "variable": "Power Type"
    }
)

st.plotly_chart(fig1, use_container_width=True)

# Irradiation graph
st.subheader("☀️ Solar Irradiation")

fig2 = px.line(
    data,
    x="DATE_TIME",
    y="IRRADIATION",
    title="Solar Irradiation Over Time",
    labels={
        "DATE_TIME": "Date and Time",
        "IRRADIATION": "Irradiation"
    }
)

st.plotly_chart(fig2, use_container_width=True)

# Temperature graph
st.subheader("🌡️ Ambient Temperature")

fig3 = px.line(
    data,
    x="DATE_TIME",
    y="AMBIENT_TEMPERATURE",
    title="Ambient Temperature Over Time",
    labels={
        "DATE_TIME": "Date and Time",
        "AMBIENT_TEMPERATURE": "Temperature (°C)"
    }
)

st.plotly_chart(fig3, use_container_width=True)

# Performance ratio
st.subheader("📈 Performance Ratio")

fig4 = px.line(
    data,
    x="DATE_TIME",
    y="performance_ratio",
    title="Actual Power / Expected Power",
    labels={
        "DATE_TIME": "Date and Time",
        "performance_ratio": "Performance Ratio"
    }
)

fig4.add_hline(
    y=0.8,
    line_dash="dash",
    line_color="red",
    annotation_text="80% Threshold"
)

st.plotly_chart(fig4, use_container_width=True)

# Underperformance report
st.subheader("⚠️ Underperformance Report")

low_data = data[
    data["underperforming"] == True
].copy()

if low_data.empty:
    st.success("No low-output readings found.")
else:
    st.warning(
        f"{len(low_data)} low-output readings detected."
    )

    report_columns = [
        "DATE_TIME",
        "AC_POWER",
        "expected_power",
        "IRRADIATION",
        "performance_ratio"
    ]

    st.dataframe(
        low_data[report_columns],
        use_container_width=True
    )

    # Download report
    csv = low_data[report_columns].to_csv(index=False)

    st.download_button(
        label="📥 Download Underperformance Report",
        data=csv,
        file_name="solar_underperformance_report.csv",
        mime="text/csv"
    )

# Complete dataset
st.subheader("📋 Complete Solar Dataset")

with st.expander("View All Records"):
    st.dataframe(data, use_container_width=True)

st.download_button(
    label="📥 Download Complete Data",
    data=data.to_csv(index=False),
    file_name="solar_complete_data.csv",
    mime="text/csv"
)

st.divider()

st.info(
    "Low-output periods are identified using a historical "
    "irradiation-based baseline and an 80% threshold. "
    "These flags do not establish the cause of underperformance."
)

st.caption(
    "Solar Plant Underperformance Investigation | "
    "Google Colab + Neon PostgreSQL + Streamlit"
)
