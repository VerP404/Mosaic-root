create table oms.detaildd_log
(
    "File_name" text,
    "File_date" text,
    "Count"     bigint,
    name_text   text
);

alter table oms.detaildd_log
    owner to postgres;

