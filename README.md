# ☀️ Solar Plant Underperformance Investigation

## 📌 Project Overview

Solar Plant Underperformance Investigation is a data visualization and analytics project designed to monitor solar power generation, compare actual output with expected output, and identify periods of low performance.

The project uses **Google Colab, Python, Neon PostgreSQL, and Streamlit** to process, store, analyze, and visualize solar plant data.

## 🌐 Live Website

**[Click Here to Open Solar Plant Analytics Dashboard](https://owy8njldbvmx3vuwgzh2dv.streamlit.app/)**

Website: https://owy8njldbvmx3vuwgzh2dv.streamlit.app/

## 🎯 Project Objectives

- Analyze solar power generation data.
- Compare actual and expected solar power output.
- Identify underperformance periods.
- Monitor solar irradiation and temperature.
- Identify missing readings.
- Store processed data in Neon PostgreSQL.
- Visualize results using an interactive Streamlit dashboard.
- Generate downloadable CSV reports.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Data processing and analysis |
| Google Colab | Data preprocessing |
| Pandas | Data cleaning and manipulation |
| Neon PostgreSQL | Cloud database |
| SQLAlchemy | Database connectivity |
| Streamlit | Web application |
| Plotly | Interactive data visualization |
| GitHub | Source code hosting |

## 📂 Dataset

The project uses Solar Power Generation Data containing two datasets:

**1. Plant 1 Generation Data**
- Date and time
- Inverter ID
- DC power
- AC power
- Daily yield
- Total yield

**2. Plant 1 Weather Sensor Data**
- Date and time
- Solar irradiation
- Ambient temperature
- Module temperature

## ⚙️ How the Project Works

1. Upload solar generation and weather datasets into Google Colab.
2. Clean and merge the datasets using Python and Pandas.
3. Calculate expected solar power using a historical irradiation-based baseline.
4. Identify low-output readings using an 80% performance threshold.
5. Store processed data in Neon PostgreSQL.
6. Connect the Streamlit website to the database.
7. Display interactive charts, inverter filters, and performance reports.

## 📊 Dashboard Features

- **Inverter Selection:** Select from Inverter 1 to Inverter 22.
- **Performance Overview:** View total readings, low-output readings, and missing data.
- **Power Comparison:** Compare actual AC power with expected power.
- **Solar Irradiation:** Analyze solar irradiation over time.
- **Temperature Analysis:** Monitor ambient temperature.
- **Performance Ratio:** View performance relative to the calculated baseline.
- **Underperformance Report:** View flagged low-output readings.
- **CSV Download:** Export analysis results.

## 🗄️ Database

The project uses **Neon PostgreSQL** to store processed solar data in the `solar_readings` table.

The Streamlit application retrieves this data directly from the cloud database.

## 🚀 Running the Project

1. Clone or download this GitHub repository.
2. Install the required libraries:

   `pip install -r requirements.txt`

3. Configure your Neon PostgreSQL connection string as `DATABASE_URL` in Streamlit Secrets.
4. Run the application:

   `streamlit run app.py`

## ⚠️ Limitations

The current datasets contain generation and weather observations but do not include equipment alarms, cleaning records, or maintenance tickets.

Underperformance is detected using an approximate historical baseline. Flagged periods indicate potential performance issues requiring further investigation and do not confirm equipment faults or root causes.

## ✅ Conclusion

This project demonstrates how solar power plant performance can be monitored using data analytics, cloud database storage, and interactive visualization. It helps identify low-output periods, examine weather conditions, and generate reports for further investigation.

---

**Live Project:** https://owy8njldbvmx3vuwgzh2dv.streamlit.app/

**Project Type:** Data Visualization Mini Project
