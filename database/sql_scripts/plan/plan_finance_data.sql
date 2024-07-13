create table plan.plan_finance_data
(
    "Год"             bigint,
    "Группа"          text,
    "Тип"             text,
    "Корпус"          text,
    "Январь_талон"    bigint,
    "Январь_финанс"   numeric(20, 2),
    "Февраль_талон"   bigint,
    "Февраль_финанс"  numeric(20, 2),
    "Март_талон"      bigint,
    "Март_финанс"     numeric(20, 2),
    "Апрель_талон"    bigint,
    "Апрель_финанс"   numeric(20, 2),
    "Май_талон"       bigint,
    "Май_финанс"      numeric(20, 2),
    "Июнь_талон"      bigint,
    "Июнь_финанс"     numeric(20, 2),
    "Июль_талон"      bigint,
    "Июль_финанс"     numeric(20, 2),
    "Август_талон"    bigint,
    "Август_финанс"   numeric(20, 2),
    "Сентябрь_талон"  bigint,
    "Сентябрь_финанс" numeric(20, 2),
    "Октябрь_талон"   bigint,
    "Октябрь_финанс"  numeric(20, 2),
    "Ноябрь_талон"    bigint,
    "Ноябрь_финанс"   numeric(20, 2),
    "Декабрь_талон"   bigint,
    "Декабрь_финанс"  numeric(20, 2)
);

alter table plan.plan_finance_data
    owner to postgres;

