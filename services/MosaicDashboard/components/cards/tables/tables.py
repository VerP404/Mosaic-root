# MosaicDashboard/components/tables/tables.py
import pandas as pd
from MosaicDashboard.components.cards.tables.table_utils import generate_table

# Доступность первичной записи к ВОП, терапевтам и педиатрам
data1 = {
    "Корпус": ["Корпус 1", "Корпус 2", "Корпус 3", "Корпус 6", "ДП 1", "ДП 8", "Итого"],
    "Выложено": ["2 975", "1 581", "2 330", "510", "2 122", "1 021", "10 539"],
    "Свободно": ["2 607", "1 449", "1 624", "301", "1 552", "630", "8 163"],
    "% своб.": ["88 %", "92 %", "70 %", "59 %", "73 %", "62 %", "77 %"]
}
# Доступность первичной записи по специальностям
data2 = {
    "Специальность": ["Акушер-гинеколог", "Отоларинголог", "Офтальмолог", "Хирург"],
    "Выложено": ["1 242", "755", "747", "824"],
    "Свободно": ["718", "446", "238", "648"],
    "% своб.": ["58 %", "59 %", "32 %", "79 %"]
}
data3 = {
    "Корпус": ["Корпус 1", "Корпус 2", "Корпус 3", "Корпус 6", "ДП 1", "ДП 8", "Итого"],
    "всего": ["116", "58", "127", "43", "0", "0", "344"],
    "за 7 дней": ["11", "6", "13", "8", "0", "0", "38"],
    "вчера": ["2", "1", "4", "1", "0", "0", "8"]
}
data4 = {
    "Подразделение": ["Ж ГП №11", "Ж ГП №3", "Ж Итого", "М ГП №11", "М ГП №3", "М ОАПП №1", "М Итого", "Итого"],
    "всего": ["286", "739", "1025", "286", "739", "430", "1025", "2050"],
    "В работе": ["286", "723", "1009", "286", "723", "430", "1009", "2018"],
    "Оплачено": ["268", "454", "722", "268", "454", "220", "722", "1444"],
    "В ТФОМС": ["18", "260", "278", "18", "260", "209", "278", "511"],
    "Отказано": ["0", "16", "16", "0", "16", "0", "16", "32"],
    "Отменено": ["0", "9", "9", "0", "9", "1", "9", "18"],
}

card_table_1 = generate_table(pd.DataFrame(data1), max_rows=10)
card_table_2 = generate_table(pd.DataFrame(data2), max_rows=10)
card_table_3 = generate_table(pd.DataFrame(data3), max_rows=10)
card_table_4 = generate_table(pd.DataFrame(data4), max_rows=10)
