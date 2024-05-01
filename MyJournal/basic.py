from dash import Dash, html, Input, Output, callback, ctx, State, MATCH, ALL
import dash_bootstrap_components as dbc

categories = ['first']

def get_dropdown_menu_items():
        dropdown_menu_items = []
        #Get all current categories aka columns in the df. ignore date, title and note
        for category in categories:
            dropdown_menu_items.append(
                dbc.DropdownMenuItem(category.title())
            )

        return dropdown_menu_items


def category_input():
    return dbc.InputGroup(
        [
            dbc.DropdownMenu(get_dropdown_menu_items(), label='Category', color="info", id='dropdown-menu-id'),
            dbc.Input(placeholder="Value", id='input-box')
        ],
    )

def get_page():
    return [category_input(),dbc.Button('YEAH', id='save-button')]


app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# @app.callback(
#     [
#         Output('dropdown-menu-id', 'label'),
#     ],
#     [State('dropdown-menu-id', 'n_clicks')]
# )
# def dropdown_button(n_clicks):
#     return 'YEAH!'

@app.callback(
    [
        Output('the-whole-page', 'children'),
        Output('dropdown-menu-id', 'label'),
        Output('input-box', 'value')
    ],
    [Input('save-button', 'n_clicks')]
)
def save_button(n_clicks):
    button_id = 'None'
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if n_clicks:
        categories.append(str(n_clicks))
    return get_page(), len(categories), button_id

if __name__ == '__main__':
    app.layout = html.Div(get_page(), id='the-whole-page')
    app.run(debug=True, port=8051)