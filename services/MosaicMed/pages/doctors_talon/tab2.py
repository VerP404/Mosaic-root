from datetime import datetime, timedelta
from dash import html, dcc, Output, Input, dash_table
import dash_bootstrap_components as dbc
from database.db_conn import engine
from services.MosaicMed.app import app
from services.MosaicMed.callback.callback import get_selected_doctors, TableUpdater
from services.MosaicMed.generate_pages.filters import filter_years, filter_doctors, filter_months
from services.MosaicMed.pages.doctors_talon.query import sql_query_amb_def, sql_query_stac_def, sql_query_dd_def, sql_query_stac_date_form_def
from services.MosaicMed.utils import months_sql_labels

type_page = "tab2-doctor-talon"

tab2_doctor_talon_layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            dbc.CardHeader("Фильтры"),
                            dbc.Row(
                                [
                                    filter_doctors(type_page),  # фильтр по врачам
                                    filter_years(type_page)  # фильтр по годам
                                ]
                            ),
                            dbc.Row(
                                [
                                    filter_months(type_page)  # фильтр по месяцам
                                ]
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Div([
                                            dcc.RadioItems(
                                                id=f'date-type-{type_page}',
                                                options=[
                                                    {"label": "По дате лечения", "value": "treatment"},
                                                    {"label": "По дате формирования", "value": "formation"}
                                                ],
                                                value='treatment',
                                            )
                                        ]),
                                        width=2
                                    ),
                                    dbc.Col(
                                        html.Div([
                                            html.Label('Начало:', style={'width': '120px', 'display': 'inline-block'}),
                                            dcc.DatePickerSingle(
                                                id=f'date-picker-start-{type_page}',
                                                first_day_of_week=1,
                                                date=(datetime.now() - timedelta(days=1)).date(),
                                                display_format='DD.MM.YYYY',
                                                className='filter-date'
                                            ),
                                        ], className='filters'),
                                        width=3
                                    ),
                                    dbc.Col(
                                        html.Div([
                                            html.Label('Окончание:', style={'width': '120px', 'display': 'inline-block'}),
                                            dcc.DatePickerSingle(
                                                id=f'date-picker-end-{type_page}',
                                                first_day_of_week=1,
                                                date=(datetime.now() - timedelta(days=1)).date(),
                                                display_format='DD.MM.YYYY',
                                                className='filter-date'
                                            ),
                                        ], className='filters'),
                                        width=4
                                    )
                                ]
                            ),
                            html.Div(id=f'selected-doctor-{type_page}', className='filters-label', style={'display': 'none'}),
                            html.Div(id=f'selected-period-{type_page}', className='filters-label', style={'display': 'none'}),
                        ]
                    ),
                    style={"width": "100%", "padding": "0rem", "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)", "border-radius": "10px"}
                ),
                width=12
            ),
            style={"margin": "0 auto", "padding": "0rem"}
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            dbc.CardHeader("Амбулаторная помощь"),
                            html.Div(
                                dash_table.DataTable(
                                    id=f'result-table1-{type_page}',
                                    style_table={'overflowX': 'auto'},
                                    style_cell={'minWidth': '0px', 'maxWidth': '180px', 'whiteSpace': 'normal'}
                                ),
                                style={"maxWidth": "100%", "overflowX": "auto"}
                            )
                        ]
                    ),
                    style={"width": "100%", "padding": "0rem", "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)", "border-radius": "10px"}
                ),
                width=12
            ),
            style={"margin": "0 auto", "padding": "0rem"}
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            dbc.CardHeader("Диспансеризация"),
                            html.Div(
                                dash_table.DataTable(
                                    id=f'result-table2-{type_page}',
                                    style_table={'overflowX': 'auto'},
                                    style_cell={'minWidth': '0px', 'maxWidth': '180px', 'whiteSpace': 'normal'}
                                ),
                                style={"maxWidth": "100%", "overflowX": "auto"}
                            )
                        ]
                    ),
                    style={"width": "100%", "padding": "0rem", "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)", "border-radius": "10px"}
                ),
                width=12
            ),
            style={"margin": "0 auto", "padding": "0rem"}
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            dbc.CardHeader("Стационары"),
                            html.Div(
                                dash_table.DataTable(
                                    id=f'result-table3-{type_page}',
                                    style_table={'overflowX': 'auto'},
                                    style_cell={'minWidth': '0px', 'maxWidth': '180px', 'whiteSpace': 'normal'}
                                ),
                                style={"maxWidth": "100%", "overflowX": "auto"}
                            )
                        ]
                    ),
                    style={"width": "100%", "padding": "0rem", "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)", "border-radius": "10px"}
                ),
                width=12
            ),
            style={"margin": "0 auto", "padding": "0rem"}
        ),
    ],
    style={"padding": "0rem"}
)

@app.callback(
    [Output(f'dropdown-doctor-{type_page}', 'options'),
     Output(f'selected-doctor-{type_page}', 'children'),
     Output(f'selected-period-{type_page}', 'children')],
    [Input(f'dropdown-doctor-{type_page}', 'value'),
     Input(f'range-slider-month-{type_page}', 'value'),
     Input(f'dropdown-year-{type_page}', 'value'),
     Input(f'date-picker-start-{type_page}', 'date'),
     Input(f'date-picker-end-{type_page}', 'date'),
     Input(f'date-type-{type_page}', 'value')]
)
def update_dropdown(selected_doctor, selected_months_range, selected_year, start_date, end_date, date_type):
    dropdown_options, selected_item_text = get_selected_doctors(selected_doctor)

    if selected_months_range and selected_year:
        selected_period = [f"{months_sql_labels[i]} {selected_year}" for i in range(selected_months_range[0], selected_months_range[1] + 1)]
    else:
        selected_period = []

    selected_dates = f"с {start_date} по {end_date}" if start_date and end_date else ""

    return dropdown_options, selected_item_text, selected_period

@app.callback(
    [Output(f'result-table1-{type_page}', 'columns'),
     Output(f'result-table1-{type_page}', 'data'),
     Output(f'result-table2-{type_page}', 'columns'),
     Output(f'result-table2-{type_page}', 'data'),
     Output(f'result-table3-{type_page}', 'columns'),
     Output(f'result-table3-{type_page}', 'data')],
    [Input(f'dropdown-doctor-{type_page}', 'value'),
     Input(f'selected-period-{type_page}', 'children'),
     Input(f'date-picker-start-{type_page}', 'date'),
     Input(f'date-picker-end-{type_page}', 'date'),
     Input(f'date-type-{type_page}', 'value')]
)
def update_table_dd(value_doctor, selected_period, start_date, end_date, date_type):
    if value_doctor is None or not selected_period:
        return [], [], [], [], [], []

    months_placeholder = ', '.join([f"'{month}'" for month in selected_period])
    bind_params = {
        'value_doctor': value_doctor,
        'start_date': start_date,
        'end_date': end_date,
        'date_type': date_type
    }

    columns1, data1 = TableUpdater.query_to_df(engine, sql_query_amb_def(months_placeholder), bind_params)
    columns2, data2 = TableUpdater.query_to_df(engine, sql_query_dd_def(months_placeholder), bind_params)
    columns3, data3 = TableUpdater.query_to_df(engine, sql_query_stac_def(months_placeholder), bind_params)

    return columns1, data1, columns2, data2, columns3, data3

@app.callback(
    [Output(f'result-table3-{type_page}', 'columns'),
     Output(f'result-table3-{type_page}', 'data')],
    [Input(f'dropdown-doctor-{type_page}', 'value'),
     Input(f'date-picker-start-{type_page}', 'date'),
     Input(f'date-picker-end-{type_page}', 'date')]
)
def update_table_dd_with_dates(value_doctor, start_date, end_date):
    if value_doctor is None or start_date is None or end_date is None:
        return [], []

    # запрос для формирования отчета
    sql_query = sql_query_stac_date_form_def()
    start_date_formatted = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d-%m-%Y')
    end_date_formatted = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d-%m-%Y')
    bind_params = {
        'value_doctor': value_doctor,
        'start_date': start_date_formatted,
        'end_date': end_date_formatted
    }
    columns, data = TableUpdater.query_to_df(engine, sql_query, bind_params)
    return columns, data
