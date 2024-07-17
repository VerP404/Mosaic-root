from dash import html, dcc, Output, Input, dash_table
from datetime import datetime
import dash_bootstrap_components as dbc
from database.db_conn import engine
from services.MosaicMed.app import app
from services.MosaicMed.callback.callback import get_selected_doctors, TableUpdater
from services.MosaicMed.pages.doctors_talon.query import sql_query_amb_def

type_page = "tab1-doctor-talon"

current_year = datetime.now().year

months_labels = {
    1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь', 7: 'Июль',
    8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
}

months_sql_labels = {
    1: 'Января', 2: 'Февраля', 3: 'Марта', 4: 'Апреля', 5: 'Мая', 6: 'Июня', 7: 'Июля',
    8: 'Августа', 9: 'Сентября', 10: 'Октября', 11: 'Ноября', 12: 'Декабря'
}

tab1_doctor_talon_layout = html.Div(
    [
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2("Фильтры", className="card-title mb-4"),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dcc.Dropdown(id=f'dropdown-doctor-{type_page}', options=[], placeholder='Выберите врача...')
                                    ),
                                    dbc.Col(
                                        dcc.Dropdown(options=[
                                            {'label': '2023', 'value': 2023},
                                            {'label': '2024', 'value': 2024},
                                            {'label': '2025', 'value': 2025}
                                        ], id=f'dropdown-year-{type_page}', placeholder='Выберите год...', value=current_year)
                                    )
                                ]
                            ),
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dcc.RangeSlider(
                                            id=f'range-slider-month-{type_page}',
                                            min=1,
                                            max=12,
                                            marks={i: month for i, month in months_labels.items()},
                                            value=[1, 12],
                                            step=1
                                        )
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
                            html.H2("Амбулаторная помощь", className="card-title mb-4"),
                            html.Div(
                                dash_table.DataTable(
                                    id=f'result-table2-{type_page}',
                                    style_table={'overflowX': 'auto'},
                                    style_cell={'minWidth': '0px', 'maxWidth': '180px', 'whiteSpace': 'normal'}  # Ограничение ширины ячеек
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
        )
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
    [Output(f'result-table2-{type_page}', 'columns'),
     Output(f'result-table2-{type_page}', 'data')],
    [Input(f'dropdown-doctor-{type_page}', 'value'),
     Input(f'selected-period-{type_page}', 'children')]
)
def update_table_amb(value_doctor, selected_period):
    if value_doctor is None or not selected_period:
        return [], []

    months_placeholder = ', '.join([f"'{month}'" for month in selected_period])
    sql_query = sql_query_amb_def(months_placeholder)
    bind_params = {
        'value_doctor': value_doctor
    }

    columns, data = TableUpdater.query_to_df(engine, sql_query, bind_params)
    return columns, data
