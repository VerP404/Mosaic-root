create table iszl.people_log
(
    "File_name" text,
    "File_date" text,
    "Count"     bigint,
    name_text   text
);

alter table iszl.people_log
    owner to postgres;

