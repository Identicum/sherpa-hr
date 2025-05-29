from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Position, Employee
from sqlalchemy.orm import aliased

employees_bp = Blueprint('employees', __name__)

@employees_bp.route('/employees')
def employees():
    Manager = aliased(Employee)
    from models import Department
    employees = db.session.query(Employee, Position, Department, Manager).\
        outerjoin(Position, Employee.position_id == Position.position_id).\
        outerjoin(Department, Position.department_id == Department.department_id).\
        outerjoin(Manager, Employee.manager_id == Manager.employee_id).\
        order_by(Employee.employee_id).all()
    def emp_row(e, p, d, m):
        manager_fullname = f"{m.first_name} {m.last_name}" if m else ''
        return (
            e.employee_id, e.first_name, e.last_name, e.personal_email,
            p.title if p else '',
            d.name if d else '',
            manager_fullname
        )
    return render_template('employees.html', employees=[emp_row(*row) for row in employees])

@employees_bp.route('/employees/add', methods=['GET', 'POST'])
def add_employee():
    positions = Position.query.order_by(Position.title).all()
    managers = Employee.query.order_by(Employee.first_name, Employee.last_name).all()
    if request.method == 'POST':
        data = request.form
        emp = Employee(
            first_name=data['first_name'],
            last_name=data['last_name'],
            personal_email=data['personal_email'],
            org_email=data.get('org_email'),
            username=data.get('username'),
            id_number=data.get('id_number'),
            tax_id=data.get('tax_id'),
            start_date=data['start_date'],
            end_date=data.get('end_date') or None,
            position_id=data.get('position_id') or None,
            manager_id=data.get('manager_id') or None
        )
        db.session.add(emp)
        db.session.commit()
        flash('Employee added!')
        return redirect(url_for('employees.employees'))
    return render_template('employee_form.html', action='Add', positions=[(p.position_id, p.title) for p in positions], managers=[(m.employee_id, m.first_name, m.last_name) for m in managers])

@employees_bp.route('/employees/edit/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    emp = Employee.query.get_or_404(employee_id)
    positions = Position.query.order_by(Position.title).all()
    managers = Employee.query.filter(Employee.employee_id != employee_id).order_by(Employee.first_name, Employee.last_name).all()
    if request.method == 'POST':
        data = request.form
        emp.first_name = data['first_name']
        emp.last_name = data['last_name']
        emp.personal_email = data['personal_email']
        emp.org_email = data.get('org_email')
        emp.username = data.get('username')
        emp.id_number = data.get('id_number')
        emp.tax_id = data.get('tax_id')
        emp.start_date = data['start_date']
        emp.end_date = data.get('end_date') or None
        emp.position_id = data.get('position_id') or None
        emp.manager_id = data.get('manager_id') or None
        db.session.commit()
        flash('Employee updated!')
        return redirect(url_for('employees.employees'))
    employee = (
        emp.first_name, emp.last_name, emp.personal_email, emp.org_email, emp.username, emp.id_number, emp.tax_id, emp.start_date, emp.end_date, emp.position_id, emp.manager_id
    )
    return render_template('employee_form.html', action='Edit', employee=employee, employee_id=employee_id, positions=[(p.position_id, p.title) for p in positions], managers=[(m.employee_id, m.first_name, m.last_name) for m in managers])

@employees_bp.route('/employees/delete/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    emp = Employee.query.get_or_404(employee_id)
    db.session.delete(emp)
    db.session.commit()
    flash('Employee deleted!')
    return redirect(url_for('employees.employees'))
