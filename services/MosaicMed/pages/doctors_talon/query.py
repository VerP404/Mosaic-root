sql_query_prof_cel = """
select Корпус,
       st_3                                       as Оплачено,
       st_2 + st_6 + st_8 + st_1                  as Выставлено,
       st_5 + st_7 + st_12 + st_17 + st_13 + st_0 as Отказано,
       Всего
from (select coalesce("Подразделение", ' Итого ')              as Корпус,
             sum(case when "Статус" = '1' then 1 else 0 end)  as st_1,
             sum(case when "Статус" = '2' then 1 else 0 end)  as st_2,
             sum(case when "Статус" = '3' then 1 else 0 end)  as st_3,
             sum(case when "Статус" = '5' then 1 else 0 end)  as st_5,
             sum(case when "Статус" = '6' then 1 else 0 end)  as st_6,
             sum(case when "Статус" = '7' then 1 else 0 end)  as st_7,
             sum(case when "Статус" = '8' then 1 else 0 end)  as st_8,
             sum(case when "Статус" = '12' then 1 else 0 end) as st_12,
             sum(case when "Статус" = '13' then 1 else 0 end) as st_13,
             sum(case when "Статус" = '17' then 1 else 0 end) as st_17,
             sum(case when "Статус" = '0' then 1 else 0 end)  as st_0,
             sum(case
                     when "Статус" = '0' or "Статус" = '1' or "Статус" = '2' or "Статус" = '3' or "Статус" = '5'
                         or "Статус" = '6' or "Статус" = '7' or "Статус" = '8' or "Статус" = '12' or "Статус" = '13' or
                          "Статус" = '17'
                         then 1
                     else 0 end)                              as Всего
      from oms.oms_data
      where to_date("Окончание лечения", 'DD-MM-YYYY') BETWEEN to_date(:start_date, 'DD-MM-YYYY') and to_date(:end_date, 'DD-MM-YYYY') 
            and "Цель" = :text_1 and "Подразделение" not like '%ДП%'
      group by rollup ("Подразделение")) as tab
group by Корпус, Оплачено, Выставлено, Отказано, Всего
"""

sql_query_disp = """
SELECT
    Корпус,
    COUNT("Подразделение") AS "к-во"
FROM (
    SELECT
        "Подразделение",
        CASE
            WHEN "Подразделение" LIKE 'ДП №8%' THEN 'ДП №8'
            ELSE "Подразделение"
        END AS Корпус
    FROM oms.oms_data
    WHERE "Тариф" != '0' AND
          ("Номер счёта" LIKE '%/08/%' OR "Номер счёта" IS NULL OR "Статус" = '6' OR "Статус" = '8') AND
          ("Статус" = '1' OR "Статус" = '2' OR "Статус" = '3' OR "Статус" = '6' OR "Статус" = '8')
) AS subquery
GROUP BY Корпус
UNION ALL
SELECT
    'Итого' AS Корпус,
    COUNT("Подразделение") AS "к-во"
FROM (
    SELECT
        "Подразделение",
        CASE
            WHEN "Подразделение" LIKE 'ДП №8%' THEN 'ДП №8'
            ELSE "Подразделение"
        END AS Корпус
    FROM oms.oms_data
    WHERE "Тариф" != '0' AND
          ("Номер счёта" LIKE :month OR "Номер счёта" IS NULL OR "Статус" = '6' OR "Статус" = '8') AND
          ("Статус" = '1' OR "Статус" = '2' OR "Статус" = '3' OR "Статус" = '6' OR "Статус" = '8')
) AS subquery;
"""


def sql_query_dd_def(sql_cond):
    return f"""
        SELECT "Цель",
               COUNT(*)                                       AS Всего,
               SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END)  AS "Оплачен(3)",
               SUM(CASE WHEN "Статус" = '1' or "Статус" = '2' or "Статус" = '3' or "Статус" = '6' or "Статус" = '8' THEN 1 ELSE 0 END)  AS "В работе(1,2,3,6,8)",
               SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END)  AS "В ТФОМС(2)",
               SUM(CASE WHEN "Статус" = '0' or "Статус" = '13' or "Статус" = '17' THEN 1 ELSE 0 END)  AS "Отменен(0,13,17)",
               SUM(CASE WHEN "Статус" = '5' or "Статус" = '7' or "Статус" = '12' THEN 1 ELSE 0 END)  AS "Отказан(5,7,12)",
               SUM(CASE WHEN "Статус" = '6' or "Статус" = '8' THEN 1 ELSE 0 END)  AS "Исправлен(6,8)",               
               SUM(CASE WHEN "Статус" = '0' THEN 1 ELSE 0 END)  AS "0",
               SUM(CASE WHEN "Статус" = '1' THEN 1 ELSE 0 END)  AS "1",
               SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END)  AS "2",
               SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END)  AS "3",
               SUM(CASE WHEN "Статус" = '5' THEN 1 ELSE 0 END)  AS "5",
               SUM(CASE WHEN "Статус" = '6' THEN 1 ELSE 0 END)  AS "6",
               SUM(CASE WHEN "Статус" = '7' THEN 1 ELSE 0 END)  AS "7",
               SUM(CASE WHEN "Статус" = '8' THEN 1 ELSE 0 END)  AS "8",
               SUM(CASE WHEN "Статус" = '12' THEN 1 ELSE 0 END) AS "12",
               SUM(CASE WHEN "Статус" = '13' THEN 1 ELSE 0 END) AS "13",
               SUM(CASE WHEN "Статус" = '17' THEN 1 ELSE 0 END) AS "17"
        FROM (SELECT *,
                     "Подразделение" || ' ' || split_part("Врач", ' ', 2) || ' ' || left(split_part("Врач", ' ', 3), 1) ||
                     '.' || left(split_part("Врач", ' ', 4), 1) || '.' || ' ' ||
                     CASE
                         WHEN "Врач (Профиль МП)" ~ '\(.*\)' THEN
                             substring("Врач (Профиль МП)" from 1 for position('(' in "Врач (Профиль МП)") - 1)
                         ELSE
                             "Врач (Профиль МП)"
                         END AS "Корпус Врач"
              FROM oms.oms_data) as oms

        WHERE "Сумма" != '0'  
          AND "Цель" IN ('ДВ4', 'ДВ2', 'ОПВ', 'УД1', 'УД2', 'ПН1', 'ДС2')
          AND "Корпус Врач" = :value_doctor
          AND (("Номер счёта" LIKE :update_value_month) {sql_cond} )

        GROUP BY "Цель"
        ORDER BY CASE "Цель"
                     WHEN 'ДВ4' THEN 1
                     WHEN 'ДВ2' THEN 2
                     WHEN 'ОПВ' THEN 3
                     WHEN 'УД1' THEN 4
                     WHEN 'УД2' THEN 5
                     WHEN 'ПН1' THEN 6
                     WHEN 'ДС2' THEN 7
                     END
        """


def sql_query_amb_def(sql_cond):
    return f"""
        SELECT "Цель",
               COUNT(*)                                       AS Всего,
               SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END)  AS "Оплачен(3)",
               SUM(CASE WHEN "Статус" = '1' or "Статус" = '2' or "Статус" = '3' or "Статус" = '6' or "Статус" = '8' THEN 1 ELSE 0 END)  AS "В работе(1,2,3,6,8)",
               SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END)  AS "В ТФОМС(2)",
               SUM(CASE WHEN "Статус" = '0' or "Статус" = '13' or "Статус" = '17' THEN 1 ELSE 0 END)  AS "Отменен(0,13,17)",
               SUM(CASE WHEN "Статус" = '5' or "Статус" = '7' or "Статус" = '12' THEN 1 ELSE 0 END)  AS "Отказан(5,7,12)",
               SUM(CASE WHEN "Статус" = '6' or "Статус" = '8' THEN 1 ELSE 0 END)  AS "Исправлен(6,8)",               
               SUM(CASE WHEN "Статус" = '0' THEN 1 ELSE 0 END)  AS "0",
               SUM(CASE WHEN "Статус" = '1' THEN 1 ELSE 0 END)  AS "1",
               SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END)  AS "2",
               SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END)  AS "3",
               SUM(CASE WHEN "Статус" = '5' THEN 1 ELSE 0 END)  AS "5",
               SUM(CASE WHEN "Статус" = '6' THEN 1 ELSE 0 END)  AS "6",
               SUM(CASE WHEN "Статус" = '7' THEN 1 ELSE 0 END)  AS "7",
               SUM(CASE WHEN "Статус" = '8' THEN 1 ELSE 0 END)  AS "8",
               SUM(CASE WHEN "Статус" = '12' THEN 1 ELSE 0 END) AS "12",
               SUM(CASE WHEN "Статус" = '13' THEN 1 ELSE 0 END) AS "13",
               SUM(CASE WHEN "Статус" = '17' THEN 1 ELSE 0 END) AS "17"
        FROM (SELECT *,
                     "Подразделение" || ' ' || split_part("Врач", ' ', 2) || ' ' || left(split_part("Врач", ' ', 3), 1) ||
                     '.' || left(split_part("Врач", ' ', 4), 1) || '.' || ' ' ||
                     CASE
                         WHEN "Врач (Профиль МП)" ~ '\(.*\)' THEN
                             substring("Врач (Профиль МП)" from 1 for position('(' in "Врач (Профиль МП)") - 1)
                         ELSE
                             "Врач (Профиль МП)"
                         END AS "Корпус Врач"
              FROM oms.oms_data) as oms
        WHERE "Цель" IN ('1', '3', '5', '7', '9', '10', '13', '14', '140', '22', '30', '32', '64', '640', '301', '305', 
                        '307', '541', '561')
          AND "Корпус Врач" = :value_doctor
          AND (("Номер счёта" LIKE :update_value_month) {sql_cond})

        GROUP BY "Цель"
        
        union all
        
        SELECT
    CASE
        WHEN "Цель" IN ('1', '5', '7', '9', '10', '32') THEN 'Посещения(1, 5, 7, 9, 10, 32)'
        WHEN "Цель" IN ('30', '301', '305', '307') THEN 'Обращения(30, 301, 305, 307)'
        WHEN "Цель" IN ('22') THEN 'Неотложка(22)'
        WHEN "Цель" IN ('3') THEN 'Диспансерное набл.(3)'        
        ELSE 'Другая цель'        
    END AS "Тип",
    COUNT(*) AS Всего,
    SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END) AS "Оплачен(3)",
    SUM(CASE WHEN "Статус" IN ('1', '2', '3', '6', '8') THEN 1 ELSE 0 END) AS "В работе(1,2,3,6,8)",
    SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END) AS "Выставлен(2)",
    SUM(CASE WHEN "Статус" IN ('0', '13', '17') THEN 1 ELSE 0 END) AS "Отменен(0,13,17)",
    SUM(CASE WHEN "Статус" IN ('5', '7', '12') THEN 1 ELSE 0 END) AS "Отказан(5,7,12)",
    SUM(CASE WHEN "Статус" IN ('6', '8') THEN 1 ELSE 0 END) AS "Исправлен(6,8)",
    SUM(CASE WHEN "Статус" = '0' THEN 1 ELSE 0 END) AS "0",
    SUM(CASE WHEN "Статус" = '1' THEN 1 ELSE 0 END) AS "1",
    SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END) AS "2",
    SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END) AS "3",
    SUM(CASE WHEN "Статус" = '5' THEN 1 ELSE 0 END) AS "5",
    SUM(CASE WHEN "Статус" = '6' THEN 1 ELSE 0 END) AS "6",
    SUM(CASE WHEN "Статус" = '7' THEN 1 ELSE 0 END) AS "7",
    SUM(CASE WHEN "Статус" = '8' THEN 1 ELSE 0 END) AS "8",
    SUM(CASE WHEN "Статус" = '12' THEN 1 ELSE 0 END) AS "12",
    SUM(CASE WHEN "Статус" = '13' THEN 1 ELSE 0 END) AS "13",
    SUM(CASE WHEN "Статус" = '17' THEN 1 ELSE 0 END) AS "17"
FROM (
    SELECT *,
           "Подразделение" || ' ' || split_part("Врач", ' ', 2) || ' ' || left(split_part("Врач", ' ', 3), 1) ||
           '.' || left(split_part("Врач", ' ', 4), 1) || '.' || ' ' ||
           CASE
               WHEN "Врач (Профиль МП)" ~ '\(.*\)' THEN
                   substring("Врач (Профиль МП)" from 1 for position('(' in "Врач (Профиль МП)") - 1)
               ELSE
                   "Врач (Профиль МП)"
           END AS "Корпус Врач"
    FROM oms.oms_data
) AS oms
WHERE  
    "Цель" IN ('1', '3', '5', '7', '9', '10', '13', '14', '140', '22', '30', '32', '64', '640', '301', '305',
                '307', '541', '561')
          AND "Корпус Врач" = :value_doctor
          AND (("Номер счёта" LIKE :update_value_month) {sql_cond})
GROUP BY "Тип"
    """


def sql_query_stac_def(sql_cond):
    return f"""
        SELECT "Цель",
               COUNT(*)                                       AS Всего,
               SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END)  AS "Оплачен(3)",
               SUM(CASE WHEN "Статус" = '1' or "Статус" = '2' or "Статус" = '3' or "Статус" = '6' or "Статус" = '8' THEN 1 ELSE 0 END)  AS "В работе(1,2,3,6,8)",
               SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END)  AS "В ТФОМС(2)",
               SUM(CASE WHEN "Статус" = '0' or "Статус" = '13' or "Статус" = '17' THEN 1 ELSE 0 END)  AS "Отменен(0,13,17)",
               SUM(CASE WHEN "Статус" = '5' or "Статус" = '7' or "Статус" = '12' THEN 1 ELSE 0 END)  AS "Отказан(5,7,12)",
               SUM(CASE WHEN "Статус" = '6' or "Статус" = '8' THEN 1 ELSE 0 END)  AS "Исправлен(6,8)",               
               SUM(CASE WHEN "Статус" = '0' THEN 1 ELSE 0 END)  AS "0",
               SUM(CASE WHEN "Статус" = '1' THEN 1 ELSE 0 END)  AS "1",
               SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END)  AS "2",
               SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END)  AS "3",
               SUM(CASE WHEN "Статус" = '5' THEN 1 ELSE 0 END)  AS "5",
               SUM(CASE WHEN "Статус" = '6' THEN 1 ELSE 0 END)  AS "6",
               SUM(CASE WHEN "Статус" = '7' THEN 1 ELSE 0 END)  AS "7",
               SUM(CASE WHEN "Статус" = '8' THEN 1 ELSE 0 END)  AS "8",
               SUM(CASE WHEN "Статус" = '12' THEN 1 ELSE 0 END) AS "12",
               SUM(CASE WHEN "Статус" = '13' THEN 1 ELSE 0 END) AS "13",
               SUM(CASE WHEN "Статус" = '17' THEN 1 ELSE 0 END) AS "17"
        FROM (SELECT *,
                     "Подразделение" || ' ' || split_part("Врач", ' ', 2) || ' ' || left(split_part("Врач", ' ', 3), 1) ||
                     '.' || left(split_part("Врач", ' ', 4), 1) || '.' || ' ' ||
                     CASE
                         WHEN "Врач (Профиль МП)" ~ '\(.*\)' THEN
                             substring("Врач (Профиль МП)" from 1 for position('(' in "Врач (Профиль МП)") - 1)
                         ELSE
                             "Врач (Профиль МП)"
                         END AS "Корпус Врач"
              FROM oms.oms_data) as oms
        WHERE "Цель" IN ('В дневном стационаре', 'На дому')
          AND "Корпус Врач" = :value_doctor
          AND (("Номер счёта" LIKE :update_value_month) {sql_cond})
        GROUP BY "Цель"
        ORDER BY CASE "Цель"
                     WHEN 'На дому' THEN 1
                     WHEN 'В дневном стационаре' THEN 2
                     END
        """


def sql_query_dd_date_form_def():
    return f"""
        SELECT "Цель",
               COUNT(*)                                       AS Всего,
               SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END)  AS "Оплачен(3)",
               SUM(CASE WHEN "Статус" = '1' or "Статус" = '2' or "Статус" = '3' or "Статус" = '6' or "Статус" = '8' THEN 1 ELSE 0 END)  AS "В работе(1,2,3,6,8)",
               SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END)  AS "В ТФОМС(2)",
               SUM(CASE WHEN "Статус" = '0' or "Статус" = '13' or "Статус" = '17' THEN 1 ELSE 0 END)  AS "Отменен(0,13,17)",
               SUM(CASE WHEN "Статус" = '5' or "Статус" = '7' or "Статус" = '12' THEN 1 ELSE 0 END)  AS "Отказан(5,7,12)",
               SUM(CASE WHEN "Статус" = '6' or "Статус" = '8' THEN 1 ELSE 0 END)  AS "Исправлен(6,8)",               
               SUM(CASE WHEN "Статус" = '0' THEN 1 ELSE 0 END)  AS "0",
               SUM(CASE WHEN "Статус" = '1' THEN 1 ELSE 0 END)  AS "1",
               SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END)  AS "2",
               SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END)  AS "3",
               SUM(CASE WHEN "Статус" = '5' THEN 1 ELSE 0 END)  AS "5",
               SUM(CASE WHEN "Статус" = '6' THEN 1 ELSE 0 END)  AS "6",
               SUM(CASE WHEN "Статус" = '7' THEN 1 ELSE 0 END)  AS "7",
               SUM(CASE WHEN "Статус" = '8' THEN 1 ELSE 0 END)  AS "8",
               SUM(CASE WHEN "Статус" = '12' THEN 1 ELSE 0 END) AS "12",
               SUM(CASE WHEN "Статус" = '13' THEN 1 ELSE 0 END) AS "13",
               SUM(CASE WHEN "Статус" = '17' THEN 1 ELSE 0 END) AS "17"
        FROM (SELECT *,
                     "Подразделение" || ' ' || split_part("Врач", ' ', 2) || ' ' || left(split_part("Врач", ' ', 3), 1) ||
                     '.' || left(split_part("Врач", ' ', 4), 1) || '.' || ' ' ||
                     CASE
                         WHEN "Врач (Профиль МП)" ~ '\(.*\)' THEN
                             substring("Врач (Профиль МП)" from 1 for position('(' in "Врач (Профиль МП)") - 1)
                         ELSE
                             "Врач (Профиль МП)"
                         END AS "Корпус Врач"
              FROM oms.oms_data) as oms

        WHERE "Сумма" != '0'  
          AND "Цель" IN ('ДВ4', 'ДВ2', 'ОПВ', 'УД1', 'УД2', 'ПН1', 'ДС2')
          AND "Корпус Врач" = :value_doctor
          AND to_date("Первоначальная дата ввода", 'DD-MM-YYYY') BETWEEN to_date(:start_date, 'DD-MM-YYYY') and to_date(:end_date, 'DD-MM-YYYY') 

        GROUP BY "Цель"
        ORDER BY CASE "Цель"
                     WHEN 'ДВ4' THEN 1
                     WHEN 'ДВ2' THEN 2
                     WHEN 'ОПВ' THEN 3
                     WHEN 'УД1' THEN 4
                     WHEN 'УД2' THEN 5
                     WHEN 'ПН1' THEN 6
                     WHEN 'ДС2' THEN 7
                     END
        """


def sql_query_amb_date_form_def():
    return f"""
        SELECT "Цель",
               COUNT(*)                                       AS Всего,
               SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END)  AS "Оплачен(3)",
               SUM(CASE WHEN "Статус" = '1' or "Статус" = '2' or "Статус" = '3' or "Статус" = '6' or "Статус" = '8' THEN 1 ELSE 0 END)  AS "В работе(1,2,3,6,8)",
               SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END)  AS "В ТФОМС(2)",
               SUM(CASE WHEN "Статус" = '0' or "Статус" = '13' or "Статус" = '17' THEN 1 ELSE 0 END)  AS "Отменен(0,13,17)",
               SUM(CASE WHEN "Статус" = '5' or "Статус" = '7' or "Статус" = '12' THEN 1 ELSE 0 END)  AS "Отказан(5,7,12)",
               SUM(CASE WHEN "Статус" = '6' or "Статус" = '8' THEN 1 ELSE 0 END)  AS "Исправлен(6,8)",               
               SUM(CASE WHEN "Статус" = '0' THEN 1 ELSE 0 END)  AS "0",
               SUM(CASE WHEN "Статус" = '1' THEN 1 ELSE 0 END)  AS "1",
               SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END)  AS "2",
               SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END)  AS "3",
               SUM(CASE WHEN "Статус" = '5' THEN 1 ELSE 0 END)  AS "5",
               SUM(CASE WHEN "Статус" = '6' THEN 1 ELSE 0 END)  AS "6",
               SUM(CASE WHEN "Статус" = '7' THEN 1 ELSE 0 END)  AS "7",
               SUM(CASE WHEN "Статус" = '8' THEN 1 ELSE 0 END)  AS "8",
               SUM(CASE WHEN "Статус" = '12' THEN 1 ELSE 0 END) AS "12",
               SUM(CASE WHEN "Статус" = '13' THEN 1 ELSE 0 END) AS "13",
               SUM(CASE WHEN "Статус" = '17' THEN 1 ELSE 0 END) AS "17"
        FROM (SELECT *,
                     "Подразделение" || ' ' || split_part("Врач", ' ', 2) || ' ' || left(split_part("Врач", ' ', 3), 1) ||
                     '.' || left(split_part("Врач", ' ', 4), 1) || '.' || ' ' ||
                     CASE
                         WHEN "Врач (Профиль МП)" ~ '\(.*\)' THEN
                             substring("Врач (Профиль МП)" from 1 for position('(' in "Врач (Профиль МП)") - 1)
                         ELSE
                             "Врач (Профиль МП)"
                         END AS "Корпус Врач"
              FROM oms.oms_data) as oms
        WHERE "Цель" IN ('1', '3', '5', '7', '9', '10', '13', '14', '140', '22', '30', '32', '64', '640', '301', '305', 
                        '307', '541', '561')
          AND "Корпус Врач" = :value_doctor
          AND to_date("Первоначальная дата ввода", 'DD-MM-YYYY') BETWEEN to_date(:start_date, 'DD-MM-YYYY') and to_date(:end_date, 'DD-MM-YYYY') 
          and "Тариф" != '0'
        GROUP BY "Цель"

    """


def sql_query_stac_date_form_def():
    return f"""
        SELECT "Цель",
               COUNT(*)                                       AS Всего,
               SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END)  AS "Оплачен(3)",
               SUM(CASE WHEN "Статус" = '1' or "Статус" = '2' or "Статус" = '3' or "Статус" = '6' or "Статус" = '8' THEN 1 ELSE 0 END)  AS "В работе(1,2,3,6,8)",
               SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END)  AS "В ТФОМС(2)",
               SUM(CASE WHEN "Статус" = '0' or "Статус" = '13' or "Статус" = '17' THEN 1 ELSE 0 END)  AS "Отменен(0,13,17)",
               SUM(CASE WHEN "Статус" = '5' or "Статус" = '7' or "Статус" = '12' THEN 1 ELSE 0 END)  AS "Отказан(5,7,12)",
               SUM(CASE WHEN "Статус" = '6' or "Статус" = '8' THEN 1 ELSE 0 END)  AS "Исправлен(6,8)",               
               SUM(CASE WHEN "Статус" = '0' THEN 1 ELSE 0 END)  AS "0",
               SUM(CASE WHEN "Статус" = '1' THEN 1 ELSE 0 END)  AS "1",
               SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END)  AS "2",
               SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END)  AS "3",
               SUM(CASE WHEN "Статус" = '5' THEN 1 ELSE 0 END)  AS "5",
               SUM(CASE WHEN "Статус" = '6' THEN 1 ELSE 0 END)  AS "6",
               SUM(CASE WHEN "Статус" = '7' THEN 1 ELSE 0 END)  AS "7",
               SUM(CASE WHEN "Статус" = '8' THEN 1 ELSE 0 END)  AS "8",
               SUM(CASE WHEN "Статус" = '12' THEN 1 ELSE 0 END) AS "12",
               SUM(CASE WHEN "Статус" = '13' THEN 1 ELSE 0 END) AS "13",
               SUM(CASE WHEN "Статус" = '17' THEN 1 ELSE 0 END) AS "17"
        FROM (SELECT *,
                     "Подразделение" || ' ' || split_part("Врач", ' ', 2) || ' ' || left(split_part("Врач", ' ', 3), 1) ||
                     '.' || left(split_part("Врач", ' ', 4), 1) || '.' || ' ' ||
                     CASE
                         WHEN "Врач (Профиль МП)" ~ '\(.*\)' THEN
                             substring("Врач (Профиль МП)" from 1 for position('(' in "Врач (Профиль МП)") - 1)
                         ELSE
                             "Врач (Профиль МП)"
                         END AS "Корпус Врач"
              FROM oms.oms_data) as oms
        WHERE "Цель" IN ('В дневном стационаре', 'На дому')
          AND "Корпус Врач" = :value_doctor
          AND to_date("Первоначальная дата ввода", 'DD-MM-YYYY') BETWEEN to_date(:start_date, 'DD-MM-YYYY') and to_date(:end_date, 'DD-MM-YYYY')
        GROUP BY "Цель"
        ORDER BY CASE "Цель"
                     WHEN 'На дому' THEN 1
                     WHEN 'В дневном стационаре' THEN 2
                     END
        """

def sql_query_dd_date_treatment_def():
    return f"""
        SELECT "Цель",
               COUNT(*)                                       AS Всего,
               SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END)  AS "Оплачен(3)",
               SUM(CASE WHEN "Статус" = '1' or "Статус" = '2' or "Статус" = '3' or "Статус" = '6' or "Статус" = '8' THEN 1 ELSE 0 END)  AS "В работе(1,2,3,6,8)",
               SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END)  AS "В ТФОМС(2)",
               SUM(CASE WHEN "Статус" = '0' or "Статус" = '13' or "Статус" = '17' THEN 1 ELSE 0 END)  AS "Отменен(0,13,17)",
               SUM(CASE WHEN "Статус" = '5' or "Статус" = '7' or "Статус" = '12' THEN 1 ELSE 0 END)  AS "Отказан(5,7,12)",
               SUM(CASE WHEN "Статус" = '6' or "Статус" = '8' THEN 1 ELSE 0 END)  AS "Исправлен(6,8)",               
               SUM(CASE WHEN "Статус" = '0' THEN 1 ELSE 0 END)  AS "0",
               SUM(CASE WHEN "Статус" = '1' THEN 1 ELSE 0 END)  AS "1",
               SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END)  AS "2",
               SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END)  AS "3",
               SUM(CASE WHEN "Статус" = '5' THEN 1 ELSE 0 END)  AS "5",
               SUM(CASE WHEN "Статус" = '6' THEN 1 ELSE 0 END)  AS "6",
               SUM(CASE WHEN "Статус" = '7' THEN 1 ELSE 0 END)  AS "7",
               SUM(CASE WHEN "Статус" = '8' THEN 1 ELSE 0 END)  AS "8",
               SUM(CASE WHEN "Статус" = '12' THEN 1 ELSE 0 END) AS "12",
               SUM(CASE WHEN "Статус" = '13' THEN 1 ELSE 0 END) AS "13",
               SUM(CASE WHEN "Статус" = '17' THEN 1 ELSE 0 END) AS "17"
        FROM (SELECT *,
                     "Подразделение" || ' ' || split_part("Врач", ' ', 2) || ' ' || left(split_part("Врач", ' ', 3), 1) ||
                     '.' || left(split_part("Врач", ' ', 4), 1) || '.' || ' ' ||
                     CASE
                         WHEN "Врач (Профиль МП)" ~ '\(.*\)' THEN
                             substring("Врач (Профиль МП)" from 1 for position('(' in "Врач (Профиль МП)") - 1)
                         ELSE
                             "Врач (Профиль МП)"
                         END AS "Корпус Врач"
              FROM oms.oms_data) as oms

        WHERE "Сумма" != '0'  
          AND "Цель" IN ('ДВ4', 'ДВ2', 'ОПВ', 'УД1', 'УД2', 'ПН1', 'ДС2')
          AND "Корпус Врач" = :value_doctor
          AND to_date("Окончание лечения", 'DD-MM-YYYY') BETWEEN to_date(:start_date, 'DD-MM-YYYY') and to_date(:end_date, 'DD-MM-YYYY') 

        GROUP BY "Цель"
        ORDER BY CASE "Цель"
                     WHEN 'ДВ4' THEN 1
                     WHEN 'ДВ2' THEN 2
                     WHEN 'ОПВ' THEN 3
                     WHEN 'УД1' THEN 4
                     WHEN 'УД2' THEN 5
                     WHEN 'ПН1' THEN 6
                     WHEN 'ДС2' THEN 7
                     END
        """


def sql_query_amb_date_treatment_def():
    return f"""
        SELECT "Цель",
               COUNT(*)                                       AS Всего,
               SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END)  AS "Оплачен(3)",
               SUM(CASE WHEN "Статус" = '1' or "Статус" = '2' or "Статус" = '3' or "Статус" = '6' or "Статус" = '8' THEN 1 ELSE 0 END)  AS "В работе(1,2,3,6,8)",
               SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END)  AS "В ТФОМС(2)",
               SUM(CASE WHEN "Статус" = '0' or "Статус" = '13' or "Статус" = '17' THEN 1 ELSE 0 END)  AS "Отменен(0,13,17)",
               SUM(CASE WHEN "Статус" = '5' or "Статус" = '7' or "Статус" = '12' THEN 1 ELSE 0 END)  AS "Отказан(5,7,12)",
               SUM(CASE WHEN "Статус" = '6' or "Статус" = '8' THEN 1 ELSE 0 END)  AS "Исправлен(6,8)",               
               SUM(CASE WHEN "Статус" = '0' THEN 1 ELSE 0 END)  AS "0",
               SUM(CASE WHEN "Статус" = '1' THEN 1 ELSE 0 END)  AS "1",
               SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END)  AS "2",
               SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END)  AS "3",
               SUM(CASE WHEN "Статус" = '5' THEN 1 ELSE 0 END)  AS "5",
               SUM(CASE WHEN "Статус" = '6' THEN 1 ELSE 0 END)  AS "6",
               SUM(CASE WHEN "Статус" = '7' THEN 1 ELSE 0 END)  AS "7",
               SUM(CASE WHEN "Статус" = '8' THEN 1 ELSE 0 END)  AS "8",
               SUM(CASE WHEN "Статус" = '12' THEN 1 ELSE 0 END) AS "12",
               SUM(CASE WHEN "Статус" = '13' THEN 1 ELSE 0 END) AS "13",
               SUM(CASE WHEN "Статус" = '17' THEN 1 ELSE 0 END) AS "17"
        FROM (SELECT *,
                     "Подразделение" || ' ' || split_part("Врач", ' ', 2) || ' ' || left(split_part("Врач", ' ', 3), 1) ||
                     '.' || left(split_part("Врач", ' ', 4), 1) || '.' || ' ' ||
                     CASE
                         WHEN "Врач (Профиль МП)" ~ '\(.*\)' THEN
                             substring("Врач (Профиль МП)" from 1 for position('(' in "Врач (Профиль МП)") - 1)
                         ELSE
                             "Врач (Профиль МП)"
                         END AS "Корпус Врач"
              FROM oms.oms_data) as oms
        WHERE "Цель" IN ('1', '3', '5', '7', '9', '10', '13', '14', '140', '22', '30', '32', '64', '640', '301', '305', 
                        '307', '541', '561')
          AND "Корпус Врач" = :value_doctor
          AND to_date("Окончание лечения", 'DD-MM-YYYY') BETWEEN to_date(:start_date, 'DD-MM-YYYY') and to_date(:end_date, 'DD-MM-YYYY') 

        GROUP BY "Цель"

    """


def sql_query_stac_date_treatment_def():
    return f"""
        SELECT "Цель",
               COUNT(*)                                       AS Всего,
               SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END)  AS "Оплачен(3)",
               SUM(CASE WHEN "Статус" = '1' or "Статус" = '2' or "Статус" = '3' or "Статус" = '6' or "Статус" = '8' THEN 1 ELSE 0 END)  AS "В работе(1,2,3,6,8)",
               SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END)  AS "В ТФОМС(2)",
               SUM(CASE WHEN "Статус" = '0' or "Статус" = '13' or "Статус" = '17' THEN 1 ELSE 0 END)  AS "Отменен(0,13,17)",
               SUM(CASE WHEN "Статус" = '5' or "Статус" = '7' or "Статус" = '12' THEN 1 ELSE 0 END)  AS "Отказан(5,7,12)",
               SUM(CASE WHEN "Статус" = '6' or "Статус" = '8' THEN 1 ELSE 0 END)  AS "Исправлен(6,8)",               
               SUM(CASE WHEN "Статус" = '0' THEN 1 ELSE 0 END)  AS "0",
               SUM(CASE WHEN "Статус" = '1' THEN 1 ELSE 0 END)  AS "1",
               SUM(CASE WHEN "Статус" = '2' THEN 1 ELSE 0 END)  AS "2",
               SUM(CASE WHEN "Статус" = '3' THEN 1 ELSE 0 END)  AS "3",
               SUM(CASE WHEN "Статус" = '5' THEN 1 ELSE 0 END)  AS "5",
               SUM(CASE WHEN "Статус" = '6' THEN 1 ELSE 0 END)  AS "6",
               SUM(CASE WHEN "Статус" = '7' THEN 1 ELSE 0 END)  AS "7",
               SUM(CASE WHEN "Статус" = '8' THEN 1 ELSE 0 END)  AS "8",
               SUM(CASE WHEN "Статус" = '12' THEN 1 ELSE 0 END) AS "12",
               SUM(CASE WHEN "Статус" = '13' THEN 1 ELSE 0 END) AS "13",
               SUM(CASE WHEN "Статус" = '17' THEN 1 ELSE 0 END) AS "17"
        FROM (SELECT *,
                     "Подразделение" || ' ' || split_part("Врач", ' ', 2) || ' ' || left(split_part("Врач", ' ', 3), 1) ||
                     '.' || left(split_part("Врач", ' ', 4), 1) || '.' || ' ' ||
                     CASE
                         WHEN "Врач (Профиль МП)" ~ '\(.*\)' THEN
                             substring("Врач (Профиль МП)" from 1 for position('(' in "Врач (Профиль МП)") - 1)
                         ELSE
                             "Врач (Профиль МП)"
                         END AS "Корпус Врач"
              FROM oms.oms_data) as oms
        WHERE "Цель" IN ('В дневном стационаре', 'На дому')
          AND "Корпус Врач" = :value_doctor
          AND to_date("Окончание лечения", 'DD-MM-YYYY') BETWEEN to_date(:start_date, 'DD-MM-YYYY') and to_date(:end_date, 'DD-MM-YYYY')
        GROUP BY "Цель"
        ORDER BY CASE "Цель"
                     WHEN 'На дому' THEN 1
                     WHEN 'В дневном стационаре' THEN 2
                     END
        """


def sql_query_by_doc(sql_cond=None):
    return f"""
    select distinct "Корпус Врач"                                                                  as "ФИО Врача",
                "Подразделение"                                                                as "Корпус",
                CASE
                    WHEN "Врач (Профиль МП)" ~ '\(.*\)' THEN
                        substring("Врач (Профиль МП)" from 1 for position('(' in "Врач (Профиль МП)") - 1)
                    ELSE
                        "Врач (Профиль МП)"
                    END                                                                        AS "Профиль",
                count(*)                                                                       as "Всего",
                SUM(CASE WHEN "Цель" in ('1') THEN 1 ELSE 0 END)                              AS "1",
                SUM(CASE WHEN "Цель" in ('3') THEN 1 ELSE 0 END)                               AS "3",
                SUM(CASE WHEN "Цель" in ('5') THEN 1 ELSE 0 END)                              AS "5",
                SUM(CASE WHEN "Цель" in ('7') THEN 1 ELSE 0 END)                              AS "7",
                SUM(CASE WHEN "Цель" in ('9') THEN 1 ELSE 0 END)                              AS "9",
                SUM(CASE WHEN "Цель" in ('10') THEN 1 ELSE 0 END)                              AS "10",
                SUM(CASE WHEN "Цель" in ('13') THEN 1 ELSE 0 END)                              AS "13",
                SUM(CASE WHEN "Цель" in ('14') THEN 1 ELSE 0 END)                              AS "14",
                SUM(CASE WHEN "Цель" in ('22') THEN 1 ELSE 0 END)                              AS "22",
                SUM(CASE WHEN "Цель" in ('30') THEN 1 ELSE 0 END)                              AS "30",
                SUM(CASE WHEN "Цель" in ('32') THEN 1 ELSE 0 END)                              AS "32",
                SUM(CASE WHEN "Цель" in ('64') THEN 1 ELSE 0 END)                              AS "64",
                SUM(CASE WHEN "Цель" in ('140') THEN 1 ELSE 0 END)                              AS "140",
                SUM(CASE WHEN "Цель" in ('301') THEN 1 ELSE 0 END)                             AS "301",
                SUM(CASE WHEN "Цель" in ('305') THEN 1 ELSE 0 END)                              AS "305",
                SUM(CASE WHEN "Цель" in ('307') THEN 1 ELSE 0 END)                              AS "307",
                SUM(CASE WHEN "Цель" in ('541') THEN 1 ELSE 0 END)                              AS "541",
                SUM(CASE WHEN "Цель" in ('561') THEN 1 ELSE 0 END)                              AS "561",
                SUM(CASE WHEN "Цель" in ('В дневном стационаре') THEN 1 ELSE 0 END)              AS "В дс",
                SUM(CASE WHEN "Цель" in ('На дому') THEN 1 ELSE 0 END)                              AS "На дому",
                SUM(CASE WHEN "Цель" in ('ДВ4') THEN 1 ELSE 0 END)                             AS "ДВ4",
                SUM(CASE WHEN "Цель" in ('ДВ2') THEN 1 ELSE 0 END)                             AS "ДВ2",
                SUM(CASE WHEN "Цель" in ('ОПВ') THEN 1 ELSE 0 END)                             AS "ОПВ",
                SUM(CASE WHEN "Цель" in ('УД1') THEN 1 ELSE 0 END)                             AS "УД1",
                SUM(CASE WHEN "Цель" in ('УД2') THEN 1 ELSE 0 END)                             AS "УД2",
                SUM(CASE WHEN "Цель" in ('ПН1') THEN 1 ELSE 0 END)                             AS "ПН1",
                SUM(CASE WHEN "Цель" in ('ДС2') THEN 1 ELSE 0 END)                             AS "ДС2"
from (SELECT *, split_part("Врач", ' ', 2) || ' ' || left(split_part("Врач", ' ', 3), 1) ||
             '.' || left(split_part("Врач", ' ', 4), 1) || '.' AS "Корпус Врач"
      FROM oms.oms_data) as oms
WHERE (("Номер счёта" LIKE ANY (:list_months)) {sql_cond})
  AND "Статус" IN :status_list
  AND "Тариф" != '0'
group by "ФИО Врача", "Корпус", "Профиль"
order by "Корпус", "ФИО Врача"
    """

def sql_query_by_doc_end_treatment(sql_cond=None):
    return f"""
    select distinct "Корпус Врач"                                                                  as "ФИО Врача",
                "Подразделение"                                                                as "Корпус",
                CASE
                    WHEN "Врач (Профиль МП)" ~ '\(.*\)' THEN
                        substring("Врач (Профиль МП)" from 1 for position('(' in "Врач (Профиль МП)") - 1)
                    ELSE
                        "Врач (Профиль МП)"
                    END                                                                        AS "Профиль",
                count(*)                                                                       as "Всего",
                SUM(CASE WHEN "Цель" in ('1') THEN 1 ELSE 0 END)                              AS "1",
                SUM(CASE WHEN "Цель" in ('3') THEN 1 ELSE 0 END)                               AS "3",
                SUM(CASE WHEN "Цель" in ('5') THEN 1 ELSE 0 END)                              AS "5",
                SUM(CASE WHEN "Цель" in ('7') THEN 1 ELSE 0 END)                              AS "7",
                SUM(CASE WHEN "Цель" in ('9') THEN 1 ELSE 0 END)                              AS "9",
                SUM(CASE WHEN "Цель" in ('10') THEN 1 ELSE 0 END)                              AS "10",
                SUM(CASE WHEN "Цель" in ('13') THEN 1 ELSE 0 END)                              AS "13",
                SUM(CASE WHEN "Цель" in ('14') THEN 1 ELSE 0 END)                              AS "14",
                SUM(CASE WHEN "Цель" in ('22') THEN 1 ELSE 0 END)                              AS "22",
                SUM(CASE WHEN "Цель" in ('30') THEN 1 ELSE 0 END)                              AS "30",
                SUM(CASE WHEN "Цель" in ('32') THEN 1 ELSE 0 END)                              AS "32",
                SUM(CASE WHEN "Цель" in ('64') THEN 1 ELSE 0 END)                              AS "64",
                SUM(CASE WHEN "Цель" in ('140') THEN 1 ELSE 0 END)                              AS "140",
                SUM(CASE WHEN "Цель" in ('301') THEN 1 ELSE 0 END)                             AS "301",
                SUM(CASE WHEN "Цель" in ('305') THEN 1 ELSE 0 END)                              AS "305",
                SUM(CASE WHEN "Цель" in ('307') THEN 1 ELSE 0 END)                              AS "307",
                SUM(CASE WHEN "Цель" in ('541') THEN 1 ELSE 0 END)                              AS "541",
                SUM(CASE WHEN "Цель" in ('561') THEN 1 ELSE 0 END)                              AS "561",
                SUM(CASE WHEN "Цель" in ('В дневном стационаре') THEN 1 ELSE 0 END)              AS "В дс",
                SUM(CASE WHEN "Цель" in ('На дому') THEN 1 ELSE 0 END)                              AS "На дому",
                SUM(CASE WHEN "Цель" in ('ДВ4') THEN 1 ELSE 0 END)                             AS "ДВ4",
                SUM(CASE WHEN "Цель" in ('ДВ2') THEN 1 ELSE 0 END)                             AS "ДВ2",
                SUM(CASE WHEN "Цель" in ('ОПВ') THEN 1 ELSE 0 END)                             AS "ОПВ",
                SUM(CASE WHEN "Цель" in ('УД1') THEN 1 ELSE 0 END)                             AS "УД1",
                SUM(CASE WHEN "Цель" in ('УД2') THEN 1 ELSE 0 END)                             AS "УД2",
                SUM(CASE WHEN "Цель" in ('ПН1') THEN 1 ELSE 0 END)                             AS "ПН1",
                SUM(CASE WHEN "Цель" in ('ДС2') THEN 1 ELSE 0 END)                             AS "ДС2"
from (SELECT *, split_part("Врач", ' ', 2) || ' ' || left(split_part("Врач", ' ', 3), 1) ||
             '.' || left(split_part("Врач", ' ', 4), 1) || '.' AS "Корпус Врач"
      FROM oms.oms_data) as oms
WHERE to_date("Окончание лечения", 'DD-MM-YYYY') BETWEEN to_date(:start_date, 'DD-MM-YYYY') and to_date(:end_date, 'DD-MM-YYYY')
  AND "Тариф" != '0'
group by "ФИО Врача", "Корпус", "Профиль"
order by "Корпус", "ФИО Врача"
    """