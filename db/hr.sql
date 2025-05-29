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
    department_id INT REFERENCES department(department_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE employee (
    employee_id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1001),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    personal_email VARCHAR(100) UNIQUE NOT NULL,
    org_email VARCHAR(100),
    username VARCHAR(50),
    id_number VARCHAR(10) UNIQUE NOT NULL,
    tax_id VARCHAR(15) UNIQUE NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    position_id INT REFERENCES position(position_id),
    manager_id INT REFERENCES employee(employee_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contractor (
    contractor_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    personal_email VARCHAR(100) UNIQUE NOT NULL,
    org_email VARCHAR(100),
    username VARCHAR(50),
    id_number VARCHAR(10) UNIQUE NOT NULL,
    tax_id VARCHAR(15) UNIQUE NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,
    company_name VARCHAR(100),
    department_id INT REFERENCES department(department_id),
    manager_id INT REFERENCES employee(employee_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

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


INSERT INTO employee (
    first_name, last_name, personal_email, id_number, tax_id, start_date, position_id
) VALUES
('John', 'Lennon', 'john.lennon@example.com', '15012345', '20-15012345-3', '1960-08-18', (SELECT position_id FROM position WHERE title = 'Information Security Analyst')),
('Paul', 'McCartney', 'paul.mccartney@example.com', '20023456', '20-20023456-7', '1960-08-18', (SELECT position_id FROM position WHERE title = 'Administrative Analyst')),
('George', 'Harrison', 'george.harrison@example.com', '25034567', '20-25034567-1', '1960-08-18', (SELECT position_id FROM position WHERE title = 'HR Analyst')),
('Ringo', 'Starr', 'ringo.starr@example.com', '30045678', '20-30045678-5', '1962-08-14', (SELECT position_id FROM position WHERE title = 'Administrative Analyst'));



INSERT INTO contractor (
    first_name, last_name, personal_email, id_number, tax_id, start_date, company_name, department_id, manager_id
) VALUES
('Eve', 'Adams', 'eve.adams@example.com', '35056789', '27-35056789-2', '2022-01-10', 'Tech Solutions Inc.', (SELECT department_id FROM department WHERE name = 'Information Security'), (SELECT employee_id FROM employee WHERE first_name = 'John')),
('Frank', 'White', 'frank.white@example.com', '40067890', '20-40067890-8', '2023-03-01', 'Creative Minds LLC', (SELECT department_id FROM department WHERE name = 'Marketing'), (SELECT employee_id FROM employee WHERE first_name = 'Paul'));


-- Update manager_id for some employees (example: Paul manages John and George)
UPDATE employee SET manager_id = (SELECT employee_id FROM employee WHERE first_name = 'Paul' AND last_name = 'McCartney') WHERE first_name IN ('John', 'George');

