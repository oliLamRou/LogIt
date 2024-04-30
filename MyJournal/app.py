import pandas as pd

from dash import Dash, dash_table, html, dcc, Input, Output, callback, ctx, State
import dash_bootstrap_components as dbc

from app_style import SIDEBAR_STYLE, CONTENT_STYLE, FORM_STYLE, CARD_STYLE
from data import Data

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

data = Data()
df = data.df

def get_categories():
    categories = []
    for category in data.df.columns:
        if category in ['title', 'note']:
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
    note = [dcc.Markdown(f'### {note}')]

    categories = []
    for category in get_categories():
        if str(row[category]) == 'nan':
            continue

        categories.append(
            dcc.Markdown(f'- {category.title()}: {row[category]}')
        )

    metadata = [dcc.Markdown(f'###### {row.name}')]

    return dbc.CardBody(
        note + categories + metadata
    )

def card(row):
    return dbc.Card(
        [
            dbc.CardHeader(row.title),
            card_body(row)
        ]
    )

def cards():
    _cards = [dcc.Markdown('## Hello')]
    for date in df.index:
        row = df.loc[date]
        _cards.append(dbc.Container(card(row), style = CARD_STYLE))

    return _cards

def get_dropdownmenu():
    dropdownmenu = [dbc.DropdownMenuItem(category.title(), id=category) for category in get_categories()]
    dropdownmenu.append(dbc.DropdownMenuItem(divider=True))
    dropdownmenu.append(dbc.DropdownMenuItem('New Category', id='new category'))
    return dropdownmenu

def get_inputs():
    inputs = [Input(category, 'n_clicks') for category in get_categories()]
    inputs.append(Input('new category', 'n_clicks'))
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

        #Categories & Value
        dbc.InputGroup(
            [
                dbc.DropdownMenu(
                    get_dropdownmenu(),
                    label="Generate", id='dropdownmenu-label'
                ),
                dbc.Input(placeholder="new category", id='new-category'),
                dbc.Input(placeholder="Value", id='value-input')
            ],
        ),

        #Plus
        dbc.InputGroup(
            [
                dbc.Button("+", color="success", className="me-1"),
            ], 
            style = FORM_STYLE
        ),

        #Save & Clear
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
        Output('new-category', 'value'),
        Output('cards_container', 'children'),
        Output('form_container', 'children')
    ],
    [
        Input('save-button', 'n_clicks'),
        Input('clear-button', 'n_clicks'),
    ],
    [
        State('title-input', 'value'),
        State('note-input', 'value'),
        State('dropdownmenu-label', 'label'),
        State('new-category', 'value'),
        State('value-input', 'value'),
    ])
def ok_cancel_button(ok, cancel, title, note, category, new, metric):
    button_id = None
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id and button_id == 'save-button':
        data.new_entry('title', title)
        data.new_entry('note', note)
        if category == 'New Category':
            data.new_entry(new.lower(), metric)
        else:
            data.new_entry(category, metric)

        data.save()

    #Clear anyway after saving or clearing
    return '', '', '', '', cards(), form()

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

    if button_id == 'new category':
        return {'display': 'block'}, button_id.title(), False
    else:
        return {'display': 'none'}, button_id.title(), False

if __name__ == '__main__':
    app.layout = html.Div([
        dbc.Container(form(), style=SIDEBAR_STYLE, id='form_container'),
        dbc.Container(cards(), style=CONTENT_STYLE, id='cards_container')
    ])
    app.run(debug=True)