CREATE DATABASE hrdb;

\c hrdb;

CREATE USER hrusr WITH PASSWORD 'hrpwd';
GRANT ALL PRIVILEGES ON DATABASE hrdb TO hrusr;
ALTER ROLE hrusr SET search_path TO public;

-- --------------------------------------------------------------
-- FUNCTIONS

CREATE OR REPLACE FUNCTION set_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.modification_time = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- --------------------------------------------------------------
-- TABLES

CREATE TABLE department (
    department_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE position (
    position_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    department_id INT REFERENCES department(department_id) ON DELETE RESTRICT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE person (
    person_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 10001),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    personal_email VARCHAR(100) UNIQUE NOT NULL,
    org_email VARCHAR(100),
    username VARCHAR(50),
    id_number VARCHAR(10) UNIQUE NOT NULL,
    tax_id VARCHAR(15) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE employee (
    employee_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 20001),
    person_id INT NOT NULL UNIQUE REFERENCES person(person_id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE,
    position_id INT REFERENCES position(position_id) ON DELETE RESTRICT,
    manager_id INT REFERENCES person(person_id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contractor (
    contractor_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 30001),
    person_id INT NOT NULL UNIQUE REFERENCES person(person_id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE,
    company_name VARCHAR(100),
    department_id INT REFERENCES department(department_id) ON DELETE RESTRICT,
    manager_id INT REFERENCES person(person_id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------------
-- VIEWS

CREATE OR REPLACE VIEW vw_employee AS
SELECT
    e.employee_id,
    e.person_id,
    per.first_name,
    per.last_name,
    per.personal_email,
    per.org_email,
    per.username,
    per.id_number,
    per.tax_id,
    e.start_date,
    e.end_date,
    e.position_id,
    e.manager_id,
    p.title AS position_name,
    d.name AS department_name,
    CASE
        WHEN e.start_date <= CURRENT_DATE AND (e.end_date IS NULL OR e.end_date >= CURRENT_DATE) THEN 'A'
        ELSE 'I'
    END AS status
FROM employee e
JOIN person per ON e.person_id = per.person_id
LEFT JOIN position p ON e.position_id = p.position_id
LEFT JOIN department d ON p.department_id = d.department_id;

CREATE OR REPLACE VIEW vw_contractor AS
SELECT
    c.contractor_id,
    c.person_id,
    per.first_name,
    per.last_name,
    per.personal_email,
    per.org_email,
    per.username,
    per.id_number,
    per.tax_id,
    c.start_date,
    c.end_date,
    c.company_name,
    c.department_id,
    c.manager_id,
    d.name AS department_name,
    CASE
        WHEN c.start_date <= CURRENT_DATE AND (c.end_date IS NULL OR c.end_date >= CURRENT_DATE) THEN 'A'
        ELSE 'I'
    END AS status
FROM contractor c
JOIN person per ON c.person_id = per.person_id
LEFT JOIN department d ON c.department_id = d.department_id;

-- view listing persons along with their current work relationship
CREATE OR REPLACE VIEW vw_person AS
SELECT
    per.person_id,
    per.first_name,
    per.last_name,
    per.personal_email,
    per.org_email,
    per.username,
    per.id_number,
    per.tax_id,
    COALESCE(e.employee_id, c.contractor_id) AS workforce_id,
    CASE
        WHEN e.employee_id IS NOT NULL THEN 'employee'
        WHEN c.contractor_id IS NOT NULL THEN 'contractor'
        ELSE NULL
    END AS work_type,
    CASE
        WHEN e.employee_id IS NOT NULL THEN e.manager_id
        WHEN c.contractor_id IS NOT NULL THEN c.manager_id
    END AS manager_id,
    CASE
        WHEN e.employee_id IS NOT NULL THEN e.start_date
        WHEN c.contractor_id IS NOT NULL THEN c.start_date
    END AS start_date,
    CASE
        WHEN e.employee_id IS NOT NULL THEN e.end_date
        WHEN c.contractor_id IS NOT NULL THEN c.end_date
    END AS end_date
FROM person per
LEFT JOIN employee e ON per.person_id = e.person_id
    AND e.start_date <= CURRENT_DATE
    AND (e.end_date IS NULL OR e.end_date >= CURRENT_DATE)
LEFT JOIN contractor c ON per.person_id = c.person_id
    AND c.start_date <= CURRENT_DATE
    AND (c.end_date IS NULL OR c.end_date >= CURRENT_DATE);


-- --------------------------------------------------------------
-- PERMISSIONS

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO hrusr;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO hrusr;

-- --------------------------------------------------------------
-- DATA

INSERT INTO department (name, description) VALUES
('Information Security', 'Responsible for information and systems security.'),
('Administration', 'Manages administrative and office operations.'),
('Human Resources', 'Handles human resources, including recruitment and benefits.'),
('Marketing', 'Manages branding, advertising, and market research.');

INSERT INTO position (title, description, department_id) VALUES
('Information Security Analyst', 'Analysis and security of information.', (SELECT department_id FROM department WHERE name = 'Information Security')),
('Administrative Analyst', 'Administrative support and daily operations.', (SELECT department_id FROM department WHERE name = 'Administration')),
('HR Analyst', 'Support in human resources and personnel management.', (SELECT department_id FROM department WHERE name = 'Human Resources'));

INSERT INTO person (first_name,last_name,personal_email,id_number,tax_id,org_email,username) VALUES
('John','Lennon','john.lennon@example.com','15012345','20-15012345-3',NULL,NULL),
('Paul','McCartney','paul.mccartney@example.com','20023456','20-20023456-7',NULL,NULL),
('George','Harrison','george.harrison@example.com','25034567','20-25034567-1',NULL,NULL),
('Ringo','Starr','ringo.starr@example.com','30045678','20-30045678-5',NULL,NULL),
('Eve','Adams','eve.adams@example.com','35056789','27-35056789-2',NULL,NULL),
('Frank','White','frank.white@example.com','40067890','20-40067890-8',NULL,NULL);

INSERT INTO employee (person_id,start_date,position_id,manager_id) VALUES
((SELECT person_id FROM person WHERE first_name='John' AND last_name='Lennon'),'1960-08-18',(SELECT position_id FROM position WHERE title = 'Information Security Analyst'),NULL),
((SELECT person_id FROM person WHERE first_name='Paul' AND last_name='McCartney'),'1960-08-18',(SELECT position_id FROM position WHERE title = 'Administrative Analyst'),(SELECT person_id FROM person WHERE first_name='John' AND last_name='Lennon')),
((SELECT person_id FROM person WHERE first_name='George' AND last_name='Harrison'),'1960-08-18',(SELECT position_id FROM position WHERE title = 'HR Analyst'),(SELECT person_id FROM person WHERE first_name='John' AND last_name='Lennon')),
((SELECT person_id FROM person WHERE first_name='Ringo' AND last_name='Starr'),'1962-08-14',(SELECT position_id FROM position WHERE title = 'Administrative Analyst'),(SELECT person_id FROM person WHERE first_name='John' AND last_name='Lennon'));

INSERT INTO contractor (person_id,start_date,company_name,department_id,manager_id) VALUES
((SELECT person_id FROM person WHERE first_name='Eve' AND last_name='Adams'),'2022-01-10','Tech Solutions Inc.',(SELECT department_id FROM department WHERE name = 'Information Security'),(SELECT p.person_id FROM person p JOIN employee e ON p.person_id=e.person_id WHERE p.first_name='John' AND last_name='Lennon')),
((SELECT person_id FROM person WHERE first_name='Frank' AND last_name='White'),'2023-03-01','Creative Minds LLC',(SELECT department_id FROM department WHERE name = 'Marketing'),(SELECT p.person_id FROM person p JOIN employee e ON p.person_id=e.person_id WHERE p.first_name='Paul' AND last_name='McCartney'));
