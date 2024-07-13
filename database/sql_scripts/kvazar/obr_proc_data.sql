create table kvazar.obr_proc_data
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
    "Процедура"       text,
    "Дата приема"     text,
    "Дата записи"     text,
    "Тип расписания"  text,
    "Источник записи" text,
    "Подразделение"   text,
    "Создавший"       text,
    "Не явился"       text,
    "ЭПМЗ"            text
);

alter table kvazar.obr_proc_data
    owner to postgres;

