create table kvazar.flu_log
(
    "File_name" text,
    "File_date" text,
    "Count"     bigint,
    name_text   text
);

alter table kvazar.flu_log
    owner to postgres;

