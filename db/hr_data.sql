\c hrdb;

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
