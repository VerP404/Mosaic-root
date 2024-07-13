from dash import State, html, Output, Input
from datetime import datetime
import dash_bootstrap_components as dbc
from services.MosaicMed.app import app
from services.MosaicMed.components import site_mo, name_mo

year = datetime.now().year

footer_style = {
    'position': 'fixed',
    'bottom': 0,
    'margin': 0,
    'height': '30px',
    'width': '100%',
    'background-color': '#0d6efd',
    'color': 'white',
    'text-align': 'center',
    'display': 'flex',
    'justify-content': 'space-between',
}

footer_main = html.Div([
    html.Footer(children=[
        html.P(html.A("МозаикаМед", href="http://mosaicmed.ru/", style={'text-decoration': 'none', 'color': 'white'}),
               style={'margin-left': '8%'}),
        html.P(id='open-modal', children=f"© Разработка приложения Родионов Д.Н., 2023—{year}"),
        html.P(html.A(name_mo, href=site_mo,
                      style={'text-decoration': 'none', 'color': 'white'}),
               style={'margin-right': '8%'}),
    ], style=footer_style),
])

modal = html.Div([
    dbc.Modal([
        dbc.ModalBody(html.Img(src="../assets/img/contacts.jpg", style={'width': '100%'})),
        dbc.ModalFooter(
            dbc.Button("Закрыть", id="close", className="ml-auto")
        ),
    ], id="modal", is_open=False),
])

footer = html.Div([footer_main, modal])


@app.callback(
    Output("modal", "is_open"),
    [Input("open-modal", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(open_clicks, close_clicks, is_open):
    if open_clicks or close_clicks:
        return not is_open
    return is_open

