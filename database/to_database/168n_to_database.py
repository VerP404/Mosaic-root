from database.db_conn import engine
from to_database import to_database
import os

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.abspath(os.path.join(script_dir, '..', '..', 'files', 'info', 'dn168n_data'))
    name_file = r'Выгрузка 168н*.csv'
    type_text = '168н'
    schema = 'info'
    name_table = 'dn168n_data'
    name_table_db_log = 'dn_168n_log'

    try:
        to_database(engine, folder_path, name_file, type_text, name_table, name_table_db_log)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
