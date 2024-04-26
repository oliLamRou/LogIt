import os
import pandas as pd
import numpy as np
from dash import Dash, dash_table, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc

import data

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "30rem",
    "padding": "2rem 1rem",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "32rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


app = Dash(external_stylesheets=[dbc.themes.DARKLY])


class Dashboard:
    header = dcc.Markdown('# My Journal')

    def __init__(self, filename):
        self.filename = filename
        self.path = f'../data/{filename}.csv'

        self._df = pd.DataFrame()

    @property
    def df(self):
        if self._df.empty:
            self._df = pd.read_csv(self.path).set_index('date')

        return self._df

    def card_header(self, date):
        return dbc.CardHeader(date)

    def card_body(self, date):
        #Get Note
        note = self.df.loc[date, 'note']
        #NOTE: should be a better way right ?
        if str(note) == 'nan':
            note = '---'

        #Add first elem in markdown list
        body = [dcc.Markdown(f'### {note}')]


        metrics = []
        for col in self.df.columns:
            if col == 'note':
                continue

            metric = self.df.loc[date, col]
            body.append(dcc.Markdown(f'- {metric}'))

        #Add metadata at the end
        metadata = 'metadata'
        body.append(dcc.Markdown(f'###### *{metadata}*'))

        return dbc.CardBody(
            body
        )

    def card(self, date):
        return dbc.Card(
            [
                self.card_header(date),
                self.card_body(date)
            ]
        )

    def cards(self):
        _cards = [dcc.Markdown('## Hello')]
        for date in self.df.index:
            _cards.append(self.card(date))

        return _cards

    def form(self):
        dropdown_menu_items = [
            dbc.DropdownMenuItem("cat1", id="dropdown-menu-item-1"),
            dbc.DropdownMenuItem("cat2", id="dropdown-menu-item-2"),
            dbc.DropdownMenuItem(divider=True),
            dbc.DropdownMenuItem("New", id="dropdown-menu-item-new"),
        ]

        input_group = html.Div(
        [
            #Title
            dbc.InputGroup(
                [dbc.Input(placeholder="Title")],
                className="mb-3",
            ),
            #Notes
            dbc.InputGroup(
                [dbc.Textarea(placeholder="Note")],
                className="mb-3",
            ),
            #Categories
            dbc.InputGroup(
                [
                    dbc.DropdownMenu(dropdown_menu_items, label="Categeory"),
                    dbc.Input(placeholder="New Categeory") if True else None,
                    dbc.Input(placeholder="Value", id="input-group-dropdown-input")
                ]
            ),
        ])
        return [input_group]

    def build(self):
        # self.app.layout = dbc.Container(self.cards())
        app.layout = html.Div([
                dbc.Container(self.form(), style=SIDEBAR_STYLE),
                dbc.Container(self.cards(), style=CONTENT_STYLE),
            ])

if __name__ == '__main__':
    dash = Dashboard('myLog')
    dash.build()
    app.run(debug=True)



