from dash import html, dcc, Output, Input, dash_table, exceptions, State
from app import app, engine
from callback import get_current_reporting_month, TableUpdater
import datetime
import dash_bootstrap_components as dbc
from pages.economic_reports.stationary.query import sql_query_stationary

type_page = "stationary-tab1"

# Словарь для группировки статусов
status_groups = {
    'Оплаченные (3)': ['3'],
    'Предъявленные и оплаченные (2, 3)': ['2', '3'],
    'Предъявленные первичные (1, 2, 3)': ['1', '2', '3'],
    'Предъявленные первичные и повторные (1, 2, 3, 4, 6, 8)': ['1', '2', '3', '4', '6', '8'],
    'Все статусы': ['0', '1', '2', '3', '4', '5', '6', '7', '8', '12', '13', '17']
}
cel_groups = {
    'Все': ['В дневном стационаре', 'На дому'],
    'Дневные': ['В дневном стационаре'],
    'На дому': ['На дому'],
}

alert_text = """ЦАХ:
- 11136001 Сорокина Татьяна Валентиновна
- 11136003 Сорокина Татьяна Валентиновна
- 11136005 Карандеев Максим Анатольевич
- 11112018 Шадрин Илья Сергеевич
- 11112021 Асадов Кямран Аюпович
- 11112022 Малаханова Юлия Максимовна

Гинекология:
- 11136007 Столярова Тамара Владимировна
- 11136014 Войтко Валерия Александровна

"""


def date_r():
    date_start = datetime.datetime.now()
    day_list = ['01', '02', '03', '04', '05']

    date = date_start
    day_str = date.strftime("%d")
    if day_str in day_list:
        date = (date_start - datetime.timedelta(days=8))
        mon = date.strftime("%m")

    else:
        mon = date.strftime("%m")
    return mon


# Определяем текущий месяц
month = date_r()

stationary_tab1 = html.Div(

    [
        dcc.Store(id=f'current-month-number-{type_page}'),
        dcc.Store(id=f'select-month-number-start-{type_page}'),
        dcc.Store(id=f'select-month-number-end-{type_page}'),
        # Блок 1: Выбор элемента из списка
        html.Div(
            [
                html.H3('Фильтры', className='label'),
                dcc.RangeSlider(
                    id=f'month-slider-{type_page}',
                    min=1,
                    max=12,
                    step=1,
                    marks={
                        1: 'Январь',
                        2: 'Февраль',
                        3: 'Март',
                        4: 'Апрель',
                        5: 'Май',
                        6: 'Июнь',
                        7: 'Июль',
                        8: 'Август',
                        9: 'Сентябрь',
                        10: 'Октябрь',
                        11: 'Ноябрь',
                        12: 'Декабрь'
                    },
                    value=[int(month), int(month)],
                    updatemode='mouseup'
                ),
                dcc.RadioItems(
                    id=f'status-group-radio-{type_page}',
                    options=[{'label': group, 'value': group} for group in status_groups.keys()],
                    value='Предъявленные первичные и повторные (1, 2, 3, 4, 6, 8)',
                    labelStyle={'display': 'block'}
                ),
                html.H5('Тип стационара', className='label'),
                dcc.RadioItems(
                    id=f'cel-group-radio-{type_page}',
                    options=[{'label': group, 'value': group} for group in cel_groups.keys()],
                    value='Все',
                    labelStyle={'display': 'block'}
                ),
                html.Div(id=f'current-month-name-{type_page}', className='filters-label'),
                html.Div(id=f'selected-month-{type_page}', className='filters-label'),
                html.Button('Получить данные', id=f'get-data-button-{type_page}'),
                dcc.Loading(id=f'loading-output-{type_page}', type='default'),
            ], className='filter'),

        # Блок 2: Таблица
        html.Div(
            [
                html.H3('Отчет по КСГ в разбивке по корпусам', className='label'),
                dash_table.DataTable(id=f'result-table-{type_page}', columns=[],
                                     editable=True,
                                     filter_action="native",
                                     sort_action="native",
                                     sort_mode='multi',
                                     export_format='xlsx',
                                     export_headers='display',
                                     style_table={'width': '500px'}
                                     ),
            ], className='block'),
        html.Hr(),
        dbc.Alert(dcc.Markdown(alert_text), color="danger", style={'padding': '0 0 0 10px'}),
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


@app.callback(
    Output(f'selected-month-{type_page}', 'children'),
    Input(f'month-slider-{type_page}', 'value')
)
def update_selected_month(selected_months):
    start_month, end_month = selected_months
    start_month_name = {
        1: 'Январь',
        2: 'Февраль',
        3: 'Март',
        4: 'Апрель',
        5: 'Май',
        6: 'Июнь',
        7: 'Июль',
        8: 'Август',
        9: 'Сентябрь',
        10: 'Октябрь',
        11: 'Ноябрь',
        12: 'Декабрь'
    }.get(start_month, 'Неизвестно')
    end_month_name = {
        1: 'Январь',
        2: 'Февраль',
        3: 'Март',
        4: 'Апрель',
        5: 'Май',
        6: 'Июнь',
        7: 'Июль',
        8: 'Август',
        9: 'Сентябрь',
        10: 'Октябрь',
        11: 'Ноябрь',
        12: 'Декабрь'
    }.get(end_month, 'Неизвестно')
    # print(start_month, end_month)
    if start_month_name == end_month_name:
        return f'Выбранный месяц: {start_month_name}'
    else:
        return f'Выбранный месяц: с {start_month_name} по {end_month_name}'


@app.callback(
    Output(f'select-month-number-start-{type_page}', 'data'),
    Output(f'select-month-number-end-{type_page}', 'data'),
    Input(f'month-slider-{type_page}', 'value')
)
def update_selected_months_in_store(selected_months):
    return selected_months[0], selected_months[1]


@app.callback(
    [Output(f'result-table-{type_page}', 'columns'),
     Output(f'result-table-{type_page}', 'data'),
     Output(f'loading-output-{type_page}', 'children')],
    [Input(f'get-data-button-{type_page}', 'n_clicks'),  # Срабатывание по нажатию кнопки "получить данные"
     Input(f'select-month-number-start-{type_page}', 'data'),
     Input(f'select-month-number-end-{type_page}', 'data'),
     Input(f'current-month-number-{type_page}', 'data')],
    [State(f'status-group-radio-{type_page}', 'value'),
     State(f'cel-group-radio-{type_page}', 'value')]
)
def update_table(n_clicks, month_start, month_end, current_month, selected_status, selected_cel):
    if n_clicks is None:
        raise exceptions.PreventUpdate
    loading_output = html.Div([dcc.Loading(type="default")])
    selected_status_values = status_groups[selected_status]
    selected_status_tuple = tuple(selected_status_values)
    selected_cel_values = cel_groups[selected_cel]
    selected_cel_tuple = tuple(selected_cel_values)

    sql_conditions = ''
    if month_end == current_month:
        sql_conditions = 'or ("Номер счёта" is null) or ("Статус" in (\'6\', \'8\'))'
    sql_query = sql_query_stationary(sql_conditions)
    list_months = []
    for i in range(month_start, month_end + 1):
        list_months.append(TableUpdater.get_sql_month(str(i)))
    bind_params = {
        'list_months': list_months,
        'status_list': selected_status_tuple,
        'cel_list': selected_cel_tuple

    }
    columns, data = TableUpdater.query_to_df(engine, sql_query, bind_params)
    return columns, data, loading_output
