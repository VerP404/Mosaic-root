create table oms.oms_log
(
    "File_name" text,
    "File_date" text,
    "Count"     bigint,
    name_text   text
);

alter table oms.oms_log
    owner to postgres;

