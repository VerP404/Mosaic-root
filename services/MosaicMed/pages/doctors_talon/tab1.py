from dash import html, dcc, Output, Input, dash_table
from datetime import datetime
from database.db_conn import engine
from services.MosaicMed.app import app
from services.MosaicMed.callback.callback import get_selected_doctors, TableUpdater
from services.MosaicMed.pages.doctors_talon.query import sql_query_amb_def

type_page = "tab1-doctor-talon"

months_labels = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября',
                 'Ноября', 'Декабря']

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
                            {'label': '2023', 'value': 2023},
                            {'label': '2024', 'value': 2024},
                            {'label': '2025', 'value': 2025}
                        ], id=f'dropdown-year-{type_page}', placeholder='Выберите год...'),
                    ], className='filters'),
                html.Div(
                    [
                        dcc.RangeSlider(
                            id=f'range-slider-month-{type_page}',
                            min=1,
                            max=12,
                            marks={i + 1: month for i, month in enumerate(months_labels)},
                            value=[1, 12],
                            step=1
                        ),
                    ], className='filters'),
                html.Div(id=f'selected-doctor-{type_page}', className='filters-label', style={'display': 'none'}),
                html.Div(id=f'selected-period-{type_page}', className='filters-label', style={'display': 'none'}),
            ], className='filter'),
        # Блок 2: Амбулаторная помощь
        html.Div(
            [
                html.H3('Амбулаторная помощь', className='label'),
                dash_table.DataTable(id=f'result-table2-{type_page}', columns=[]),
            ], className='block'),
    ]
)


# выводим нужные фильтры врача и дат
@app.callback(
    [Output(f'dropdown-doctor-{type_page}', 'options'),
     Output(f'selected-doctor-{type_page}', 'children'),
     Output(f'selected-period-{type_page}', 'children')],
    Input(f'dropdown-doctor-{type_page}', 'value'),
    Input(f'range-slider-month-{type_page}', 'value'),
    Input(f'dropdown-year-{type_page}', 'value')
)
def update_dropdown(selected_doctor, selected_months_range, selected_year):
    dropdown_options, selected_item_text = get_selected_doctors(selected_doctor)

    if selected_months_range and selected_year:
        selected_period = [f"{months_labels[i - 1]} {selected_year}" for i in
                           range(selected_months_range[0], selected_months_range[1] + 1)]
    else:
        selected_period = []

    return dropdown_options, selected_item_text, selected_period


# Амбулаторка
@app.callback(
    [Output(f'result-table2-{type_page}', 'columns'),
     Output(f'result-table2-{type_page}', 'data')],
    Input(f'dropdown-doctor-{type_page}', 'value'),
    Input(f'selected-period-{type_page}', 'children')
)
def update_table_amb(value_doctor, selected_period):
    if value_doctor is None or not selected_period:
        return [], []

    sql_query = sql_query_amb_def()
    bind_params = {
        'value_doctor': value_doctor,
        'months': tuple(selected_period)  # Преобразуем список в кортеж для использования в SQL
    }

    columns, data = TableUpdater.query_to_df(engine, sql_query, bind_params)
    return columns, data

