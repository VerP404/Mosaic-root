from dash import html, dcc, Output, Input, dash_table
from app import app, engine
from callback import get_current_reporting_month, get_filter_month, TableUpdater
from pages.dispensary.reproductive.query import sqlquery_people_reproductive_tab2

type_page = "tab2-reproductive"

tab2_reproductive = html.Div(
    [
        dcc.Store(id=f'current-month-number-{type_page}'),
        html.Div(
            [
                html.H3('Фильтры', className='label'),
                html.Div(
                    [
                        dcc.Dropdown({1: '01 - Январь', 2: '02 - Февраль', 3: '03 - Март',
                                      4: '04 - Апрель', 5: '05 - Май', 6: '06 - Июнь',
                                      7: '07 - Июль', 8: '08 - Август', 9: '09 - Сентябрь',
                                      10: '10 - Октябрь', 11: '11 - Ноябрь', 12: '12 - Декабрь', 0: 'Нарастающе'},
                                     id=f'dropdown-month-{type_page}', placeholder='Выберите месяц...'),
                    ], className='filters'),
                html.Div(id=f'current-month-name-{type_page}', className='filters-label'),
                html.Div(id=f'selected-spec-{type_page}', className='filters-label', style={'display': 'none'}),
                html.Div(id=f'selected-month-{type_page}', className='filters-label', style={'display': 'none'}),
            ], className='filter'),
        # Ж
        html.Div(
            [
                html.H3('ДР1 - женщины', className='label'),
                dash_table.DataTable(id=f'result-table1-{type_page}', columns=[]),
            ], className='block'),
        # М
        html.Div(
            [
                html.H3('ДР1 - мужчины', className='label'),
                dash_table.DataTable(id=f'result-table2-{type_page}', columns=[]),
            ], className='block'),
    ]
)


# Определяем отчетный месяц и выводим его на страницу и в переменную dcc Store
@app.callback(
    Output(f'current-month-number-{type_page}', 'data'),
    Output(f'current-month-name-{type_page}', 'children'),
    [Input('date-interval', 'n_intervals')]
)
def update_current_month(n_intervals):
    current_month_num, current_month_name = get_current_reporting_month()
    return current_month_num, current_month_name


# фильтр: по месяцам
@app.callback(
    Output(f'selected-month-{type_page}', 'children'),
    Input(f'dropdown-month-{type_page}', 'value'),
)
def update_filter(selected_month):
    return get_filter_month(selected_month)


@app.callback(
    [Output(f'result-table1-{type_page}', 'columns'),
     Output(f'result-table1-{type_page}', 'data')],
    Input(f'dropdown-month-{type_page}', 'value'),
    Input(f'current-month-number-{type_page}', 'data'),
)
def update_table(value_month, current_month):
    if value_month is None:
        return [], []
    # Если нужно добавить условия в where
    sql_conditions = TableUpdater.get_sql_conditions(value_month, current_month)
    sql_query = sqlquery_people_reproductive_tab2(sql_conditions)
    # Формируем нужный отчет в зависимости от выбранного пользователем месяца
    update_value_month = TableUpdater.get_sql_month(value_month)

    text = 'Ж'
    bind_params = {
        'text_1': text,
        'update_value_month': update_value_month,
    }
    columns, data = TableUpdater.query_to_df(engine, sql_query, bind_params)
    return columns, data


@app.callback(
    [Output(f'result-table2-{type_page}', 'columns'),
     Output(f'result-table2-{type_page}', 'data')],
    Input(f'dropdown-month-{type_page}', 'value'),
    Input(f'current-month-number-{type_page}', 'data'),
)
def update_table(value_month, current_month):
    if value_month is None:
        return [], []
    # Если нужно добавить условия в where
    sql_conditions = TableUpdater.get_sql_conditions(value_month, current_month)
    sql_query = sqlquery_people_reproductive_tab2(sql_conditions)
    # Формируем нужный отчет в зависимости от выбранного пользователем месяца
    update_value_month = TableUpdater.get_sql_month(value_month)

    text = 'М'
    bind_params = {
        'text_1': text,
        'update_value_month': update_value_month,
    }
    columns, data = TableUpdater.query_to_df(engine, sql_query, bind_params)
    return columns, data
