from dash import Dash, html, Input, Patch
import dash_bootstrap_components as dbc

from app_style import FORM_STYLE
from data import Data
from cards import Cards

class Form(Cards):

    new_category_label = 'new category'

    def __init__(self):
        super().__init__()

    @property
    def title_input(self):
        return dbc.InputGroup(
            [
                dbc.Input(placeholder="Title", id='title-id')
            ],
            className="mb-1",
        )

    @property
    def note_input(self):
        return dbc.InputGroup(
            [
                dbc.Textarea(placeholder="Note", id='note-id')
            ],
            className="mb-1",
        )

    @property
    def select_options(self):
        options = []
        for category in self.categories:
            options.append({"label": category.title(), "value": category})

        options.append({"label": self.new_category_label.title(), "value": self.new_category_label})
        return options

    @property
    def category_input(self):
        return dbc.InputGroup(
            [
                dbc.Select(
                    options=self.select_options,
                    id='select-category-id',
                    value=self.new_category_label
                ),
                dbc.Input(placeholder="Category", id='new-category-id'),
                dbc.Input(placeholder="Value", id='value-id')
            ],
            className="mb-1",
        )

    @property
    def save_clear_button(self):
        return dbc.InputGroup(
                [
                    dbc.Button("Save", color="success", id='save-button-id'),
                    dbc.Button("Clear", color="dark", id='clear-button-id'),
                ],
                style = FORM_STYLE
            )

    @property
    def form(self):
        return html.Div(
            [
                self.title_input,
                self.note_input,
                self.category_input,
                self.save_clear_button
            ]
        )

if __name__ == '__main__':
    f = Form()
    print(f.form)





