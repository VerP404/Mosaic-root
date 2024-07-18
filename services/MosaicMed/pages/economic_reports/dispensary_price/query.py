def sql_query_disp_dv4(sql_cond=None):
    return f"""
WITH data AS (SELECT 2024 - CAST(substring("Дата рождения" FROM LENGTH("Дата рождения") - 3) AS integer)                        as Возраст,
                     COUNT(*)                                                                   AS "Всего",
                     round(sum(CAST("Сумма" AS numeric(15, 2))):: numeric, 2) as "Сумма",
                     SUM(CASE WHEN "Пол" = 'М' THEN 1 ELSE 0 END) AS "М",
                     round(SUM(CASE WHEN "Пол" = 'М' THEN round(CAST("Сумма" AS numeric(15, 2)):: numeric, 2) ELSE 0 END):: numeric, 2) AS "М Сумма",
                     SUM(CASE WHEN "Пол" = 'Ж' THEN 1 ELSE 0 END) AS "Ж",
                     round(SUM(CASE WHEN "Пол" = 'Ж' THEN round(CAST("Сумма" AS numeric(15, 2)):: numeric, 2) ELSE 0 END):: numeric, 2) AS "Ж Сумма",
                     SUM(CASE WHEN "Подразделение" = 'ГП №3' and "Пол" = 'М' THEN 1 ELSE 0 END) AS "М ГП3",
                     round(SUM(CASE WHEN "Подразделение" = 'ГП №3' and "Пол" = 'М' THEN round(CAST("Сумма" AS numeric(15, 2)):: numeric, 2) ELSE 0 END):: numeric, 2) AS "М ГП3 Сумма",
                     SUM(CASE WHEN "Подразделение" = 'ГП №3' and "Пол" = 'Ж' THEN 1 ELSE 0 END) AS "Ж ГП3",
                     round(SUM(CASE WHEN "Подразделение" = 'ГП №3' and "Пол" = 'Ж' THEN round(CAST("Сумма" AS numeric(15, 2)):: numeric, 2) ELSE 0 END):: numeric, 2) AS "Ж ГП3 Сумма",
                     SUM(CASE WHEN "Подразделение" = 'ГП №3' THEN 1 ELSE 0 END)                 AS "ГП3",
                     round(SUM(CASE WHEN "Подразделение" = 'ГП №3'  THEN round(CAST("Сумма" AS numeric(15, 2)):: numeric, 2) ELSE 0 END):: numeric, 2) AS "ГП3 Сумма",
                     SUM(CASE WHEN "Подразделение" = 'ГП №11' and "Пол" = 'М' THEN 1 ELSE 0 END) AS "М ГП11",
                     round(SUM(CASE WHEN "Подразделение" = 'ГП №11' and "Пол" = 'М' THEN round(CAST("Сумма" AS numeric(15, 2)):: numeric, 2) ELSE 0 END):: numeric, 2) AS "М ГП11 Сумма",
                     SUM(CASE WHEN "Подразделение" = 'ГП №11' and "Пол" = 'Ж' THEN 1 ELSE 0 END) AS "Ж ГП11",
                     round(SUM(CASE WHEN "Подразделение" = 'ГП №11' and "Пол" = 'Ж' THEN round(CAST("Сумма" AS numeric(15, 2)):: numeric, 2) ELSE 0 END):: numeric, 2) AS "Ж ГП11 Сумма",
                     SUM(CASE WHEN "Подразделение" = 'ГП №11' THEN 1 ELSE 0 END)                 AS "ГП11",
                     round(SUM(CASE WHEN "Подразделение" = 'ГП №11' THEN round(CAST("Сумма" AS numeric(15, 2)):: numeric, 2) ELSE 0 END):: numeric, 2) AS "ГП11 Сумма",
                     SUM(CASE WHEN "Подразделение" = 'ОАПП №1' and "Пол" = 'М' THEN 1 ELSE 0 END) AS "М ОАПП1",
                     round(SUM(CASE WHEN "Подразделение" = 'ОАПП №1' and "Пол" = 'М' THEN round(CAST("Сумма" AS numeric(15, 2)):: numeric, 2) ELSE 0 END):: numeric, 2) AS "М ОАПП1 Сумма",
                     SUM(CASE WHEN "Подразделение" = 'ОАПП №1' and "Пол" = 'Ж' THEN 1 ELSE 0 END) AS "Ж ОАПП1",
                     round(SUM(CASE WHEN "Подразделение" = 'ОАПП №1' and "Пол" = 'Ж' THEN round(CAST("Сумма" AS numeric(15, 2)):: numeric, 2) ELSE 0 END):: numeric, 2) AS "Ж ОАПП1 Сумма",
                     SUM(CASE WHEN "Подразделение" = 'ОАПП №1' THEN 1 ELSE 0 END)              AS "ОАПП1",
                     round(SUM(CASE WHEN "Подразделение" = 'ОАПП №1' THEN round(CAST("Сумма" AS numeric(15, 2)):: numeric, 2) ELSE 0 END):: numeric, 2) AS "ОАПП1 Сумма",
                     SUM(CASE WHEN "Подразделение" = 'ОАПП №2' and "Пол" = 'М' THEN 1 ELSE 0 END) AS "М ОАПП2",
                     round(SUM(CASE WHEN "Подразделение" = 'ОАПП №2' and "Пол" = 'М' THEN round(CAST("Сумма" AS numeric(15, 2)):: numeric, 2) ELSE 0 END):: numeric, 2) AS "М ОАПП2 Сумма",
                     SUM(CASE WHEN "Подразделение" = 'ОАПП №2' and "Пол" = 'Ж' THEN 1 ELSE 0 END) AS "Ж ОАПП2",
                     round(SUM(CASE WHEN "Подразделение" = 'ОАПП №2' and "Пол" = 'Ж' THEN round(CAST("Сумма" AS numeric(15, 2)):: numeric, 2) ELSE 0 END):: numeric, 2) AS "Ж ОАПП2 Сумма",
                     SUM(CASE WHEN "Подразделение" = 'ОАПП №2' THEN 1 ELSE 0 END)              AS "ОАПП2",
                     round(SUM(CASE WHEN "Подразделение" = 'ОАПП №2' THEN round(CAST("Сумма" AS numeric(15, 2)):: numeric, 2) ELSE 0 END):: numeric, 2) AS "ОАПП2 Сумма"
              FROM oms_data
              WHERE (("Номер счёта" LIKE ANY (:list_months)) {sql_cond})
                AND "Цель" IN :dv
                AND "Статус" IN :status_list
                AND "Тариф" != '0'
                AND "Код СМО" like '360%'
                AND "Санкции" is null
              GROUP BY Возраст)
SELECT CASE
           WHEN Возраст IS NULL THEN 'Итого'
           ELSE Возраст::text
           END AS Возраст,
        "Всего",
        "Сумма",
        "М",
        "М Сумма",
        "Ж",
        "Ж Сумма",
        "М ГП3",
        "М ГП3 Сумма",
        "Ж ГП3",
        "Ж ГП3 Сумма",
        "ГП3",
        "ГП3 Сумма",
        "М ГП11",
        "М ГП11 Сумма",
        "Ж ГП11",
        "Ж ГП11 Сумма",
        "ГП11",
        "ГП11 Сумма",
        "М ОАПП1",
        "М ОАПП1 Сумма",
        "Ж ОАПП1",
        "Ж ОАПП1 Сумма",
        "ОАПП1",
        "ОАПП1 Сумма",
        "М ОАПП2",
        "М ОАПП2 Сумма",
        "Ж ОАПП2",
        "Ж ОАПП2 Сумма",
        "ОАПП2",
        "ОАПП2 Сумма"
FROM data
UNION ALL
select *
from (SELECT 'Итого' as Возраст,
             SUM("Всего"),
             SUM("Сумма"),
             SUM("М"),
             SUM("М Сумма"),
             SUM("Ж"),
             SUM("Ж Сумма"),
        SUM("М ГП3"),
        SUM("М ГП3 Сумма"),
        SUM("Ж ГП3"),
        SUM("Ж ГП3 Сумма"),
        SUM("ГП3"),
        SUM("ГП3 Сумма"),
        SUM("М ГП11"),
        SUM("М ГП11 Сумма"),
        SUM("Ж ГП11"),
        SUM("Ж ГП11 Сумма"),
        SUM("ГП11"),
        SUM("ГП11 Сумма"),
        SUM("М ОАПП1"),
        SUM("М ОАПП1 Сумма"),
        SUM("Ж ОАПП1"),
        SUM("Ж ОАПП1 Сумма"),
        SUM("ОАПП1"),
        SUM("ОАПП1 Сумма"),
        SUM("М ОАПП2"),
        SUM("М ОАПП2 Сумма"),
        SUM("Ж ОАПП2"),
        SUM("Ж ОАПП2 Сумма"),
        SUM("ОАПП2"),
        SUM("ОАПП2 Сумма")
      FROM data) d
"""