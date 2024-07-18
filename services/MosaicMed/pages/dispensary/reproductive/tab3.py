from dash import html, Input, Output, dash_table, dcc
from app import app, engine
import dash_bootstrap_components as dbc

from callback import TableUpdater
from pages.dispensary.reproductive.query import sqlquery_people_reproductive_tab3

type_page = "tab3-reproductive"

tab3_reproductive = html.Div(
    [
        html.Div(
            [
                html.H5(
                    'Пациенты прошедшие ДВ4 или ОПВ (по оплаченным) в текущем году с отметкой о прохождении ДР1 (все статусы).',
                    className='label'),
                dbc.Button(id=f'get-data-button-{type_page}', n_clicks=0, children='Получить данные'),
                dcc.Loading(id=f'loading-output-{type_page}', type='default'),
                html.Hr(),
                html.Div(
                    [
                        dash_table.DataTable(id=f'result-table1-{type_page}',
                                             columns=[],
                                             editable=False,
                                             filter_action="native",
                                             sort_action="native",
                                             sort_mode='multi',
                                             export_format='xlsx',
                                             export_headers='display',
                                             ),
                    ], className='block'),
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
        columns, data = TableUpdater.query_to_df(engine, sqlquery_people_reproductive_tab3)
        return columns, data, loading_output
    else:
        columns, data = [], []
        loading_output = html.Div()  # Пустой контейнер для отображения после выполнения операции
    return columns, data, loading_output
