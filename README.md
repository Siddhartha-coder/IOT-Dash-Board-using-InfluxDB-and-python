# 📊 IoT Environmental Dashboard with InfluxDB & Dash

A real-time interactive dashboard to monitor IoT sensor data (🌡️ Temperature, 📡 RSSI Signal Strength, and 💧 Humidity) stored in **InfluxDB Cloud**.  
Built with **Python, Plotly Dash, and InfluxDB Client**, the dashboard provides **time-series visualizations** and **live gauges** for quick insights.  

---

## 🚀 Features
- ✅ Connects to **InfluxDB Cloud** via Python client  
- ✅ Queries both **historical and live sensor data** using Flux  
- ✅ **Automatic refresh** every 10 seconds  
- ✅ **Line charts** for each metric  
- ✅ **Gauge indicators** beside each chart showing the latest value  
- ✅ Easily extendable for additional sensors  

---

## 📷 Dashboard Overview
- **Temperature**: Line chart + live gauge (0–100 °C)  
- **RSSI**: Line chart + live gauge (-120 to 0 dBm)  
- **Humidity**: Line chart + live gauge (0–100%)  

Each graph continuously updates with the latest readings.  

---

## ⚙️ Tech Stack
- **Python 3.9+**  
- [Plotly Dash](https://dash.plotly.com/) – dashboard framework  
- [InfluxDB Client](https://github.com/influxdata/influxdb-client-python) – time-series queries  
- **Pandas** – data wrangling & formatting  

---

## 📦 Installation

1. Clone this repository:
   git clone https://github.com/yourusername/iot-dashboard.git
   cd iot-dashboard
Install required dependencies:
pip install dash plotly pandas influxdb-client
Update your InfluxDB credentials inside app.py:


INFLUX_URL = "https://us-east-1-1.aws.cloud2.influxdata.com"
INFLUX_TOKEN = "your_influx_token"
INFLUX_ORG = "your_org"
INFLUX_BUCKET = "Temp_data"

Run the app:
main.py

Open the dashboard in your browser:
http://127.0.0.1:8060

## 🛠️ Customization
Add more sensor fields by modifying the Flux query in get_data()

Change refresh interval (dcc.Interval) – default is 10 seconds

Adjust gauge ranges to match your sensor specifications

## 📌 Use Cases
IoT sensor monitoring

Wireless signal performance analysis (RSSI trends)

Smart agriculture / greenhouse monitoring

Industrial environment monitoring

📄 License
This project is licensed under the MIT License – feel free to use and adapt for your own projects.

