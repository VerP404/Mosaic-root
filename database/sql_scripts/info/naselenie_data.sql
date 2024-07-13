create table info.naselenie_data
(
    "Фамилия"          text,
    "Имя"              text,
    "Отчество"         text,
    "Дата рождения"    text,
    "Пол"              text,
    "ЕНП"              text,
    "Участок"          text,
    "Корпус"           text,
    "Телефон Квазар"   text,
    "Телефон МИС КАУЗ" text,
    "Телефон ИСЗЛ"     text,
    "Адрес Квазар"     text,
    "Адрес МИС КАУЗ 1" text,
    "Адрес МИС КАУЗ 2" text,
    "Адрес ИСЗЛ"       text
);

alter table info.naselenie_data
    owner to postgres;

