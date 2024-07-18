from dash import html, Output, Input, dash_table
import dash_bootstrap_components as dbc
from database.db_conn import engine
from services.MosaicMed.app import app
from services.MosaicMed.callback.callback import get_selected_doctors, TableUpdater
from services.MosaicMed.generate_pages.filters import filter_years, filter_doctors, filter_months
from services.MosaicMed.pages.doctors_talon.query import sql_query_amb_def, sql_query_stac_def, sql_query_dd_def
from services.MosaicMed.utils import months_sql_labels

type_page = "tab1-doctor-talon"

tab1_doctor_talon_layout = html.Div(
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
                            html.Div(id=f'selected-doctor-{type_page}', className='filters-label',
                                     style={'display': 'none'}),
                            html.Div(id=f'selected-period-{type_page}', className='filters-label',
                                     style={'display': 'none'}),
                        ]
                    ),
                    style={"width": "100%", "padding": "0rem", "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)",
                           "border-radius": "10px"}
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
                    style={"width": "100%", "padding": "0rem", "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)",
                           "border-radius": "10px"}
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
                    style={"width": "100%", "padding": "0rem", "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)",
                           "border-radius": "10px"}
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
                    style={"width": "100%", "padding": "0rem", "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)",
                           "border-radius": "10px"}
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
     Input(f'dropdown-year-{type_page}', 'value')]
)
def update_dropdown(selected_doctor, selected_months_range, selected_year):
    dropdown_options, selected_item_text = get_selected_doctors(selected_doctor)

    if selected_months_range and selected_year:
        selected_period = [f"{months_sql_labels[i]} {selected_year}" for i in
                           range(selected_months_range[0], selected_months_range[1] + 1)]
    else:
        selected_period = []

    return dropdown_options, selected_item_text, selected_period


@app.callback(
    [Output(f'result-table1-{type_page}', 'columns'),
     Output(f'result-table1-{type_page}', 'data'),
     Output(f'result-table2-{type_page}', 'columns'),
     Output(f'result-table2-{type_page}', 'data'),
     Output(f'result-table3-{type_page}', 'columns'),
     Output(f'result-table3-{type_page}', 'data')
     ],
    [Input(f'dropdown-doctor-{type_page}', 'value'),
     Input(f'selected-period-{type_page}', 'children')]
)
def update_table_dd(value_doctor, selected_period):
    if value_doctor is None or not selected_period:
        return [], [], [], [], [], []

    months_placeholder = ', '.join([f"'{month}'" for month in selected_period])
    bind_params = {
        'value_doctor': value_doctor
    }
    columns1, data1 = TableUpdater.query_to_df(engine, sql_query_amb_def(months_placeholder), bind_params)
    columns2, data2 = TableUpdater.query_to_df(engine, sql_query_dd_def(months_placeholder), bind_params)
    columns3, data3 = TableUpdater.query_to_df(engine, sql_query_stac_def(months_placeholder), bind_params)

    return columns1, data1, columns2, data2, columns3, data3
