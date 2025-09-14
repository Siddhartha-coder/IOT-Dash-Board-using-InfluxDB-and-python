import pandas as pd
from influxdb_client import InfluxDBClient
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

# -----------------------------
# InfluxDB Configuration
# -----------------------------
INFLUX_URL = "https://us-east-1-1.aws.cloud2.influxdata.com"  # your cloud endpoint
INFLUX_TOKEN = "Your Token"
INFLUX_ORG = "DAQ Team"
INFLUX_BUCKET = "Temp_data"

client = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
query_api = client.query_api()

# -----------------------------
# Flux Query
# -----------------------------
def get_data():
    query = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: 0)
      |> filter(fn: (r) => r["_measurement"] == "Sensor_Data")
      |> filter(fn: (r) => r["_field"] == "temperature" or r["_field"] == "rssi" or r["_field"] == "humidity")
    '''
    tables = query_api.query(query)
    records = []
    for table in tables:
        for record in table.records:
            records.append({
                "time": record.get_time(),
                "field": record.get_field(),
                "value": record.get_value()
            })
    df = pd.DataFrame(records)
    return df

# -----------------------------
# Dash Layout
# -----------------------------
app = Dash(__name__)

app.layout = html.Div([
    html.H1("DAQ Charger Cart Dashboard", style={"textAlign": "center"}),

    dcc.Interval(
        id="interval-component",
        interval=10*1000,  # refresh every 10 seconds
        n_intervals=0
    ),

    # Temperature Row
    html.Div([
        dcc.Graph(id="temp-graph", style={"display": "inline-block", "width": "70%"}),
        dcc.Graph(id="temp-gauge", style={"display": "inline-block", "width": "28%"})
    ]),

    # RSSI Row
    html.Div([
        dcc.Graph(id="rssi-graph", style={"display": "inline-block", "width": "70%"}),
        dcc.Graph(id="rssi-gauge", style={"display": "inline-block", "width": "28%"})
    ]),

    # Humidity Row
    html.Div([
        dcc.Graph(id="humidity-graph", style={"display": "inline-block", "width": "70%"}),
        dcc.Graph(id="humidity-gauge", style={"display": "inline-block", "width": "28%"})
    ]),
])

# -----------------------------
# Callbacks
# -----------------------------
@app.callback(
    [Output("temp-graph", "figure"),
     Output("temp-gauge", "figure"),
     Output("rssi-graph", "figure"),
     Output("rssi-gauge", "figure"),
     Output("humidity-graph", "figure"),
     Output("humidity-gauge", "figure")],
    [Input("interval-component", "n_intervals")]
)
def update_graphs(n):
    df = get_data()
    if df.empty:
        return go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure(), go.Figure()

    # Split data
    temp_df = df[df["field"] == "temperature"]
    rssi_df = df[df["field"] == "rssi"]
    hum_df = df[df["field"] == "humidity"]

    # --- Temperature ---
    temp_fig = go.Figure()
    temp_fig.add_trace(go.Scatter(
        x=temp_df["time"], y=temp_df["value"],
        mode="lines+markers", name="Temperature (°C)"
    ))
    temp_fig.update_layout(title="Temperature vs Time", xaxis_title="Time", yaxis_title="°C")

    latest_temp = temp_df["value"].iloc[-1] if not temp_df.empty else 0
    temp_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=latest_temp,
        title={'text': "Temperature (°C)"},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "red"}}
    ))

    # --- RSSI ---
    rssi_fig = go.Figure()
    rssi_fig.add_trace(go.Scatter(
        x=rssi_df["time"], y=rssi_df["value"],
        mode="lines+markers", name="RSSI (dBm)"
    ))
    rssi_fig.update_layout(title="Signal Strength vs Time", xaxis_title="Time", yaxis_title="dBm")

    latest_rssi = rssi_df["value"].iloc[-1] if not rssi_df.empty else 0
    rssi_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=latest_rssi,
        title={'text': "RSSI (dBm)"},
        gauge={'axis': {'range': [-120, 0]}, 'bar': {'color': "blue"}}
    ))

    # --- Humidity ---
    hum_fig = go.Figure()
    hum_fig.add_trace(go.Scatter(
        x=hum_df["time"], y=hum_df["value"],
        mode="lines+markers", name="Humidity (%)"
    ))
    hum_fig.update_layout(title="Humidity vs Time", xaxis_title="Time", yaxis_title="%")

    latest_hum = hum_df["value"].iloc[-1] if not hum_df.empty else 0
    hum_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=latest_hum,
        title={'text': "Humidity (%)"},
        gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "green"}}
    ))

    return temp_fig, temp_gauge, rssi_fig, rssi_gauge, hum_fig, hum_gauge

# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, port=8060)  # use a free port
