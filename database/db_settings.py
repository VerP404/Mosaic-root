# Настройки подключения рутового пользователя PostgreSQL
ROOT_DATABASE = {
    'dbname': 'mosaic_db',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432',
}

DB_NAME = ROOT_DATABASE['dbname']
DB_USER = ROOT_DATABASE['user']
DB_PASSWORD = ROOT_DATABASE['password']
DB_HOST = ROOT_DATABASE['host']
DB_PORT = ROOT_DATABASE['port']
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
