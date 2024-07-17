create table info.departments
(
    id SERIAL PRIMARY KEY,
    korpus VARCHAR(255) NOT NULL,
    department_name VARCHAR(255) NOT NULL,
    registry_number VARCHAR(255) NOT NULL,
    oid VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    f003mpcod VARCHAR(255) NOT NULL,
    mis_kauz_korpus VARCHAR(255) NOT NULL
);

alter table info.departments
    owner to postgres;

