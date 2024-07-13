create table kvazar.ln_data
(
    "Номер"                             text,
    "ЭЛН"                               text,
    "Дубликат"                          text,
    "Статус"                            text,
    "Статус ФСС"                        text,
    "Дата выдачи"                       text,
    "Первичный"                         text,
    "Предыдущий ЛН"                     text,
    "Следущий ЛН"                       text,
    "Фамилия пациента"                  text,
    "Имя пациента"                      text,
    "Отчество пациента"                 text,
    "Дата рождения"                     text,
    "Пол"                               text,
    "СНИЛС"                             text,
    "Возраст"                           text,
    "Место работы"                      text,
    "Код причины нетрудоспособности"    text,
    "МКБ"                               text,
    "Период нетрудоспособности: дата н" text,
    "Период нетрудоспособности: дата о" text,
    "Количество дней"                   text,
    "ТВСП"                              text,
    "Выдавший врач"                     text,
    "Закрывший врач"                    text,
    "Дата закрытия"                     text,
    "№ истории болезни"                 text,
    "Уход за больными"                  text,
    "Unnamed: 28"                       text
);

alter table kvazar.ln_data
    owner to postgres;

