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
('Seguridad Informática', 'Responsable de la seguridad de la información y sistemas.'),
('Administración', 'Gestiona las operaciones administrativas y de oficina.'),
('RRHH', 'Administra los recursos humanos, incluyendo reclutamiento y beneficios.'),
('Marketing', 'Maneja la marca, publicidad e investigación de mercado.');

INSERT INTO position (title, description, department_id) VALUES
('Analista Seg Inf', 'Análisis y seguridad de la información.', (SELECT department_id FROM department WHERE name = 'Seguridad Informática')),
('Analista Administrativo', 'Soporte administrativo y operaciones diarias.', (SELECT department_id FROM department WHERE name = 'Administración')),
('Analista RRHH', 'Soporte en recursos humanos y gestión de personal.', (SELECT department_id FROM department WHERE name = 'RRHH'));


INSERT INTO employee (
    first_name, last_name, personal_email, id_number, tax_id, start_date, position_id
) VALUES
('John', 'Lennon', 'john.lennon@example.com', 'JL001', 'TAXJL001', '1960-08-18', (SELECT position_id FROM position WHERE title = 'Analista Seg Inf')),
('Paul', 'McCartney', 'paul.mccartney@example.com', 'PM002', 'TAXPM002', '1960-08-18', (SELECT position_id FROM position WHERE title = 'Analista Administrativo')),
('George', 'Harrison', 'george.harrison@example.com', 'GH003', 'TAXGH003', '1960-08-18', (SELECT position_id FROM position WHERE title = 'Analista RRHH')),
('Ringo', 'Starr', 'ringo.starr@example.com', 'RS004', 'TAXRS004', '1962-08-14', (SELECT position_id FROM position WHERE title = 'Analista Administrativo'));



INSERT INTO contractor (
    first_name, last_name, personal_email, id_number, tax_id, start_date, company_name, department_id, manager_id
) VALUES
('Eve', 'Adams', 'eve.adams@example.com', 'C001', 'CTAX001', '2022-01-10', 'Tech Solutions Inc.', (SELECT department_id FROM department WHERE name = 'Seguridad Informática'), (SELECT employee_id FROM employee WHERE first_name = 'John')),
('Frank', 'White', 'frank.white@example.com', 'C002', 'CTAX002', '2023-03-01', 'Creative Minds LLC', (SELECT department_id FROM department WHERE name = 'Marketing'), (SELECT employee_id FROM employee WHERE first_name = 'Paul'));


-- Update manager_id for some employees (example: Paul manages John and George)
UPDATE employee SET manager_id = (SELECT employee_id FROM employee WHERE first_name = 'Paul' AND last_name = 'McCartney') WHERE first_name IN ('John', 'George');

