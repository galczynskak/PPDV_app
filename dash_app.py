import dash
from dash import dcc
from dash import html
from plotly import graph_objects as go
from dash.dependencies import Input, Output
from storage import get_storage
import numpy as np

def legs_plot():
    if 1 in get_storage():
        pd = get_storage()[1]
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

    print(times)
    print(values)

    fig = go.Figure([go.Scatter(x = times, y = values[0, :],\
       line = dict(color = 'firebrick', width = 4), name = 'L0')
    ])
    fig.add_traces([go.Scatter(x = times, y = values[1, :],\
       line = dict(color = 'aqua', width = 4), name = 'L1'),
       go.Scatter(x = times, y = values[2, :],\
       line = dict(color = 'lime', width = 4), name = 'L2'),
       go.Scatter(x = times, y = values[3, :],\
       line = dict(color = 'sandybrown', width = 4), name = 'R0'),
       go.Scatter(x = times, y = values[4, :],\
       line = dict(color = 'olivedrab', width = 4), name = 'R1'),
       go.Scatter(x = times, y = values[5, :],\
       line = dict(color = 'rosybrown', width = 4), name = 'R2')])
    return fig

app = dash.Dash()

def create_layout():
    app.layout = html.Div( id = 'parent', children = [
        html.H1(id = 'H1', children = 'Styling using HTML components', style =  {'textAlign':'center',\
            'marginTop':40, 'marginBottom':40}),\
            dcc.Graph(id = 'the_plot', figure = legs_plot()),\
            dcc.Interval(id='interval', interval=1000, n_intervals=0)
            ]
    )

@app.callback(Output(component_id='the_plot', component_property='figure'),
    [Input(component_id='interval', component_property='n_intervals')])
def graph_update(n_intervals):
    #print(n_intervals)
    return legs_plot()