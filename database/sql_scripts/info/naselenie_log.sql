create table info.naselenie_log
(
    "File_name" text,
    "File_date" text,
    "Count"     bigint,
    name_text   text
);

alter table info.naselenie_log
    owner to postgres;

