import os
import sys
from psycopg2 import sql
import psycopg2

# Добавляем родительский каталог в путь поиска модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.db_settings import ROOT_DATABASE, PRODUCT_DATABASES

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
            # Проверка существования пользователя
            cur.execute("SELECT 1 FROM pg_roles WHERE rolname = %s;", (PRODUCT_DATABASES['default']['USER'],))
            if not cur.fetchone():
                cur.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s;")
                            .format(sql.Identifier(PRODUCT_DATABASES['default']['USER'])),
                            (PRODUCT_DATABASES['default']['PASSWORD'],))
            else:
                print(f"Пользователь {PRODUCT_DATABASES['default']['USER']} уже существует.")

            # Проверка существования базы данных
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (PRODUCT_DATABASES['default']['NAME'],))
            if not cur.fetchone():
                cur.execute(sql.SQL("CREATE DATABASE {} WITH OWNER = %s;")
                            .format(sql.Identifier(PRODUCT_DATABASES['default']['NAME'])),
                            (PRODUCT_DATABASES['default']['USER'],))
            else:
                print(f"База данных {PRODUCT_DATABASES['default']['NAME']} уже существует.")

        print("База данных и пользователь успешно созданы или уже существовали.")
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


def create_users_schema():
    conn = psycopg2.connect(
        dbname=PRODUCT_DATABASES['default']['NAME'],
        user=ROOT_DATABASE['user'],
        password=ROOT_DATABASE['password'],
        host=ROOT_DATABASE['host'],
        port=ROOT_DATABASE['port']
    )
    conn.autocommit = True

    users_schema_sql = """
    CREATE SCHEMA IF NOT EXISTS users;

    CREATE TABLE IF NOT EXISTS users.user (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        hashed_password VARCHAR(255) NOT NULL,
        last_name VARCHAR(255) NOT NULL,
        first_name VARCHAR(255) NOT NULL,
        middle_name VARCHAR(255),
        birth_date DATE,
        position VARCHAR(255),
        role VARCHAR(255) NOT NULL,
        category VARCHAR(255)
    );

    CREATE TABLE IF NOT EXISTS users.roles (
        id SERIAL PRIMARY KEY,
        role_name VARCHAR(255) UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS users.categories (
        id SERIAL PRIMARY KEY,
        category_name VARCHAR(255) UNIQUE NOT NULL
    );
    """

    try:
        with conn.cursor() as cur:
            cur.execute(users_schema_sql)
            print("Схема users и таблицы созданы успешно.")
    except psycopg2.Error as e:
        print(f"Ошибка при создании схемы users или таблиц: {e}")
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
    create_users_schema()
    execute_sql_scripts()
    grant_privileges()
