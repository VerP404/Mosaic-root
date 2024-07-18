from dash import html

from services.MosaicMed.pages.admin.settings import settings_layout
from services.MosaicMed.pages.admin.users import users_layout
from services.MosaicMed.pages.admin.roles import roles_layout
from services.MosaicMed.pages.dispensary.adults.tab import app_tabs_da
from services.MosaicMed.pages.dispensary.children.tab import app_tabs_dc
from services.MosaicMed.pages.dispensary.reproductive.tab import app_tabs_reproductive
from services.MosaicMed.pages.doctors_talon.doctor.tab import app_tabs_doctors
from services.MosaicMed.pages.doctors_talon.doctors_list.tab import app_tabs_doctors_list
from services.MosaicMed.pages.economic_reports.by_doctors.tab import app_tabs_by_doctor
from services.MosaicMed.pages.economic_reports.reports.tab import app_tabs_econ_reports
from services.MosaicMed.pages.economic_reports.sv_pod.sv_pod import tab_layout_sv_pod
from services.MosaicMed.pages.economic_reports.volumes_indicators.volumes_indicators import app_pgg_amb
from services.MosaicMed.pages.it_department.update_database.update_database import tab_layout_it_update_bd

# Проверка доступа для специфичных маршрутов
routes = {
    "/doctors-report/doctor": app_tabs_doctors,
    "/doctors-report/list-doctors": app_tabs_doctors_list,
    "/dispensary/adult": app_tabs_da,
    "/dispensary/children": app_tabs_dc,
    "/dispensary/reproductive": app_tabs_reproductive,
    "/econ/sv-pod": tab_layout_sv_pod,
    "/econ/report": app_tabs_econ_reports,
    "/econ/pgg": app_pgg_amb,
    "/econ/by-doctor": app_tabs_by_doctor,
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
