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

CREATE TABLE department_type (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE department (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    code VARCHAR(8) NOT NULL UNIQUE,
    top_level BOOLEAN NOT NULL DEFAULT TRUE,
    parent INT REFERENCES department(id) ON DELETE RESTRICT,
    department_type INT NOT NULL REFERENCES department_type(id) ON DELETE RESTRICT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_department_toplevel_parent CHECK (
        (top_level = TRUE AND parent IS NULL) OR (top_level = FALSE AND parent IS NOT NULL)
    )
);

CREATE TABLE position (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
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
    department INT NOT NULL REFERENCES department(id) ON DELETE RESTRICT,
    department_relation VARCHAR(10) NOT NULL DEFAULT 'MEMBER' CHECK (department_relation IN ('MANAGER', 'MEMBER')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- at most one employee can be the MANAGER of a given department
CREATE UNIQUE INDEX ix_employee_department_manager ON employee(department) WHERE department_relation = 'MANAGER';

CREATE TABLE contractor (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 30001),
    person INT NOT NULL REFERENCES person(id) ON DELETE CASCADE,
    start_date DATE NOT NULL,
    end_date DATE,
    company_name VARCHAR(100),
    department INT REFERENCES department(id) ON DELETE RESTRICT,
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
    employee.department,
    employee.department_relation,
    position.name AS position_name,
    department.name AS department_name,
    CASE
        WHEN employee.start_date <= CURRENT_DATE AND (employee.end_date IS NULL OR employee.end_date>=CURRENT_DATE) THEN 'A'
        ELSE 'I'
    END AS status
FROM employee
JOIN person ON employee.person=person.id
LEFT JOIN position ON employee.position=position.id
JOIN department ON employee.department=department.id;

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
        position,
        position_name,
        department_name,
        'Sherpa' AS company_name,
        department_relation,
        status
    FROM vw_employee
    UNION ALL
    SELECT
        person AS person_id,
        'Contractor' AS relationship_type,
        start_date,
        end_date,
        NULL::INT AS position,
        NULL::VARCHAR AS position_name,
        department_name,
        company_name,
        NULL::VARCHAR AS department_relation,
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
    COALESCE(r.status, 'I') AS status,
    r.position,
    r.position_name,
    r.department_name,
    r.department_relation,
    r.company_name
FROM person p
LEFT JOIN ranked_relationships r ON p.id = r.person_id AND r.rn = 1;


-- --------------------------------------------------------------
-- PERMISSIONS

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO hrusr;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO hrusr;
