# app.py
import dash
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine
from database.db_settings import DATABASE_URL

app = dash.Dash(__name__,
                update_title=None,
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP])

# Установка заголовка вкладки
app.title = 'МозаикаМед'

# Подключение к базе данных
engine = create_engine(DATABASE_URL)

server = app.server
