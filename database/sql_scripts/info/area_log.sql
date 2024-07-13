create table info.area_log
(
    "File_name" text,
    "File_date" text,
    "Count"     bigint,
    name_text   text
);

alter table info.area_log
    owner to postgres;

