import os
import psycopg2
from psycopg2 import sql
from db_settings import ROOT_DATABASE, PRODUCT_DATABASES


def create_database_and_user():
    conn = psycopg2.connect(
        dbname=ROOT_DATABASE['dbname'],
        user=ROOT_DATABASE['user'],
        password=ROOT_DATABASE['password'],
        host=ROOT_DATABASE['host'],
        port=ROOT_DATABASE['port']
    )
    conn.autocommit = True

    try:
        with conn.cursor() as cur:
            cur.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s;")
                        .format(sql.Identifier(PRODUCT_DATABASES['default']['USER'])),
                        (PRODUCT_DATABASES['default']['PASSWORD'],))
            cur.execute(sql.SQL("CREATE DATABASE {} WITH OWNER = %s;")
                        .format(sql.Identifier(PRODUCT_DATABASES['default']['NAME'])),
                        (PRODUCT_DATABASES['default']['USER'],))

        print("База данных и пользователь успешно созданы.")
    except psycopg2.Error as e:
        print(f"Ошибка при создании базы данных и пользователя: {e}")
    finally:
        if conn:
            conn.close()


def execute_sql_scripts():
    conn = psycopg2.connect(
        dbname=PRODUCT_DATABASES['default']['NAME'],
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
                if filename.endswith('.sql') and filename != 'schemas.sql':
                    file_path = os.path.join(root, filename)
                    execute_sql_file(cursor, file_path)

    try:
        with conn.cursor() as cur:
            sql_scripts_directory = os.path.join(os.path.dirname(__file__), 'sql_scripts')
            schemas_sql_path = os.path.join(sql_scripts_directory, 'schemas.sql')
            if os.path.isfile(schemas_sql_path):
                execute_sql_file(cur, schemas_sql_path)
            execute_sql_scripts_from_directory(cur, sql_scripts_directory)
    except psycopg2.Error as e:
        print(f"Ошибка при создании схем или таблиц: {e}")
    finally:
        if conn:
            conn.close()


def grant_privileges():
    conn = psycopg2.connect(
        dbname=PRODUCT_DATABASES['default']['NAME'],
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
                sql.Identifier(PRODUCT_DATABASES['default']['USER'])
            )
        )
        cursor.execute(
            sql.SQL("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA {} TO {};").format(
                sql.Identifier(schema_name),
                sql.Identifier(PRODUCT_DATABASES['default']['USER'])
            )
        )
        cursor.execute(
            sql.SQL("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA {} TO {};").format(
                sql.Identifier(schema_name),
                sql.Identifier(PRODUCT_DATABASES['default']['USER'])
            )
        )
        cursor.execute(
            sql.SQL("ALTER DEFAULT PRIVILEGES IN SCHEMA {} GRANT ALL PRIVILEGES ON TABLES TO {};").format(
                sql.Identifier(schema_name),
                sql.Identifier(PRODUCT_DATABASES['default']['USER'])
            )
        )
        cursor.execute(
            sql.SQL("ALTER DEFAULT PRIVILEGES IN SCHEMA {} GRANT ALL PRIVILEGES ON SEQUENCES TO {};").format(
                sql.Identifier(schema_name),
                sql.Identifier(PRODUCT_DATABASES['default']['USER'])
            )
        )
    print(f"Привилегии предоставлены пользователю {PRODUCT_DATABASES['default']['USER']} на все схемы")


if __name__ == "__main__":
    create_database_and_user()
    execute_sql_scripts()
    grant_privileges()
