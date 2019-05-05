"""Script to read and visualize proximity sensor data from InfluxDB"""

#from influxdb import InfluxDBClient
import plotly
import plotly.plotly as py
import plotly.graph_objs as go


plotly.tools.set_credentials_file(username='alapan9', api_key='yiU13ZYoKmYUMclQxvDe')

# Commented out since motion sensor in prototype was not working
#DB_CLIENT = InfluxDBClient('10.84.109.148', 8086, 'root', 'root', 'VL6180X1')
#DB_DISTANCES = DB_CLIENT.query('select * from distances where "time" > now() - 700m')
#DISTANCES = list(dbDistances.get_points())


DISTANCES = [
    {u'dist': 175, u'time': u'2019-05-04T07:52:52Z'},
    {u'dist': 171, u'time': u'2019-05-04T07:52:53Z'},
    {u'dist': 172, u'time': u'2019-05-04T07:52:55Z'},
    {u'dist': 47, u'time': u'2019-05-04T07:52:57Z'},
    {u'dist': 175, u'time': u'2019-05-04T07:52:58Z'},
    {u'dist': 179, u'time': u'2019-05-04T07:53:00Z'},
    {u'dist': 185, u'time': u'2019-05-04T07:53:03Z'},
    {u'dist': 58, u'time': u'2019-05-04T07:53:04Z'},
    {u'dist': 174, u'time': u'2019-05-04T07:53:06Z'},
    {u'dist': 178, u'time': u'2019-05-04T07:53:08Z'},
    {u'dist': 45, u'time': u'2019-05-04T07:53:13Z'},
    {u'dist': 180, u'time': u'2019-05-04T07:53:15Z'},
    {u'dist': 183, u'time': u'2019-05-04T07:53:17Z'},
    {u'dist': 185, u'time': u'2019-05-04T07:53:18Z'},
    {u'dist': 179, u'time': u'2019-05-04T07:53:20Z'},
    {u'dist': 176, u'time': u'2019-05-04T07:53:21Z'},
    {u'dist': 179, u'time': u'2019-05-04T07:53:22Z'},
    {u'dist': 184, u'time': u'2019-05-04T07:53:27Z'},
    {u'dist': 181, u'time': u'2019-05-04T07:53:28Z'},
    {u'dist': 185, u'time': u'2019-05-04T07:53:30Z'},
    {u'dist': 181, u'time': u'2019-05-04T07:53:32Z'},
    {u'dist': 183, u'time': u'2019-05-04T07:53:33Z'},
    {u'dist': 177, u'time': u'2019-05-04T07:53:34Z'},
    {u'dist': 181, u'time': u'2019-05-04T07:53:35Z'},
    {u'dist': 180, u'time': u'2019-05-04T07:53:41Z'},
    {u'dist': 181, u'time': u'2019-05-04T07:53:42Z'},
    {u'dist': 182, u'time': u'2019-05-04T07:53:44Z'},
    {u'dist': 185, u'time': u'2019-05-04T07:53:46Z'},
    {u'dist': 182, u'time': u'2019-05-04T07:53:47Z'},
    {u'dist': 177, u'time': u'2019-05-04T07:53:48Z'},
    {u'dist': 177, u'time': u'2019-05-04T07:53:49Z'},
    {u'dist': 81, u'time': u'2019-05-04T07:53:50Z'}
]

POINTS = {
    'time': [],
    'distance': []
}

def plot_pie_chart():
    """Plots pie chart showing percentage below and above threshold."""
    threshold = 100
    count_above_threshold = 0
    data_points = len(POINTS['distance'])
    for distance in POINTS['distance']:
        if distance > threshold:
            count_above_threshold += 1

    count_below_threshold = data_points-count_above_threshold
    labels = 'Below threshold', 'Above threshold'
    values = [count_below_threshold, count_above_threshold]
    trace = go.Pie(labels=labels, values=values)

    py.plot([trace], filename='basic_pie_chart')

def plot_line_chart():
    """Plots line chart of proximity vs time"""
    trace = go.Scatter(
        x=POINTS['time'],
        y=POINTS['distance'],
        mode='lines+markers',
        name='lines+markers'
    )

    line = go.Scatter(
        x=[min(POINTS['time']), max(POINTS['time'])],
        y=[100, 100],
        line=dict(
            color=('rgb(205, 12, 24)'),
            width=4
        )
    )

    data = [trace, line]

    layout = go.Layout(
        title=go.layout.Title(
            text='Proximity to sensor vs Time',
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
    py.plot(fig, filename='styling-names')

if DISTANCES:
    for point in DISTANCES:
        POINTS['time'].append(point['time'])
        POINTS['distance'].append(point['dist'])

    plot_line_chart()
    plot_pie_chart()

else:
    print 'There are no measurements in the given time period. Please enter a longer interval!'
