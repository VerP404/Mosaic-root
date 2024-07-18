from dash import html, Input, Output, dash_table, dcc
from app import app, engine
import dash_bootstrap_components as dbc

from callback import TableUpdater
from pages.economic_reports.new_territories.query import sql_query_new_territiries

# Отчет для сборки талонов
type_page = "new-territories-tab1"

alert_text1 = """По пациентам с адресом регистрации на новых территориях
"""

new_territories_tab1 = html.Div(
    [
        html.Div(
            [
                html.H5(
                    'Цели, количество талонов и общая сумма',
                    className='label'),
                dbc.Button(id=f'get-data-button-{type_page}', n_clicks=0, children='Получить данные'),
                dcc.Loading(id=f'loading-output-{type_page}', type='default'),
                html.Hr(),
                dbc.Alert(
                    dcc.Markdown(alert_text1),
                    color="danger",
                    style={'padding': '0'},

                ),
                html.Div(
                    [
                        dash_table.DataTable(id=f'result-table1-{type_page}',
                                             columns=[],
                                             editable=True,
                                             filter_action="native",
                                             sort_action="native",
                                             sort_mode='multi',
                                             export_format='xlsx',
                                             export_headers='display',
                                             ),
                    ], className='block', style={'width': '350px'}),
            ],
        )
    ]
)


@app.callback(
    [Output(f'result-table1-{type_page}', 'columns'),
     Output(f'result-table1-{type_page}', 'data'),
     Output(f'loading-output-{type_page}', 'children')],
    [Input(f'get-data-button-{type_page}', 'n_clicks')]
)
def update_table_dd(n_clicks):
    if n_clicks is None:
        n_clicks = 0
    if n_clicks > 0:
        # Показываем загрузку перед выполнением операции
        loading_output = html.Div([dcc.Loading(type="default")])
        columns, data = TableUpdater.query_to_df(engine, sql_query_new_territiries)
        return columns, data, loading_output
    else:
        columns, data = [], []
        loading_output = html.Div()  # Пустой контейнер для отображения после выполнения операции
    return columns, data, loading_output
