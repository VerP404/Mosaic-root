# dashboard.py
from services.MosaicMed.flaskapp.flask_app import flask_app
import dash
import dash_bootstrap_components as dbc

external_stylesheets = [
    # dbc.themes.BOOTSTRAP,
    "/assets/css/bootstrap.min.css",  # Локальный Bootstrap CSS
    "/assets/css/styles.css",  # Ваши собственные стили
    "/assets/css/fontawesome/all.css"  # Локальный Font Awesome CSS
]

app = dash.Dash(__name__,
                server=flask_app,
                url_base_pathname='/',
                external_stylesheets=external_stylesheets,
                update_title=None,
                suppress_callback_exceptions=True)

# Установка заголовка вкладки
app.title = 'МозаикаМед'
app._favicon = 'assets/img/favicon.ico'  # Локальный favicon

server = app.server
