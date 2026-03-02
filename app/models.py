from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Department(db.Model):
    __tablename__ = 'department'
    department_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    positions = db.relationship('Position', backref='department', lazy=True)
    contractors = db.relationship('Contractor', backref='department', lazy=True)

class Position(db.Model):
    __tablename__ = 'position'
    position_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id', ondelete='RESTRICT'))
    employees = db.relationship('Employee', backref='position', lazy=True)

class Person(db.Model):
    __tablename__ = 'person'
    person_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    personal_email = db.Column(db.String(100), unique=True, nullable=False)
    org_email = db.Column(db.String(100))
    username = db.Column(db.String(50))
    id_number = db.Column(db.String(10), unique=True, nullable=False)
    tax_id = db.Column(db.String(15), unique=True, nullable=False)
    # relationships: specify foreign_keys to avoid ambiguity with manager references
    employee = db.relationship('Employee', backref='person', uselist=False, lazy=True,
                                foreign_keys='Employee.person_id')
    contractor = db.relationship('Contractor', backref='person', uselist=False, lazy=True,
                                  foreign_keys='Contractor.person_id')

class Employee(db.Model):
    __tablename__ = 'employee'
    employee_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id', ondelete='CASCADE'), nullable=False, unique=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    position_id = db.Column(db.Integer, db.ForeignKey('position.position_id', ondelete='RESTRICT'))
    manager_id = db.Column(db.Integer, db.ForeignKey('person.person_id', ondelete='SET NULL'))
    manager = db.relationship('Person', foreign_keys=[manager_id], lazy=True)

class Contractor(db.Model):
    __tablename__ = 'contractor'
    contractor_id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('person.person_id', ondelete='CASCADE'), nullable=False, unique=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    company_name = db.Column(db.String(100))
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id', ondelete='RESTRICT'))
    manager_id = db.Column(db.Integer, db.ForeignKey('person.person_id', ondelete='SET NULL'))
    manager = db.relationship('Person', foreign_keys=[manager_id], lazy=True)
