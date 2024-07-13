create table kvazar.emd_data
(
    "Фамилия"         text,
    "Имя"             text,
    "Отчество"        text,
    "Дата рождения"   text,
    "Пол"             text,
    "Прикрепление"    text,
    "Серия"           text,
    "Номер"           text,
    "Столбец1"        text,
    "Фамилия_1"       text,
    "Имя_2"           text,
    "Отчество_3"      text,
    "Должность"       text,
    "Дата приема"     text,
    "Дата записи"     text,
    "Тип расписания"  text,
    "Источник записи" text,
    "Подразделение"   text,
    "Создавший"       text,
    "Не явился"       text,
    "ЭПМЗ"            text
);

alter table kvazar.emd_data
    owner to postgres;

