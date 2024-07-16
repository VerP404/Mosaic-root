from database.db_conn import engine
from to_database import to_database
import os

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.abspath(os.path.join(script_dir, '..', '..', 'files', 'iszl', 'iszl_data'))
    name_file = r'Выгрузка ИСЗЛ *.csv'
    type_text = 'ИСЗЛ'
    schema = 'iszl'
    name_table = 'iszl_data'
    name_table_db_log = 'iszl_log'

    try:
        to_database(engine, folder_path, name_file, type_text, schema, name_table, name_table_db_log)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
