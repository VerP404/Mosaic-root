def sql_query_amb_def():
    return f"""
        select count(*)
        from oms.oms_data
        where "Цель" = '64'
            and "Отчетный период выгрузки" in :months
    """
