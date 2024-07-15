import os

from dash import html, dcc, dependencies, Input, Output, State, State
from app import app
import subprocess
import dash_bootstrap_components as dbc

from callback import query_last_record_sql, last_file_csv_in_directory

# Исходное состояние
loading_state = {
    'loading': False,
    'output_text': ""
}
file_path_oms = [r'\\10.136.29.166\_it_reports\Download Web_OMS\talon',
                 r'\\10.136.29.166\_it_reports\Download ISZL\people',
                 r'\\10.136.29.166\_it_reports\Download ISZL\iszl',
                 r'\\10.136.29.166\_it_reports\Download ISZL\emd kvazar',
                 r'\\10.136.29.166\_it_reports\Download ISZL\doctors',
                 r'\\10.136.29.166\_it_reports\Download ISZL\area',
                 r'\\10.136.29.166\_it_reports\Download ISZL\168n',
                 r'\\10.136.29.166\_it_reports\Download ISZL\obr_procedur',
                 r'\\10.136.29.166\_it_reports\Download ISZL\detailed',
                 r'\\10.136.29.166\_it_reports\Download ISZL\ln',
                 r'\\10.136.29.166\_it_reports\Download ISZL\obr_doc',
                 ]
type_page = "update-bd"
dn = '"168n_log"'
tab_layout_it_update_bd = html.Div(
    [
        html.Div(
            [
                html.H5(
                    'Для обновления файлов в базе данных, необходимо добавить файлы в папку на сервере: "\\\Srv-main02\_it_reports\Download ISZL"',
                    className='label'),
                html.Div([
                    dbc.Button('Открыть папку в проводнике', id='open-folder-button'),
                ]),
                html.Hr(),
                dbc.Button('Проверить актуальность файлов', id='run-script-button'),
                html.Hr(),
                html.Div(
                    [
                        html.H3('1. Обновление файла ОМС', className='label'),
                        html.P(id="file1-in-bd"),
                        html.P(id="file1-for-bd"),
                        dbc.Alert(id='color-indicator1', color="primary"),
                        dbc.Button('Запустить скрипт', id=f'run-script1-button-{type_page}'),
                        html.Div(id=f'script1-output-{type_page}'),
                        dcc.Loading(id=f"loading1-output-{type_page}", children=[], type="default"),
                    ]),
                html.Hr(),
                html.Div(
                    [
                        html.H3('2. Обновление файла населения из ИСЗЛ', className='label'),
                        html.P(id="file2-in-bd"),
                        html.P(id="file2-for-bd"),
                        dbc.Alert(id='color-indicator2', color="primary"),
                        dbc.Button('Запустить скрипт', id=f'run-script2-button-{type_page}'),
                        html.Div(id=f'script2-output-{type_page}'),
                        dcc.Loading(id=f"loading2-output-{type_page}", children=[], type="default"),
                    ]),
                html.Hr(),
                html.Div(
                    [
                        html.H3('3. Обновление файла диспансерного наблюдения из ИСЗЛ', className='label'),
                        html.P(id="file3-in-bd"),
                        html.P(id="file3-for-bd"),
                        dbc.Alert(id='color-indicator3', color="primary"),
                        dbc.Button('Запустить скрипт', id=f'run-script3-button-{type_page}'),
                        html.Div(id=f'script3-output-{type_page}'),
                        dcc.Loading(id=f"loading3-output-{type_page}", children=[], type="default"),
                    ]),
                html.Hr(),
                html.Div(
                    [
                        html.H3('4. Обновление файла ЭМД из Квазар', className='label'),
                        html.P(id="file4-in-bd"),
                        html.P(id="file4-for-bd"),
                        dbc.Alert(id='color-indicator4', color="primary"),
                        dbc.Button('Запустить скрипт', id=f'run-script4-button-{type_page}'),
                        html.Div(id=f'script4-output-{type_page}'),
                        dcc.Loading(id=f"loading4-output-{type_page}", children=[], type="default"),
                    ]),
                html.Hr(),
                html.Div(
                    [
                        html.H3('5. Обновление файла врачей из Web.ОМС', className='label'),
                        html.P(id="file5-in-bd"),
                        html.P(id="file5-for-bd"),
                        dbc.Alert(id='color-indicator5', color="primary"),
                        dbc.Button('Запустить скрипт', id=f'run-script5-button-{type_page}'),
                        html.Div(id=f'script5-output-{type_page}'),
                        dcc.Loading(id=f"loading5-output-{type_page}", children=[], type="default"),
                    ]),
                html.Hr(),
                html.Div(
                    [
                        html.H3('6. Обновление списка участковых врачей и участков', className='label'),
                        html.P(id="file6-in-bd"),
                        html.P(id="file6-for-bd"),
                        dbc.Alert(id='color-indicator6', color="primary"),
                        dbc.Button('Запустить скрипт', id=f'run-script6-button-{type_page}'),
                        html.Div(id=f'script6-output-{type_page}'),
                        dcc.Loading(id=f"loading6-output-{type_page}", children=[], type="default"),
                    ]),
                html.Hr(),
                html.Div(
                    [
                        html.H3('7. Обновление списка диагнозов и специальностей по 168н', className='label'),
                        html.P(id="file7-in-bd"),
                        html.P(id="file7-for-bd"),
                        dbc.Alert(id='color-indicator7', color="primary"),
                        dbc.Button('Запустить скрипт', id=f'run-script7-button-{type_page}'),
                        html.Div(id=f'script7-output-{type_page}'),
                        dcc.Loading(id=f"loading7-output-{type_page}", children=[], type="default"),
                    ]),
                html.Hr(),
                html.Div(
                    [
                        html.H3('8. Обновление списка записанных на процедуры из журнала обращений Квазар',
                                className='label'),
                        html.P(id="file8-in-bd"),
                        html.P(id="file8-for-bd"),
                        dbc.Alert(id='color-indicator8', color="primary"),
                        dbc.Button('Запустить скрипт', id=f'run-script8-button-{type_page}'),
                        html.Div(id=f'script8-output-{type_page}'),
                        dcc.Loading(id=f"loading8-output-{type_page}", children=[], type="default"),
                    ]),
                html.Hr(),
                html.Div(
                    [
                        html.H3('9. Обновление детализации диспансеризации',
                                className='label'),
                        html.P(id="file9-in-bd"),
                        html.P(id="file9-for-bd"),
                        dbc.Alert(id='color-indicator9', color="primary"),
                        dbc.Button('Запустить скрипт', id=f'run-script9-button-{type_page}'),
                        html.Div(id=f'script9-output-{type_page}'),
                        dcc.Loading(id=f"loading9-output-{type_page}", children=[], type="default"),
                    ]),
                html.Hr(),
                html.Div(
                    [
                        html.H3('10. Обновление листов нетрудоспособности',
                                className='label'),
                        html.P(id="file10-in-bd"),
                        html.P(id="file10-for-bd"),
                        dbc.Alert(id='color-indicator10', color="primary"),
                        dbc.Button('Запустить скрипт', id=f'run-script10-button-{type_page}'),
                        html.Div(id=f'script10-output-{type_page}'),
                        dcc.Loading(id=f"loading10-output-{type_page}", children=[], type="default"),
                    ]),
                html.Hr(),
                html.Div(
                    [
                        html.H3('11. Обновление журнала обращений',
                                className='label'),
                        html.P(id="file11-in-bd"),
                        html.P(id="file11-for-bd"),
                        dbc.Alert(id='color-indicator11', color="primary"),
                        dbc.Button('Запустить скрипт', id=f'run-script11-button-{type_page}'),
                        html.Div(id=f'script11-output-{type_page}'),
                        dcc.Loading(id=f"loading11-output-{type_page}", children=[], type="default"),
                    ]),
                html.Hr(),
            ]
        )
    ]
)


def run_script(n_clicks, loading_children, script_output_children, path_script):
    if n_clicks is None:
        return [], "Нажмите кнопку, чтобы запустить скрипт."

    if not loading_children:
        # Начало выполнения скрипта, установите состояние loading=True
        try:
            # Запускаем скрипт
            result = subprocess.run(
                [r"venv\Scripts\python.exe", path_script  # r"C:\pythonProject\DocReport\venv\Scripts\python.exe"
                 ],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                decoded_text = result.stdout.encode('cp1251').decode('utf-8')
            except UnicodeDecodeError:
                decoded_text = result.stdout.encode('utf-8').decode('utf-8')

            # Возвращаем результат выполнения скрипта и сбрасываем состояние loading
            return [], f"Результат выполнения скрипта:\n{decoded_text}"
        except subprocess.CalledProcessError as e:
            # Возвращаем ошибку выполнения скрипта и сбрасываем состояние loading
            return [], f"Ошибка при выполнении скрипта:\n{e.output}"

    # Если кнопка уже была нажата и скрипт уже выполняется, возвращаем состояние loading и текущий вывод скрипта
    return "Выполняется скрипт, подождите...", script_output_children


@app.callback(
    [Output(f'loading1-output-{type_page}', 'children'),
     Output(f'script1-output-{type_page}', 'children')],
    [Input(f'run-script1-button-{type_page}', 'n_clicks')],
    [State(f'loading1-output-{type_page}', 'children'),
     State(f'script1-output-{type_page}', 'children')]
)
def run_script_callback(n_clicks, loading_children, script_output_children):
    path_script = r"files\to_database\oms_to_database.py"  # r"C:\pythonProject\DocReport\files\to_database\oms_to_database.py"
    return run_script(n_clicks, loading_children, script_output_children, path_script)


@app.callback(
    [Output(f'loading2-output-{type_page}', 'children'),
     Output(f'script2-output-{type_page}', 'children')],
    [Input(f'run-script2-button-{type_page}', 'n_clicks')],
    [State(f'loading2-output-{type_page}', 'children'),
     State(f'script2-output-{type_page}', 'children')]
)
def run_script_callback(n_clicks, loading_children, script_output_children):
    path_script = r"files\to_database\people_to_database.py"  # r"C:\pythonProject\DocReport\files\to_database\people_to_database.py"
    return run_script(n_clicks, loading_children, script_output_children, path_script)


@app.callback(
    [Output(f'loading3-output-{type_page}', 'children'),
     Output(f'script3-output-{type_page}', 'children')],
    [Input(f'run-script3-button-{type_page}', 'n_clicks')],
    [State(f'loading3-output-{type_page}', 'children'),
     State(f'script3-output-{type_page}', 'children')]
)
def run_script_callback(n_clicks, loading_children, script_output_children):
    path_script = r"files\to_database\iszl_to_database.py"
    return run_script(n_clicks, loading_children, script_output_children, path_script)


@app.callback(
    [Output(f'loading4-output-{type_page}', 'children'),
     Output(f'script4-output-{type_page}', 'children')],
    [Input(f'run-script4-button-{type_page}', 'n_clicks')],
    [State(f'loading4-output-{type_page}', 'children'),
     State(f'script4-output-{type_page}', 'children')]
)
def run_script_callback(n_clicks, loading_children, script_output_children):
    path_script = r"files\to_database\emd_to_database.py"
    return run_script(n_clicks, loading_children, script_output_children, path_script)


@app.callback(
    [Output(f'loading5-output-{type_page}', 'children'),
     Output(f'script5-output-{type_page}', 'children')],
    [Input(f'run-script5-button-{type_page}', 'n_clicks')],
    [State(f'loading5-output-{type_page}', 'children'),
     State(f'script5-output-{type_page}', 'children')]
)
def run_script_callback(n_clicks, loading_children, script_output_children):
    path_script = r"files\to_database\doctors_oms_to_database.py"
    return run_script(n_clicks, loading_children, script_output_children, path_script)


@app.callback(
    [Output(f'loading6-output-{type_page}', 'children'),
     Output(f'script6-output-{type_page}', 'children')],
    [Input(f'run-script6-button-{type_page}', 'n_clicks')],
    [State(f'loading6-output-{type_page}', 'children'),
     State(f'script6-output-{type_page}', 'children')]
)
def run_script_callback(n_clicks, loading_children, script_output_children):
    path_script = r"files\to_database\area_to_database.py.py"
    return run_script(n_clicks, loading_children, script_output_children, path_script)


@app.callback(
    [Output(f'loading7-output-{type_page}', 'children'),
     Output(f'script7-output-{type_page}', 'children')],
    [Input(f'run-script7-button-{type_page}', 'n_clicks')],
    [State(f'loading7-output-{type_page}', 'children'),
     State(f'script7-output-{type_page}', 'children')]
)
def run_script_callback(n_clicks, loading_children, script_output_children):
    path_script = r"files\to_database\168n_to_database.py"
    return run_script(n_clicks, loading_children, script_output_children, path_script)


@app.callback(
    [Output(f'loading8-output-{type_page}', 'children'),
     Output(f'script8-output-{type_page}', 'children')],
    [Input(f'run-script8-button-{type_page}', 'n_clicks')],
    [State(f'loading8-output-{type_page}', 'children'),
     State(f'script8-output-{type_page}', 'children')]
)
def run_script_callback(n_clicks, loading_children, script_output_children):
    path_script = r"files\to_database\obr_procedur_to_database.py"
    return run_script(n_clicks, loading_children, script_output_children, path_script)


@app.callback(
    [Output(f'loading9-output-{type_page}', 'children'),
     Output(f'script9-output-{type_page}', 'children')],
    [Input(f'run-script9-button-{type_page}', 'n_clicks')],
    [State(f'loading9-output-{type_page}', 'children'),
     State(f'script9-output-{type_page}', 'children')]
)
def run_script_callback(n_clicks, loading_children, script_output_children):
    path_script = r"files\to_database\detailed_dd_to_database.py"
    return run_script(n_clicks, loading_children, script_output_children, path_script)


@app.callback(
    [Output(f'loading10-output-{type_page}', 'children'),
     Output(f'script10-output-{type_page}', 'children')],
    [Input(f'run-script10-button-{type_page}', 'n_clicks')],
    [State(f'loading10-output-{type_page}', 'children'),
     State(f'script10-output-{type_page}', 'children')]
)
def run_script_callback(n_clicks, loading_children, script_output_children):
    path_script = r"files\to_database\ln_to_database.py"
    return run_script(n_clicks, loading_children, script_output_children, path_script)


@app.callback(
    [Output(f'loading11-output-{type_page}', 'children'),
     Output(f'script11-output-{type_page}', 'children')],
    [Input(f'run-script11-button-{type_page}', 'n_clicks')],
    [State(f'loading11-output-{type_page}', 'children'),
     State(f'script11-output-{type_page}', 'children')]
)
def run_script_callback(n_clicks, loading_children, script_output_children):
    path_script = r"files\to_database\obr_doc_to_database.py"
    return run_script(n_clicks, loading_children, script_output_children, path_script)


@app.callback(
    Output('color-indicator1', 'color'),
    Output('color-indicator2', 'color'),
    Output('color-indicator3', 'color'),
    Output('color-indicator4', 'color'),
    Output('color-indicator5', 'color'),
    Output('color-indicator6', 'color'),
    Output('color-indicator7', 'color'),
    Output('color-indicator8', 'color'),
    Output('color-indicator9', 'color'),
    Output('color-indicator10', 'color'),
    Output('color-indicator11', 'color'),
    [Input('run-script-button', 'n_clicks')],
)
def update_color_indicator(n_clicks):
    def indicator_files(n_click, file_in_bd, file_for_bd):
        if n_click is None:
            return ''
        else:
            if file_in_bd == file_for_bd:
                return "success"  # Зеленый цвет (успех)
            else:
                return "danger"  # Красный цвет (опасность)

    return \
        indicator_files(n_clicks, query_last_record_sql('oms_log'), last_file_csv_in_directory(file_path_oms[0])), \
            indicator_files(n_clicks, query_last_record_sql('people_log'),
                            last_file_csv_in_directory(file_path_oms[1])), \
            indicator_files(n_clicks, query_last_record_sql('iszl_log'), last_file_csv_in_directory(file_path_oms[2])), \
            indicator_files(n_clicks, query_last_record_sql('emd_log'), last_file_csv_in_directory(file_path_oms[3])), \
            indicator_files(n_clicks, query_last_record_sql('doctors_oms_log'),
                            last_file_csv_in_directory(file_path_oms[4])), \
            indicator_files(n_clicks, query_last_record_sql('area_log'), last_file_csv_in_directory(file_path_oms[5])), \
            indicator_files(n_clicks, query_last_record_sql(dn), last_file_csv_in_directory(file_path_oms[6])), \
            indicator_files(n_clicks, query_last_record_sql('obr_proc_log'),
                            last_file_csv_in_directory(file_path_oms[7])), \
            indicator_files(n_clicks, query_last_record_sql('detail_dd_log'),
                            last_file_csv_in_directory(file_path_oms[8])), \
            indicator_files(n_clicks, query_last_record_sql('obr_proc_log'),
                            last_file_csv_in_directory(file_path_oms[9])), \
            indicator_files(n_clicks, query_last_record_sql('ln_log'),
                            last_file_csv_in_directory(file_path_oms[10]))

@app.callback(
    Output("file1-in-bd", "children"),
    Output("file1-for-bd", "children"),
    Input('run-script-button', 'n_clicks')
)


def update_text(n_clicks):
    return update_info_file(n_clicks, query_last_record_sql('oms_log'), last_file_csv_in_directory(file_path_oms[0]))


@app.callback(
    Output("file2-in-bd", "children"),
    Output("file2-for-bd", "children"),
    Input('run-script-button', 'n_clicks')
)
def update_text(n_clicks):
    return update_info_file(n_clicks, query_last_record_sql('people_log'), last_file_csv_in_directory(file_path_oms[1]))


@app.callback(
    Output("file3-in-bd", "children"),
    Output("file3-for-bd", "children"),
    Input('run-script-button', 'n_clicks')
)
def update_text(n_clicks):
    return update_info_file(n_clicks, query_last_record_sql('iszl_log'), last_file_csv_in_directory(file_path_oms[2]))


@app.callback(
    Output("file4-in-bd", "children"),
    Output("file4-for-bd", "children"),
    Input('run-script-button', 'n_clicks')
)
def update_text(n_clicks):
    return update_info_file(n_clicks, query_last_record_sql('emd_log'), last_file_csv_in_directory(file_path_oms[3]))


@app.callback(
    Output("file5-in-bd", "children"),
    Output("file5-for-bd", "children"),
    Input('run-script-button', 'n_clicks')
)
def update_text(n_clicks):
    return update_info_file(n_clicks, query_last_record_sql('doctors_oms_log'),
                            last_file_csv_in_directory(file_path_oms[4]))


@app.callback(
    Output("file6-in-bd", "children"),
    Output("file6-for-bd", "children"),
    Input('run-script-button', 'n_clicks')
)
def update_text(n_clicks):
    return update_info_file(n_clicks, query_last_record_sql('area_log'), last_file_csv_in_directory(file_path_oms[5]))


@app.callback(
    Output("file7-in-bd", "children"),
    Output("file7-for-bd", "children"),
    Input('run-script-button', 'n_clicks')
)
def update_text(n_clicks):
    return update_info_file(n_clicks, query_last_record_sql(dn), last_file_csv_in_directory(file_path_oms[6]))


@app.callback(
    Output("file8-in-bd", "children"),
    Output("file8-for-bd", "children"),
    Input('run-script-button', 'n_clicks')
)
def update_text(n_clicks):
    return update_info_file(n_clicks, query_last_record_sql('obr_proc_log'),
                            last_file_csv_in_directory(file_path_oms[7]))


@app.callback(
    Output("file9-in-bd", "children"),
    Output("file9-for-bd", "children"),
    Input('run-script-button', 'n_clicks')
)
def update_text(n_clicks):
    return update_info_file(n_clicks, query_last_record_sql('detail_dd_log'),
                            last_file_csv_in_directory(file_path_oms[8]))


def update_info_file(n_clicks, def1, def2):
    if n_clicks is None:
        return "Последний файл загруженный в БД:", "Последний файл для загрузки в БД:"
    updated_text1 = f"Последний файл загруженный в БД: {def1}"
    updated_text2 = f"Последний файл для загрузки в БД: {def2}"
    return updated_text1, updated_text2


folder_path = r'\\10.136.29.166\_it_reports\Download ISZL'


@app.callback(
    dependencies.Output('open-folder-button', 'n_clicks'),
    [dependencies.Input('open-folder-button', 'n_clicks')]
)
def open_folder_in_explorer(n_clicks):
    if n_clicks is not None:
        try:
            # Открываем папку в проводнике
            os.startfile(folder_path)
        except Exception as e:
            return f'Ошибка при открытии папки: {str(e)}'
    return n_clicks
