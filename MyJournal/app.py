from dash import Dash, html, Input, Output, callback, ctx, State, MATCH, ALL
import dash_bootstrap_components as dbc

from app_style import SIDEBAR_STYLE, CONTENT_STYLE
from form import Form
from data import Data
from cards import Cards

app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

form = Form()

#SAVE CLEAR
@app.callback(
    [
        Output('cards_container-id', 'children'),
        Output('form_container-id', 'children')
    ],
    [
        Input('save-button-id', 'n_clicks'),
        Input('clear-button-id', 'n_clicks'),
    ],
    [
        State('title-id', 'value'),
        State('note-id', 'value'),
        State('select-category-id', 'value'),
        State('new-category-id', 'value'),
        State('value-id', 'value'),
    ])
def save_clear_button(save, clear, title, note, selected_category, new_category, value):
    category_value = new_category if selected_category == 'new category' else selected_category

    if ctx.triggered_id == 'save-button-id':
        form.new_entry('title', title)
        form.new_entry('note', note)
        form.new_entry(category_value, value)

    return form.cards, form.form

#Category Select
@app.callback(
        Output('new-category-id', 'style'),
        Input('select-category-id', 'value')
    )
def select_category_options(value):
    if value == 'new category':
        return {'display': 'block'}
        
    return {'display': 'none'}

if __name__ == '__main__':
    app.layout = html.Div(
        [
            dbc.Container(form.form, style=SIDEBAR_STYLE, id='form_container-id'),
            dbc.Container(form.cards, style=CONTENT_STYLE, id='cards_container-id')
        ]
    )
    app.run(debug=True)