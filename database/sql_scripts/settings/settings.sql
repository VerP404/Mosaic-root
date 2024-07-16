create table settings.settings
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    value TEXT NOT NULL
);

alter table settings.settings
    owner to postgres;

