import pandas as pd

from dash import Dash, dash_table, html, dcc, Input, Output, callback, ctx
import dash_bootstrap_components as dbc

from app_style import SIDEBAR_STYLE, CONTENT_STYLE, FORM_STYLE
from data import Data

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

data = Data()
df = data.df

def get_categories():
    categories = []
    for category in data.df.columns:
        if category == 'note':
            continue

        categories.append(category)

    return categories

def card_body(row):
    #Get Note
    note = row.note
    #NOTE: should be a better way right ?
    if str(note) == 'nan':
        note = '---'

    #Add first elem in markdown list
    body = [dcc.Markdown(f'### {note}')]
    body = body + [
        dcc.Markdown(f'- {category.capitalize()}: {row[category]}') for category in get_categories()
    ]

    return dbc.CardBody(
        body
    )

def card(row):
    return dbc.Card(
        [
            dbc.CardHeader(row.index),
            card_body(row)
        ]
    )

def cards():
    _cards = [dcc.Markdown('## Hello')]
    for date in df.index:
        row = df.loc[date]
        _cards.append(card(row))

    return _cards

def get_dropdownmenu():
    dropdownmenu = [dbc.DropdownMenuItem(category.capitalize(), id=category) for category in get_categories()]
    dropdownmenu.append(dbc.DropdownMenuItem(divider=True))
    dropdownmenu.append(dbc.DropdownMenuItem('New Categeory', id='new categeory'))
    return dropdownmenu

def get_inputs():
    inputs = [Input(category, 'n_clicks') for category in get_categories()]
    inputs.append(Input('new categeory', 'n_clicks'))
    return inputs

def form():
    input_group = html.Div(
    [
        #Title
        dbc.InputGroup(
            [dbc.Input(placeholder="Title", id='title-input')],
            className="mb-3",
        ),
        #Notes
        dbc.InputGroup(
            [dbc.Textarea(placeholder="Note", id='note-input')],
            className="mb-3",
        ),
        dbc.InputGroup(
            [
                dbc.DropdownMenu(
                    get_dropdownmenu(),
                    label="Generate", id='dropdownmenu-label'
                ),
                dbc.Input(placeholder="new categeory", id='new-category'),
                dbc.Input(placeholder="Value", id='value-input')
            ],
        ),
        dbc.InputGroup(
            [
                dbc.Button("+", color="success", className="me-1"),
            ], 
            style = FORM_STYLE
        ),
        dbc.InputGroup(
            [
                dbc.Button("Save", color="primary", id='save-button'),
                dbc.Button("Clear", color="secondary", id='clear-button'),
            ],
        )
    ])
    return [input_group]

@app.callback(
    [
        Output('title-input', 'value'),
        Output('note-input', 'value'),
        Output('value-input', 'value'),
        Output('new-category', 'value')
    ],
    [
        Input('save-button', 'n_clicks'),
        Input('clear-button', 'n_clicks')
    ])
def ok_cancel_button(ok, cancel):
    return '', '', '', ''

@app.callback(
    [
        Output('new-category', 'style'),
        Output('dropdownmenu-label', 'label'),
        Output('value-input', 'disabled'),
    ],
    get_inputs())
def category_button(*args,**kwargs):
    if not ctx.triggered:
        return {'display': 'none'}, 'Categeory', True
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == 'new categeory':
        return {'display': 'block'}, button_id.capitalize(), False
    else:
        return {'display': 'none'}, button_id.capitalize(), False

if __name__ == '__main__':
    app.layout = html.Div([
        dbc.Container(form(), style=SIDEBAR_STYLE),
        dbc.Container(cards(), style=CONTENT_STYLE)
    ])
    app.run(debug=True)