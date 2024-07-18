sql_query_new_territiries = """
select "Цель" ,
       count(*) as "К-во случаев",
       ROUND(SUM(CAST("Сумма" AS numeric(15, 2))) ::numeric, 2) AS "Cумма"
from oms_data
where "ЕНП" in (
 '3691499779000290',
 '3687989740000375',
 '6147600847310131',
 '3647110877000588',
 '3652830871000621',
 '3649830829000653',
 '3656530894000568',
 '3693599720000527',
 '3676450885000202',
 '3657610880000753',
 '3695289744000285',
 '3658700872000546',
 '8558230892000342',
 '3647720823000423',
 '6153010874310163',
 '3691499718000385',
 '3688899728000355',
 '3655420871000446',
 '4896799774000133',
 '1054310873000307',
 '3655440891000465',
'3658610826000668',
'3648720898000455',
'3653630825000605',
'3658140893000771',
'3688299739000280',
'3688289724000015',
'4857100876000187',
'3653900879000573',
'3657920845000511',
'3654120868000554',
'3649600883000463'
)
group by "Цель"
"""

sqlquery_new_territory = f"""
    select "Страховая",
       count(*)                                                            as "Всего",
       SUM(CASE WHEN "Цель" in ('1') THEN 1 ELSE 0 END)                    AS "1",
       SUM(CASE WHEN "Цель" in ('3') THEN 1 ELSE 0 END)                    AS "3",
       SUM(CASE WHEN "Цель" in ('5') THEN 1 ELSE 0 END)                    AS "5",
       SUM(CASE WHEN "Цель" in ('7') THEN 1 ELSE 0 END)                    AS "7",
       SUM(CASE WHEN "Цель" in ('9') THEN 1 ELSE 0 END)                    AS "9",
       SUM(CASE WHEN "Цель" in ('10') THEN 1 ELSE 0 END)                   AS "10",
       SUM(CASE WHEN "Цель" in ('13') THEN 1 ELSE 0 END)                   AS "13",
       SUM(CASE WHEN "Цель" in ('14') THEN 1 ELSE 0 END)                   AS "14",
       SUM(CASE WHEN "Цель" in ('22') THEN 1 ELSE 0 END)                   AS "22",
       SUM(CASE WHEN "Цель" in ('30') THEN 1 ELSE 0 END)                   AS "30",
       SUM(CASE WHEN "Цель" in ('32') THEN 1 ELSE 0 END)                   AS "32",
       SUM(CASE WHEN "Цель" in ('64') THEN 1 ELSE 0 END)                   AS "64",
       SUM(CASE WHEN "Цель" in ('140') THEN 1 ELSE 0 END)                  AS "140",
       SUM(CASE WHEN "Цель" in ('301') THEN 1 ELSE 0 END)                  AS "301",
       SUM(CASE WHEN "Цель" in ('305') THEN 1 ELSE 0 END)                  AS "305",
       SUM(CASE WHEN "Цель" in ('307') THEN 1 ELSE 0 END)                  AS "307",
       SUM(CASE WHEN "Цель" in ('541') THEN 1 ELSE 0 END)                  AS "541",
       SUM(CASE WHEN "Цель" in ('561') THEN 1 ELSE 0 END)                  AS "561",
       SUM(CASE WHEN "Цель" in ('В дневном стационаре') THEN 1 ELSE 0 END) AS "В дс",
       SUM(CASE WHEN "Цель" in ('На дому') THEN 1 ELSE 0 END)              AS "На дому",
       SUM(CASE WHEN "Цель" in ('ДВ4') THEN 1 ELSE 0 END)                  AS "ДВ4",
       SUM(CASE WHEN "Цель" in ('ДВ2') THEN 1 ELSE 0 END)                  AS "ДВ2",
       SUM(CASE WHEN "Цель" in ('ОПВ') THEN 1 ELSE 0 END)                  AS "ОПВ",
       SUM(CASE WHEN "Цель" in ('УД1') THEN 1 ELSE 0 END)                  AS "УД1",
       SUM(CASE WHEN "Цель" in ('УД2') THEN 1 ELSE 0 END)                  AS "УД2",
       SUM(CASE WHEN "Цель" in ('ДР1') THEN 1 ELSE 0 END)                  AS "ДР1",
       SUM(CASE WHEN "Цель" in ('ДР2') THEN 1 ELSE 0 END)                  AS "ДР2",
       SUM(CASE WHEN "Цель" in ('ПН1') THEN 1 ELSE 0 END)                  AS "ПН1",
       SUM(CASE WHEN "Цель" in ('ДС2') THEN 1 ELSE 0 END)                  AS "ДС2"
    from oms_data
    where "Страховая" like '%ТФОМС%'
    and to_date("Окончание лечения", 'DD-MM-YYYY') BETWEEN to_date(:start_date, 'DD-MM-YYYY') and to_date(:end_date, 'DD-MM-YYYY')
    group by rollup ("Страховая")
    """
