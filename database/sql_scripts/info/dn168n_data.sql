create table info.dn168n_data
(
    "Код МКБ"                  text,
    "Профиль"                  text,
    "Специальность"            text,
    "Специальность совместная" text
);

alter table info.dn168n_data
    owner to postgres;

