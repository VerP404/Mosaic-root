def sql_query_amb_def(months_placeholder):
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
                         WHEN "Врач (Профиль МП)" ~ '\\(.*\\)' THEN
                             substring("Врач (Профиль МП)" from 1 for position('(' in "Врач (Профиль МП)") - 1)
                         ELSE
                             "Врач (Профиль МП)"
                         END AS "Корпус Врач"
              FROM oms.oms_data) as oms
        WHERE "Цель" IN ('1', '3', '5', '7', '9', '10', '13', '14', '140', '22', '30', '32', '64', '640', '301', '305', 
                        '307', '541', '561')
          AND "Корпус Врач" = :value_doctor
          AND "Отчетный период выгрузки" IN ({months_placeholder})

        GROUP BY "Цель"

        UNION ALL

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
               WHEN "Врач (Профиль МП)" ~ '\\(.*\\)' THEN
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
          AND "Отчетный период выгрузки" IN ({months_placeholder})
GROUP BY "Тип"
    """
