from dash import Input, Output, dcc, html, State
from services.MosaicMed.app import app
from services.MosaicMed.callback.date_reports import get_current_reporting_month
from services.MosaicMed.components.content import content
from services.MosaicMed.components.footer import footer
from services.MosaicMed.components.header import header
from services.MosaicMed.components.sidebar import sidebar
from services.MosaicMed.pages.doctors_talon.tab import app_tabs_dtr
from services.MosaicMed.pages.main.main import main_layout

type_page = 'index'

app.layout = html.Div(
    [
        dcc.Store(id='current-month-number', data=None),
        dcc.Store(id='current-month-name', data=None),
        dcc.Interval(id='date-interval-main', interval=600000, n_intervals=0),  # 1 час
        dcc.Location(id="url"),
        header,
        html.Div([
            sidebar,
            content
        ], style={"position": "relative"}),
        footer
    ]
)


# Определяем отчетный месяц и выводим его на страницу и в переменную Store
@app.callback(
    Output('current-month-number', 'data'),
    Output('current-month-name', 'data'),
    [Input('date-interval-main', 'n_intervals')]
)
def update_current_month(n_intervals):
    current_month_num, current_month_name = get_current_reporting_month()
    return current_month_num, current_month_name


@app.callback(Output("page-content", "children"),
              [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return main_layout
    elif pathname == "/doctors-talon-report":
        return app_tabs_dtr
    else:
        return html.H2("Страница не найдена")


if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0', port='8080')
