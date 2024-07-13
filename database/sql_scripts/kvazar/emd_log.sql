create table kvazar.emd_log
(
    "File_name" text,
    "File_date" text,
    "Count"     bigint,
    name_text   text
);

alter table kvazar.emd_log
    owner to postgres;

