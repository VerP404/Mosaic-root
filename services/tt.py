import fdb

# Параметры подключения
dsn = '10.136.29.166/3050:D:\\CLINIC.FDB'
user = 'sysdba'
password = 'masterkey'

# Подключение к базе данных
con = fdb.connect(
    dsn=dsn,
    user=user,
    password=password,
    charset='WIN1251'  # Указание кодировки
)

# Создание курсора
cur = con.cursor()

# Выполнение SQL-запроса
cur.execute("SELECT * FROM ANKET_TYPE")

# Получение и вывод результатов
for row in cur.fetchall():
    print(row)

# Закрытие курсора и соединения
cur.close()
con.close()
