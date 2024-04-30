from dash import Dash, html, Input, Patch
import dash_bootstrap_components as dbc

from app_style import FORM_STYLE
from data import Data
from cards import Cards

class Form(Cards):
    def __init__(self):
        super().__init__()

        #Data
        self._dropdown_menu_items = None

        #Form elements
        self._save_clear_button = None

        self._form = None

        self.dropdown_categories_list = None
        self.set_dropdown_categories_list()

    def set_dropdown_categories_list(self):
        self.dropdown_categories_list = [Input(category, 'n_clicks') for category in self.categories]
        self.dropdown_categories_list.append(Input('new category', 'n_clicks'))

    @property
    def dropdown_menu_items(self):
        self._dropdown_menu_items = Patch()
        #Get all current categories aka columns in the df. ignore date, title and note
        for category in self.categories:
            self._dropdown_menu_items.append(
                dbc.DropdownMenuItem(category.title(), id=category)
            )
        # self._dropdown_menu_items = [dbc.DropdownMenuItem(category.title(), id=category) for category in self.categories]
        
        #Seperator
        self._dropdown_menu_items.append(dbc.DropdownMenuItem(divider=True))
        
        #New Category button
        self._dropdown_menu_items.append(dbc.DropdownMenuItem('New Category', id='new category'))

        return self._dropdown_menu_items

    @property
    def title_input(self):
        return dbc.InputGroup(
            [
                dbc.Input(placeholder="Title", id='title-input')
            ]
        )

    @property
    def note_input(self):
        return dbc.InputGroup(
            [
                dbc.Textarea(placeholder="Note", id='note-input')
            ]
        )

    @property
    def category_dropdown(self):
        return 

    @property
    def category_input(self):
        return dbc.InputGroup(
                [
                    dbc.DropdownMenu(
                        children=self.dropdown_menu_items, 
                        label='Category', 
                        id='category-dynamic-dropdown', 
                        color="info"
                    ),
                    dbc.Input(placeholder="new category", id='new-category'),
                    dbc.Input(placeholder="Value", id='value-input')
                ],
            )

    @property
    def save_clear_button(self):
        self._save_clear_button = dbc.InputGroup(
                [
                    dbc.Button("Save", color="success", id='save-button'),
                    dbc.Button("Clear", color="dark", id='clear-button'),
                ],
                style = FORM_STYLE
            )

        return self._save_clear_button

    @property
    def form(self):
        self._form = html.Div(
            [
                self.title_input,
                self.note_input,
                self.category_input,
                self.save_clear_button
            ]
        )
        return self._form

if __name__ == '__main__':
    f = Form()
    print(f.form)





