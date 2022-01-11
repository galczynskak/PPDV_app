import dash
import numpy as np
from dash import dcc, callback_context, dash_table
from dash import html
from dash.dependencies import Input, Output
from plotly import graph_objects as go
import dash_bootstrap_components as dbc
from PIL import Image
import plotly.express as px

from collector import *

app = dash.Dash(external_stylesheets=[dbc.themes.GRID])


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
        df = pd["df"].iloc[-15:]
        times = np.array(df["timestamp"])
        values = [[], [], [], [], [], []]
        points = ["L0_value", "L1_value", "L2_value", "R0_value", "R1_value", "R2_value"]
        for j in range(0, len(points)):
            for i in range(0, len(df.index)):
                values[j].append(df[points[j]].iloc[i])

        values = np.array(values)
    else:
        times = np.array([0])
        values = np.array([[0]])

    fig = go.Figure()
    fig.add_traces([go.Scatter(x=times, y=values[0, :], \
                                line=dict(color='#8c510a', width=2), name='L0'),
                     go.Scatter(x=times, y=values[1, :], \
                               line=dict(color='#d8b365', width=2), name='L1'),
                    go.Scatter(x=times, y=values[2, :], \
                               line=dict(color='#f6e8c3', width=2), name='L2'),
                    go.Scatter(x=times, y=values[3, :], \
                               line=dict(color='#c7eae5', width=2), name='R0'),
                    go.Scatter(x=times, y=values[4, :], \
                               line=dict(color='#5ab4ac', width=2), name='R1'),
                    go.Scatter(x=times, y=values[5, :], \
                               line=dict(color='#01665e', width=2), name='R2')])

    fig.update_traces(marker=dict(size=7, color = '#FFFFFF',
                              line=dict(width=2)))

    fig.update_layout(
        xaxis_title="timestamp",
        yaxis_title="value",
        legend_title="sensors"
    )

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
                                      line=dict(color='#8c510a', width=2), name='L0', 
                                      marker=dict(size=7, color = '#FFFFFF',
                                      line=dict(width=2)), showlegend=False)
                           ])
    sensor_L0.update_layout(autosize=False, width=900, height=200, title="L0", title_y=0.5,
                            margin_l=100, margin_b=0, margin_r=0, margin_t=0)
    sensor_L1 = go.Figure([go.Scatter(x=times, y=values[1, :], \
                                      line=dict(color='#d8b365', width=2), name='L1',
                                      marker=dict(size=7, color = '#FFFFFF',
                                      line=dict(width=2)), showlegend=False)
                           ])
    sensor_L1.update_layout(autosize=False, width=900, height=200, title="L1", title_y=0.5,
                            margin_l=100, margin_b=0, margin_r=0, margin_t=0)
    sensor_L2 = go.Figure([go.Scatter(x=times, y=values[2, :], \
                                      line=dict(color='#f6e8c3', width=2), name='L2',
                                      marker=dict(size=7, color = '#FFFFFF',
                                      line=dict(width=2)), showlegend=False)
                           ])
    sensor_L2.update_layout(autosize=False, width=900, height=200, title="L1", title_y=0.5,
                            margin_l=100, margin_b=0, margin_r=0, margin_t=0)
    sensor_R0 = go.Figure([go.Scatter(x=times, y=values[3, :], \
                                      line=dict(color='#c7eae5', width=2), name='R0',
                                      marker=dict(size=7, color = '#FFFFFF',
                                      line=dict(width=2)), showlegend=False)
                           ])
    sensor_R0.update_layout(autosize=False, width=900, height=200, title="R0", title_y=0.5, title_x=1.0,
                            margin_l=0, margin_b=0, margin_r=100, margin_t=0)
    sensor_R0.update_yaxes(side="right")
    sensor_R1 = go.Figure([go.Scatter(x=times, y=values[4, :], \
                                      line=dict(color='#5ab4ac', width=2), name='R1',
                                      marker=dict(size=7, color = '#FFFFFF',
                                      line=dict(width=2)), showlegend=False)
                           ])
    sensor_R1.update_layout(autosize=False, width=900, height=200, title="R1", title_y=0.5, title_x=1.0,
                            margin_l=0, margin_b=0, margin_r=100, margin_t=0)
    sensor_R1.update_yaxes(side="right")
    sensor_R2 = go.Figure([go.Scatter(x=times, y=values[5, :], \
                                      line=dict(color='#01665e', width=2), name='R2',
                                      marker=dict(size=7, color = '#FFFFFF',
                                      line=dict(width=2)), showlegend=False)
                           ])
    sensor_R2.update_layout(autosize=False, width=900, height=200, title="R2", title_y=0.5, title_x=1.0,
                            margin_l=0, margin_b=0, margin_r=100, margin_t=0)
    sensor_R2.update_yaxes(side="right")

    return [sensor_L0, sensor_L1, sensor_L2, sensor_R0, sensor_R1, sensor_R2]


def animate_mean():
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

    mean_sensors = []
    for i in range(0, 6):
        try:
            mean_sensors.append(round(values[i, :].mean(), 2))
        except Exception:
            mean_sensors.append(0)
    fig = go.Figure([go.Scatter(x=['L0', 'L1', 'L2', 'R0', 'R1', 'R2'], y=mean_sensors, mode='markers', marker=dict(
            color='#feedde',
            size=40,
            line=dict(
                color='#8c510a',
                width=2
            )))])
    fig.update_layout(title_text='Mean value tendencies', title_x=0.5)
    return fig

def animate_max():
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

    v = []
    for i in range(0, 6):
        try:
            v.append(values[i, :].max())
        except Exception:
            v.append(0)
    fig = go.Figure([go.Scatter(x=['L0', 'L1', 'L2', 'R0', 'R1', 'R2'], y=v, mode='markers', marker=dict(
        color='#feedde',
        size=40,
        line=dict(
            color='#8c510a',
            width=2
        )))])
    fig.update_layout(title_text='Maximal value tendencies', title_x=0.5)
    return fig

def animate_min():
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

    v = []
    for i in range(0, 6):
        try:
            v.append(values[i, :].min())
        except Exception:
            v.append(0)
    fig = go.Figure([go.Scatter(x=['L0', 'L1', 'L2', 'R0', 'R1', 'R2'], y=v, mode='markers', marker=dict(
        color='#feedde',
        size=40,
        line=dict(
            color='#8c510a',
            width=2
        )))])
    fig.update_layout(title_text='Minimal value tendencies', title_x=0.5)
    return fig


def create_feet_plot():
    cols = ["L0_value", "L1_value", "L2_value", "R0_value", "R1_value", "R2_value"]
    data = get_storage()[get_current_patient()]['df'][cols]
    feet_image = Image.open("feet.png")
    if(len(data) > 0):
        vals = (data.iloc[-1]).to_list()
    else:
        vals = [0, 0, 0, 0, 0, 0]
    fig = go.Figure(px.scatter(
        x=[1.8, 2, 2.15, 2.7, 2.85, 3.05], y=[7.5, 3.4, 8, 5.8, 1, 5], size=vals, size_max=60
    ))

    fig.update_yaxes(range=[0,10], showgrid=False, visible=False)
    fig.update_xaxes(range=[0,5], showgrid=False, visible=False)
    fig.update_layout(width=1000, height=500,
                      margin_b=0, margin_t=0, margin_r=0, margin_l=0)
    fig.update_traces(marker=dict(color="white", gradient=dict(color="darkcyan", type="radial")))
    fig.add_layout_image(
        dict(
            source=feet_image,
            xref='x', yref='y',
            x=0, y=0,
            sizex=5, sizey=10,
            xanchor='left', yanchor='bottom',
            sizing='stretch', layer='below'
        )
    )

    return fig

def create_layout():
    storage = get_storage()
    set_patient_id(1)
    app.layout = html.Div(id='parent', children=[
        html.H1(id='H1', children='PPDV - walking visualisation', style={'align-items': 'center', \
                                                                         'marginTop': 0, 'marginBottom': 10,
                                                                         'height':120, 'text-align':'middle', 'display':'flex',
                                                                         'background-color':'darkslategray', 'color': 'white',
                                                                         'font-family': 'Open Sans', 'font-weight':'normal',
                                                                         'font-size':40, 'justify-content':'center'}),
        dbc.Row(
            [
                dbc.Col(html.Button('STOP/ACTIVATE\nDATA GATHERING', id='gather-data', n_clicks=0,
                                    style = {'font-family':'Open Sans', 'font-weight':'normal',
                                             'background-color': 'whitesmoke', 'font-size':16, 'margin-left':10,
                                             'color': 'black','height': '50px','width': '200px',
                                             "border-radius":8, "box-shadow":"2px 2px 1px 1px lightgrey"})),
                dbc.Col(html.Div(id='data-gathering')),
                dbc.Col(dcc.Dropdown(
                    id='input-dropdown',
                    options=[
                        {'label': storage[i]["firstname"] + ' ' + storage[i]["lastname"], 'value': i} for i in range(1, 7)
                    ],
                    value=1
                )),
                dbc.Col(html.Div(id='output-info')),
            ], justify="center", align="center"
        ),
        html.Hr(),
        html.H2("Feet sensors visualisation", style={'font-family':'Open Sans', 'font-weight':'normal',
                                                  'text-align':'center', 'margin-bottom':20, 'background-color':'whitesmoke'}),
        html.Div(dcc.Graph(id='feet-plot', figure=create_feet_plot()), style={'margin':'auto', "display":'flex', 'justify-content':"center"}),
        dcc.Interval(id='input-sensor-feet', interval=1000, n_intervals=0),
        html.Hr(),
        html.H2("Aggregated sensors plot", style={'font-family':'Open Sans', 'font-weight':'normal',
                                                 'text-align':'center', 'margin-bottom':20, 'background-color':'whitesmoke'}),
        dcc.Graph(id='output-plot', figure=legs_plot()), \
        dcc.Interval(id='input-interval', interval=1000, n_intervals=0),
        html.Hr(),
        html.H2("Mean value tendencies", style={'font-family':'Open Sans', 'font-weight':'normal',
                                                 'text-align':'center', 'margin-bottom':20, 'background-color':'whitesmoke'}),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='an_min', figure=animate_min()),
                dcc.Interval(id='input-min-animate', interval=1000, n_intervals=0)
            ]),
            dbc.Col([
                dcc.Graph(id='an_max', figure=animate_max()),
                dcc.Interval(id='input-max-animate', interval=1000, n_intervals=0)
            ]),
            dbc.Col([
                dcc.Graph(id='an_mean', figure=animate_mean()),
                dcc.Interval(id='input-mean-animate', interval=1000, n_intervals=0)
            ])
        ]),
        html.Hr(),
        html.H2("Detailed sensors plots", style={'font-family':'Open Sans', 'font-weight':'normal',
                                                 'text-align':'center', 'margin-bottom':20, 'background-color':'whitesmoke'}),
        dbc.Row(
            [
                dbc.Col([
                    dcc.Graph(id='sensor_L0'),
                    dcc.Interval(id='input-sensor-interval-1', interval=1000, n_intervals=0),
                    dcc.Graph(id='sensor_L1'),
                    dcc.Interval(id='input-sensor-interval-2', interval=1000, n_intervals=0),
                    dcc.Graph(id='sensor_L2'),
                    dcc.Interval(id='input-sensor-interval-3', interval=1000, n_intervals=0)
                ]),
                dbc.Col([
                    dcc.Graph(id='sensor_R0'),
                    dcc.Interval(id='input-sensor-interval-4', interval=1000, n_intervals=0),
                    dcc.Graph(id='sensor_R1'),
                    dcc.Interval(id='input-sensor-interval-5', interval=1000, n_intervals=0),
                    dcc.Graph(id='sensor_R2'),
                    dcc.Interval(id='input-sensor-interval-6', interval=1000, n_intervals=0)
                ])
            ]
        ),
        html.Hr(),
        html.H2("Anomalies monitoring dashboard", style={'font-family':'Open Sans', 'font-weight':'normal',
                                                  'text-align':'center', 'margin-bottom':20, 'background-color':'whitesmoke'}),
        html.Div(id='live_data'),
        dcc.Interval(id='data-interval', interval=1000, n_intervals=0)
    ]
                          )


@app.callback(Output(component_id='output-info', component_property='children'),
              Input(component_id='input-dropdown', component_property='value'))
def define_parameters(patient_id):
    storage = get_storage()
    set_patient_id(patient_id)
    return html.Div([html.H3("Currently displaying data for patient:", style={'font-family':'Open Sans', 'font-weight':'normal'}),
                     html.H4("Fullname: " + str(storage[patient_id]["fullname"]), style={'font-family':'Open Sans', 'font-weight':'normal'}),
                     html.H4("Detailed name: " + str(storage[patient_id]["name"]), style={'font-family':'Open Sans', 'font-weight':'normal'}),
                     html.H4("Birthdate: " + str(storage[patient_id]["birthdate"]), style={'font-family':'Open Sans', 'font-weight':'normal'}),
                     html.H4("Disability: " + str(storage[patient_id]["disabled"]), style={'font-family':'Open Sans', 'font-weight':'normal'}),
                     html.H4("ID: " + str(storage[patient_id]["id"]), style={'font-family':'Open Sans', 'font-weight':'normal'})],
                    style={"border-radius":8, "box-shadow":"2px 2px 1px 1px lightgrey", "border":2, "border-color":"black",
                           "border-style":'solid', "background":"whitesmoke", "padding-left":10, "line-height":6})


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

@app.callback(Output(component_id='an_mean', component_property='figure'),
              [Input(component_id='input-mean-animate', component_property='n_intervals')])
def update_animated_mean(n_intervals):
    return animate_mean()

@app.callback(Output(component_id='an_max', component_property='figure'),
              [Input(component_id='input-max-animate', component_property='n_intervals')])
def update_animated_max(n_intervals):
    return animate_max()

@app.callback(Output(component_id='an_min', component_property='figure'),
              [Input(component_id='input-min-animate', component_property='n_intervals')])
def update_animated_min(n_intervals):
    return animate_min()

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
    return html.H3(message, style={'font-family':'Open Sans', 'font-weight':'normal'})


@app.callback(Output(component_id='live_data', component_property='children'),
              Input(component_id='data-interval', component_property='n_intervals'))
def update_anomalies(n_intervals):
    df = get_storage()['anomalies']
    titles = ["Patient full name", "Measurement ID", "Time", "Sensor ID", "Sensor value"]
    return html.Div(
        dash_table.DataTable(
            id='anomalies-table',
            columns=[{"name": i, "id": i} for i in titles],
            data=df.to_dict('records'),
            style_header={'backgroundColor':"tomato", 'text-align':'center',
                          'font-family':'Open Sans', 'color':'white'},
            style_cell={'textAlign':'center','font-family':'Open Sans'},
            style_table={'width':'80%', 'margin-right':'auto', 'margin-left':'auto'}
    ))

@app.callback(Output(component_id='feet-plot', component_property='figure'),
              [Input(component_id='input-sensor-feet', component_property='n_intervals')])
def update_animated_grphs(n_intervals):
    return create_feet_plot()