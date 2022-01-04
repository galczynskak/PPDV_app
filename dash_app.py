import dash
from dash import dcc
from dash import html
from plotly import graph_objects as go
from dash.dependencies import Input, Output
from storage import get_storage
import numpy as np

def legs_plot():

    store = get_storage()
    print(store.keys())

    if 1 in store.keys():
        print("one is here")
        rec = get_storage()[1]
        print(rec)
        times = np.array(rec["df"]["timestamp"])
        values = []
        for y in range(0, len(rec["df"].index)):
            meas = []
            for x in ["L0_value", "L1_value", "L2_value", "R0_value", "R1_value", "R2_value"]:
                meas.append(rec["df"][y][x])
            values.append(meas)
    else:
        #times = np.array([0])
        #values = np.array([[0]])
        times = np.array([0])
        values = np.array([[0]])

    print(times)
    print(values)

    # if "2" in get_storage():
    #     pd = get_storage()["2"]
    #     times = np.array(pd["timestamp"])
    #     values = np.array(pd["values"])
    # else:
    #     times = np.array([0])
    #     values = np.array([[0]])     

    # print(times)
    # print(values)

    fig = go.Figure([go.Scatter(x = times, y = values[:, 0],\
        line = dict(color = 'firebrick', width = 4), name = 'L0')
    ])
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