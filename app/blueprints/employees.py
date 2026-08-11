from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from models import db, Contractor, Department, Employee, Position, Person

employees_bp = Blueprint('employees', __name__)

DEPARTMENT_RELATIONS = ['MANAGER', 'MEMBER']

@employees_bp.route('/employees')
def list():
    employees = db.session.query(Employee, Person, Position, Department).\
        join(Person, Employee.person == Person.id).\
        outerjoin(Position, Employee.position_id == Position.id).\
        join(Department, Employee.department_id == Department.id).\
        order_by(Employee.id).all()
    def emp_row(e, p, pos, d):
        return (
            e.id,
            p.first_name,
            p.last_name,
            pos.name if pos else '',
            d.name,
            e.department_relation
        )
    return render_template('employees.html', employees=[emp_row(*row) for row in employees])

def _has_other_manager(department_id, department_relation, exclude_employee_id=None):
    if department_relation != 'MANAGER':
        return False
    query = Employee.query.filter_by(department_id=department_id, department_relation='MANAGER')
    if exclude_employee_id is not None:
        query = query.filter(Employee.id != exclude_employee_id)
    return query.first() is not None

@employees_bp.route('/employees/add', methods=['GET', 'POST'])
def add():
    persons = Person.query.order_by(Person.last_name, Person.first_name).all()
    positions = Position.query.order_by(Position.name).all()
    departments = Department.query.order_by(Department.name).all()
    if request.method == 'POST':
        data = request.form
        person_id = data['person']
        department_id = data['department_id']
        department_relation = data.get('department_relation') or 'MEMBER'
        current_app.logger.debug("Attempting to add employee for person: {}", person_id)
        active_employee = Employee.query.filter_by(person=person_id).filter(Employee.end_date.is_(None)).first()
        if active_employee:
            current_app.logger.warn("Cannot add employee: this person already has an active employee.")
            flash('Cannot add employee: this person already has an active employee.')
            return redirect(url_for('employees.add'))
        active_contractor = Contractor.query.filter_by(person=person_id).filter(Contractor.end_date.is_(None)).first()
        if active_contractor:
            current_app.logger.warn("Cannot add employee: this person already has an active contractor.")
            flash('Cannot add employee: this person already has an active contractor.')
            return redirect(url_for('employees.add'))
        if _has_other_manager(department_id, department_relation):
            flash('Cannot add employee: this department already has a manager.')
            return redirect(url_for('employees.add'))
        emp = Employee(
            person=person_id,
            start_date=data['start_date'],
            end_date=data.get('end_date') or None,
            position_id=data.get('position_id') or None,
            department_id=department_id,
            department_relation=department_relation
        )
        db.session.add(emp)
        db.session.commit()
        flash('Employee added!')
        return redirect(url_for('employees.list'))
    return render_template('employee_form.html', action='Add',
                            persons=[(p.id, p.first_name, p.last_name) for p in persons],
                            positions=[(p.id, p.name) for p in positions],
                            departments=[(d.id, d.name) for d in departments],
                            department_relations=DEPARTMENT_RELATIONS)

@employees_bp.route('/employees/edit/<int:employee_id>', methods=['GET', 'POST'])
def update(employee_id):
    emp = Employee.query.get_or_404(employee_id)
    positions = Position.query.order_by(Position.name).all()
    departments = Department.query.order_by(Department.name).all()
    if request.method == 'POST':
        data = request.form
        department_id = data['department_id']
        department_relation = data.get('department_relation') or 'MEMBER'
        if _has_other_manager(department_id, department_relation, exclude_employee_id=emp.id):
            flash('Cannot update employee: this department already has a manager.')
            return redirect(url_for('employees.update', employee_id=employee_id))
        emp.start_date = data['start_date']
        emp.end_date = data.get('end_date') or None
        emp.position_id = data.get('position_id') or None
        emp.department_id = department_id
        emp.department_relation = department_relation
        db.session.commit()
        flash('Employee updated!')
        return redirect(url_for('employees.list'))
    return render_template('employee_form.html', action='Update', employee=emp, employee_id=employee_id,
                            positions=[(p.id, p.name) for p in positions],
                            departments=[(d.id, d.name) for d in departments],
                            department_relations=DEPARTMENT_RELATIONS)

@employees_bp.route('/employees/delete/<int:employee_id>', methods=['POST'])
def delete(employee_id):
    emp = Employee.query.get_or_404(employee_id)
    db.session.delete(emp)
    db.session.commit()
    flash('Employee deleted!')
    return redirect(url_for('employees.list'))
