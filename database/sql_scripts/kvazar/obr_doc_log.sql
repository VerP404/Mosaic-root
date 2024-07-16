create table kvazar.obrdoc_log
(
    "File_name" text,
    "File_date" text,
    "Count"     bigint,
    name_text   text
);

alter table kvazar.obrdoc_log
    owner to postgres;

