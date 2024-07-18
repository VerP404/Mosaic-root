from dash import dcc
import dash_bootstrap_components as dbc

from services.MosaicMed.utils import current_year, months_labels


def filter_years(type_page):
    return (
        dbc.Col(
            dcc.Dropdown(options=[
                {'label': '2023', 'value': 2023},
                {'label': '2024', 'value': 2024},
                {'label': '2025', 'value': 2025}
            ], id=f'dropdown-year-{type_page}', placeholder='Выберите год...',
                value=current_year)
        ))


def filter_doctors(type_page):
    return (dbc.Col(
        dcc.Dropdown(id=f'dropdown-doctor-{type_page}', options=[],
                     placeholder='Выберите врача...')
    ))


def filter_months(type_page):
    return (
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
    )
