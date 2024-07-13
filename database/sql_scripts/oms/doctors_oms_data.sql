create table oms.doctors_oms_data
(
    "СНИЛС:"                     text,
    "Код врача:"                 text,
    "Фамилия:"                   text,
    "Имя:"                       text,
    "Отчество:"                  text,
    "Дата рождения:"             text,
    "Пол"                        text,
    "Дата начала работы:"        text,
    "Дата окончания работы:"     text,
    "Структурное подразделение:" text,
    "Код профиля медпомощи:"     text,
    "Код специальности:"         text,
    "Код отделения:"             text,
    "Комментарий:"               text
);

alter table oms.doctors_oms_data
    owner to postgres;

