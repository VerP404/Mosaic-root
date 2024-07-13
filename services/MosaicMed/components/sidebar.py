from dash import html
import dash_bootstrap_components as dbc

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "56px",
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar = html.Div(
    [
        html.H2("ВГП №3", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Главная", href="/", active="exact"),
                dbc.NavLink("По врачам", href="/doctors-talon-report", active="exact"),
                dbc.DropdownMenu(
                    [dbc.DropdownMenuItem("По специальности", href="/dispensary-observation-speciality"),
                     dbc.DropdownMenuItem("По врачу", href="/dispensary-observation-doctor"),
                     dbc.DropdownMenuItem("По корпусам", href="/dispensary-observation-korpus"),
                     dbc.DropdownMenuItem("Уникальные по группам", href="/dispensary-observation-unique-group"),
                     ],
                    label="Диспансерное наблюдение",
                    nav=True,
                ),
                dbc.DropdownMenu(
                    [dbc.DropdownMenuItem("Взрослые", href="/dispensary-adult"),
                     dbc.DropdownMenuItem("Дети", href="/dispensary-children"),
                     dbc.DropdownMenuItem("Репродуктивное", href="/dispensary-reproductive"),
                     ],
                    label="Диспансеризация",
                    nav=True,
                ),
                dbc.DropdownMenu(
                    [dbc.DropdownMenuItem("Диспансерное наблюдение", href="/iszl-disp-nab"),
                     dbc.DropdownMenuItem("Население", href="/iszl-people")],
                    label="ИСЗЛ",
                    nav=True,
                ),
                dbc.NavLink("Другие отчеты", href="/other-reports", active="exact"),
                dbc.NavLink("Отказы в оплате", href="/errors", active="exact"),
                dbc.NavLink("ЭЛН", href="/eln", active="exact"),
                dbc.DropdownMenu(
                    [dbc.DropdownMenuItem("Для сборки счетов", href="/gen-invoices"),
                     dbc.DropdownMenuItem("Обновление базы данных", href="/update-bd"),
                     dbc.DropdownMenuItem("Месяцы по статусам", href="/stat-months"),
                     dbc.DropdownMenuItem("Месяцы по смо", href="/for-smo"),
                     dbc.DropdownMenuItem("Цель 3", href="/cel3"),
                     ],
                    label="iT отдел",
                    nav=True,
                ),
                dbc.DropdownMenu(
                    [dbc.DropdownMenuItem("Сверхподушевик", href="/econ-sv-pod"),
                     dbc.DropdownMenuItem("Объемные показатели", href="/econ-report"),
                     dbc.DropdownMenuItem("ПГГ", href="/econ-pgg"),
                     dbc.DropdownMenuItem("По врачам", href="/econ-by-doctor"),
                     dbc.DropdownMenuItem("По врачам оплаченные", href="/econ-by-doctor-cel"),
                     dbc.DropdownMenuItem("По врачам диспансеризация", href="/econ-by-doctor-dispensary"),
                     dbc.DropdownMenuItem("Новые территории", href="/econ-new-territories"),
                     dbc.DropdownMenuItem("Маршруты ПН1", href="/econ-route-children"),
                     dbc.DropdownMenuItem("Диспансеризация по возрастам", href="/econ-disp"),
                     dbc.DropdownMenuItem("Стационары", href="/stationary"),
                     ],
                    label="Экономические отчеты",
                    nav=True,
                ),
                dbc.DropdownMenu(
                    [dbc.DropdownMenuItem("Талоны", href="/volumes"),
                     dbc.DropdownMenuItem("Финансы", href="/finance"),
                     ],
                    label="Объемы",
                    nav=True,
                ),
                dbc.NavLink("Шаблоны", href="/templates", active="exact"),
                dbc.NavLink("Заполнение списков", href="/filling-lists", active="exact"),
                dbc.NavLink("Талоны WEB-ОМС", href="/wo-coupons", active="exact"),
                dbc.DropdownMenu(
                    [dbc.DropdownMenuItem("Главный врач", href="http://10.136.29.166:5010/"),
                     dbc.DropdownMenuItem("Пациенты", href="http://10.136.29.72:8001/")
                     ],
                    label="Дашборды",
                    nav=True,
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
