\c hrdb;

-- --------------------------------------------------------------
-- DATA

INSERT INTO department_type (name) VALUES
('Division'),
('Team');

INSERT INTO department (name, description, code, top_level, parent, department_type) VALUES
('CEO', 'CEO', 'CEO', TRUE, NULL, (SELECT id FROM department_type WHERE name = 'Division'));

INSERT INTO department (name, description, code, top_level, parent, department_type) VALUES
('Information Security', 'Responsible for information and systems security.', 'INFOSEC0', FALSE, (SELECT id FROM department WHERE name = 'CEO'), (SELECT id FROM department_type WHERE name = 'Division')),
('Finance', 'Manages financial operations, accounting, and reporting.', 'FIN00000', FALSE, (SELECT id FROM department WHERE name = 'CEO'), (SELECT id FROM department_type WHERE name = 'Division')),
('Human Resources', 'Handles human resources, including recruitment and benefits.', 'HR000000', FALSE, (SELECT id FROM department WHERE name = 'CEO'), (SELECT id FROM department_type WHERE name = 'Division')),
('Marketing', 'Manages branding, advertising, and market research.', 'MKTG0000', FALSE, (SELECT id FROM department WHERE name = 'CEO'), (SELECT id FROM department_type WHERE name = 'Division'));

INSERT INTO department (name, description, code, top_level, parent, department_type) VALUES
('Security Operations', 'Monitors and responds to security incidents.', 'INFOSEC1', FALSE, (SELECT id FROM department WHERE name = 'Information Security'), (SELECT id FROM department_type WHERE name = 'Team')),
('Facilities', 'Manages offices, equipment and physical infrastructure.', 'FIN00001', FALSE, (SELECT id FROM department WHERE name = 'Finance'), (SELECT id FROM department_type WHERE name = 'Team')),
('Accounts Payable', 'Manages outgoing payments to vendors and suppliers.', 'FIN00002', FALSE, (SELECT id FROM department WHERE name = 'Finance'), (SELECT id FROM department_type WHERE name = 'Team')),
('Accounts Receivable', 'Manages incoming payments and customer invoicing.', 'FIN00003', FALSE, (SELECT id FROM department WHERE name = 'Finance'), (SELECT id FROM department_type WHERE name = 'Team'));

INSERT INTO position (name, description) VALUES
('Information Security Analyst', 'Analysis and security of information.'),
('Administrative Analyst', 'Administrative support and daily operations.'),
('HR Analyst', 'Support in human resources and personnel management.');

INSERT INTO person (first_name,last_name,personal_email,id_number,tax_id,org_email,username) VALUES
('John','Lennon','john.lennon@example.com','15012345','20-15012345-3',NULL,NULL),
('Paul','McCartney','paul.mccartney@example.com','20023456','20-20023456-7',NULL,NULL),
('George','Harrison','george.harrison@example.com','25034567','20-25034567-1',NULL,NULL),
('Ringo','Starr','ringo.starr@example.com','30045678','20-30045678-5',NULL,NULL),
('Eve','Adams','eve.adams@example.com','35056789','27-35056789-2',NULL,NULL),
('Frank','White','frank.white@example.com','40067890','20-40067890-8',NULL,NULL);

INSERT INTO employee (person,start_date,position,department,department_relation) VALUES
((SELECT id FROM person WHERE first_name='John' AND last_name='Lennon'),'1960-08-18',(SELECT id FROM position WHERE name='Information Security Analyst'),(SELECT id FROM department WHERE name='Information Security'),'MANAGER'),
((SELECT id FROM person WHERE first_name='Paul' AND last_name='McCartney'),'1960-08-18',(SELECT id FROM position WHERE name='Administrative Analyst'),(SELECT id FROM department WHERE name='Finance'),'MEMBER'),
((SELECT id FROM person WHERE first_name='George' AND last_name='Harrison'),'1960-08-18',(SELECT id FROM position WHERE name='HR Analyst'),(SELECT id FROM department WHERE name='Human Resources'),'MEMBER'),
((SELECT id FROM person WHERE first_name='Ringo' AND last_name='Starr'),'1962-08-14',(SELECT id FROM position WHERE name='Administrative Analyst'),(SELECT id FROM department WHERE name='Finance'),'MEMBER');

INSERT INTO contractor (person,start_date,company_name,department) VALUES
((SELECT id FROM person WHERE first_name='Eve' AND last_name='Adams'),'2022-01-10','Tech Solutions Inc.',(SELECT id FROM department WHERE name='Information Security')),
((SELECT id FROM person WHERE first_name='Frank' AND last_name='White'),'2023-03-01','Creative Minds LLC',(SELECT id FROM department WHERE name='Marketing'));
