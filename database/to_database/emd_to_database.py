from database.db_conn import engine
from to_database import to_database
import os

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.abspath(os.path.join(script_dir, '..', '..', 'files', 'kvazar', 'emd_data'))
    name_file = r'Выгрузка ЭМД*.csv'
    type_text = 'ЭМД'
    schema = 'kvazar'
    name_table = 'emd_data'
    name_table_db_log = 'emd_log'

    try:
        to_database(engine, folder_path, name_file, type_text, schema, name_table, name_table_db_log)
    except Exception as e:
        print(f"Произошла ошибка: {e}")