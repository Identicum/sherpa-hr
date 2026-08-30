from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DepartmentType(db.Model):
    __tablename__ = 'department_type'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

class Department(db.Model):
    __tablename__ = 'department'
    __table_args__ = (
        db.CheckConstraint(
            "(top_level = true AND parent IS NULL) OR (top_level = false AND parent IS NOT NULL)",
            name='ck_department_toplevel_parent'
        ),
    )
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    code = db.Column(db.String(8), unique=True, nullable=False)
    top_level = db.Column(db.Boolean, nullable=False, default=True)
    parent_id = db.Column('parent', db.Integer, db.ForeignKey('department.id', ondelete='RESTRICT'))
    parent = db.relationship('Department', remote_side=[id], backref='children')
    department_type_id = db.Column('department_type', db.Integer, db.ForeignKey('department_type.id', ondelete='RESTRICT'), nullable=False)
    department_type = db.relationship('DepartmentType', backref='departments')
    employees = db.relationship('Employee', backref='department', lazy=True)
    contractors = db.relationship('Contractor', backref='department', lazy=True)
    manager_employee = db.relationship(
        'Employee',
        primaryjoin="and_(Employee.department_id==Department.id, Employee.department_relation=='MANAGER')",
        uselist=False,
        viewonly=True,
    )

    @property
    def manager_employee_id(self):
        return self.manager_employee.id if self.manager_employee else None

    @property
    def manager_person_id(self):
        return self.manager_employee.person if self.manager_employee else None

class Position(db.Model):
    __tablename__ = 'position'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    employees = db.relationship('Employee', backref='position', lazy=True)

class Person(db.Model):
    __tablename__ = 'person'
    __table_args__ = (
        db.CheckConstraint(
            "gender IN ('M', 'F', 'O')",
            name='ck_person_gender'
        ),
    )
    id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    personal_email = db.Column(db.String(100), unique=True, nullable=False)
    org_email = db.Column(db.String(100))
    username = db.Column(db.String(50))
    id_number = db.Column(db.String(10), unique=True, nullable=False)
    tax_id = db.Column(db.String(15), unique=True, nullable=False)
    gender = db.Column(db.String(1))
    birthdate = db.Column(db.Date)
    employee = db.relationship('Employee', backref='person_rel', uselist=False, lazy=True, foreign_keys='Employee.person')
    contractor = db.relationship('Contractor', backref='person_rel', uselist=False, lazy=True, foreign_keys='Contractor.person')

class Employee(db.Model):
    __tablename__ = 'employee'
    __table_args__ = (
        db.CheckConstraint(
            "department_relation IN ('MANAGER', 'MEMBER')",
            name='ck_employee_department_relation'
        ),
    )
    id = db.Column('id', db.Integer, primary_key=True)
    person = db.Column('person', db.Integer, db.ForeignKey('person.id', ondelete='CASCADE'), nullable=False, unique=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    position_id = db.Column('position', db.Integer, db.ForeignKey('position.id', ondelete='RESTRICT'))
    department_id = db.Column('department', db.Integer, db.ForeignKey('department.id', ondelete='RESTRICT'), nullable=False)
    department_relation = db.Column(db.String(10), nullable=False, default='MEMBER')
    # position relationship provided by Position.employees backref
    # department relationship provided by Department.employees backref

class Contractor(db.Model):
    __tablename__ = 'contractor'
    id = db.Column('id', db.Integer, primary_key=True)
    person = db.Column('person', db.Integer, db.ForeignKey('person.id', ondelete='CASCADE'), nullable=False, unique=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    company_name = db.Column(db.String(100))
    department_id = db.Column('department', db.Integer, db.ForeignKey('department.id', ondelete='RESTRICT'))
    # department relationship provided by Department.contractors backref

class PersonData(db.Model):
    __tablename__ = 'vw_persondata'
    # This is a view, so it should be read-only for ORM
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    personal_email = db.Column(db.String(100))
    org_email = db.Column(db.String(100))
    id_number = db.Column(db.String(10))
    tax_id = db.Column(db.String(15))
    gender = db.Column(db.String(1))
    birthdate = db.Column(db.Date)
    relationship_type = db.Column(db.String(20))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(1))
    position_id = db.Column(db.Integer)
    position_name = db.Column(db.String(100))
    department_id = db.Column(db.Integer)
    department_name = db.Column(db.String(100))
    department_relation = db.Column(db.String(10))
    company_name = db.Column(db.String(100))

class DepartmentData(db.Model):
    __tablename__ = 'vw_department'
    # This is a view, so it should be read-only for ORM
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text)
    code = db.Column(db.String(8))
    top_level = db.Column(db.Boolean)
    parent = db.Column(db.Integer)
    parent_name = db.Column(db.String(100))
    department_type = db.Column(db.Integer)
    department_type_name = db.Column(db.String(100))
    manager_employee_id = db.Column(db.Integer)
    manager_person_id = db.Column(db.Integer)
    manager_first_name = db.Column(db.String(50))
    manager_last_name = db.Column(db.String(50))
