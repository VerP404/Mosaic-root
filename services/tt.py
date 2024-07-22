import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_table

app = dash.Dash(__name__)

# Dummy data for demonstration
data = {
    'Specialty': ['General Practitioner', 'Obstetrician-Gynecologist', 'Ophthalmologist', 'District Therapist', 'Surgeon'],
    'Slots Today': [32, 29, 0, 57, 18],
    'Available Today': [30, 24, 0, 44, 5],
    'Available in 14 Days': [332, 308, 11, 437, 159]
}
df = pd.DataFrame(data)

app.layout = html.Div(
    style={'backgroundColor': '#344299', 'color': 'white', 'fontFamily': 'Arial'},
    children=[
        html.H1('Doctor Appointment Availability', style={'textAlign': 'center', 'padding': '10px'}),
        dash_table.DataTable(
            id='table',
            columns=[{'name': col, 'id': col} for col in df.columns],
            data=df.to_dict('records'),
            style_header={'backgroundColor': '#0052cc', 'color': 'white', 'fontWeight': 'bold'},
            style_cell={'backgroundColor': '#344299', 'color': 'white', 'textAlign': 'center'},
            style_data_conditional=[
                {'if': {'row_index': 'odd'}, 'backgroundColor': '#3d54a6'},
                {'if': {'column_id': 'Specialty'}, 'textAlign': 'left'},
            ]
        ),
        html.Div(
            style={'padding': '20px'},
            children=[
                html.H2('Update Data'),
                dcc.Input(id='specialty', type='text', placeholder='Specialty'),
                dcc.Input(id='slots_today', type='number', placeholder='Slots Today'),
                dcc.Input(id='available_today', type='number', placeholder='Available Today'),
                dcc.Input(id='available_14_days', type='number', placeholder='Available in 14 Days'),
                html.Button('Add', id='add_button', n_clicks=0),
                html.Button('Update', id='update_button', n_clicks=0)
            ]
        )
    ]
)

@app.callback(
    Output('table', 'data'),
    [Input('add_button', 'n_clicks'), Input('update_button', 'n_clicks')],
    [State('table', 'data'), State('table', 'columns'), State('specialty', 'value'),
     State('slots_today', 'value'), State('available_today', 'value'), State('available_14_days', 'value')]
)
def update_table(n_add, n_update, rows, columns, specialty, slots_today, available_today, available_14_days):
    if n_add > 0 or n_update > 0:
        new_row = {columns[0]['id']: specialty, columns[1]['id']: slots_today, columns[2]['id']: available_today,
                   columns[3]['id']: available_14_days}
        rows.append(new_row)
    return rows

if __name__ == '__main__':
    app.run_server(debug=True)
