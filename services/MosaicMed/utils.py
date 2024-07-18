from sqlalchemy import text
from datetime import datetime

current_year = datetime.now().year

months_labels = {
    1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь', 7: 'Июль',
    8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
}

months_sql_labels = {
    1: 'Января', 2: 'Февраля', 3: 'Марта', 4: 'Апреля', 5: 'Мая', 6: 'Июня', 7: 'Июля',
    8: 'Августа', 9: 'Сентября', 10: 'Октября', 11: 'Ноября', 12: 'Декабря'
}


# Получаем список специальностей
def get_extracted_names_list_specialist(engine, sql_query):
    with engine.connect() as conn:
        query = text(sql_query)
        result = conn.execute(query)
        extracted_names_list = [row[0] for row in result.fetchall()]
        return extracted_names_list


# Получаем список врачей для фильтра
def get_extracted_names_list_doctors(engine):
    with engine.connect() as conn:
        sql_query = """
        SELECT DISTINCT
        "Подразделение" || ' ' || split_part("Врач", ' ', 2) || ' ' || left(split_part("Врач", ' ', 3), 1) || '.' || left(split_part("Врач", ' ', 4), 1) || '.' || ' ' ||
        CASE
            WHEN "Врач (Профиль МП)" ~ '\(.*\)' THEN
                substring("Врач (Профиль МП)" from 1 for position('(' in "Врач (Профиль МП)") - 1)
             ELSE
                 "Врач (Профиль МП)"
        END AS extracted_names
        FROM oms.oms_data
        order by extracted_names
        """
        query = text(sql_query)
        result = conn.execute(query)
        extracted_names_list = [row[0] for row in result.fetchall()]
        return extracted_names_list


# Актуальный файл выгрузки ОМС
def last_record_sql(engine):
    sql_query_file_info = """
        SELECT "File_name", "File_date", "Count", "name_text"
        FROM oms.oms_log
        ORDER BY CAST("File_date" AS TIMESTAMP) DESC
        LIMIT 1
    """
    # Получить последнюю запись из базы данных
    with engine.connect() as conn:
        result = conn.execute(text(sql_query_file_info))
        last_record = result.fetchone()
        return last_record
