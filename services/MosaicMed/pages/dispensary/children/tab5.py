import dash_bootstrap_components as dbc
from dash import html, dcc, Output, Input, dash_table
from app import app, engine
from callback import TableUpdater
from pages.dispensary.children.query import  query_download_children_list_not_pn1

type_page = "children_list_not_pn"

tab5_layout_children_list_not_pn = html.Div(
    [
        html.Div(
            [
                html.H3('Список прикрепленных детей без профилактического осмотра (ПН1)', className='label'),
                dbc.Button(id=f'get-data-button-{type_page}', n_clicks=0, children='Получить данные'),
                dash_table.DataTable(id=f'result-table-{type_page}',
                                     columns=[],
                                     page_size=15,
                                     editable=True,
                                     filter_action="native",
                                     sort_action="native",
                                     sort_mode='multi',
                                     export_format='xlsx',
                                     export_headers='display',
                                     ),
            ], className='block'),
    ]
)


@app.callback(
    [Output(f'result-table-{type_page}', 'columns'),
     Output(f'result-table-{type_page}', 'data')],
    [Input(f'get-data-button-{type_page}', 'n_clicks')]
)
def update_table_dd(n_clicks):
    if n_clicks is None:
        n_clicks = 0

    if n_clicks > 0:
        columns, data = TableUpdater.query_to_df(engine, query_download_children_list_not_pn1)
    else:
        columns, data = [], []

    return columns, data
