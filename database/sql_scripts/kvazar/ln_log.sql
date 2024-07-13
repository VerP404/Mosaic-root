create table kvazar.ln_log
(
    "File_name" text,
    "File_date" text,
    "Count"     bigint,
    name_text   text
);

alter table kvazar.ln_log
    owner to postgres;

