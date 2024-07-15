from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from services.MosaicMed.app import app
from services.MosaicMed.Authentication.models import RoleModuleAccess, SessionLocal

def get_roles():
    return ['operator', 'doctor', 'economist', 'statistician', 'manager', 'head', 'admin']

def get_modules():
    return ['main', 'doctors-talon-report', 'it-admin', 'other-modules']

def fetch_access_data():
    session = SessionLocal()
    access_data = session.query(RoleModuleAccess).all()
    session.close()
    return [{'role': access.role, 'module': access.module} for access in access_data]

def generate_access_table():
    roles = get_roles()
    modules = get_modules()
    access_data = fetch_access_data()

    data = []
    for module in modules:
        row = {'module': module}
        for role in roles:
            row[role] = 'Да' if any(item['role'] == role and item['module'] == module for item in access_data) else 'Нет'
        data.append(row)

    columns = [{'name': 'Модуль', 'id': 'module', 'editable': False}] + [{'name': role, 'id': role, 'presentation': 'dropdown'} for role in roles]

    return dash_table.DataTable(
        id='access-table',
        columns=columns,
        data=data,
        editable=True,
        dropdown={
            role: {
                'options': [
                    {'label': 'Да', 'value': 'Да'},
                    {'label': 'Нет', 'value': 'Нет'}
                ]
            } for role in roles
        },
    )

def admin_access_layout():
    return html.Div([
        html.H2("Управление доступом к модулям", style={"margin-top": "20px"}),
        generate_access_table(),
        dbc.Button("Сохранить изменения", id="save-access-button", color="primary", className="mr-2", style={"margin-top": "20px"}),
        dbc.Alert(id="save-alert", color="success", is_open=False, dismissable=True, children="Изменения сохранены.")
    ], style={"margin": "50px"})

@app.callback(
    Output('access-table', 'data'),
    Output('save-alert', 'is_open'),
    [Input('save-access-button', 'n_clicks')],
    [State('access-table', 'data')]
)
def save_access_data(n_clicks, table_data):
    if n_clicks:
        session = SessionLocal()
        session.query(RoleModuleAccess).delete()
        for row in table_data:
            for role, access in row.items():
                if role != 'module' and access == 'Да':
                    new_access = RoleModuleAccess(role=role, module=row['module'])
                    session.add(new_access)
        session.commit()
        session.close()
        return table_data, True
    return table_data, False
