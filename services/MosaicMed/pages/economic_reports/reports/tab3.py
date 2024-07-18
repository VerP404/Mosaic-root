# import pandas as pd
# from sqlalchemy import text
# import dash_bootstrap_components as dbc
# from app import engine, app
# from dash import html, dash_table
#
#
# # Получаем список диагнозов приказа 168н
# def diagnoses_168n_to_df(eng):
#     with eng.connect() as conn:
#         sql_query = """
#             SELECT *
#             FROM plan
#         """
#         query = text(sql_query)
#         result = conn.execute(query)
#         columns = [desc[0] for desc in result.cursor.description]
#         rows = result.fetchall()
#         return pd.DataFrame(rows, columns=columns)
#
#
# df_do = diagnoses_168n_to_df(engine)
#
# tab3_layout_ec_report = html.Div(
#     [
#         dbc.Alert("Планы объемных показателей", color="primary"),
#         dash_table.DataTable(
#             id='result-table',
#             columns=[
#                 {'name': col, 'id': col} for col in df_do.columns
#             ],
#             data=df_do.to_dict('records'),
#             page_size=30,
#             editable=False,
#             filter_action="native",
#             sort_action="native",
#             sort_mode='multi',
#             export_format='xlsx',
#             export_headers='display', ),
#     ]
# )
