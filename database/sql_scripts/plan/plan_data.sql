create table plan.plan_data
(
    год        text,
    "Цель"     text,
    "Корпус"   text,
    "Тип"      text,
    "Январь"   text,
    "Февраль"  text,
    "Март"     text,
    "Апрель"   text,
    "Май"      text,
    "Июнь"     text,
    "Июль"     text,
    "Август"   text,
    "Сентябрь" text,
    "Октябрь"  text,
    "Ноябрь"   text,
    "Декабрь"  text
);

alter table plan.plan_data
    owner to postgres;

