# MosaicDashboard/app.py

from datetime import datetime

import dash
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine

from MosaicDashboard import main_color
from db_setup.db_settings import DATABASE_URL
from MosaicDashboard.components.header import header
from MosaicDashboard.components.footer import footer
from MosaicDashboard.components.content import content
from dash import dcc, html, Output, Input

# Создание приложения Dash
app = dash.Dash(__name__,
                update_title=None,
                suppress_callback_exceptions=True,
                external_stylesheets=[dbc.themes.BOOTSTRAP,
                                      'assets/css/styles.css',
                                      'assets/css/card.css',
                                      ])

# Установка заголовка вкладки
app.title = 'МозаикаДашборд'

# Подключение к базе данных
engine = create_engine(DATABASE_URL)

server = app.server

# Установка layout приложения
app.layout = html.Div(
    [
        dcc.Location(id="url"),
        header,
        html.Div([
            content
        ], style={"position": "relative", "minHeight": "calc(100vh - 120px)"}),  # Учитываем высоту хедера и футера
        footer
    ],
    style={"backgroundColor": main_color, "height": "100vh", "overflow": "hidden"}
)


# Callback для обновления времени
@app.callback(Output('live-time', 'children'),
              Input('interval-component', 'n_intervals'))
def update_time(n):
    return datetime.now().strftime("%d-%m-%Y %H:%M")



if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0', port='8070')
