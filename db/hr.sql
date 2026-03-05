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
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE position (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    department INT REFERENCES department(id) ON DELETE RESTRICT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE person (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 10001),
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
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 20001),
    person INT NOT NULL REFERENCES person(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE,
    position INT REFERENCES position(id) ON DELETE RESTRICT,
    manager INT REFERENCES person(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contractor (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 30001),
    person INT NOT NULL REFERENCES person(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE,
    company_name VARCHAR(100),
    department INT REFERENCES department(id) ON DELETE RESTRICT,
    manager INT REFERENCES person(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- --------------------------------------------------------------
-- VIEWS

CREATE OR REPLACE VIEW vw_employee AS
SELECT
    employee.id,
    employee.person,
    person.first_name,
    person.last_name,
    person.personal_email,
    person.org_email,
    person.username,
    person.id_number,
    person.tax_id,
    employee.start_date,
    employee.end_date,
    employee.position,
    employee.manager,
    position.name AS position_name,
    department.name AS department_name,
    CASE
        WHEN employee.start_date <= CURRENT_DATE AND (employee.end_date IS NULL OR employee.end_date>=CURRENT_DATE) THEN 'A'
        ELSE 'I'
    END AS status
FROM employee
JOIN person ON employee.person=person.id
LEFT JOIN position ON employee.position=position.id
LEFT JOIN department ON position.department=department.id;

CREATE OR REPLACE VIEW vw_contractor AS
SELECT
    contractor.id,
    contractor.person AS person,
    person.first_name,
    person.last_name,
    person.personal_email,
    person.org_email,
    person.username,
    person.id_number,
    person.tax_id,
    contractor.start_date,
    contractor.end_date,
    contractor.company_name,
    contractor.department,
    contractor.manager,
    department.name AS department_name,
    CASE
        WHEN contractor.start_date<=CURRENT_DATE AND (contractor.end_date IS NULL OR contractor.end_date>=CURRENT_DATE) THEN 'A'
        ELSE 'I'
    END AS status
FROM contractor
JOIN person ON contractor.person=person.id
LEFT JOIN department ON contractor.department=department.id;

-- view listing persons along with their current/last work relationship
CREATE OR REPLACE VIEW vw_persondata AS
WITH all_relationships AS (
    SELECT
        person AS person_id,
        'Employee' AS relationship_type,
        start_date,
        end_date,
        position_name,
        department_name,
        NULL::VARCHAR AS company_name,
        manager,
        status
    FROM vw_employee
    UNION ALL
    SELECT
        person AS person_id,
        'Contractor' AS relationship_type,
        start_date,
        end_date,
        NULL::VARCHAR AS position_name,
        department_name,
        company_name,
        manager,
        status
    FROM vw_contractor
),
ranked_relationships AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY person_id ORDER BY start_date DESC, end_date DESC NULLS FIRST) as rn
    FROM all_relationships
)
SELECT
    p.id,
    p.username,
    p.first_name,
    p.last_name,
    p.personal_email,
    p.org_email,
    p.id_number,
    p.tax_id,
    r.relationship_type,
    p.created_at,
    p.updated_at,
    r.start_date,
    r.end_date,
    r.status,
    r.position_name,
    r.department_name,
    r.manager,
    r.company_name
FROM person p
LEFT JOIN ranked_relationships r ON p.id = r.person_id AND r.rn = 1;


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

INSERT INTO position (name, description, department) VALUES
('Information Security Analyst', 'Analysis and security of information.', (SELECT id FROM department WHERE name = 'Information Security')),
('Administrative Analyst', 'Administrative support and daily operations.', (SELECT id FROM department WHERE name = 'Administration')),
('HR Analyst', 'Support in human resources and personnel management.', (SELECT id FROM department WHERE name = 'Human Resources'));

INSERT INTO person (first_name,last_name,personal_email,id_number,tax_id,org_email,username) VALUES
('John','Lennon','john.lennon@example.com','15012345','20-15012345-3',NULL,NULL),
('Paul','McCartney','paul.mccartney@example.com','20023456','20-20023456-7',NULL,NULL),
('George','Harrison','george.harrison@example.com','25034567','20-25034567-1',NULL,NULL),
('Ringo','Starr','ringo.starr@example.com','30045678','20-30045678-5',NULL,NULL),
('Eve','Adams','eve.adams@example.com','35056789','27-35056789-2',NULL,NULL),
('Frank','White','frank.white@example.com','40067890','20-40067890-8',NULL,NULL);

INSERT INTO employee (person,start_date,position,manager) VALUES
((SELECT id FROM person WHERE first_name='John' AND last_name='Lennon'),'1960-08-18',(SELECT id FROM position WHERE name='Information Security Analyst'),NULL),
((SELECT id FROM person WHERE first_name='Paul' AND last_name='McCartney'),'1960-08-18',(SELECT id FROM position WHERE name='Administrative Analyst'),(SELECT id FROM person WHERE first_name='John' AND last_name='Lennon')),
((SELECT id FROM person WHERE first_name='George' AND last_name='Harrison'),'1960-08-18',(SELECT id FROM position WHERE name='HR Analyst'),(SELECT id FROM person WHERE first_name='John' AND last_name='Lennon')),
((SELECT id FROM person WHERE first_name='Ringo' AND last_name='Starr'),'1962-08-14',(SELECT id FROM position WHERE name='Administrative Analyst'),(SELECT id FROM person WHERE first_name='John' AND last_name='Lennon'));

INSERT INTO contractor (person,start_date,company_name,department,manager) VALUES
((SELECT id FROM person WHERE first_name='Eve' AND last_name='Adams'),'2022-01-10','Tech Solutions Inc.',(SELECT id FROM department WHERE name='Information Security'),(SELECT person.id FROM person JOIN employee ON person.id=employee.person WHERE first_name='John' AND last_name='Lennon')),
((SELECT id FROM person WHERE first_name='Frank' AND last_name='White'),'2023-03-01','Creative Minds LLC',(SELECT id FROM department WHERE name='Marketing'),(SELECT person.id FROM person JOIN employee ON person.id=employee.person WHERE first_name='Paul' AND last_name='McCartney'));
