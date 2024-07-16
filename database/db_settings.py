# Настройки подключения рутового пользователя PostgreSQL
ROOT_DATABASE = {
    'dbname': 'postgres',
    'user': 'postgres',
    'password': 'Qaz123',
    'host': 'localhost',
    'port': '5432',
}

# Настройки целевой базы данных
PRODUCT_DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mosaic_db',
        'USER': 'mosaic_db',
        'PASSWORD': '440856Mo',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

DB_NAME = PRODUCT_DATABASES['default']['NAME']
DB_USER = PRODUCT_DATABASES['default']['USER']
DB_PASSWORD = PRODUCT_DATABASES['default']['PASSWORD']
DB_HOST = PRODUCT_DATABASES['default']['HOST']
DB_PORT = PRODUCT_DATABASES['default']['PORT']
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
