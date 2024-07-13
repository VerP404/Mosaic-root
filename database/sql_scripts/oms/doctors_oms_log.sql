CREATE SCHEMA IF NOT EXISTS oms AUTHORIZATION postgres;

create table oms.doctors_oms_log
(
    "File_name" text,
    "File_date" text,
    "Count"     bigint,
    name_text   text
);

alter table oms.doctors_oms_log
    owner to postgres;

