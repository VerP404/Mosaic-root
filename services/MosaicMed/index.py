# index.py
from dash import Input, Output, dcc, html
from flask_login import current_user

from services.MosaicMed.Authentication.models import user_has_access
from services.MosaicMed.app import app
from services.MosaicMed.components.content import content
from services.MosaicMed.components.footer import footer
from services.MosaicMed.components.header import header
from services.MosaicMed.components.sidebar import get_sidebar  # Импортируем функцию
from services.MosaicMed.pages.doctors_talon.tab import app_tabs_doctors
from services.MosaicMed.pages.it_department.admin.admin import admin_layout
from services.MosaicMed.pages.it_department.admin.admin_access import admin_access_layout
from services.MosaicMed.pages.main.main import main_layout
from services.MosaicMed.callback.date_reports import get_current_reporting_month
from database.db_conn import init_db

app.layout = html.Div(
    [
        dcc.Store(id='current-month-number', data=None),
        dcc.Store(id='current-month-name', data=None),
        dcc.Interval(id='date-interval-main', interval=600000, n_intervals=0),  # 1 час
        dcc.Location(id="url"),
        header,
        html.Div([
            html.Div(id='sidebar-container'),
            content
        ], style={"position": "relative"}),
        footer
    ]
)

@app.callback(
    Output('sidebar-container', 'children'),
    [Input('url', 'pathname')]
)
def update_sidebar(pathname):
    return get_sidebar()

@app.callback(
    Output('current-month-number', 'data'),
    Output('current-month-name', 'data'),
    [Input('date-interval-main', 'n_intervals')]
)
def update_current_month(n_intervals):
    current_month_num, current_month_name = get_current_reporting_month()
    return current_month_num, current_month_name

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if not current_user.is_authenticated and pathname != '/login':
        return dcc.Location(pathname='/login', id='redirect')

    if pathname == "/main":
        return main_layout
    elif pathname == "/login":
        return dcc.Location(pathname='/login', id='redirect')
    elif pathname == "/doctors-talon-report":
        if current_user.has_role('admin') or user_has_access(current_user.role, '/doctors-talon-report'):
            return app_tabs_doctors
        else:
            return html.H2("Доступ запрещен")
    elif pathname == "/dispensary-adult" or pathname == "/dispensary-children" or pathname == "/dispensary-reproductive":
        if current_user.has_role('admin') or user_has_access(current_user.role, pathname):
            return html.H2("Страница диспансеризации")
        else:
            return html.H2("Доступ запрещен")
    elif pathname.startswith("/econ"):
        if current_user.has_role('admin') or user_has_access(current_user.role, pathname):
            return html.H2("Экономические отчеты")
        else:
            return html.H2("Доступ запрещен")
    elif pathname.startswith("/it"):
        if current_user.has_role('admin') or user_has_access(current_user.role, pathname):
            return admin_access_layout()
        else:
            return html.H2("Доступ запрещен")
    elif pathname == "/admin/roles":
        if current_user.has_role('admin') or user_has_access(current_user.role, '/admin/roles'):
            return admin_access_layout()
        else:
            return html.H2("Доступ запрещен")
    elif pathname == "/other-reports":
        if current_user.has_role('admin') or user_has_access(current_user.role, '/other-reports'):
            return html.H2("Другие отчеты")
        else:
            return html.H2("Доступ запрещен")
    elif pathname == "/errors":
        if current_user.has_role('admin') or user_has_access(current_user.role, '/errors'):
            return html.H2("Отказы в оплате")
        else:
            return html.H2("Доступ запрещен")
    elif pathname == "/eln":
        if current_user.has_role('admin') or user_has_access(current_user.role, '/eln'):
            return html.H2("ЭЛН")
        else:
            return html.H2("Доступ запрещен")

    return html.H2("Страница не найдена")


if __name__ == "__main__":
    init_db()
    app.run_server(debug=True, host='0.0.0.0', port='8080')
