# Отчет по профосмотрам детским
sql_query_pn = """
    select coalesce("Подразделение", 'Итого')               as Корпус,
           sum(case when "Статус" = '1' then 1 else 0 end)  as Статус_1,
           sum(case when "Статус" = '2' then 1 else 0 end)  as Статус_2,
           sum(case when "Статус" = '3' then 1 else 0 end)  as Статус_3,
           sum(case when "Статус" = '5' then 1 else 0 end)  as Статус_5,
           sum(case when "Статус" = '6' then 1 else 0 end)  as Статус_6,
           sum(case when "Статус" = '7' then 1 else 0 end)  as Статус_7,
           sum(case when "Статус" = '8' then 1 else 0 end)  as Статус_8,
           sum(case when "Статус" = '12' then 1 else 0 end) as Статус_12,
           sum(case when "Статус" = '13' then 1 else 0 end) as Статус_13,
           sum(case when "Статус" = '17' then 1 else 0 end) as Статус_17,
           sum(case when "Статус" = '0' then 1 else 0 end)  as Статус_0,
           sum(case
                   when "Статус" = '0' or "Статус" = '1' or "Статус" = '2' or "Статус" = '3' or "Статус" = '5'
                       or "Статус" = '6' or "Статус" = '7' or "Статус" = '8' or "Статус" = '12' or "Статус" = '13' or
                        "Статус" = '17'
                       then 1
                   else 0 end)                              as Итого
    from oms_data
    where to_date("Первоначальная дата ввода", 'DD-MM-YYYY') BETWEEN to_date(:start_date, 'DD-MM-YYYY') and to_date(:end_date, 'DD-MM-YYYY') 
    and ("Подразделение" like '%ДП%')
      and ("Цель" = 'ПН1')
    group by rollup ("Подразделение")
    order by Корпус DESC
"""

# Отчет по профосмотрам детским
sql_query_ds2 = """
    select coalesce("Подразделение", 'Итого')               as Корпус,
           sum(case when "Статус" = '1' then 1 else 0 end)  as Статус_1,
           sum(case when "Статус" = '2' then 1 else 0 end)  as Статус_2,
           sum(case when "Статус" = '3' then 1 else 0 end)  as Статус_3,
           sum(case when "Статус" = '5' then 1 else 0 end)  as Статус_5,
           sum(case when "Статус" = '6' then 1 else 0 end)  as Статус_6,
           sum(case when "Статус" = '7' then 1 else 0 end)  as Статус_7,
           sum(case when "Статус" = '8' then 1 else 0 end)  as Статус_8,
           sum(case when "Статус" = '12' then 1 else 0 end) as Статус_12,
           sum(case when "Статус" = '13' then 1 else 0 end) as Статус_13,
           sum(case when "Статус" = '17' then 1 else 0 end) as Статус_17,
           sum(case when "Статус" = '0' then 1 else 0 end)  as Статус_0,
           sum(case
                   when "Статус" = '0' or "Статус" = '1' or "Статус" = '2' or "Статус" = '3' or "Статус" = '5'
                       or "Статус" = '6' or "Статус" = '7' or "Статус" = '8' or "Статус" = '12' or "Статус" = '13' or
                        "Статус" = '17' then 1 else 0 end)                              as Итого
    from oms_data
    where to_date("Первоначальная дата ввода", 'DD-MM-YYYY') BETWEEN to_date(:start_date, 'DD-MM-YYYY') and to_date(:end_date, 'DD-MM-YYYY') 
    and ("Подразделение" like '%ДП%')
      and ("Цель" = 'ДС2')
    group by rollup ("Подразделение")
    order by Корпус DESC
"""

# Отчет по уникальным детям в профосмотрах
sql_query_pn_uniq = """
with ss as (select
                ROW_NUMBER() OVER (PARTITION BY "Полис" ORDER BY "Номер счёта") AS rnk,
                case when "Подразделение" = 'ДП №8 К7' then 'ДП №8' else "Подразделение" end as Корпус ,
                *
            from oms_data
            where to_date("Первоначальная дата ввода", 'DD-MM-YYYY') BETWEEN to_date(:start_date, 'DD-MM-YYYY') and to_date(:end_date, 'DD-MM-YYYY')
              and "Цель" = 'ПН1'
              and "Статус" = '3'),
    ff as (select *
           from ss
           where rnk = 1),

    un as (select coalesce(Корпус, 'Итого')                                as Корпус,
           COUNT(DISTINCT "Полис")                                           as Уникальные_дети
    from ff
    group by rollup (Корпус)
    order by Корпус DESC),

    talon as (select coalesce(Корпус, 'Итого')                                as Корпус,
              sum(case when "Цель" = 'ПН1' then 1 else 0 end) as Талоны
    from ss
    group by rollup (Корпус)
    order by Корпус DESC)

select un.Корпус AS "Корпус",
       Талоны,
       Уникальные_дети
from un left join talon on un.Корпус=talon.Корпус
"""


sql_query_pn_uniq_tab2 = """
select COALESCE("Подразделение", 'Итого талонов')                                     AS "Подразделение",
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
where "Цель" = 'ПН1'
      AND "Санкции" is null
  and "Тариф" != '0'
  and (("Номер счёта" LIKE :month) or ("Номер счёта" is null) or ("Статус" in ('6', '8')))
                  and "Код СМО" like '360%'
GROUP BY ROLLUP ("Подразделение")
union all
select COALESCE("Подразделение", 'Итого уникальных')                                  AS "Подразделение",
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
from (SELECT *
      FROM oms_data AS A
      WHERE "Цель" = 'ПН1'
      AND "Санкции" is null
              AND "Тариф" != '0'
        and (("Номер счёта" LIKE :month ) or ("Номер счёта" is null) or
             ((("Статус" = '6') or ("Статус" = '8')) and ("Номер счёта" is not null)))
        AND NOT EXISTS(
              SELECT *
              FROM oms_data AS B
              WHERE "Цель" = 'ПН1'
                AND "Тариф" != '0'
                and (("Номер счёта" not LIKE :month and B."Статус" = '3'))
                AND A."ЕНП" = B."ЕНП"
                and "Код СМО" like '360%'
          )) as oms_filtred
GROUP BY ROLLUP ("Подразделение");
"""

sql_query_children_age_dispensary = """
WITH data AS (SELECT 2024 - CAST(substring("Дата рождения" FROM LENGTH("Дата рождения") - 3) AS integer)                        as Возраст,
                     COUNT(*)                                                                   AS "Всего",
                     SUM(CASE WHEN "Пол" = 'М' THEN 1 ELSE 0 END) AS "М",
                     SUM(CASE WHEN "Пол" = 'Ж' THEN 1 ELSE 0 END) AS "Ж",                     
                     SUM(CASE WHEN "Подразделение" = 'ДП №1' and "Пол" = 'М' THEN 1 ELSE 0 END) AS "М ДП №1",
                     SUM(CASE WHEN "Подразделение" = 'ДП №1' and "Пол" = 'Ж' THEN 1 ELSE 0 END) AS "Ж ДП №1",
                     SUM(CASE WHEN "Подразделение" = 'ДП №1' THEN 1 ELSE 0 END)                 AS "ДП №1",
                     SUM(CASE WHEN "Подразделение" = 'ДП №8' and "Пол" = 'М' THEN 1 ELSE 0 END) AS "М ДП №8",
                     SUM(CASE WHEN "Подразделение" = 'ДП №8' and "Пол" = 'Ж' THEN 1 ELSE 0 END) AS "Ж ДП №8",
                     SUM(CASE WHEN "Подразделение" = 'ДП №8' THEN 1 ELSE 0 END)                 AS "ДП №8",
                     SUM(CASE WHEN "Подразделение" = 'ДП №8 К7' and "Пол" = 'М' THEN 1 ELSE 0 END) AS "М ДП №8 К7",
                     SUM(CASE WHEN "Подразделение" = 'ДП №8 К7' and "Пол" = 'Ж' THEN 1 ELSE 0 END) AS "Ж ДП №8 К7",                  
                     SUM(CASE WHEN "Подразделение" = 'ДП №8 К7' THEN 1 ELSE 0 END)              AS "ДП №8 К7"
              FROM oms_data
              WHERE "Цель" IN ('ПН1')
                and to_date("Первоначальная дата ввода", 'DD-MM-YYYY') BETWEEN to_date(:start_date, 'DD-MM-YYYY') and to_date(:end_date, 'DD-MM-YYYY')
              GROUP BY Возраст)
SELECT CASE
           WHEN Возраст IS NULL THEN 'Итого'
           ELSE Возраст::text
           END AS Возраст,
       "Всего",
       "М",
       "Ж",
       "М ДП №1",
       "Ж ДП №1",
       "ДП №1",
       "М ДП №8",
       "Ж ДП №8",
       "ДП №8",
       "М ДП №8 К7",
       "Ж ДП №8 К7",
       "ДП №8 К7"
FROM data
UNION ALL
select *
from (SELECT 'Итого' as Возраст,
             SUM("Всего"),
             SUM("М"),
             SUM("Ж"),
             SUM("М ДП №1"),
             SUM("Ж ДП №1"),
             SUM("ДП №1"),
             SUM("М ДП №8"),
             SUM("Ж ДП №8"),
             SUM("ДП №8"),
             SUM("М ДП №8 К7"),
             SUM("Ж ДП №8 К7"),
             SUM("ДП №8 К7")
      FROM data) d
"""


query_download_children_list = '''
    SELECT "Пациент",
           "Дата рождения",
           "Пол",
           "Подразделение"                                                                as Корпус,
           STRING_AGG(concat("Окончание лечения", ' ', SPLIT_PART("Врач", ' ', 2)), ', ') AS "Талон: Дата и врач",
           COUNT(*)                                                                       AS "К-во талонов",
           round(SUM(CAST("Сумма" AS numeric(15, 2)))::numeric, 2)                                                as Сумма
    FROM oms_data
    WHERE "Цель" = 'ПН1'
      AND to_date("Дата рождения", 'DD-MM-YYYY') > '01-10-2022'      
      and "Статус" in ('1', '2', '3', '6', '8') 
    GROUP BY "Пациент", "Дата рождения", "Пол", "Подразделение"
'''

query_download_children_list_not_pn1 = """
with
    sel_nas as (
        select people_data."FIO",
               people_data."DR",
               2024 - CAST(substring("DR" FROM LENGTH("DR") - 3) AS integer) as  "Возраст",
               people_data."ENP",
               people_data."LPUUCH",
               area_data."Корпус"
        from people_data left join area_data on people_data."LPUUCH" = area_data."Участок"
        where 2024 - CAST(substring("DR" FROM LENGTH("DR") - 3) AS integer) < 18
),
    itog as     (
        select *,
               case when sel_nas."ENP" in (select "ЕНП" from oms_data where "Цель" = 'ПН1') then 'да' else 'нет' end as "Есть ПН1"
        from sel_nas
    ),

    nas as (
        select itog.*,
               naselenie."Пол",
               naselenie."Телефон Квазар",
               naselenie."Телефон МИС КАУЗ",
               naselenie."Адрес Квазар",
               naselenie."Адрес ИСЗЛ",
               naselenie."Адрес МИС КАУЗ 1"

        from itog left join naselenie on itog."ENP" = naselenie."ЕНП"
    )
select *
from nas
where "Есть ПН1" = 'нет'
order by "FIO"
"""