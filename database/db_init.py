import os
import sys
import psycopg2
from psycopg2 import sql

# Добавляем родительский каталог в путь поиска модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_settings import ROOT_DATABASE

def create_database_and_user():
    conn = psycopg2.connect(
        dbname='postgres',
        user=ROOT_DATABASE['user'],
        password=ROOT_DATABASE['password'],
        host=ROOT_DATABASE['host'],
        port=ROOT_DATABASE['port']
    )
    conn.autocommit = True

    try:
        with conn.cursor() as cur:
            # Проверка существования базы данных
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (ROOT_DATABASE['dbname'],))
            if not cur.fetchone():
                cur.execute(sql.SQL("CREATE DATABASE {} WITH OWNER = %s;")
                            .format(sql.Identifier(ROOT_DATABASE['dbname'])),
                            (ROOT_DATABASE['user'],))
            else:
                print(f"База данных {ROOT_DATABASE['dbname']} уже существует.")

        print("База данных успешно создана или уже существовала.")
    except psycopg2.Error as e:
        print(f"Ошибка при создании базы данных: {e}")
    finally:
        if conn:
            conn.close()


def execute_sql_scripts():
    conn = psycopg2.connect(
        dbname=ROOT_DATABASE['dbname'],
        user=ROOT_DATABASE['user'],
        password=ROOT_DATABASE['password'],
        host=ROOT_DATABASE['host'],
        port=ROOT_DATABASE['port']
    )
    conn.autocommit = True

    def execute_sql_file(cursor, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
            try:
                cursor.execute(sql_content)
                print(f"Файл {file_path} выполнен успешно")
            except psycopg2.Error as e:
                print(f"Ошибка при выполнении файла: {e}")

    def execute_sql_scripts_from_directory(cursor, directory):
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.sql'):
                    file_path = os.path.join(root, filename)
                    execute_sql_file(cursor, file_path)

    try:
        with conn.cursor() as cur:
            sql_scripts_directory = os.path.join(os.path.dirname(__file__), 'sql_scripts')
            execute_sql_scripts_from_directory(cur, sql_scripts_directory)
    except psycopg2.Error as e:
        print(f"Ошибка при создании схем или таблиц: {e}")
    finally:
        if conn:
            conn.close()


def grant_privileges():
    conn = psycopg2.connect(
        dbname=ROOT_DATABASE['dbname'],
        user=ROOT_DATABASE['user'],
        password=ROOT_DATABASE['password'],
        host=ROOT_DATABASE['host'],
        port=ROOT_DATABASE['port']
    )
    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute(
        "SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT IN ('information_schema', 'pg_catalog');"
    )
    schemas = cursor.fetchall()

    for schema in schemas:
        schema_name = schema[0]
        cursor.execute(
            sql.SQL("GRANT USAGE ON SCHEMA {} TO {};").format(
                sql.Identifier(schema_name),
                sql.Identifier(ROOT_DATABASE['user'])
            )
        )
        cursor.execute(
            sql.SQL("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA {} TO {};").format(
                sql.Identifier(schema_name),
                sql.Identifier(ROOT_DATABASE['user'])
            )
        )
        cursor.execute(
            sql.SQL("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA {} TO {};").format(
                sql.Identifier(schema_name),
                sql.Identifier(ROOT_DATABASE['user'])
            )
        )
        cursor.execute(
            sql.SQL("ALTER DEFAULT PRIVILEGES IN SCHEMA {} GRANT ALL PRIVILEGES ON TABLES TO {};").format(
                sql.Identifier(schema_name),
                sql.Identifier(ROOT_DATABASE['user'])
            )
        )
        cursor.execute(
            sql.SQL("ALTER DEFAULT PRIVILEGES IN SCHEMA {} GRANT ALL PRIVILEGES ON SEQUENCES TO {};").format(
                sql.Identifier(schema_name),
                sql.Identifier(ROOT_DATABASE['user'])
            )
        )

        # Изменение владельца таблиц в схеме
        cursor.execute(
            sql.SQL("SELECT tablename FROM pg_tables WHERE schemaname = %s;"),
            [schema_name]
        )
        tables = cursor.fetchall()
        for table in tables:
            table_name = table[0]
            cursor.execute(
                sql.SQL("ALTER TABLE {}.{} OWNER TO {};").format(
                    sql.Identifier(schema_name),
                    sql.Identifier(table_name),
                    sql.Identifier(ROOT_DATABASE['user'])
                )
            )
    print(f"Привилегии предоставлены пользователю {ROOT_DATABASE['user']} на все схемы и таблицы")


if __name__ == "__main__":
    create_database_and_user()
    execute_sql_scripts()
    grant_privileges()
