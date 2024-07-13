create table iszl.iszl_log
(
    "File_name" text,
    "File_date" text,
    "Count"     bigint,
    name_text   text
);

alter table iszl.iszl_log
    owner to postgres;

