create table kvazar.obr_doc_log
(
    "File_name" text,
    "File_date" text,
    "Count"     bigint,
    name_text   text
);

alter table kvazar.obr_doc_log
    owner to postgres;

