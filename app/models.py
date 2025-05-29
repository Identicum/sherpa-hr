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
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'))
    employees = db.relationship('Employee', backref='position', lazy=True)

class Employee(db.Model):
    __tablename__ = 'employee'
    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    personal_email = db.Column(db.String(100), unique=True, nullable=False)
    org_email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    id_number = db.Column(db.String(10), unique=True, nullable=False)
    tax_id = db.Column(db.String(15), unique=True, nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    position_id = db.Column(db.Integer, db.ForeignKey('position.position_id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
    subordinates = db.relationship('Employee', backref=db.backref('manager', remote_side=[employee_id]), lazy=True)
    contractors = db.relationship('Contractor', backref='manager', lazy=True, foreign_keys='Contractor.manager_id')

class Contractor(db.Model):
    __tablename__ = 'contractor'
    contractor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    personal_email = db.Column(db.String(100), unique=True, nullable=False)
    org_email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(50), unique=True)
    id_number = db.Column(db.String(10), unique=True, nullable=False)
    tax_id = db.Column(db.String(15), unique=True, nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    company_name = db.Column(db.String(100))
    department_id = db.Column(db.Integer, db.ForeignKey('department.department_id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.employee_id'))
