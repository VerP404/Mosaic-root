create table kvazar.obr_doc_data
(
    "Фамилия"         text,
    "Имя"             text,
    "Отчество"        text,
    "Дата рождения"   text,
    "Пол"             text,
    "Телефон"         text,
    "ЕНП"             text,
    "Прикрепление"    text,
    "Серия"           text,
    "Номер"           text,
    "Фамилия.1"       text,
    "Имя.1"           text,
    "Отчество.1"      text,
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

alter table kvazar.obr_doc_data
    owner to postgres;

