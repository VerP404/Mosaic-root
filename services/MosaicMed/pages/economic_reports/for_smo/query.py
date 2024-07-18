sql_query_for_smo = """
SELECT
    '01' as "Месяц",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36065' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Инко-Мед",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36071' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "СОГАЗ",
    TO_CHAR(sum(CASE WHEN "Код СМО" in ('36071','36065') THEN CAST("Сумма" AS numeric(10, 2))ELSE 0 END)::numeric, 'FM999999990.00') as "Итого"
FROM oms_data
WHERE "Номер счёта" LIKE '%/01/%'
    AND "Статус" IN ('2', '3')
GROUP BY "Месяц"
UNION ALL
SELECT
    '02' as "Месяц",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36065' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Инко-Мед",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36071' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "СОГАЗ",
    TO_CHAR(sum(CASE WHEN "Код СМО" in ('36071','36065') THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Итого"
FROM oms_data
WHERE "Номер счёта" LIKE '%/02/%'
    AND "Статус" IN ('2', '3')
GROUP BY "Месяц"
UNION ALL
SELECT
    '03' as "Месяц",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36065' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Инко-Мед",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36071' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "СОГАЗ",
    TO_CHAR(sum(CASE WHEN "Код СМО" in ('36071','36065') THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Итого"
FROM oms_data
WHERE "Номер счёта" LIKE '%/03/%'
    AND "Статус" IN ('2', '3')
GROUP BY "Месяц"
UNION ALL
SELECT
    '04' as "Месяц",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36065' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Инко-Мед",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36071' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "СОГАЗ",
    TO_CHAR(sum(CASE WHEN "Код СМО" in ('36071','36065') THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Итого"
FROM oms_data
WHERE "Номер счёта" LIKE '%/04/%'
    AND "Статус" IN ('2', '3')
GROUP BY "Месяц"
UNION ALL
SELECT
    '05' as "Месяц",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36065' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Инко-Мед",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36071' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "СОГАЗ",
    TO_CHAR(sum(CASE WHEN "Код СМО" in ('36071','36065') THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Итого"
FROM oms_data
WHERE "Номер счёта" LIKE '%/05/%'
    AND "Статус" IN ('2', '3')
GROUP BY "Месяц"
UNION ALL
SELECT
    '06' as "Месяц",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36065' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Инко-Мед",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36071' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "СОГАЗ",
    TO_CHAR(sum(CASE WHEN "Код СМО" in ('36071','36065') THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Итого"
FROM oms_data
WHERE "Номер счёта" LIKE '%/06/%'
    AND "Статус" IN ('2', '3')
GROUP BY "Месяц"
UNION ALL
SELECT
    '07' as "Месяц",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36065' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Инко-Мед",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36071' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "СОГАЗ",
    TO_CHAR(sum(CASE WHEN "Код СМО" in ('36071','36065') THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Итого"
FROM oms_data
WHERE "Номер счёта" LIKE '%/07/%'
    AND "Статус" IN ('2', '3')
GROUP BY "Месяц"
UNION ALL
SELECT
    '08' as "Месяц",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36065' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Инко-Мед",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36071' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "СОГАЗ",
    TO_CHAR(sum(CASE WHEN "Код СМО" in ('36071','36065') THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Итого"
FROM oms_data
WHERE "Номер счёта" LIKE '%/08/%'
    AND "Статус" IN ('2', '3')
GROUP BY "Месяц"
UNION ALL
SELECT
    '09' as "Месяц",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36065' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Инко-Мед",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36071' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "СОГАЗ",
    TO_CHAR(sum(CASE WHEN "Код СМО" in ('36071','36065') THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Итого"
FROM oms_data
WHERE "Номер счёта" LIKE '%/09/%'
    AND "Статус" IN ('2', '3')
GROUP BY "Месяц"
UNION ALL
SELECT
    '10' as "Месяц",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36065' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Инко-Мед",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36071' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "СОГАЗ",
    TO_CHAR(sum(CASE WHEN "Код СМО" in ('36071','36065') THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Итого"
FROM oms_data
WHERE "Номер счёта" LIKE '%/10/%'
    AND "Статус" IN ('2', '3')
    and "Санкции" is null
GROUP BY "Месяц"
UNION ALL
SELECT
    '11' as "Месяц",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36065' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Инко-Мед",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36071' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "СОГАЗ",
    TO_CHAR(sum(CASE WHEN "Код СМО" in ('36071','36065') THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Итого"
FROM oms_data
WHERE "Номер счёта" LIKE '%/11/%'
    AND "Статус" IN ('2', '3')
    and "Санкции" is null
GROUP BY "Месяц"
UNION ALL
SELECT
    '12' as "Месяц",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36065' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Инко-Мед",
    TO_CHAR(sum(CASE WHEN "Код СМО" = '36071' THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "СОГАЗ",
    TO_CHAR(sum(CASE WHEN "Код СМО" in ('36071','36065') THEN CAST("Сумма" AS numeric(10, 2)) ELSE 0 END)::numeric, 'FM999999990.00') as "Итого"
FROM oms_data
WHERE "Номер счёта" LIKE '%/12/%'
    AND "Статус" IN ('2', '3')
    and "Санкции" is null
GROUP BY "Месяц"
order by "Месяц"
"""