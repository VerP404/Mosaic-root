# app.py
from services.MosaicMed.Authentication.flask_app import flask_app
import dash
import dash_bootstrap_components as dbc

external_stylesheets = [
    dbc.themes.BOOTSTRAP,
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css",
    "/assets/styles.css"
]

app = dash.Dash(__name__,
                server=flask_app,
                url_base_pathname='/',
                external_stylesheets=external_stylesheets,
                update_title=None,
                suppress_callback_exceptions=True)

# Установка заголовка вкладки
app.title = 'МозаикаМед'
app._favicon = 'assets/img/favicon.ico'

server = app.server
