from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc
from app import app
from pages.economic_reports.new_territories.tab1 import new_territories_tab1
from pages.economic_reports.new_territories.tab2 import new_territories_tab2

type_page = "new-territories"
# вкладки
new_territories = html.Div(
    [
        html.Div(
            [
                dbc.Alert("Отчеты по новым территориям", color="primary"),
                dcc.Tabs(
                    [
                        dcc.Tab(label='По адресам', value='tab1', selected_className='custom-tab--selected'),
                        dcc.Tab(label='По страховым', value='tab2',
                                selected_className='custom-tab--selected'),
                    ],
                    id='tabs',
                    value='tab1',
                    parent_className='custom-tabs',
                    className='custom-tabs-container',
                ),
            ], className='tabs'
        ),
        html.Div(id=f'tabs-content-dtr-{type_page}')
    ], className='tabs-app'
)


# возвращаем вкладки
@app.callback(
    Output(f'tabs-content-dtr-{type_page}', 'children'),
    [Input('tabs', 'value')]
)
def switch_tab(tab_chose):
    if tab_chose == 'tab1':
        return new_territories_tab1
    elif tab_chose == 'tab2':
        return new_territories_tab2
    else:
        return html.H2('Страница не выбрана..')
