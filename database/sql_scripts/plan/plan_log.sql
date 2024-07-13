create table plan.plan_log
(
    "File_name" text,
    "File_date" text,
    "Count"     bigint,
    name_text   text
);

alter table plan.plan_log
    owner to postgres;

