import dash
import numpy as np
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from plotly import graph_objects as go

from storage import get_storage


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
                                line=dict(color='firebrick', width=4), name='L0')
                     ])
    fig.add_traces([go.Scatter(x=times, y=values[1, :], \
                               line=dict(color='aqua', width=4), name='L1'),
                    go.Scatter(x=times, y=values[2, :], \
                               line=dict(color='lime', width=4), name='L2'),
                    go.Scatter(x=times, y=values[3, :], \
                               line=dict(color='sandybrown', width=4), name='R0'),
                    go.Scatter(x=times, y=values[4, :], \
                               line=dict(color='olivedrab', width=4), name='R1'),
                    go.Scatter(x=times, y=values[5, :], \
                               line=dict(color='rosybrown', width=4), name='R2')])
    return fig


app = dash.Dash()


def create_layout():
    storage = get_storage()
    set_patient_id(1)
    app.layout = html.Div(id='parent', children=[
        html.H1(id='H1', children='PPDV - walking visualisation', style={'textAlign': 'center', \
                                                                         'marginTop': 40, 'marginBottom': 40}),
        dcc.Dropdown(
            id='input-dropdown',
            options=[
                {'label': storage[i]["firstname"] + ' ' + storage[i]["lastname"], 'value': i} for i in range(1, 7)
            ],
            value=1
        ),
        html.Div(id='output-info'),
        dcc.Graph(id='output-plot', figure=legs_plot()), \
        dcc.Interval(id='input-interval', interval=1000, n_intervals=0)
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
