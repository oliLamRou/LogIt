import os

import pandas as pd

from dash import Dash, dash_table, html, dcc, Input, Output, callback

white_button_style = {'background-color': 'red',
                      'color': 'black',
                      'height': '50px',
                      'width': '100px',
                      'margin-top': '50px',
                      'margin-left': '50px'}

style={
    'font-size': '30px', 
    'width': '50px', 
    'display': 'inline-block', 
    'margin-bottom': '10px', 
    'margin-right': '5px', 
    'height':'50px', 
    'verticalAlign': 'top'
}

class Dashboard:

    def __init__(self):
        self.app = Dash(__name__)

    def today(self):
        self.app.layout = html.Div([
            html.Button('+', id='entry', n_clicks=0, style=style),
        ])

    @callback(
        Output('container-button-basic', 'children'),
        Input('submit-val', 'n_clicks'),
        State('input-on-submit', 'value'),
        prevent_initial_call=True
    )
    def update_output(n_clicks, value):
        return 'The input value was "{}" and the button has been clicked {} times'.format(
            value,
            n_clicks
        )

    def build(self):
        pass

if __name__ == '__main__':
    dash = Dashboard()
    dash.today()
    dash.app.run(debug=True)
