from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc
from app import app
from pages.economic_reports.reports.tab1 import tab1_layout_ec_report

type_page = "econ_reports"
# вкладки
app_tabs_econ_reports = html.Div(
    [
        html.Div(
            [
                dbc.Alert("Отчет по объемным показателям", color="primary"),
                dcc.Tabs(
                    [
                        dcc.Tab(label='Объемы', value='tab1', selected_className='custom-tab--selected'),
                        dcc.Tab(label='Финансы', value='tab2', selected_className='custom-tab--selected'),
                        dcc.Tab(label='План', value='tab3', selected_className='custom-tab--selected'),
                    ],
                    id='tabs',
                    value='tab1',
                    parent_className='custom-tabs',
                    className='custom-tabs-container',
                ),
            ], className='tabs'
        ),
        html.Div(id=f'tabs-content-{type_page}')
    ], className='tabs-app'
)


# возвращаем вкладки
@app.callback(
    Output(f'tabs-content-{type_page}', 'children'),
    [Input('tabs', 'value')]
)
def switch_tab(tab_chose):
    if tab_chose == 'tab1':
        return tab1_layout_ec_report
    elif tab_chose == 'tab2':
        return html.H2('Страница в разработке..')
    elif tab_chose == 'tab3':
        return html.H2('Страница в разработке..')
    else:
        return html.H2('Страница в разработке..')
