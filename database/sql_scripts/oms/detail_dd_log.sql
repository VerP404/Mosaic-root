create table oms.detail_dd_log
(
    "File_name" text,
    "File_date" text,
    "Count"     bigint,
    name_text   text
);

alter table oms.detail_dd_log
    owner to postgres;

