sql_query_stat_month = """
SELECT
    '/' || substring("Номер счёта" from 4 for 2) || '/' AS "Значение",
    count(*) AS "Количество",
           sum(case when "Статус" = '3' then 1 else 0 end)                                   as Оплачено,
       sum(case when "Статус" = '2' or "Статус" = '1' then 1 else 0 end)                   as "В ТФОМС",
       sum(case when "Статус" = '5' or "Статус" = '7' or "Статус" = '12' then 1 else 0 end)  as "Отказано",
       sum(case when "Статус" = '0' or "Статус" = '13' or "Статус" = '17' then 1 else 0 end) as "Отменен",
       sum(case when "Статус" = '1' then 1 else 0 end)                                   as "1",
       sum(case when "Статус" = '2' then 1 else 0 end)                                   as "2",
       sum(case when "Статус" = '3' then 1 else 0 end)                                   as "3",
       sum(case when "Статус" = '5' then 1 else 0 end)                                   as "5",
       sum(case when "Статус" = '6' then 1 else 0 end)                                   as "6",
       sum(case when "Статус" = '7' then 1 else 0 end)                                   as "7",
       sum(case when "Статус" = '8' then 1 else 0 end)                                   as "8",
       sum(case when "Статус" = '12' then 1 else 0 end)                                  as "12",
       sum(case when "Статус" = '13' then 1 else 0 end)                                  as "13",
       sum(case when "Статус" = '17' then 1 else 0 end)                                  as "17",
       sum(case when "Статус" = '0' then 1 else 0 end)                                   as "0"
FROM oms_data
WHERE "Номер счёта" ~ '/[0-9]{2}/' and "Санкции" is null
GROUP BY "Значение"
ORDER BY "Значение"
"""