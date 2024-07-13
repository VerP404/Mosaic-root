from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc
from services.MosaicMed.app import app
from services.MosaicMed.pages.doctors_talon.tab1 import tab1_doctor_talon_layout

type_page = 'doctors-talon'

# вкладки
app_tabs_dtr = html.Div(
    [
        html.Div(
            [
                dbc.Alert("Отчет по врачам", color="primary"),
                dcc.Tabs(
                    [
                        dcc.Tab(label='Помесячно', value='tab1', selected_className='custom-tab--selected'),
                    ],
                    id='tabs',
                    value='tab1',
                    parent_className='custom-tabs',
                    className='custom-tabs-container',
                ),
            ], className='tabs'
        ),
        html.Div(id=f'tabs-{type_page}')
    ], className='tabs-app'
)

# возвращаем вкладки
@app.callback(
    Output(f'tabs-{type_page}', 'children'),
    [Input('tabs', 'value')]
)
def switch_tab(tab_chose):
    if tab_chose == 'tab1':
        return tab1_doctor_talon_layout
    else:
        return html.H2('Страница не выбрана..')
