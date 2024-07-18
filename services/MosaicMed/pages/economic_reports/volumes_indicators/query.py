sql_query_pgg_amb = """
SELECT "Месяц",
       SUM(CASE WHEN "Цель" in ('30', '301', '305') THEN 1 ELSE 0 END) AS "Обращения",
       SUM(CASE WHEN "Цель" in ('22') THEN 1 ELSE 0 END)               AS "Неотложка",
       SUM(CASE WHEN "Цель" in ('3') THEN 1 ELSE 0 END)                AS "Д.наб",
       SUM(CASE WHEN "Цель" in ('64') THEN 1 ELSE 0 END)               AS "Гериатрия",
       SUM(CASE WHEN "Цель" in ('307') THEN 1 ELSE 0 END)               AS "307",
       SUM(CASE WHEN "Цель" in ('561') THEN 1 ELSE 0 END)               AS "561",
       SUM(CASE WHEN "Цель" in ('541') and "Сумма" = '542.13' THEN 1 ELSE 0 END) AS "541 УЗИ",
       SUM(CASE WHEN "Цель" in ('541') and "Сумма" = '857.55' THEN 1 ELSE 0 END) AS "541 Эндоскопия",
       SUM(CASE WHEN "Цель" in ('541') and "Сумма" = '2004.27' THEN 1 ELSE 0 END) AS "541 Колоноскопия"
FROM (SELECT CASE
                 WHEN "Номер счёта" LIKE '%/01/%' THEN '01'
                 WHEN "Номер счёта" LIKE '%/02/%' THEN '02'
                 WHEN "Номер счёта" LIKE '%/03/%' THEN '03'
                 WHEN "Номер счёта" LIKE '%/04/%' THEN '04'
                 WHEN "Номер счёта" LIKE '%/05/%' THEN '05'
                 WHEN "Номер счёта" LIKE '%/06/%' THEN '06'
                 WHEN "Номер счёта" LIKE '%/07/%' THEN '07'
                 WHEN "Номер счёта" LIKE '%/08/%' THEN '08'
                 WHEN "Номер счёта" LIKE '%/09/%' THEN '09'
                 WHEN "Номер счёта" LIKE '%/10/%' THEN '10'
                 WHEN "Номер счёта" LIKE '%/11/%' THEN '11'
                 WHEN "Номер счёта" LIKE '%/12/%' THEN '12'
                 END AS "Месяц",
             "Цель",
             "Сумма"
      FROM oms_data
      WHERE "Статус" = '3'
        and "Санкции" is null
        and "Номер счёта" not like '%I%') subquery
GROUP BY "Месяц"
union all
SELECT 'Итого',
       SUM(CASE WHEN "Цель" in ('30', '301', '305') THEN 1 ELSE 0 END) AS "Обращения",
       SUM(CASE WHEN "Цель" in ('22') THEN 1 ELSE 0 END)               AS "Неотложка",
       SUM(CASE WHEN "Цель" in ('3') THEN 1 ELSE 0 END)                AS "Д.наб",
       SUM(CASE WHEN "Цель" in ('64') THEN 1 ELSE 0 END)               AS "Гериатрия",
       SUM(CASE WHEN "Цель" in ('307') THEN 1 ELSE 0 END)               AS "307",
       SUM(CASE WHEN "Цель" in ('561') THEN 1 ELSE 0 END)               AS "561",
       SUM(CASE WHEN "Цель" in ('541') and "Сумма" = '542.13' THEN 1 ELSE 0 END) AS "541 УЗИ",
       SUM(CASE WHEN "Цель" in ('541') and "Сумма" = '857.55' THEN 1 ELSE 0 END) AS "541 Эндоскопия",
       SUM(CASE WHEN "Цель" in ('541') and "Сумма" = '2004.27' THEN 1 ELSE 0 END) AS "541 Колоноскопия"
FROM oms_data
WHERE "Статус" = '3'
  and "Санкции" is null
  and "Номер счёта" not like '%I%'
ORDER BY "Месяц"
        """


sql_query_pgg_dd = """
SELECT "Месяц",
       SUM(CASE WHEN "Цель" in ('ДВ4') THEN 1 else 0 END)              AS "ДВ4",
       ROUND(SUM(CASE WHEN "Цель" in ('ДВ4') THEN CAST("Сумма" AS numeric(15, 2)) else 0 END), 2) AS "ДВ4 сумма",
       SUM(CASE WHEN "Цель" in ('ДВ2') THEN 1 else 0 END)              AS "ДВ2",
       ROUND(SUM(CASE WHEN "Цель" in ('ДВ2') THEN CAST("Сумма" AS numeric(15, 2)) else 0 END), 2)              AS "ДВ2 сумма",
       SUM(CASE WHEN "Цель" in ('ОПВ') THEN 1 else 0 END)              AS "ОПВ",
       ROUND(SUM(CASE WHEN "Цель" in ('ОПВ') THEN CAST("Сумма" AS numeric(15, 2)) else 0 END), 2)              AS "ОПВ сумма",
       SUM(CASE WHEN "Цель" in ('УД1') THEN 1 else 0 END)              AS "УД1",
       ROUND(SUM(CASE WHEN "Цель" in ('УД1') THEN CAST("Сумма" AS numeric(15, 2)) else 0 END), 2)              AS "УД1 сумма",
       SUM(CASE WHEN "Цель" in ('УД2') THEN 1 else 0 END)              AS "УД2",
       ROUND(SUM(CASE WHEN "Цель" in ('УД2') THEN CAST("Сумма" AS numeric(15, 2)) else 0 END), 2)              AS "УД2 сумма",
       SUM(CASE WHEN "Цель" in ('ПН1') THEN 1 else 0 END)              AS "ПН1",
       ROUND(SUM(CASE WHEN "Цель" in ('ПН1') THEN CAST("Сумма" AS numeric(15, 2)) else 0 END), 2)             AS "ПН1 сумма",
       SUM(CASE WHEN "Цель" in ('ДС2') THEN 1 else 0 END)              AS "ДС2",
       ROUND(SUM(CASE WHEN "Цель" in ('ДС2') THEN CAST("Сумма" AS numeric(15, 2)) else 0 END), 2)              AS "ДС2 сумма"
FROM (SELECT CASE
                 WHEN "Номер счёта" LIKE '%/01/%' THEN '01'
                 WHEN "Номер счёта" LIKE '%/02/%' THEN '02'
                 WHEN "Номер счёта" LIKE '%/03/%' THEN '03'
                 WHEN "Номер счёта" LIKE '%/04/%' THEN '04'
                 WHEN "Номер счёта" LIKE '%/05/%' THEN '05'
                 WHEN "Номер счёта" LIKE '%/06/%' THEN '06'
                 WHEN "Номер счёта" LIKE '%/07/%' THEN '07'
                 WHEN "Номер счёта" LIKE '%/08/%' THEN '08'
                 WHEN "Номер счёта" LIKE '%/09/%' THEN '09'
                 WHEN "Номер счёта" LIKE '%/10/%' THEN '10'
                 WHEN "Номер счёта" LIKE '%/11/%' THEN '11'
                 WHEN "Номер счёта" LIKE '%/12/%' THEN '12'
                 END AS "Месяц",
             "Цель", 
             "Сумма"
      FROM oms_data
      WHERE "Статус" = '3'
        and "Санкции" is null
        and "Номер счёта" not like '%I%') subquery
GROUP BY "Месяц"
union all
SELECT 'Итого',
       SUM(CASE WHEN "Цель" in ('ДВ4') THEN 1 else 0 END)              AS "ДВ4",
       ROUND(SUM(CASE WHEN "Цель" in ('ДВ4') THEN CAST("Сумма" AS numeric(15, 2)) else 0 END), 2) AS "ДВ4 сумма",
       SUM(CASE WHEN "Цель" in ('ДВ2') THEN 1 else 0 END)              AS "ДВ2",
       ROUND(SUM(CASE WHEN "Цель" in ('ДВ2') THEN CAST("Сумма" AS numeric(15, 2)) else 0 END), 2)              AS "ДВ2 сумма",
       SUM(CASE WHEN "Цель" in ('ОПВ') THEN 1 else 0 END)              AS "ОПВ",
       ROUND(SUM(CASE WHEN "Цель" in ('ОПВ') THEN CAST("Сумма" AS numeric(15, 2)) else 0 END), 2)              AS "ОПВ сумма",
       SUM(CASE WHEN "Цель" in ('УД1') THEN 1 else 0 END)              AS "УД1",
       ROUND(SUM(CASE WHEN "Цель" in ('УД1') THEN CAST("Сумма" AS numeric(15, 2)) else 0 END), 2)              AS "УД1 сумма",
       SUM(CASE WHEN "Цель" in ('УД2') THEN 1 else 0 END)              AS "УД2",
       ROUND(SUM(CASE WHEN "Цель" in ('УД2') THEN CAST("Сумма" AS numeric(15, 2)) else 0 END), 2)              AS "УД2 сумма",
       SUM(CASE WHEN "Цель" in ('ПН1') THEN 1 else 0 END)              AS "ПН1",
       ROUND(SUM(CASE WHEN "Цель" in ('ПН1') THEN CAST("Сумма" AS numeric(15, 2)) else 0 END), 2)             AS "ПН1 сумма",
       SUM(CASE WHEN "Цель" in ('ДС2') THEN 1 else 0 END)              AS "ДС2",
       ROUND(SUM(CASE WHEN "Цель" in ('ДС2') THEN CAST("Сумма" AS numeric(15, 2)) else 0 END), 2)              AS "ДС2 сумма"
FROM oms_data
WHERE "Статус" = '3'
  and "Санкции" is null
  and "Номер счёта" not like '%I%'
ORDER BY "Месяц"
"""

sql_query_pgg_ds = """
SELECT "Месяц",
        count(*) as "Всего",
        ROUND(SUM(CAST("Сумма" AS numeric(15, 2))) ::numeric, 2)             AS "Всего сумма",
       SUM(CASE WHEN "Цель" in ('В дневном стационаре') THEN 1 ELSE 0 END)              AS "В дневном стационаре",
       ROUND(SUM(CASE WHEN "Цель" in ('В дневном стационаре') THEN CAST("Сумма" AS numeric(15, 2)) else 0 END) ::numeric, 2)             AS "В дневном стационаре сумма",
       SUM(CASE WHEN "Цель" in ('На дому') THEN 1 ELSE 0 END)              AS "На дому",
       ROUND(SUM(CASE WHEN "Цель" in ('На дому') THEN CAST("Сумма" AS numeric(15, 2)) else 0 END) ::numeric, 2)             AS "На дому сумма"
FROM (SELECT CASE
                 WHEN "Номер счёта" LIKE '%/01/%' THEN '01'
                 WHEN "Номер счёта" LIKE '%/02/%' THEN '02'
                 WHEN "Номер счёта" LIKE '%/03/%' THEN '03'
                 WHEN "Номер счёта" LIKE '%/04/%' THEN '04'
                 WHEN "Номер счёта" LIKE '%/05/%' THEN '05'
                 WHEN "Номер счёта" LIKE '%/06/%' THEN '06'
                 WHEN "Номер счёта" LIKE '%/07/%' THEN '07'
                 WHEN "Номер счёта" LIKE '%/08/%' THEN '08'
                 WHEN "Номер счёта" LIKE '%/09/%' THEN '09'
                 WHEN "Номер счёта" LIKE '%/10/%' THEN '10'
                 WHEN "Номер счёта" LIKE '%/11/%' THEN '11'
                 WHEN "Номер счёта" LIKE '%/12/%' THEN '12'
                 END AS "Месяц",
             "Цель",
             "Сумма"
      FROM oms_data
      WHERE "Статус" = '3'
        and "Тип талона" = 'Стационар'
        and "Санкции" is null
        and "Номер счёта" not like '%I%') subquery
GROUP BY "Месяц"
union all
SELECT 'Итого',
        count(*) as "Всего",
        ROUND(SUM(CAST("Сумма" AS numeric(15, 2))) ::numeric, 2)             AS "Всего сумма",
       SUM(CASE WHEN "Цель" in ('В дневном стационаре') THEN 1 ELSE 0 END)              AS "В дневном стационаре",
       ROUND(SUM(CASE WHEN "Цель" in ('В дневном стационаре') THEN CAST("Сумма" AS numeric(15, 2)) else 0 END) ::numeric, 2)             AS "В дневном стационаре сумма",
       SUM(CASE WHEN "Цель" in ('На дому') THEN 1 ELSE 0 END)              AS "На дому",
       ROUND(SUM(CASE WHEN "Цель" in ('На дому') THEN CAST("Сумма" AS numeric(15, 2)) else 0 END) ::numeric, 2)             AS "На дому сумма"
FROM oms_data
WHERE "Статус" = '3'
  and "Санкции" is null
  and "Тип талона" = 'Стационар'
  and "Номер счёта" not like '%I%'
ORDER BY "Месяц";
"""