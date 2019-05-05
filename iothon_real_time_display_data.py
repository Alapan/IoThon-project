"""
Script to read and visualize proximity sensor data from InfluxDB
in real-time, as target is moved towards and away from sensor.
UNTESTED - motion sensor was not working at the time of writing this.
"""
import time
from influxdb import InfluxDBClient
import plotly
import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='alapan9', api_key='yiU13ZYoKmYUMclQxvDe')


DB_CLIENT = InfluxDBClient('10.84.109.148', 8086, 'root', 'root', 'VL6180X1')

def plot_graph(points):
    """Plots graph using sensor data."""
    trace = go.Scatter(
        x=points['time'],
        y=points['distance'],
        mode='lines+markers',
        name='lines+markers'
    )

    horizontal_line = go.Scatter(
        x=[min(points['time']), max(points['time'])],
        y=[100, 100],
        line=dict(
            color=('rgb(205, 12, 24)'),
            width=4
        )
    )

    data = [trace, horizontal_line]

    layout = go.Layout(
        title=go.layout.Title(
            text='Proximity to sensor vs Time (last 10 minutes)',
            xref='paper',
            x=0
        ),
        xaxis=go.layout.XAxis(
            title=go.layout.xaxis.Title(
                text='Time',
                font=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            )
        ),
        yaxis=go.layout.YAxis(
            title=go.layout.yaxis.Title(
                text='Proximity to sensor',
                font=dict(
                    family='Courier New, monospace',
                    size=18,
                    color='#7f7f7f'
                )
            )
        )
    )
    fig = go.Figure(data=data, layout=layout)
    fig['layout']['yaxis']['autorange'] = "reversed"
    py.plot(fig, filename='styling-names', fileopt='extend')

def read_sensor_data(interval=''):
    """Reads sensor data and generates data points for plotting"""
    interval = interval if interval else '1s'
    db_distances = DB_CLIENT.query('select * from distances where "time" > now() - %s' % interval)
    distances = list(db_distances.get_points())

    points = {
        'time': [],
        'distance': []
    }
    if distances:
        for point in distances:
            points['time'].append(point['time'])
            points['distance'].append(point['dist'])
        plot_graph(points)
        time.sleep(1)

read_sensor_data('700m')

while True:
    read_sensor_data()
