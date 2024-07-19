from dash import html, dcc, Output, Input, dash_table, exceptions, State
import dash_bootstrap_components as dbc
from database.db_conn import engine
from services.MosaicMed.app import app
from services.MosaicMed.callback.callback import TableUpdater, get_current_reporting_month
from services.MosaicMed.callback.slider_months import get_selected_period
from services.MosaicMed.generate_pages.elements import card_table
from services.MosaicMed.generate_pages.filters import filter_years, filter_months, filter_status
from services.MosaicMed.pages.doctors_talon.doctors_list.query import sql_query_by_doc
from services.MosaicMed.generate_pages.constants import status_groups, months_labels, months_sql_labels
from services.MosaicMed.pages.economic_reports.by_doctors_dispensary.query import \
    sql_query_by_doctor_dispensary_adult_f1, sql_query_by_doctor_dispensary_adult_f2, \
    sql_query_by_doctor_dispensary_adult_f3, sql_query_by_doctor_dispensary_children_f3, \
    sql_query_by_doctor_dispensary_children_f2, sql_query_by_doctor_dispensary_children_f1
from services.MosaicMed.pages.economic_reports.sv_pod.query import sql_qery_sv_pod

type_page = "by-doctor-dispensary-children"

tab2_layout_by_doctor_dispensary = html.Div(
    [
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            dbc.CardHeader("Фильтры"),
                            dbc.Row(
                                [
                                    filter_status(type_page),  # фильтр по статусам
                                    filter_years(type_page)  # фильтр по годам
                                ]
                            ),
                            dbc.Row(
                                [
                                    filter_months(type_page)  # фильтр по месяцам
                                ]
                            ),
                            html.Div(id=f'selected-doctor-{type_page}', className='filters-label',
                                     style={'display': 'none'}),
                            html.Div(id=f'selected-period-{type_page}', className='filters-label',
                                     style={'display': 'none'}),
                            html.Div(id=f'current-month-name-{type_page}', className='filters-label'),
                            html.Div(id=f'selected-month-{type_page}', className='filters-label'),
                            html.Button('Получить данные', id=f'get-data-button-{type_page}'),
                            dcc.Loading(id=f'loading-output-{type_page}', type='default'),
                        ]
                    ),
                    style={"width": "100%", "padding": "0rem", "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)",
                           "border-radius": "10px"}
                ),
                width=12
            ),
            style={"margin": "0 auto", "padding": "0rem"}
        ),
        card_table(f'result-table1-{type_page}', "Форма 1: по врачам, закрывшим карту"),
        card_table(f'result-table2-{type_page}', "Форма 2: по услугам"),
        card_table(f'result-table3-{type_page}', "Форма 3: по врачам в услугах"),
    ],
    style={"padding": "0rem"}
)


# Определяем отчетный месяц и выводим его на страницу и в переменную dcc Store
@app.callback(
    Output(f'current-month-name-{type_page}', 'children'),
    Input('date-interval', 'n_intervals')
)
def update_current_month(n_intervals):
    current_month_num, current_month_name = get_current_reporting_month()
    return current_month_name


@app.callback(
    Output(f'selected-month-{type_page}', 'children'),
    Input(f'range-slider-month-{type_page}', 'value')
)
def update_selected_month(selected_months):
    if selected_months is None:
        return "Выбранный месяц: Не выбран"

    start_month, end_month = selected_months
    start_month_name = months_labels.get(start_month, 'Неизвестно')
    end_month_name = months_labels.get(end_month, 'Неизвестно')
    if start_month_name == end_month_name:
        return f'Выбранный месяц: {start_month_name}'
    else:
        return f'Выбранный месяц: с {start_month_name} по {end_month_name}'


@app.callback(
    Output(f'selected-period-{type_page}', 'children'),
    [Input(f'range-slider-month-{type_page}', 'value'),
     Input(f'dropdown-year-{type_page}', 'value'),
     Input(f'current-month-name-{type_page}', 'children')]
)
def update_selected_period_list(selected_months_range, selected_year, current_month_name):
    return get_selected_period(selected_months_range, selected_year, current_month_name)


@app.callback(
    [Output(f'result-table1-{type_page}', 'columns'),
     Output(f'result-table1-{type_page}', 'data'),
     Output(f'result-table2-{type_page}', 'columns'),
     Output(f'result-table2-{type_page}', 'data'),
     Output(f'result-table3-{type_page}', 'columns'),
     Output(f'result-table3-{type_page}', 'data'),
     Output(f'loading-output-{type_page}', 'children')],
    [Input(f'get-data-button-{type_page}', 'n_clicks'),
     State(f'selected-period-{type_page}', 'children'),
     State(f'status-group-radio-{type_page}', 'value')]
)
def update_table(n_clicks, selected_period, selected_status):
    if n_clicks is None or not selected_period or not selected_status:
        raise exceptions.PreventUpdate

    loading_output = html.Div([dcc.Loading(type="default")])
    selected_status_values = status_groups[selected_status]
    selected_status_tuple = tuple(selected_status_values)

    sql_cond = ', '.join([f"'{period}'" for period in selected_period])

    bind_params = {
        'status_list': selected_status_tuple
    }
    columns1, data1 = TableUpdater.query_to_df(engine, sql_query_by_doctor_dispensary_children_f1(sql_cond), bind_params)
    columns2, data2 = TableUpdater.query_to_df(engine, sql_query_by_doctor_dispensary_children_f2(sql_cond), bind_params)
    columns3, data3 = TableUpdater.query_to_df(engine, sql_query_by_doctor_dispensary_children_f3(sql_cond), bind_params)
    return columns1, data2, columns2, data2, columns3, data3, loading_output
