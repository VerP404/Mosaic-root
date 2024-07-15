from dash import html, dcc, Output, Input, dash_table

from database.db_conn import engine
from services.MosaicMed.app import app
from services.MosaicMed.callback.callback import get_selected_doctors, get_filter_month, TableUpdater
from services.MosaicMed.pages.doctors_talon.query import sql_query_dd_def, sql_query_amb_def, sql_query_stac_def

type_page = "tab1-doctor-talon"

tab1_doctor_talon_layout = html.Div(
    [
        # Блок 1: Выбор элемента из списка
        html.Div(
            [
                html.H3('Фильтры', className='label'),
                html.Div(
                    [
                        dcc.Dropdown(id=f'dropdown-doctor-{type_page}', options=[], placeholder='Выберите врача...'),
                    ], className='filters'),
                html.Div(
                    [
                        dcc.Dropdown(options=[
                            {'label': '01 - Январь', 'value': 1},
                            {'label': '02 - Февраль', 'value': 2},
                            {'label': '03 - Март', 'value': 3},
                            {'label': '04 - Апрель', 'value': 4},
                            {'label': '05 - Май', 'value': 5},
                            {'label': '06 - Июнь', 'value': 6},
                            {'label': '07 - Июль', 'value': 7},
                            {'label': '08 - Август', 'value': 8},
                            {'label': '09 - Сентябрь', 'value': 9},
                            {'label': '10 - Октябрь', 'value': 10},
                            {'label': '11 - Ноябрь', 'value': 11},
                            {'label': '12 - Декабрь', 'value': 12},
                            {'label': 'Нарастающе', 'value': 0}
                        ], id=f'dropdown-month-{type_page}', placeholder='Выберите месяц...'),
                    ], className='filters'),
                html.Div(id='current-month-name', className='filters-label'),
                html.Div(id=f'selected-doctor-{type_page}', className='filters-label', style={'display': 'none'}),
                html.Div(id=f'selected-month-{type_page}', className='filters-label', style={'display': 'none'}),
            ], className='filter'),
        # Блок 2: Диспансеризация
        html.Div(
            [
                html.H3('Диспансеризация', className='label'),
                dash_table.DataTable(id=f'result-table1-{type_page}', columns=[]),
            ], className='block'),
        # Блок 3: Амбулаторная помощь
        html.Div(
            [
                html.H3('Амбулаторная помощь', className='label'),
                dash_table.DataTable(id=f'result-table2-{type_page}', columns=[]),
            ], className='block'),
        # Блок 4: Стационарозамещающая помощь
        html.Div(
            [
                html.H3('Стационарозамещающая помощь', className='label'),
                dash_table.DataTable(id=f'result-table3-{type_page}', columns=[]),
            ], className='block'),
    ]
)


# выводим нужные фильтры врача и дат
@app.callback(
    [Output(f'dropdown-doctor-{type_page}', 'options'),
     Output(f'selected-doctor-{type_page}', 'children'),
     Output(f'selected-month-{type_page}', 'children')],
    Input(f'dropdown-doctor-{type_page}', 'value'),
    Input(f'dropdown-month-{type_page}', 'value'),
    Input('current-month-name', 'data')
)
def update_dropdown(selected_value, selected_month, current_month_name):
    dropdown_options, selected_item_text = get_selected_doctors(selected_value)
    selected_month_name = get_filter_month(selected_month)
    return dropdown_options, selected_item_text, selected_month_name


# Диспансеризация
@app.callback(
    [Output(f'result-table1-{type_page}', 'columns'),
     Output(f'result-table1-{type_page}', 'data')],
    Input(f'dropdown-doctor-{type_page}', 'value'),
    Input(f'dropdown-month-{type_page}', 'value'),
    Input('current-month-number', 'data'),
)
def update_table_dd(value_doctor, value_month, current_month):
    if value_doctor is None or value_month is None:
        return [], []
    sql_conditions = TableUpdater.get_sql_conditions(value_month, current_month)
    sql_query = sql_query_dd_def(sql_conditions)
    update_value_month = TableUpdater.get_sql_month(value_month)
    bind_params = {
        'value_doctor': value_doctor,
        'update_value_month': update_value_month
    }
    columns, data = TableUpdater.query_to_df(engine, sql_query, bind_params)
    return columns, data


# Амбулаторка
@app.callback(
    [Output(f'result-table2-{type_page}', 'columns'),
     Output(f'result-table2-{type_page}', 'data')],
    Input(f'dropdown-doctor-{type_page}', 'value'),
    Input(f'dropdown-month-{type_page}', 'value'),
    Input('current-month-number', 'data'),
)
def update_table_amb(value_doctor, value_month, current_month):
    if value_doctor is None or value_month is None:
        return [], []
    sql_conditions = TableUpdater.get_sql_conditions(value_month, current_month)
    sql_query = sql_query_amb_def(sql_conditions)
    update_value_month = TableUpdater.get_sql_month(value_month)
    bind_params = {
        'value_doctor': value_doctor,
        'update_value_month': update_value_month
    }
    columns, data = TableUpdater.query_to_df(engine, sql_query, bind_params)
    return columns, data


# Стационар
@app.callback(
    [Output(f'result-table3-{type_page}', 'columns'),
     Output(f'result-table3-{type_page}', 'data')],
    Input(f'dropdown-doctor-{type_page}', 'value'),
    Input(f'dropdown-month-{type_page}', 'value'),
    Input('current-month-number', 'data'),
)
def update_table_stac(value_doctor, value_month, current_month):
    if value_doctor is None or value_month is None:
        return [], []
    sql_conditions = TableUpdater.get_sql_conditions(value_month, current_month)
    sql_query = sql_query_stac_def(sql_conditions)
    update_value_month = TableUpdater.get_sql_month(value_month)
    bind_params = {
        'value_doctor': value_doctor,
        'update_value_month': update_value_month
    }
    columns, data = TableUpdater.query_to_df(engine, sql_query, bind_params)
    return columns, data
