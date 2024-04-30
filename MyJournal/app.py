from dash import Dash, html, Input, Output, callback, ctx, State, MATCH, ALL
import dash_bootstrap_components as dbc

from app_style import SIDEBAR_STYLE, CONTENT_STYLE
from form import Form
from data import Data
from cards import Cards

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

cards = Cards()
form = Form()

def get_inputs():
    #Get inputs based on categories
    inputs = [Input({'type': 'category-dynamic-dropdown', 'index': MATCH}, 'value')]
    # inputs = [Input(category, 'n_clicks') for category in form.categories]
    inputs.append(Input('new category', 'n_clicks'))
    return inputs

#SAVE CLEAR
@app.callback(
    [
        Output('title-input',       'value'),
        Output('note-input',        'value'),
        Output('value-input',       'value'),
        Output('new-category',      'value'),
        Output('cards_container',   'children'),
        Output('form_container',    'children'),
        
    ],
    [
        Input('save-button',        'n_clicks'),
        Input('clear-button',       'n_clicks'),
    ],
    [
        State('title-input',        'value'),
        State('note-input',         'value'),
        State('category-dropdown',  'label'),
        State('new-category',       'value'),
        State('value-input',        'value'),
    ])
def save_clear_button(save, clear, title, note, category, new_category, metric):
    button_id = None
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id and button_id == 'save-button':
        form.new_entry('title', title)
        form.new_entry('note', note)
        if category == 'new category':
            form.new_entry(new_category.lower(), metric)
        else:
            form.new_entry(category, metric)

        #NOTE: ok to save each time ?
        form.save()

    return '', '', '', '', form.cards, form.form

#Dropdown Category
@app.callback(
        [
            Output('new-category', 'style'),
            Output('category-dropdown', 'label'),
            Output('value-input', 'disabled'),
        ],
        [
            Input({'type': 'category-dynamic-dropdown', 'index': ALL}, 'children'),
            Input('new category', 'n_clicks')
        ]
    )
def category_button(values, n_clicks):
    button_id = 'Category'
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if button_id == 'new category':
            return {'display': 'block'}, button_id, False
        
    return {'display': 'none'}, button_id, False

if __name__ == '__main__':
    app.layout = html.Div(
        [
            dbc.Container(form.form, style=SIDEBAR_STYLE, id='form_container'),
            dbc.Container(form.cards, style=CONTENT_STYLE, id='cards_container')
        ]
    )
    app.run(debug=True)