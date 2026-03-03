from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Department(db.Model):
    __tablename__ = 'department'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    positions = db.relationship('Position', backref='department', lazy=True)
    contractors = db.relationship('Contractor', backref='department', lazy=True)

class Position(db.Model):
    __tablename__ = 'position'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    department_id = db.Column('department', db.Integer, db.ForeignKey('department.id', ondelete='RESTRICT'))
    employees = db.relationship('Employee', backref='position', lazy=True)
    # department relationship provided by Department.positions backref

class Person(db.Model):
    __tablename__ = 'person'
    id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    personal_email = db.Column(db.String(100), unique=True, nullable=False)
    org_email = db.Column(db.String(100))
    username = db.Column(db.String(50))
    id_number = db.Column(db.String(10), unique=True, nullable=False)
    tax_id = db.Column(db.String(15), unique=True, nullable=False)
    employee = db.relationship('Employee', backref='person_rel', uselist=False, lazy=True, foreign_keys='Employee.person')
    contractor = db.relationship('Contractor', backref='person_rel', uselist=False, lazy=True, foreign_keys='Contractor.person')

class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column('id', db.Integer, primary_key=True)
    person = db.Column('person', db.Integer, db.ForeignKey('person.id', ondelete='CASCADE'), nullable=False, unique=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    position_id = db.Column('position', db.Integer, db.ForeignKey('position.id', ondelete='RESTRICT'))
    manager_id = db.Column('manager', db.Integer, db.ForeignKey('person.id', ondelete='SET NULL'))
    manager = db.relationship('Person', foreign_keys=[manager_id], lazy=True)
    # position relationship provided by Position.employees backref

class Contractor(db.Model):
    __tablename__ = 'contractor'
    id = db.Column('id', db.Integer, primary_key=True)
    person = db.Column('person', db.Integer, db.ForeignKey('person.id', ondelete='CASCADE'), nullable=False, unique=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    company_name = db.Column(db.String(100))
    department_id = db.Column('department', db.Integer, db.ForeignKey('department.id', ondelete='RESTRICT'))
    manager_id = db.Column('manager', db.Integer, db.ForeignKey('person.id', ondelete='SET NULL'))
    manager = db.relationship('Person', foreign_keys=[manager_id], lazy=True)
    # department relationship provided by Department.contractors backref
