create table iszl.people_data
(
    "PID"         bigint,
    "FIO"         text,
    "DR"          text,
    "SMO"         text,
    "ENP"         text,
    "LPU"         text,
    "SS_DOCTOR"   text,
    "LPUUCH"      text,
    "Upd"         text,
    "CLOSED"      double precision,
    "Unnamed: 10" double precision
);

alter table iszl.people_data
    owner to postgres;

