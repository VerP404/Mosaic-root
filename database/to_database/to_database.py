import glob
import os
import pandas as pd
import datetime


def lastfile(pathoms: str):
    list_of_files = glob.glob(pathoms)
    if not list_of_files:
        raise FileNotFoundError(f"Файлы, соответствующие шаблону {pathoms}, не найдены.")
    latest_file_oms = max(list_of_files, key=os.path.getctime)
    file_name = os.path.basename(latest_file_oms)
    return [latest_file_oms, file_name]


def network_folder(folder, n_f):
    if os.path.exists(folder):
        print("Сетевая папка доступна.")
        return os.path.join(folder, n_f)
    else:
        print("Сетевая папка недоступна.")
        return None


def upload_file_in_database(conn, schema, name_table, latest_file, type_text):
    # Подгрузка файла ОМС
    if type_text == 'ОМС':
        df = pd.read_csv(latest_file, sep=';', low_memory=False, na_values="-", dtype='str')
        df.to_sql(name_table, con=conn, schema=schema, if_exists='replace', index=False)
        return df
    if type_text == 'Детализация':
        df = pd.read_csv(latest_file, sep=';', low_memory=False, dtype='str')
        df.to_sql('oms.detailed_data', con=conn, schema=schema, if_exists='replace', index=False)
        return df
    if type_text == 'врач':
        df = pd.read_csv(latest_file, sep=';', low_memory=False, dtype='str')
        df.to_sql('oms.doctors_oms_data', con=conn, schema=schema, if_exists='replace', index=False)
        return df
    if type_text == 'население':
        df = pd.read_csv(latest_file, sep=';', low_memory=False, dtype='str')
        df = df.replace('`', '', regex=True)
        df.to_sql('people_data', con=conn, schema=schema, if_exists='replace', index=False)
        return df
    if type_text == '168н':
        df = pd.read_csv(latest_file, sep=';', low_memory=False, dtype='str')
        df.to_sql('168n_data', con=conn, schema=schema, if_exists='replace', index=False)
        return df
    if type_text == 'План':
        df = pd.read_csv(latest_file, sep=';', low_memory=False)
        df.to_sql('plan', con=conn, schema=schema, if_exists='replace', index=False)
        return df
    if type_text == 'ЭМД':
        df = pd.read_csv(latest_file, sep=';', low_memory=False, dtype='str', encoding='cp1251')
        df.to_sql('emd_data', con=conn, schema=schema, if_exists='replace', index=False)
        return df
    if type_text == 'участки':
        df = pd.read_csv(latest_file, sep=';', low_memory=False, dtype='str')
        df = df.replace('`', '', regex=True)
        df.to_sql('area_data', con=conn, schema=schema, if_exists='replace', index=False)
        return df
    if type_text == 'ИСЗЛ':
        df = pd.read_csv(latest_file, sep=';', dtype='str', encoding='cp1251', low_memory=False)
        df = df.replace('`', '', regex=True)
        # Удаляем дубликаты по id записи
        df = df.drop_duplicates(subset=['ldwID'])
        df.to_sql('iszl_data', con=conn, schema=schema, if_exists='replace', index=False)
        return df
    if type_text == 'Процедуры':
        script_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.abspath(os.path.join(script_dir, '..', '..', 'files', 'kvazar', 'obrproc_data'))
        all_data = pd.DataFrame()
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                df = pd.read_csv(file_path, sep=';', low_memory=False, dtype='str', encoding='cp1251')
                all_data = pd.concat([all_data, df], ignore_index=True)
        all_data = all_data.drop_duplicates()
        all_data.to_sql('obrproc', con=conn, schema=schema, if_exists='replace', index=False)
        return all_data
    if type_text == 'Обращения':
        script_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.abspath(os.path.join(script_dir, '..', '..', 'files', 'kvazar', 'obrdoc_data'))
        all_data = pd.DataFrame()
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                df = pd.read_csv(file_path, sep=';', low_memory=False, dtype='str', encoding='cp1251')
                all_data = pd.concat([all_data, df], ignore_index=True)
        all_data = all_data.drop_duplicates()
        all_data.to_sql('obrdoc', con=conn, schema=schema, if_exists='replace', index=False)
        return all_data
    if type_text == 'ЛН':
        script_dir = os.path.dirname(os.path.abspath(__file__))
        folder_path = os.path.abspath(os.path.join(script_dir, '..', '..', 'files', 'kvazar', 'ln_data'))
        all_data = pd.DataFrame()
        for filename in os.listdir(folder_path):
            if filename.endswith(".csv"):
                file_path = os.path.join(folder_path, filename)
                df = pd.read_csv(file_path, sep=';', low_memory=False, dtype='str', encoding='cp1251')
                all_data = pd.concat([all_data, df], ignore_index=True)
        all_data = all_data.drop_duplicates()
        all_data.to_sql('ln_data', con=conn, schema=schema, if_exists='replace', index=False)
        return all_data


def upload_info_log_in_database(conn, df, name_last_file, type_text, schema, name_table_db_log):
    # Подгрузка сведений о выгрузке в БД
    # Подготовка данных
    df_log = pd.DataFrame(columns=['File_name', 'File_date', 'Count', 'name_text'])
    date_time = datetime.datetime.today().strftime("%d-%m-%Y %H:%M")
    df_log.loc[0, 'File_name'] = name_last_file
    df_log.loc[0, 'File_date'] = date_time
    df_log.loc[0, 'Count'] = len(df)
    # Преобразование даты и времени в требуемый формат
    date_time_str = name_last_file.split("на ")[1].split(".")[0]
    date_time = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H_%M")
    formatted_date = date_time.strftime("%d.%m.%Y")
    formatted_time = date_time.strftime("%H:%M")
    # Формирование новой строки
    output_string = f"Выгрузка {type_text} на {formatted_date} {formatted_time}"
    df_log.loc[0, 'name_text'] = output_string
    # выгрузка в БД
    try:
        df_log.to_sql(name_table_db_log, schema=schema, con=conn, if_exists='append', index=False)
    except:
        df_log.to_sql(name_table_db_log, schema=schema, con=conn, if_exists='replace', index=False)
    return output_string


def to_database(conn, folder_path, name_file, type_text, schema, name_table, name_table_db_log):
    # Проверка доступности сетевой папки и возврат пути до папки с заданным шаблоном поиска файла
    path_file = network_folder(folder_path, name_file)
    if path_file is None:
        raise FileNotFoundError(f"Сетевая папка недоступна: {folder_path}")
    # Возвращаем полный путь к последнему файлу выгрузки и имя файла
    path_latest_file, name_last_file = lastfile(path_file)
    # загружаем данные в базу данных и возвращаем датафрейм
    upload_df = upload_file_in_database(conn, schema, name_table, path_latest_file, type_text)
    print(f"Файл {type_text} подгружен: количество строк -> {len(upload_df)}")
    # загружаем данные о выгрузке в базу данных и возвращаем информацию о загруженном файле
    output_string_log = upload_info_log_in_database(conn, upload_df, name_last_file, type_text, schema,
                                                    name_table_db_log)
    # print(output_string_log)
