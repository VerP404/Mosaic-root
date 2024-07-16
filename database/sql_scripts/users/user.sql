create table users.user
(
    id              SERIAL PRIMARY KEY,
    username        VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255)        NOT NULL,
    last_name       VARCHAR(255)        NOT NULL,
    first_name      VARCHAR(255)        NOT NULL,
    middle_name     VARCHAR(255),
    birth_date      DATE,
    position        VARCHAR(255),
    role            VARCHAR(255)        NOT NULL,
    category        VARCHAR(255)
);

alter table users.user
    owner to postgres;

