import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from services.MosaicMed.app import app
from services.MosaicMed.authentication.models import Setting, SessionLocal

def get_setting(name: str) -> str:
    session = SessionLocal()
    setting = session.query(Setting).filter(Setting.name == name).first()
    session.close()
    return setting.value if setting else ""

def set_setting(name: str, value: str) -> None:
    session = SessionLocal()
    setting = session.query(Setting).filter(Setting.name == name).first()
    if setting:
        setting.value = value
    else:
        setting = Setting(name=name, value=value)
        session.add(setting)
    session.commit()
    session.close()

settings_layout = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    dbc.Alert(id="settings-output-state", is_open=False, duration=4000, color="danger"),
                    html.H2("Настройки", className="card-title mb-4"),
                    dbc.Form([
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Сайт МО:", html_for="site_mo"),
                                dbc.Input(type="text", id="site_mo", placeholder="Введите URL",
                                          value=get_setting("site_mo"), required=True)
                            ], width=6),
                            dbc.Col([
                                dbc.Label("Название МО:", html_for="name_mo"),
                                dbc.Input(type="text", id="name_mo", placeholder="Введите название",
                                          value=get_setting("name_mo"), required=True)
                            ], width=6)
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Краткое название МО:", html_for="short_name_mo"),
                                dbc.Input(type="text", id="short_name_mo", placeholder="Введите краткое название",
                                          value=get_setting("short_name_mo"), required=True)
                            ], width=6),
                            dbc.Col([
                                dbc.Label("Дашборд главного врача:", html_for="dashboard_chef"),
                                dbc.Input(type="text", id="dashboard_chef", placeholder="Введите URL",
                                          value=get_setting("dashboard_chef"), required=True)
                            ], width=6)
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Дашборд пациента:", html_for="dashboard_patient"),
                                dbc.Input(type="text", id="dashboard_patient", placeholder="Введите URL",
                                          value=get_setting("dashboard_patient"), required=True)
                            ], width=6)
                        ], className="mb-3"),
                        dbc.Row([
                            dbc.Col([
                                dbc.Button("Сохранить", id="save-settings-button", color="primary", className="mr-2",
                                           style={"width": "100%"})
                            ])
                        ])
                    ])
                ]),
                style={"width": "100%", "padding": "2rem", "box-shadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2)",
                       "border-radius": "10px"}
            )
        ], width=8)
    ], style={"margin": "0 auto", "max-width": "1200px"})
], style={"padding": "2rem"})

@app.callback(
    Output("settings-output-state", "children"),
    Output("settings-output-state", "is_open"),
    Output('site_mo', 'value'),
    Output('name_mo', 'value'),
    Output('short_name_mo', 'value'),
    Output('dashboard_chef', 'value'),
    Output('dashboard_patient', 'value'),
    Input("save-settings-button", "n_clicks"),
    State("site_mo", "value"),
    State("name_mo", "value"),
    State("short_name_mo", "value"),
    State("dashboard_chef", "value"),
    State("dashboard_patient", "value")
)
def manage_settings(save_clicks, site_mo, name_mo, short_name_mo, dashboard_chef, dashboard_patient):
    ctx = dash.callback_context

    if not ctx.triggered:
        return "", False, get_setting("site_mo"), get_setting("name_mo"), get_setting("short_name_mo"), get_setting("dashboard_chef"), get_setting("dashboard_patient")

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'save-settings-button':
        set_setting("site_mo", site_mo)
        set_setting("name_mo", name_mo)
        set_setting("short_name_mo", short_name_mo)
        set_setting("dashboard_chef", dashboard_chef)
        set_setting("dashboard_patient", dashboard_patient)
        return "Настройки сохранены.", True, site_mo, name_mo, short_name_mo, dashboard_chef, dashboard_patient

    return "", False, site_mo, name_mo, short_name_mo, dashboard_chef, dashboard_patient
