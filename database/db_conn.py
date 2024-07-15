# db_conn.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from database.db_settings import DATABASE_URL

# Создаем подключение к базе данных
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Создаем сессию для взаимодействия с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Функция для инициализации базы данных
def init_db():
    Base.metadata.create_all(bind=engine)
