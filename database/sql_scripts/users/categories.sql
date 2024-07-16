create table users.categories
(
    id            SERIAL PRIMARY KEY,
    category_name VARCHAR(255) UNIQUE NOT NULL
);

alter table users.categories
    owner to postgres;

