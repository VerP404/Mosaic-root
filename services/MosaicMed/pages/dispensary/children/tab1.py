from datetime import datetime, timedelta
from dash import html, dcc, Output, Input, dash_table
from app import app, engine

from callback import get_selected_dates, TableUpdater
from pages.dispensary.children.query import sql_query_pn, sql_query_ds2, sql_query_pn_uniq

type_page = "tab1-dс"

tab1_layout_dc = html.Div(
    [
        # Блок 1: Выбор элемента из списка
        html.Div(
            [
                html.H3('Фильтры', className='label'),
                html.Div(
                    [
                        html.Div([
                            html.Label('Дата начала:', style={'width': '120px', 'display': 'inline-block'}),
                            dcc.DatePickerSingle(
                                id=f'date-picker-start-{type_page}',
                                first_day_of_week=1,
                                date=datetime.now().date() - timedelta(days=1),  # Устанавливаем начальную дату
                                display_format='DD.MM.YYYY',
                                className='filter-date'
                            ),
                        ], className='filters'),
                        html.Div([
                            html.Label('Дата окончания:', style={'width': '120px', 'display': 'inline-block'}),
                            dcc.DatePickerSingle(
                                id=f'date-picker-end-{type_page}',
                                first_day_of_week=1,
                                date=datetime.now().date() - timedelta(days=1),  # Устанавливаем конечную дату
                                display_format='DD.MM.YYYY',
                                className='filter-date'
                            ),
                        ], className='filters'),
                    ], className='filters-line'),
                html.Div(id=f'selected-spec-{type_page}', className='filters-label', style={'display': 'none'}),
                html.Div(id=f'selected-date-{type_page}', className='filters-label'),
            ], className='filter'),
        # Блок 2: Профосмотр несовершеннолетних
        html.Div(
            [
                html.H3('Профосмотр несовершеннолетних', className='label'),
                dash_table.DataTable(id=f'result-table1-{type_page}', columns=[],
                                     editable=True,
                                     export_format='xlsx',
                                     export_headers='display'),
            ], className='block'),
        # Блок 3: Диспансеризация детей сирот
        html.Div(
            [
                html.H3('Диспансеризация детей сирот', className='label'),
                dash_table.DataTable(id=f'result-table2-{type_page}', columns=[],
                                     editable=True,
                                     export_format='xlsx',
                                     export_headers='display'),
            ], className='block'),
        # Блок 4: Уникальные пациенты
        html.Div(
            [
                html.H3('Уникальные дети в оплаченных картах ПН1', className='label'),
                dash_table.DataTable(id=f'result-table3-{type_page}', columns=[],
                                     editable=True,
                                     export_format='xlsx',
                                     export_headers='display',
                                     style_table={'width': '500px'}),
            ], className='block'),
    ]
)


@app.callback(
    Output(f'selected-date-{type_page}', 'children'),
    Input(f'date-picker-start-{type_page}', 'date'),
    Input(f'date-picker-end-{type_page}', 'date')
)
def update_selected_dates(start_date, end_date):
    return get_selected_dates(start_date, end_date)


@app.callback(
    [Output(f'result-table1-{type_page}', 'columns'),
     Output(f'result-table1-{type_page}', 'data')],
    Input(f'date-picker-start-{type_page}', 'date'),
    Input(f'date-picker-end-{type_page}', 'date')
)
def update_table_dd(start_date, end_date):
    if (start_date is None) or (end_date is None):
        return [], []
    start_date_formatted = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d-%m-%Y')
    end_date_formatted = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d-%m-%Y')
    bind_params = {
        'start_date': start_date_formatted,
        'end_date': end_date_formatted
    }
    columns, data = TableUpdater.query_to_df(engine, sql_query_pn, bind_params)
    return columns, data


@app.callback(
    [Output(f'result-table2-{type_page}', 'columns'),
     Output(f'result-table2-{type_page}', 'data')],
    Input(f'date-picker-start-{type_page}', 'date'),
    Input(f'date-picker-end-{type_page}', 'date')
)
def update_table_dd(start_date, end_date):
    if (start_date is None) or (end_date is None):
        return [], []
    start_date_formatted = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d-%m-%Y')
    end_date_formatted = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d-%m-%Y')
    bind_params = {
        'start_date': start_date_formatted,
        'end_date': end_date_formatted
    }
    columns, data = TableUpdater.query_to_df(engine, sql_query_ds2, bind_params)
    return columns, data


@app.callback(
    [Output(f'result-table3-{type_page}', 'columns'),
     Output(f'result-table3-{type_page}', 'data')],
    Input(f'date-picker-start-{type_page}', 'date'),
    Input(f'date-picker-end-{type_page}', 'date')
)
def update_table_dd(start_date, end_date):
    if (start_date is None) or (end_date is None):
        return [], []
    start_date_formatted = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d-%m-%Y')
    end_date_formatted = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d-%m-%Y')
    bind_params = {
        'start_date': start_date_formatted,
        'end_date': end_date_formatted
    }
    columns, data = TableUpdater.query_to_df(engine, sql_query_pn_uniq, bind_params)
    return columns, data
