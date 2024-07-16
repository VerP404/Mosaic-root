create table users.roles
(
    id        SERIAL PRIMARY KEY,
    role_name VARCHAR(255) UNIQUE NOT NULL
);

alter table users.roles
    owner to postgres;

