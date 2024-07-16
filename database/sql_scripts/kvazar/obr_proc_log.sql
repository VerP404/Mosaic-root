create table kvazar.obrproc_log
(
    "File_name" text,
    "File_date" text,
    "Count"     bigint,
    name_text   text
);

alter table kvazar.obrproc_log
    owner to postgres;

