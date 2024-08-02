-- Create schema users
CREATE SCHEMA IF NOT EXISTS users;

-- Create table user
CREATE TABLE IF NOT EXISTS users.user
(
    id              SERIAL PRIMARY KEY,
    username        VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255)        NOT NULL,
    last_name       VARCHAR(255),
    first_name      VARCHAR(255),
    middle_name     VARCHAR(255),
    birth_date      DATE,
    position        VARCHAR(255),
    role            VARCHAR(255),
    category        VARCHAR(255)
);

-- Create table role_module_access
CREATE TABLE IF NOT EXISTS role_module_access
(
    id     SERIAL PRIMARY KEY,
    role   VARCHAR(255) NOT NULL,
    module VARCHAR(255) NOT NULL
);

-- Create table role_page_access
CREATE TABLE IF NOT EXISTS role_page_access
(
    id   SERIAL PRIMARY KEY,
    role VARCHAR(255) NOT NULL,
    page VARCHAR(255) NOT NULL
);

-- Create schema settings
CREATE SCHEMA IF NOT EXISTS settings;

-- Create table settings
CREATE TABLE IF NOT EXISTS settings.settings
(
    id    SERIAL PRIMARY KEY,
    name  VARCHAR(50) UNIQUE NOT NULL,
    value TEXT               NOT NULL
);

-- Create schema info
CREATE SCHEMA IF NOT EXISTS info;

-- Create table departments
CREATE TABLE IF NOT EXISTS info.departments
(
    id              SERIAL PRIMARY KEY,
    korpus          VARCHAR(255) NOT NULL,
    department_name VARCHAR(255) NOT NULL,
    registry_number VARCHAR(255) NOT NULL,
    oid             VARCHAR(255) NOT NULL,
    start_date      DATE         NOT NULL,
    end_date        DATE,
    f003mpcod       VARCHAR(255) NOT NULL,
    mis_kauz_korpus VARCHAR(255) NOT NULL
);
