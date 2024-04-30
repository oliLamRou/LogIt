import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import time

class PlotlyDashboard:
    _X = deque(maxlen=20)
    _X.append(1)

    _Y = deque(maxlen=20)
    _Y.append(1)

    _app = dash.Dash(__name__)

    def __init__(self):
        self._app.layout = html.Div(
            [
                dcc.Graph(id="live-graph", animate=True),
                dcc.Interval(id="graph-update", interval=1000, n_intervals=0),
            ]
        )

        if self._app is not None and hasattr(self, "callbacks"):
            self.callbacks(self._app)

    def callbacks(self, _app):
        @_app.callback(
            Output("live-graph", "figure"), [Input("graph-update", "n_intervals")]
        )
        def update_graph_scatter(n):
            # let's update data here to show class callbacks are working
            self.update()
            data = plotly.graph_objs.Scatter(
                x=list(self._X), y=list(self._Y), name="Scatter", mode="lines+markers"
            )

            return {
                "data": [data],
                "layout": go.Layout(
                    xaxis=dict(range=[min(self._X), max(self._X)]),
                    yaxis=dict(range=[min(self._Y), max(self._Y)]),
                ),
            }

    def update(self):
        self._X.append(self._X[-1] + 1)
        self._Y.append(self._Y[-1] + self._Y[-1] * random.uniform(-0.1, 0.1))

    def start(self):
        print("starting")
        self._app.run_server(port=8050)
        # this will never be seen !!!!
        print("started")


live_plotter = PlotlyDashboard()


live_plotter.start()
# this code will never run as run_server() is a blocking not a sub-process
while True:
    live_plotter.update()
    time.sleep(1)