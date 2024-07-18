from dash import html, dcc, Output, Input, dash_table
from app import app, engine
from callback import get_current_reporting_month, get_filter_month, TableUpdater

from pages.dispensary.children.query import sql_query_pn_uniq_tab2

type_page = "tab2-dc"

tab2_layout_dc = html.Div(
    [
        dcc.Store(id=f'current-month-number-{type_page}'),
        # Блок 1: Выбор элемента из списка
        html.Div(
            [
                html.H3('Фильтры', className='label'),
                html.Div(
                    [
                        dcc.Dropdown({1: '01 - Январь', 2: '02 - Февраль', 3: '03 - Март',
                                      4: '04 - Апрель', 5: '05 - Май', 6: '06 - Июнь',
                                      7: '07 - Июль', 8: '08 - Август', 9: '09 - Сентябрь',
                                      10: '10 - Октябрь', 11: '11 - Ноябрь', 12: '12 - Декабрь'},
                                     id=f'dropdown-month-{type_page}', placeholder='Выберите месяц...'),
                    ], className='filters'),
                html.Div(id=f'current-month-name-{type_page}', className='filters-label'),
                html.Div(id=f'selected-month-{type_page}', className='filters-label', style={'display': 'none'}),
            ], className='filter'),
        # Блок 2: Таблица с БСК
        html.Div(
            [
                html.H3('Талоны и уникальные пациенты в текущем году', className='label'),
                dash_table.DataTable(id=f'result-table1-{type_page}', columns=[],
                                     editable=True,
                                     export_format='xlsx',
                                     export_headers='display'),
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
    Input(f'dropdown-month-{type_page}', 'value')
)
def update_table(value_month):
    if value_month is None:
        return [], []
    if value_month in ("10", "11", "12"):
        value_month = f'%/{value_month}/%'
    else:
        value_month = f'%/0{value_month}/%'
    bind_params = {
        'month': value_month,
    }
    columns, data = TableUpdater.query_to_df(engine, sql_query_pn_uniq_tab2, bind_params)

    return columns, data
