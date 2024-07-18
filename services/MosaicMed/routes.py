from dash import html

from services.MosaicMed.pages.admin.settings import settings_layout
from services.MosaicMed.pages.admin.users import users_layout
from services.MosaicMed.pages.admin.roles import roles_layout
from services.MosaicMed.pages.doctors_talon.doctor.tab import app_tabs_doctors
from services.MosaicMed.pages.doctors_talon.doctors_list.tab import app_tabs_doctors_list
from services.MosaicMed.pages.it_department.update_database.update_database import tab_layout_it_update_bd

# Проверка доступа для специфичных маршрутов
routes = {
    "/doctors-report/doctor": app_tabs_doctors,
    "/doctors-report/list-doctors": app_tabs_doctors_list,
    "/dispensary/adult": html.H2("Взрослые"),
    "/dispensary/children": html.H2("Дети"),
    "/dispensary/reproductive": html.H2("Репродуктивное"),
    "/econ/sv-pod": html.H2("Экономические отчеты1"),
    "/econ/report": html.H2("Экономические отчеты2"),
    "/econ/pgg": html.H2("Экономические отчеты3"),
    "/econ/by-doctor": html.H2("Экономические отчеты4"),
    "/econ/by-doctor-cel": html.H2("Экономические отчеты5"),
    "/econ/by-doctor-dispensary": html.H2("Экономические отчеты6"),
    "/econ/new-territories": html.H2("Экономические отчеты7"),
    "/econ/route-children": html.H2("Экономические отчеты8"),
    "/econ/disp": html.H2("Экономические отчеты9"),
    "/it/gen-invoices": html.H2("it1"),
    "/it/update-bd": tab_layout_it_update_bd,
    "/it/stat-months": html.H2("it3"),
    "/it/for-smo": html.H2("it4"),
    "/it/cel3": html.H2("it5"),
    "/admin/users": users_layout,
    "/admin/roles": roles_layout(),
    "/admin/settings": settings_layout,
    "/iszl/disp-nab": html.H2("исзл1"),
    "/iszl/people": html.H2("исзл2"),
    "/dispensary-observation/adult": html.H2("Взрослые"),
    "/dispensary-observation/children": html.H2("Дети"),
    "/dispensary-observation/iszl": html.H2("ИСЗЛ"),
    "/other-reports": html.H2("Другие"),
    "/eln": html.H2("ЭЛН"),
    "/volumes/target": html.H2("Талоны"),
    "/volumes/finance": html.H2("Финансы"),
    "/templates": html.H2("Шаблоны"),
    "/filling-lists": html.H2("Списки"),
    "/wo-coupons": html.H2("Веб ОМС"),
    "/dashboard/chef": html.H2("Главный врач"),
    "/dashboard/patient": html.H2("Пациент"),
}
