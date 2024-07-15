# sidebar.py
from dash import html
import dash_bootstrap_components as dbc
from flask_login import current_user

from database.db_conn import SessionLocal
from services.MosaicMed import short_name_mo, dashboard_chef, dashboard_patient
from services.MosaicMed.Authentication.models import RoleModuleAccess

SIDEBAR_CONTENT_STYLE_HIDE_SCROLL = {
    "overflow-y": "scroll",
    "height": "calc(100% - 60px)",
    "padding": "0rem 1px 30px",
    "scrollbar-width": "none",
    "::-webkit-scrollbar": {
        "width": "0px"
    },
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "56px",
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "background-color": "#f8f9fa",
    "transition": "all 0.2s",
    "display": "flex",
    "flex-direction": "column",
}

sidebar2 = html.Div(
    [
        html.H2(short_name_mo, className="display-8 text-center", id="sidebar-title"),
        html.Hr(style={"margin": "1px"}),
        html.Div(
            dbc.Nav(
                [
                    dbc.NavLink(
                        [html.I(className="fas fa-home"), html.Span(" Главная", className="nav-text", title="Главная")],
                        href="/main", active="exact", className="nav-item", id="nav-home"),
                    dbc.NavLink(
                        [html.I(className="fas fa-user-md"), html.Span(" Врачи", className="nav-text", title="Врачи")],
                        href="/doctors-talon-report", active="exact", className="nav-item", id="nav-doctors"),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem("По специальности", href="/dispensary-observation-speciality"),
                            dbc.DropdownMenuItem("По корпусам", href="/dispensary-observation-korpus"),
                            dbc.DropdownMenuItem("Уникальные по группам", href="/dispensary-observation-unique-group"),
                        ],
                        label=[html.I(className="fas fa-eye"),
                               html.Span(" Диспансерное наблюдение", className="nav-text",
                                         title="Диспансерное наблюдение")],
                        nav=True,
                        id="nav-disp-obs",
                        right=True,
                    ),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem("Взрослые", href="/dispensary-adult"),
                            dbc.DropdownMenuItem("Дети", href="/dispensary-children"),
                            dbc.DropdownMenuItem("Репродуктивное", href="/dispensary-reproductive"),
                        ],
                        label=[html.I(className="fas fa-stethoscope"),
                               html.Span(" Диспансеризация", className="nav-text", title="Диспансеризация")],
                        nav=True,
                        id="nav-dispensary",
                        right=True,
                    ),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem("Диспансерное наблюдение", href="/iszl-disp-nab"),
                            dbc.DropdownMenuItem("Население", href="/iszl-people"),
                        ],
                        label=[html.I(className="fas fa-heartbeat"),
                               html.Span(" ИСЗЛ", className="nav-text", title="ИСЗЛ")],
                        nav=True,
                        id="nav-iszl",
                        right=True,
                    ),
                    dbc.NavLink([html.I(className="fas fa-chart-bar"),
                                 html.Span(" Другие отчеты", className="nav-text", title="Другие отчеты")],
                                href="/other-reports", active="exact", className="nav-item", id="nav-other-reports"),
                    dbc.NavLink([html.I(className="fas fa-times-circle"),
                                 html.Span(" Отказы в оплате", className="nav-text", title="Отказы в оплате")],
                                href="/errors", active="exact", className="nav-item", id="nav-errors"),
                    dbc.NavLink(
                        [html.I(className="fas fa-file-medical"), html.Span(" ЭЛН", className="nav-text", title="ЭЛН")],
                        href="/eln", active="exact", className="nav-item", id="nav-eln"),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem("Для сборки счетов", href="/gen-invoices"),
                            dbc.DropdownMenuItem("Обновление базы данных", href="/update-bd"),
                            dbc.DropdownMenuItem("Месяцы по статусам", href="/stat-months"),
                            dbc.DropdownMenuItem("Месяцы по смо", href="/for-smo"),
                            dbc.DropdownMenuItem("Цель 3", href="/cel3"),
                            dbc.DropdownMenuItem("Администрирование", href="/it/admin"),
                        ],
                        label=[html.I(className="fas fa-desktop"),
                               html.Span(" iT отдел", className="nav-text", title="iT отдел")],
                        nav=True,
                        id="nav-it",
                        right=True,
                    ),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem("Сверхподушевик", href="/econ-sv-pod"),
                            dbc.DropdownMenuItem("Объемные показатели", href="/econ-report"),
                            dbc.DropdownMenuItem("ПГГ", href="/econ-pgg"),
                            dbc.DropdownMenuItem("По врачам", href="/econ-by-doctor"),
                            dbc.DropdownMenuItem("По врачам оплаченные", href="/econ-by-doctor-cel"),
                            dbc.DropdownMenuItem("По врачам диспансеризация", href="/econ-by-doctor-dispensary"),
                            dbc.DropdownMenuItem("Новые территории", href="/econ-new-territories"),
                            dbc.DropdownMenuItem("Маршруты ПН1", href="/econ-route-children"),
                            dbc.DropdownMenuItem("Диспансеризация по возрастам", href="/econ-disp"),
                        ],
                        label=[html.I(className="fas fa-dollar-sign"),
                               html.Span(" Экономические отчеты", className="nav-text", title="Экономические отчеты")],
                        nav=True,
                        id="nav-econ-reports",
                        right=True,
                    ),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem("Талоны", href="/volumes"),
                            dbc.DropdownMenuItem("Финансы", href="/finance"),
                        ],
                        label=[html.I(className="fas fa-chart-line"),
                               html.Span(" Объемы", className="nav-text", title="Объемы")],
                        nav=True,
                        id="nav-volumes",
                        right=True,
                    ),
                    dbc.NavLink([html.I(className="fas fa-file-alt"),
                                 html.Span(" Шаблоны", className="nav-text", title="Шаблоны")], href="/templates",
                                active="exact", className="nav-item", id="nav-templates"),
                    dbc.NavLink([html.I(className="fas fa-edit"),
                                 html.Span(" Заполнение списков", className="nav-text", title="Заполнение списков")],
                                href="/filling-lists", active="exact", className="nav-item", id="nav-filling-lists"),
                    dbc.NavLink([html.I(className="fas fa-list-alt"),
                                 html.Span(" Талоны WEB-ОМС", className="nav-text", title="Талоны WEB-ОМС")],
                                href="/wo-coupons", active="exact", className="nav-item", id="nav-wo-coupons"),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem("Главный врач", href=dashboard_chef),
                            dbc.DropdownMenuItem("Пациенты", href=dashboard_patient)
                        ],
                        label=[html.I(className="fas fa-tachometer-alt"),
                               html.Span(" Дашборды", className="nav-text", title="Дашборды")],
                        nav=True,
                        id="nav-dashboards",
                        right=True,
                    ),
                ],
                vertical=True,
                pills=True,
            ),
            style=SIDEBAR_CONTENT_STYLE_HIDE_SCROLL
        )
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)


def fetch_role_access(role):
    session = SessionLocal()
    access_data = session.query(RoleModuleAccess).filter_by(role=role).all()
    session.close()
    return [access.module for access in access_data]

def get_sidebar():
    nav_items = [
        dbc.NavLink([html.I(className="fas fa-home"), html.Span(" Главная", className="nav-text", title="Главная")], href="/main", active="exact", className="nav-item", id="nav-home"),
    ]

    if current_user.is_authenticated:
        modules = fetch_role_access(current_user.role)
        if 'doctors-talon-report' in modules:
            nav_items.append(dbc.NavLink([html.I(className="fas fa-user-md"), html.Span(" Врачи", className="nav-text", title="Врачи")], href="/doctors-talon-report", active="exact", className="nav-item", id="nav-doctors"))
        if 'it-admin' in modules:
            nav_items.append(dbc.NavLink([html.I(className="fas fa-desktop"), html.Span(" IT отдел", className="nav-text", title="IT отдел")], href="/it/admin", active="exact", className="nav-item", id="nav-it"))

    sidebar_content = dbc.Nav(nav_items, vertical=True, pills=True)

    return html.Div(
        [
            html.H2("МозаикаМед", className="display-8 text-center", id="sidebar-title"),
            html.Hr(style={"margin": "1px"}),
            html.Div(sidebar_content, style=SIDEBAR_CONTENT_STYLE_HIDE_SCROLL)
        ],
        id="sidebar",
        style=SIDEBAR_STYLE,
    )
