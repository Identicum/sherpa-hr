from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from models import db, Contractor, Department, Employee, Position, Person

employees_bp = Blueprint('employees', __name__)

@employees_bp.route('/employees')
def list():
    employees = db.session.query(Employee, Person, Position, Department).\
        join(Person, Employee.person_id == Person.person_id).\
        outerjoin(Position, Employee.position_id == Position.position_id).\
        outerjoin(Department, Position.department_id == Department.department_id).\
        order_by(Employee.employee_id).all()
    def emp_row(e, p, pos, d):
        return (
            e.employee_id,
            p.first_name,
            p.last_name,
            pos.title if pos else '',
            d.name if d else ''
        )
    return render_template('employees.html', employees=[emp_row(*row) for row in employees])

@employees_bp.route('/employees/add', methods=['GET', 'POST'])
def add():
    persons = Person.query.order_by(Person.last_name, Person.first_name).all()
    positions = Position.query.order_by(Position.title).all()
    managers = Person.query.order_by(Person.last_name, Person.first_name).all()
    if request.method == 'POST':
        data = request.form
        person_id = data['person_id']
        current_app.logger.debug("Attempting to add employee for person_id: %s", person_id)
        active_employee = Employee.query.filter_by(person_id=person_id).filter(Employee.end_date.is_(None)).first()
        if active_employee:
            current_app.logger.warn("Cannot add employee: this person already has an active employee.")
            flash('Cannot add employee: this person already has an active employee.')
            return redirect(url_for('employees.add'))
        active_contractor = Contractor.query.filter_by(person_id=person_id).filter(Contractor.end_date.is_(None)).first()
        if active_contractor:
            current_app.logger.warn("Cannot add employee: this person already has an active contractor.")
            flash('Cannot add employee: this person already has an active contractor.')
            return redirect(url_for('employees.add'))
        emp = Employee(
            person_id=person_id,
            start_date=data['start_date'],
            end_date=data.get('end_date') or None,
            position_id=data.get('position_id') or None,
            manager_id=data.get('manager_id') or None
        )
        db.session.add(emp)
        db.session.commit()
        flash('Employee added!')
        return redirect(url_for('employees.list'))
    return render_template('employee_form.html', action='Add', persons=[(p.person_id, p.first_name, p.last_name) for p in persons], positions=[(p.position_id, p.title) for p in positions], managers=[(p.person_id, p.first_name, p.last_name) for p in managers if p])

@employees_bp.route('/employees/edit/<int:employee_id>', methods=['GET', 'POST'])
def update(employee_id):
    emp = Employee.query.get_or_404(employee_id)
    positions = Position.query.order_by(Position.title).all()
    managers = Person.query.order_by(Person.last_name, Person.first_name).all()
    if request.method == 'POST':
        data = request.form
        emp.start_date = data['start_date']
        emp.end_date = data.get('end_date') or None
        emp.position_id = data.get('position_id') or None
        emp.manager_id = data.get('manager_id') or None
        db.session.commit()
        flash('Employee updated!')
        return redirect(url_for('employees.list'))
    return render_template('employee_form.html', action='Update', employee=emp, employee_id=employee_id, positions=[(p.position_id, p.title) for p in positions], managers=[(p.person_id, p.first_name, p.last_name) for p in managers if p])

@employees_bp.route('/employees/delete/<int:employee_id>', methods=['POST'])
def delete(employee_id):
    emp = Employee.query.get_or_404(employee_id)
    db.session.delete(emp)
    db.session.commit()
    flash('Employee deleted!')
    return redirect(url_for('employees.list'))
