sqlquery_people_reproductive = """
with nas as (select people_data."FIO",
                    people_data."DR",
                    people_data."ENP",
                    people_data."LPUUCH",
                    area_data."Корпус",
                    area_data."Врач",
                    EXTRACT(YEAR FROM CURRENT_DATE) -
                    CAST(substring("DR" FROM LENGTH("DR") - 3) AS integer) as "Возраст",

                    case
                        when "FIO" like any
                             (array ['%НА','%на', '%ЫЗЫ', '%ызы', '%а', '%я', '%А', '%Я', '%а ', '%я ', '%А ', '%Я '])
                            then 'ж'
                        when "FIO" like any (array ['%ИЧ','%ич', '%ГЛЫ', '%глы']) then 'м'
                        else 'м' end                                       as "пол"

             from people_data
                      left join area_data on people_data."LPUUCH" = area_data."Участок"),

     nas_gr as (select *,
                       case
                           when "Возраст" >= 18 and "Возраст" <= 29 then '18-29'
                           when "Возраст" >= 30 and "Возраст" <= 49 then '30-49'
                           else '-'
                           end as "Группа"
                from nas),

     iszl_nas as (select "Корпус",
                         "LPUUCH",
                         count(*)                                                            as "Всего",
                         sum(case when пол = 'ж' then 1 else 0 end)                          as "ж",
                         sum(case when пол = 'м' then 1 else 0 end)                          as "м",
                         sum(case when "Группа" = '18-29' then 1 else 0 end)                 as "18-29",
                         sum(case when (пол = 'ж' and "Группа" = '18-29') then 1 else 0 end) as "18-29 ж",
                         sum(case when (пол = 'м' and "Группа" = '18-29') then 1 else 0 end) as "18-29 м",
                         sum(case when "Группа" = '30-49' then 1 else 0 end)                 as "30-49",
                         sum(case when (пол = 'ж' and "Группа" = '30-49') then 1 else 0 end) as "30-49 ж",
                         sum(case when (пол = 'м' and "Группа" = '30-49') then 1 else 0 end) as "30-49 м"

                  from nas_gr
                  where "Группа" in ('18-29', '30-49')
                  group by "Корпус", "LPUUCH")

select iszl_nas."LPUUCH",
       iszl_nas."Всего",
       iszl_nas."ж",
       iszl_nas."м",
       iszl_nas."18-29",
       iszl_nas."18-29 ж",
       iszl_nas."18-29 м",
       iszl_nas."30-49",
       iszl_nas."30-49 ж",
       iszl_nas."30-49 м"
from iszl_nas
where "Корпус" = :korp
union all
select 'Итого',
       count(*)                                                            as "Всего",
       sum(case when пол = 'ж' then 1 else 0 end)                          as "ж",
       sum(case when пол = 'м' then 1 else 0 end)                          as "м",
       sum(case when "Группа" = '18-29' then 1 else 0 end)                 as "18-29",
       sum(case when (пол = 'ж' and "Группа" = '18-29') then 1 else 0 end) as "18-29 ж",
       sum(case when (пол = 'м' and "Группа" = '18-29') then 1 else 0 end) as "18-29 м",
       sum(case when "Группа" = '30-49' then 1 else 0 end)                 as "30-49",
       sum(case when (пол = 'ж' and "Группа" = '30-49') then 1 else 0 end) as "30-49 ж",
       sum(case when (пол = 'м' and "Группа" = '30-49') then 1 else 0 end) as "30-49 м"
from nas_gr
where "Корпус" = :korp and "Группа" in ('18-29', '30-49')
order by "LPUUCH"
"""

sqlquery_people_reproductive_all = """
with nas as (select people_data."FIO",
                    people_data."DR",
                    people_data."ENP",
                    people_data."LPUUCH",
                    area_data."Корпус",
                    area_data."Врач",
                    EXTRACT(YEAR FROM CURRENT_DATE) -
                    CAST(substring("DR" FROM LENGTH("DR") - 3) AS integer) as "Возраст",

                    case
                        when "FIO" like any
                             (array ['%НА','%на', '%ЫЗЫ', '%ызы', '%а', '%я', '%А', '%Я', '%а ', '%я ', '%А ', '%Я '])
                            then 'ж'
                        when "FIO" like any (array ['%ИЧ','%ич', '%ГЛЫ', '%глы']) then 'м'
                        else 'м' end                                       as "пол"

             from people_data
                      left join area_data on people_data."LPUUCH" = area_data."Участок"),

     nas_gr as (select *,
                       case
                           when "Возраст" >= 18 and "Возраст" <= 29 then '18-29'
                           when "Возраст" >= 30 and "Возраст" <= 49 then '30-49'
                           else '-'
                           end as "Группа"
                from nas),

     iszl_nas as (select "Корпус",
                         count(*)                                                            as "Всего",
                         sum(case when пол = 'ж' then 1 else 0 end)                          as "ж",
                         sum(case when пол = 'м' then 1 else 0 end)                          as "м",
                         sum(case when "Группа" = '18-29' then 1 else 0 end)                 as "18-29",
                         sum(case when (пол = 'ж' and "Группа" = '18-29') then 1 else 0 end) as "18-29 ж",
                         sum(case when (пол = 'м' and "Группа" = '18-29') then 1 else 0 end) as "18-29 м",
                         sum(case when "Группа" = '30-49' then 1 else 0 end)                 as "30-49",
                         sum(case when (пол = 'ж' and "Группа" = '30-49') then 1 else 0 end) as "30-49 ж",
                         sum(case when (пол = 'м' and "Группа" = '30-49') then 1 else 0 end) as "30-49 м"

                  from nas_gr
                  where "Группа" in ('18-29', '30-49')
                  group by "Корпус")

select iszl_nas."Корпус",
       iszl_nas."Всего",
       iszl_nas."ж",
       iszl_nas."м",
       iszl_nas."18-29",
       iszl_nas."18-29 ж",
       iszl_nas."18-29 м",
       iszl_nas."30-49",
       iszl_nas."30-49 ж",
       iszl_nas."30-49 м"
from iszl_nas
union all
select 'Итого',
       count(*)                                                            as "Всего",
       sum(case when пол = 'ж' then 1 else 0 end)                          as "ж",
       sum(case when пол = 'м' then 1 else 0 end)                          as "м",
       sum(case when "Группа" = '18-29' then 1 else 0 end)                 as "18-29",
       sum(case when (пол = 'ж' and "Группа" = '18-29') then 1 else 0 end) as "18-29 ж",
       sum(case when (пол = 'м' and "Группа" = '18-29') then 1 else 0 end) as "18-29 м",
       sum(case when "Группа" = '30-49' then 1 else 0 end)                 as "30-49",
       sum(case when (пол = 'ж' and "Группа" = '30-49') then 1 else 0 end) as "30-49 ж",
       sum(case when (пол = 'м' and "Группа" = '30-49') then 1 else 0 end) as "30-49 м"
from nas_gr
where  "Группа" in ('18-29', '30-49')
"""


def sqlquery_people_reproductive_tab2(sql_cond=None):
    return f"""
        select
               COALESCE("Подразделение", 'Итого') AS "Подразделение",
               sum(case when "Статус" in ('1', '2', '3', '4', '5', '6', '7', '8', '12') then 1 else 0 end)         as "Всего",
               sum(case when "Статус" in ('1', '2', '3', '4', '6', '8') then 1 else 0 end)                   as "В работе",
               sum(case when "Статус" = '3' then 1 else 0 end)                                  as Оплачено,
               sum(case when "Статус" = '2' or "Статус" = '1' then 1 else 0 end)                  as "В ТФОМС",
               sum(case when "Статус" = '5' or "Статус" = '7' or "Статус" = '12' then 1 else 0 end) as "Отказано",
               sum(case when "Статус" = '6' or "Статус" = '8' then 1 else 0 end)                  as "Исправлен",
               sum(case when "Статус" = '1' then 1 else 0 end)                                  as "1",
               sum(case when "Статус" = '2' then 1 else 0 end)                                  as "2",
               sum(case when "Статус" = '3' then 1 else 0 end)                                  as "3",
               sum(case when "Статус" = '4' then 1 else 0 end)                                  as "4",
               sum(case when "Статус" = '5' then 1 else 0 end)                                  as "5",
               sum(case when "Статус" = '6' then 1 else 0 end)                                  as "6",
               sum(case when "Статус" = '7' then 1 else 0 end)                                  as "7",
               sum(case when "Статус" = '8' then 1 else 0 end)                                  as "8",
               sum(case when "Статус" = '12' then 1 else 0 end)                                 as "12"
        from oms_data
        where "Цель" = 'ДР1'
            and "Тариф" != '0'
            and "Пол" = :text_1
        AND (("Номер счёта" LIKE :update_value_month) {sql_cond} )
        GROUP BY ROLLUP("Подразделение")
        """


sqlquery_people_reproductive_tab3 = """
with DR as ( select EXTRACT(YEAR FROM CURRENT_DATE) -
                    CAST(substring("Дата рождения" FROM LENGTH("Дата рождения") - 3) AS integer) as "Возраст",
    "Талон",
    "Статус",
    "Пациент",
    "Дата рождения",
    "Пол",
    "Цель",
    "ЕНП",
    "Начало лечения",
    "Окончание лечения",
    "Врач",
    "Подразделение",
        SUBSTRING("Диагноз основной (DS1)", 1, POSITION(' ' IN "Диагноз основной (DS1)") - 1) AS "DS1",
        SUBSTRING("Сопутствующий диагноз (DS2)", 1, POSITION(' ' IN "Сопутствующий диагноз (DS2)") - 1) AS "DS2"
from oms_data
where "Цель" = 'ДР1'),
    DV_OPV as (
        select EXTRACT(YEAR FROM CURRENT_DATE) -
                    CAST(substring("Дата рождения" FROM LENGTH("Дата рождения") - 3) AS integer) as "Возраст",
    "Талон",
    "Статус",
    "Пациент",
    "Дата рождения",
    "Пол",
    "Цель",
    "ЕНП",
    "Начало лечения",
    "Окончание лечения",
    "Врач",
    "Подразделение",
        SUBSTRING("Диагноз основной (DS1)", 1, POSITION(' ' IN "Диагноз основной (DS1)") - 1) AS "DS1",
        SUBSTRING("Сопутствующий диагноз (DS2)", 1, POSITION(' ' IN "Сопутствующий диагноз (DS2)") - 1) AS "DS2"
from oms_data
where "Цель" in ('ДВ4', 'ОПВ') and "Статус" = '3'
    ),
    itog as (
        select DV_OPV."Пациент",
               DV_OPV."Дата рождения",
               DV_OPV."Возраст",
               DV_OPV."ЕНП",
               DV_OPV."Пол",
               DV_OPV."Цель",
               DV_OPV."Окончание лечения",
               DV_OPV."Врач",
               DV_OPV."Подразделение",
               case when DR."Цель" = 'ДР1' then 'да' else 'нет' end as "Статус ДР",
               DR."DS1"
        from DV_OPV left join DR on DV_OPV."ЕНП" = DR."ЕНП"
    )

select *
from itog
where "Возраст" > 17 and "Возраст" < 50
order by "Пациент"
"""
