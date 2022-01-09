import dash
import numpy as np
from dash import dcc, callback_context, dash_table
from dash import html
from dash.dependencies import Input, Output
from plotly import graph_objects as go

from collector import *

app = dash.Dash()


def set_patient_id(n):
    global current_patient
    current_patient = n
    return current_patient


def get_current_patient():
    return current_patient


def legs_plot():
    patient_id = get_current_patient()
    if patient_id in get_storage():
        pd = get_storage()[patient_id]
        times = np.array(pd["df"]["timestamp"])
        values = [[], [], [], [], [], []]
        points = ["L0_value", "L1_value", "L2_value", "R0_value", "R1_value", "R2_value"]
        df = pd["df"]
        for j in range(0, len(points)):
            for i in range(0, len(df.index)):
                values[j].append(df[points[j]][i])

        values = np.array(values)
    else:
        times = np.array([0])
        values = np.array([[0]])

    fig = go.Figure([go.Scatter(x=times, y=values[0, :], \
                                line=dict(color='#8c510a', width=4), name='L0')
                     ])
    fig.add_traces([go.Scatter(x=times, y=values[1, :], \
                               line=dict(color='#d8b365', width=4), name='L1'),
                    go.Scatter(x=times, y=values[2, :], \
                               line=dict(color='#f6e8c3', width=4), name='L2'),
                    go.Scatter(x=times, y=values[3, :], \
                               line=dict(color='#c7eae5', width=4), name='R0'),
                    go.Scatter(x=times, y=values[4, :], \
                               line=dict(color='#5ab4ac', width=4), name='R1'),
                    go.Scatter(x=times, y=values[5, :], \
                               line=dict(color='#01665e', width=4), name='R2')])

    fig.update_traces(marker=dict(size=7, color = '#FFFFFF',
                              line=dict(width=2)))
    return fig


def sensor_plots():
    patient_id = get_current_patient()
    if patient_id in get_storage():
        pd = get_storage()[patient_id]
        times = np.array(pd["df"]["timestamp"])
        values = [[], [], [], [], [], []]
        points = ["L0_value", "L1_value", "L2_value", "R0_value", "R1_value", "R2_value"]
        df = pd["df"]
        for j in range(0, len(points)):
            for i in range(0, len(df.index)):
                values[j].append(df[points[j]][i])

        values = np.array(values)
    else:
        times = np.array([0])
        values = np.array([[0]])

    sensor_L0 = go.Figure([go.Scatter(x=times, y=values[0, :], \
                                      line=dict(color='#8c510a', width=4), name='L0', 
                                      marker=dict(size=7, color = '#FFFFFF',
                                      line=dict(width=2)), showlegend=True)
                           ])
    sensor_L0.update_layout(autosize=False, width=900, height=400)
    sensor_L1 = go.Figure([go.Scatter(x=times, y=values[1, :], \
                                      line=dict(color='#d8b365', width=4), name='L1',
                                      marker=dict(size=7, color = '#FFFFFF',
                                      line=dict(width=2)), showlegend=True)
                           ])
    sensor_L1.update_layout(autosize=False, width=900, height=400)
    sensor_L2 = go.Figure([go.Scatter(x=times, y=values[2, :], \
                                      line=dict(color='#f6e8c3', width=4), name='L2',
                                      marker=dict(size=7, color = '#FFFFFF',
                                      line=dict(width=2)), showlegend=True)
                           ])
    sensor_L2.update_layout(autosize=False, width=900, height=400)
    sensor_R0 = go.Figure([go.Scatter(x=times, y=values[3, :], \
                                      line=dict(color='#c7eae5', width=4), name='R0',
                                      marker=dict(size=7, color = '#FFFFFF',
                                      line=dict(width=2)), showlegend=True)
                           ])
    sensor_R0.update_layout(autosize=False, width=900, height=400)
    sensor_R1 = go.Figure([go.Scatter(x=times, y=values[4, :], \
                                      line=dict(color='#5ab4ac', width=4), name='R1',
                                      marker=dict(size=7, color = '#FFFFFF',
                                      line=dict(width=2)), showlegend=True)
                           ])
    sensor_R1.update_layout(autosize=False, width=900, height=400)
    sensor_R2 = go.Figure([go.Scatter(x=times, y=values[5, :], \
                                      line=dict(color='#01665e', width=4), name='R2',
                                      marker=dict(size=7, color = '#FFFFFF',
                                      line=dict(width=2)), showlegend=True)
                           ])
    sensor_R2.update_layout(autosize=False, width=900, height=400)

    return [sensor_L0, sensor_L1, sensor_L2, sensor_R0, sensor_R1, sensor_R2]


def create_layout():
    storage = get_storage()
    set_patient_id(1)
    app.layout = html.Div(id='parent', children=[
        html.H1(id='H1', children='PPDV - walking visualisation', style={'textAlign': 'center', \
                                                                         'marginTop': 40, 'marginBottom': 40}),
        html.Button('Stop data gathering', id='gather-data', n_clicks=0, style = {'background-color': '#feedde',
                                                                                    'color': 'black',
                                                                                    'height': '50px',
                                                                                    'width': '200px'}),
        html.Div(id='data-gathering'),
        dcc.Dropdown(
            id='input-dropdown',
            options=[
                {'label': storage[i]["firstname"] + ' ' + storage[i]["lastname"], 'value': i} for i in range(1, 7)
            ],
            value=1
        ),
        html.Div(id='output-info'),
        dash_table.DataTable(
            id='anomalies-table',
            columns=[{"name": i, "id": i} for i in storage["anomalies"].columns],
            data=storage["anomalies"].to_dict('records')
        ),
        dcc.Graph(id='output-plot', figure=legs_plot()), \
        dcc.Interval(id='input-interval', interval=1000, n_intervals=0),
        html.Div([
            dcc.Graph(id='sensor_L0'),
            dcc.Interval(id='input-sensor-interval-1', interval=1000, n_intervals=0),
            dcc.Graph(id='sensor_L1'),
            dcc.Interval(id='input-sensor-interval-2', interval=1000, n_intervals=0),
            dcc.Graph(id='sensor_L2'),
            dcc.Interval(id='input-sensor-interval-3', interval=1000, n_intervals=0),
            dcc.Graph(id='sensor_R0'),
            dcc.Interval(id='input-sensor-interval-4', interval=1000, n_intervals=0),
            dcc.Graph(id='sensor_R1'),
            dcc.Interval(id='input-sensor-interval-5', interval=1000, n_intervals=0),
            dcc.Graph(id='sensor_R2'),
            dcc.Interval(id='input-sensor-interval-6', interval=1000, n_intervals=0)
        ])
    ]
                          )


@app.callback(Output(component_id='output-info', component_property='children'),
              Input(component_id='input-dropdown', component_property='value'))
def define_parameters(patient_id):
    storage = get_storage()
    set_patient_id(patient_id)
    return html.Div(html.H4("Presenting data for patient: " + storage[patient_id]["fullname"]))


@app.callback(Output(component_id='output-plot', component_property='figure'),
              [Input(component_id='input-interval', component_property='n_intervals')])
def graph_update(n_intervals):
    return legs_plot()


@app.callback([Output(component_id='sensor_L0', component_property='figure'),
               Output(component_id='sensor_L1', component_property='figure'),
               Output(component_id='sensor_L2', component_property='figure'),
               Output(component_id='sensor_R0', component_property='figure'),
               Output(component_id='sensor_R1', component_property='figure'),
               Output(component_id='sensor_R2', component_property='figure')],
              Input(component_id='input-sensor-interval-1', component_property='n_intervals'))
def update_sensor_graphs(n_intervals):
    return sensor_plots()


@app.callback(Output(component_id='data-gathering', component_property="children"),
              Input('gather-data', 'n_clicks'))
def update_data_gathering(n_clicks):
    changed_button = [p['prop_id'] for p in callback_context.triggered][0]
    if 'gather-data' in changed_button:
        set_collector_state(not get_collector_state())

    if get_collector_state():
        message = "Data gathering is not active."
    else:
        message = "Data gathering is active."
    return html.H3(message)
