\c hrdb;

-- --------------------------------------------------------------
-- DATA

INSERT INTO department_type (name) VALUES
('Board'),
('Division'),
('Team');

INSERT INTO department (name, description, code, top_level, parent, department_type) VALUES
('Sherpa_Inc', 'Sherpa, Inc.', 'Sherpa', TRUE, NULL, (SELECT id FROM department_type WHERE name = 'Board'));

INSERT INTO department (name, description, code, top_level, parent, department_type) VALUES
('Information Security', 'Responsible for information and systems security.', 'INFOSEC', FALSE, (SELECT id FROM department WHERE name = 'Sherpa_Inc'), (SELECT id FROM department_type WHERE name = 'Division')),
('Finance', 'Manages financial operations, accounting, and reporting.', 'FINANCE', FALSE, (SELECT id FROM department WHERE name = 'Sherpa_Inc'), (SELECT id FROM department_type WHERE name = 'Division')),
('Human Resources', 'Handles human resources, including recruitment and benefits.', 'HR', FALSE, (SELECT id FROM department WHERE name = 'Sherpa_Inc'), (SELECT id FROM department_type WHERE name = 'Division')),
('Marketing', 'Manages branding, advertising, and market research.', 'MKTG', FALSE, (SELECT id FROM department WHERE name = 'Sherpa_Inc'), (SELECT id FROM department_type WHERE name = 'Division')),
('Sales', 'Manages sales operations and client relationships.', 'SALES', FALSE, (SELECT id FROM department WHERE name = 'Sherpa_Inc'), (SELECT id FROM department_type WHERE name = 'Division'));

INSERT INTO department (name, description, code, top_level, parent, department_type) VALUES
('Security Operations', 'Monitors and responds to security incidents.', 'INFOSEC1', FALSE, (SELECT id FROM department WHERE code='INFOSEC'), (SELECT id FROM department_type WHERE name = 'Team')),
('Facilities', 'Manages offices, equipment and physical infrastructure.', 'FINANCE1', FALSE, (SELECT id FROM department WHERE code = 'FINANCE'), (SELECT id FROM department_type WHERE name = 'Team')),
('Accounts Payable', 'Manages outgoing payments to vendors and suppliers.', 'FINANCE2', FALSE, (SELECT id FROM department WHERE code = 'FINANCE'), (SELECT id FROM department_type WHERE name = 'Team')),
('Accounts Receivable', 'Manages incoming payments and customer invoicing.', 'FINANCE3', FALSE, (SELECT id FROM department WHERE code = 'FINANCE'), (SELECT id FROM department_type WHERE name = 'Team'));

INSERT INTO position (name, description) VALUES
('Manager', 'Manages a team and oversees departmental operations.'),
('Analyst', 'Performs analysis and supports daily operations.'),
('Director', 'Directs strategy and leads a department.');

INSERT INTO person (first_name,last_name,personal_email,id_number,tax_id,gender,birthdate) VALUES
('John','Lennon','john.lennon@example.com','15012345','20-15012345-3','M','1940-10-09'),
('Paul','McCartney','paul.mccartney@example.com','20023456','20-20023456-7','M','1942-06-18'),
('George','Harrison','george.harrison@example.com','25034567','20-25034567-1','M','1943-02-25'),
('Ringo','Starr','ringo.starr@example.com','30045678','20-30045678-5','M','1940-07-07');

INSERT INTO employee (person,start_date,position,department,department_relation) VALUES
((SELECT id FROM person WHERE personal_email='john.lennon@example.com'),'1960-08-18',(SELECT id FROM position WHERE name='Manager'),(SELECT id FROM department WHERE code='INFOSEC'),'MANAGER'),
((SELECT id FROM person WHERE personal_email='paul.mccartney@example.com'),'1960-08-18',(SELECT id FROM position WHERE name='Analyst'),(SELECT id FROM department WHERE code='FINANCE'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='george.harrison@example.com'),'1960-08-18',(SELECT id FROM position WHERE name='Analyst'),(SELECT id FROM department WHERE code='HR'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='ringo.starr@example.com'),'1962-08-14',(SELECT id FROM position WHERE name='Analyst'),(SELECT id FROM department WHERE code='FINANCE'),'MEMBER');

INSERT INTO person (first_name,last_name,personal_email,id_number,tax_id,gender,birthdate) VALUES
('Juan','Perez','jperez@example.com','10005','20-00010005-4','M','1993-10-01'),
('Maria','Rodriguez','mrodriguez@example.com','10006','27-00010006-4','F','1984-01-22'),
('Guillermo','Lopez','glopez@example.com','10007','20-00010007-4','M','1986-11-29'),
('Ana','Castro','acastro@example.com','10008','27-00010008-4','F','1995-08-31'),
('Roberto','Martinez','rmartinez@example.com','10009','20-00010009-4','M','1966-11-02'),
('Elena','Sosa','esosa@example.com','10010','27-00010010-4','F','1973-10-05'),
('Pedro','Lopez','plopez@example.com','10011','20-00010011-4','M','1999-11-05'),
('Juliana','Carrera','jcarrera@example.com','10012','27-00010012-4','F','1988-01-16'),
('Fabiana','Sanchez','fsanchez@example.com','10013','27-00010013-4','F','1969-07-24'),
('Jose','Valdez','jvaldez@example.com','10014','20-00010014-4','M','2000-07-02'),
('Raul','Mendez','rmendez@example.com','10015','20-00010015-4','M','1989-08-17'),
('Zoe','Prieto','zprieto@example.com','10016','27-00010016-4','F','1967-04-21'),
('Alonso','Luna','aluna@example.com','10017','20-00010017-4','M','1987-05-06'),
('Renata','Vargas','rvargas@example.com','10018','27-00010018-4','F','1983-09-22'),
('Ricardo','Lopez','rlopez@example.com','10019','20-00010019-4','M','1991-09-11'),
('Gabriela','Gomez','ggomez@example.com','10020','27-00010020-4','F','1974-03-12'),
('Javier','Garcia','jgarcia@example.com','10021','20-00010021-4','M','1983-12-07'),
('Marta','Torres','mtorres@example.com','10022','27-00010022-4','F','1988-03-09'),
('Rocio','Reyes','rreyes@example.com','10023','27-00010023-4','F','1994-11-05'),
('Carlos','Lopez','clopez@example.com','10024','20-00010024-4','M','1976-11-07'),
('Carmen','Alvarez','calvarez@example.com','10025','27-00010025-4','F','1979-03-14'),
('Julio','Villalba','jvillalba@example.com','10026','20-00010026-4','M','1984-10-11'),
('Sofia','Arias','sarias@example.com','10027','27-00010027-4','F','1972-06-19'),
('Luis','Vasquez','lvasquez@example.com','10028','20-00010028-4','M','1994-03-31'),
('Miguel','Vera','mvera@example.com','10029','20-00010029-4','M','1996-06-27'),
('Daniel','Cruz','dcruz@example.com','10030','20-00010030-4','M','1983-08-06'),
('Belen','Luna','bluna@example.com','10031','27-00010031-4','F','1978-07-11'),
('Alfredo','Serrano','aserrano@example.com','10032','20-00010032-4','M','1989-09-14'),
('Laura','Leiva','lleiva@example.com','10033','27-00010033-4','F','1996-10-12'),
('Olga','Gonzalez','ogonzalez@example.com','10034','27-00010034-4','F','1987-02-14'),
('Valeria','Quintero','vquintero@example.com','10035','27-00010035-4','F','1996-01-16'),
('Mario','Rios','mrios@example.com','10036','20-00010036-4','M','1995-04-01'),
('Alvaro','Beltran','abeltran@example.com','10037','20-00010037-4','M','1984-05-08'),
('Lucia','Perez','lperez@example.com','10038','27-00010038-4','F','1977-12-11'),
('Josefa','Parra','jparra@example.com','10039','27-00010039-4','F','1978-03-19'),
('Francisco','Gomez','fgomez@example.com','10040','20-00010040-4','M','1988-08-27'),
('Diego','Mendez','dmendez@example.com','10041','20-00010041-4','M','1984-09-12'),
('Gloria','Vera','gvera@example.com','10042','27-00010042-4','F','1997-07-27'),
('Yolanda','Gomez','ygomez@example.com','10043','27-00010043-4','F','1991-06-19'),
('Lidia','Barrera','lbarrera@example.com','10044','27-00010044-4','F','1985-12-11'),
('Nicolas','Reyes','nreyes@example.com','10045','20-00010045-4','M','1972-03-31'),
('Hector','Benitez','hbenitez@example.com','10046','20-00010046-4','M','1984-08-11'),
('Gabriela','Castro','gcastro@example.com','10047','27-00010047-4','F','1966-01-09'),
('Laura','Gomez','lgomez@example.com','10048','27-00010048-4','F','1980-10-17'),
('Fabio','Suarez','fsuarez@example.com','10049','20-00010049-4','M','1986-10-05'),
('Jorge','Torres','jtorres@example.com','10050','20-00010050-4','M','1981-04-12'),
('Clara','Serrano','cserrano@example.com','10051','27-00010051-4','F','1983-10-22'),
('Tatiana','Campos','tcampos@example.com','10052','27-00010052-4','F','1988-07-05'),
('Agustin','Gonzalez','agonzalez@example.com','10053','20-00010053-4','M','1981-01-05'),
('Vanesa','Bazan','vbazan@example.com','10054','27-00010054-4','F','1970-04-09');

INSERT INTO employee (person,start_date,position,department,department_relation) VALUES
((SELECT id FROM person WHERE personal_email='jperez@example.com'),'2025-09-01',(SELECT id FROM position WHERE name='Manager'),(SELECT id FROM department WHERE code='SALES'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='glopez@example.com'),'2018-03-16',(SELECT id FROM position WHERE name='Director'),(SELECT id FROM department WHERE code='MKTG'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='acastro@example.com'),'2020-08-19',(SELECT id FROM position WHERE name='Analyst'),(SELECT id FROM department WHERE code='MKTG'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='rmartinez@example.com'),'2018-02-17',(SELECT id FROM position WHERE name='Manager'),(SELECT id FROM department WHERE code='HR'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='plopez@example.com'),'2026-01-08',(SELECT id FROM position WHERE name='Manager'),(SELECT id FROM department WHERE code='SALES'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='jcarrera@example.com'),'2020-11-22',(SELECT id FROM position WHERE name='Analyst'),(SELECT id FROM department WHERE code='MKTG'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='fsanchez@example.com'),'2024-08-10',(SELECT id FROM position WHERE name='Director'),(SELECT id FROM department WHERE code='SALES'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='rmendez@example.com'),'2023-12-16',(SELECT id FROM position WHERE name='Analyst'),(SELECT id FROM department WHERE code='HR'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='zprieto@example.com'),'2023-02-13',(SELECT id FROM position WHERE name='Analyst'),(SELECT id FROM department WHERE code='SALES'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='aluna@example.com'),'2019-12-02',(SELECT id FROM position WHERE name='Manager'),(SELECT id FROM department WHERE code='MKTG'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='rvargas@example.com'),'2018-02-07',(SELECT id FROM position WHERE name='Director'),(SELECT id FROM department WHERE code='HR'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='rlopez@example.com'),'2026-06-06',(SELECT id FROM position WHERE name='Director'),(SELECT id FROM department WHERE code='SALES'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='jgarcia@example.com'),'2017-01-14',(SELECT id FROM position WHERE name='Manager'),(SELECT id FROM department WHERE code='HR'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='mtorres@example.com'),'2016-01-21',(SELECT id FROM position WHERE name='Analyst'),(SELECT id FROM department WHERE code='SALES'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='rreyes@example.com'),'2026-07-03',(SELECT id FROM position WHERE name='Director'),(SELECT id FROM department WHERE code='MKTG'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='clopez@example.com'),'2017-06-17',(SELECT id FROM position WHERE name='Manager'),(SELECT id FROM department WHERE code='HR'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='jvillalba@example.com'),'2018-08-03',(SELECT id FROM position WHERE name='Manager'),(SELECT id FROM department WHERE code='MKTG'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='sarias@example.com'),'2024-06-20',(SELECT id FROM position WHERE name='Analyst'),(SELECT id FROM department WHERE code='HR'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='lvasquez@example.com'),'2022-12-07',(SELECT id FROM position WHERE name='Director'),(SELECT id FROM department WHERE code='SALES'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='dcruz@example.com'),'2023-08-19',(SELECT id FROM position WHERE name='Director'),(SELECT id FROM department WHERE code='HR'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='bluna@example.com'),'2023-07-24',(SELECT id FROM position WHERE name='Manager'),(SELECT id FROM department WHERE code='SALES'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='aserrano@example.com'),'2025-07-01',(SELECT id FROM position WHERE name='Director'),(SELECT id FROM department WHERE code='MKTG'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='lleiva@example.com'),'2024-09-17',(SELECT id FROM position WHERE name='Analyst'),(SELECT id FROM department WHERE code='HR'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='ogonzalez@example.com'),'2020-08-21',(SELECT id FROM position WHERE name='Manager'),(SELECT id FROM department WHERE code='SALES'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='mrios@example.com'),'2017-05-18',(SELECT id FROM position WHERE name='Manager'),(SELECT id FROM department WHERE code='HR'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='abeltran@example.com'),'2017-07-27',(SELECT id FROM position WHERE name='Director'),(SELECT id FROM department WHERE code='SALES'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='lperez@example.com'),'2020-12-25',(SELECT id FROM position WHERE name='Manager'),(SELECT id FROM department WHERE code='MKTG'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='jparra@example.com'),'2022-08-18',(SELECT id FROM position WHERE name='Director'),(SELECT id FROM department WHERE code='HR'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='dmendez@example.com'),'2021-08-01',(SELECT id FROM position WHERE name='Director'),(SELECT id FROM department WHERE code='MKTG'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='gvera@example.com'),'2024-06-10',(SELECT id FROM position WHERE name='Analyst'),(SELECT id FROM department WHERE code='HR'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='ygomez@example.com'),'2018-07-19',(SELECT id FROM position WHERE name='Manager'),(SELECT id FROM department WHERE code='SALES'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='nreyes@example.com'),'2015-01-27',(SELECT id FROM position WHERE name='Manager'),(SELECT id FROM department WHERE code='HR'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='hbenitez@example.com'),'2020-11-27',(SELECT id FROM position WHERE name='Director'),(SELECT id FROM department WHERE code='SALES'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='lgomez@example.com'),'2019-01-03',(SELECT id FROM position WHERE name='Director'),(SELECT id FROM department WHERE code='HR'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='fsuarez@example.com'),'2026-05-21',(SELECT id FROM position WHERE name='Manager'),(SELECT id FROM department WHERE code='SALES'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='jtorres@example.com'),'2017-05-21',(SELECT id FROM position WHERE name='Manager'),(SELECT id FROM department WHERE code='MKTG'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='tcampos@example.com'),'2026-05-21',(SELECT id FROM position WHERE name='Director'),(SELECT id FROM department WHERE code='SALES'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='agonzalez@example.com'),'2019-06-18',(SELECT id FROM position WHERE name='Analyst'),(SELECT id FROM department WHERE code='MKTG'),'MEMBER'),
((SELECT id FROM person WHERE personal_email='vbazan@example.com'),'2018-06-06',(SELECT id FROM position WHERE name='Manager'),(SELECT id FROM department WHERE code='HR'),'MEMBER');

INSERT INTO contractor (person,start_date,company_name,department) VALUES
((SELECT id FROM person WHERE personal_email='mrodriguez@example.com'),'2025-04-16',NULL,(SELECT id FROM department WHERE code='SALES')),
((SELECT id FROM person WHERE personal_email='esosa@example.com'),'2020-07-13',NULL,(SELECT id FROM department WHERE code='HR')),
((SELECT id FROM person WHERE personal_email='jvaldez@example.com'),'2025-10-09',NULL,(SELECT id FROM department WHERE code='MKTG')),
((SELECT id FROM person WHERE personal_email='ggomez@example.com'),'2026-01-25',NULL,(SELECT id FROM department WHERE code='MKTG')),
((SELECT id FROM person WHERE personal_email='calvarez@example.com'),'2018-06-06',NULL,(SELECT id FROM department WHERE code='SALES')),
((SELECT id FROM person WHERE personal_email='mvera@example.com'),'2019-03-14',NULL,(SELECT id FROM department WHERE code='MKTG')),
((SELECT id FROM person WHERE personal_email='vquintero@example.com'),'2024-03-31',NULL,(SELECT id FROM department WHERE code='MKTG')),
((SELECT id FROM person WHERE personal_email='fgomez@example.com'),'2017-07-02',NULL,(SELECT id FROM department WHERE code='SALES')),
((SELECT id FROM person WHERE personal_email='lbarrera@example.com'),'2025-03-05',NULL,(SELECT id FROM department WHERE code='MKTG')),
((SELECT id FROM person WHERE personal_email='gcastro@example.com'),'2026-03-24',NULL,(SELECT id FROM department WHERE code='MKTG')),
((SELECT id FROM person WHERE personal_email='cserrano@example.com'),'2021-09-10',NULL,(SELECT id FROM department WHERE code='HR'));
