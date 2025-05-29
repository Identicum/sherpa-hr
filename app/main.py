import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Department, Position, Employee, Contractor
import config as config
from sqlalchemy.orm import aliased

app = Flask(__name__)
app.config.from_object(config)
app.secret_key = app.config.get('SECRET_KEY', 'supersecretkey')
db.init_app(app)

# --- Position Views ---
@app.route('/positions')
def positions():
    positions = Position.query.outerjoin(Department).add_entity(Department).order_by(Position.position_id).all()
    # positions is a list of (Position, Department) tuples
    return render_template('positions.html', positions=[(p.position_id, p.title, p.description, d.name if d else None) for p, d in positions])

@app.route('/positions/add', methods=['GET', 'POST'])
def add_position():
    departments = Department.query.order_by(Department.name).all()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        department_id = request.form['department_id'] or None
        pos = Position(title=title, description=description, department_id=department_id)
        db.session.add(pos)
        db.session.commit()
        flash('Position added!')
        return redirect(url_for('positions'))
    return render_template('position_form.html', action='Add', departments=[(d.department_id, d.name) for d in departments])

@app.route('/positions/edit/<int:position_id>', methods=['GET', 'POST'])
def edit_position(position_id):
    pos = Position.query.get_or_404(position_id)
    departments = Department.query.order_by(Department.name).all()
    if request.method == 'POST':
        pos.title = request.form['title']
        pos.description = request.form['description']
        pos.department_id = request.form['department_id'] or None
        db.session.commit()
        flash('Position updated!')
        return redirect(url_for('positions'))
    position = (pos.title, pos.description, pos.department_id)
    return render_template('position_form.html', action='Edit', position=position, position_id=position_id, departments=[(d.department_id, d.name) for d in departments])

@app.route('/positions/delete/<int:position_id>', methods=['POST'])
def delete_position(position_id):
    pos = Position.query.get_or_404(position_id)
    db.session.delete(pos)
    db.session.commit()
    flash('Position deleted!')
    return redirect(url_for('positions'))

@app.route('/employees')
def employees():
    Manager = aliased(Employee)
    employees = db.session.query(Employee, Position, Department, Manager).\
        outerjoin(Position, Employee.position_id == Position.position_id).\
        outerjoin(Department, Position.department_id == Department.department_id).\
        outerjoin(Manager, Employee.manager_id == Manager.employee_id).\
        order_by(Employee.employee_id).all()
    # employees is a list of (Employee, Position, Department, Manager) tuples
    def emp_row(e, p, d, m):
        return (
            e.employee_id, e.first_name, e.last_name, e.personal_email,
            p.title if p else '', d.name if d else '',
            (m.first_name if m else None), (m.last_name if m else None)
        )
    return render_template('employees.html', employees=[emp_row(*row) for row in employees])

@app.route('/employees/add', methods=['GET', 'POST'])
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
        return redirect(url_for('employees'))
    return render_template('employee_form.html', action='Add', positions=[(p.position_id, p.title) for p in positions], managers=[(m.employee_id, m.first_name, m.last_name) for m in managers])

@app.route('/employees/edit/<int:employee_id>', methods=['GET', 'POST'])
def edit_employee(employee_id):
    emp = Employee.query.get_or_404(employee_id)
    positions = Position.query.order_by(Position.title).all()
    # Exclude the current employee from the manager list
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
        return redirect(url_for('employees'))
    employee = (
        emp.first_name, emp.last_name, emp.personal_email, emp.org_email, emp.username, emp.id_number, emp.tax_id, emp.start_date, emp.end_date, emp.position_id, emp.manager_id
    )
    return render_template('employee_form.html', action='Edit', employee=employee, employee_id=employee_id, positions=[(p.position_id, p.title) for p in positions], managers=[(m.employee_id, m.first_name, m.last_name) for m in managers])

@app.route('/employees/delete/<int:employee_id>', methods=['POST'])
def delete_employee(employee_id):
    emp = Employee.query.get_or_404(employee_id)
    db.session.delete(emp)
    db.session.commit()
    flash('Employee deleted!')
    return redirect(url_for('employees'))
# --- Contractor Views ---
@app.route('/contractors')
def contractors():
    contractors = db.session.query(Contractor, Department, Employee).\
        outerjoin(Department, Contractor.department_id == Department.department_id).\
        outerjoin(Employee, Contractor.manager_id == Employee.employee_id).\
        order_by(Contractor.contractor_id).all()
    # contractors is a list of (Contractor, Department, Manager) tuples
    def contractor_row(c, d, m):
        return (
            c.contractor_id, c.first_name, c.last_name, c.personal_email, c.company_name,
            d.name if d else '',
            (m.first_name if m else None), (m.last_name if m else None)
        )
    return render_template('contractors.html', contractors=[contractor_row(*row) for row in contractors])

@app.route('/contractors/add', methods=['GET', 'POST'])
def add_contractor():
    departments = Department.query.order_by(Department.name).all()
    managers = Employee.query.order_by(Employee.first_name, Employee.last_name).all()
    if request.method == 'POST':
        data = request.form
        contractor = Contractor(
            first_name=data['first_name'],
            last_name=data['last_name'],
            personal_email=data['personal_email'],
            org_email=data.get('org_email'),
            username=data.get('username'),
            id_number=data.get('id_number'),
            tax_id=data['tax_id'],
            start_date=data['start_date'],
            end_date=data.get('end_date') or None,
            company_name=data.get('company_name'),
            department_id=data.get('department_id') or None,
            manager_id=data.get('manager_id') or None
        )
        db.session.add(contractor)
        db.session.commit()
        flash('Contractor added!')
        return redirect(url_for('contractors'))
    return render_template('contractor_form.html', action='Add', departments=[(d.department_id, d.name) for d in departments], managers=[(m.employee_id, m.first_name, m.last_name) for m in managers])

@app.route('/contractors/edit/<int:contractor_id>', methods=['GET', 'POST'])
def edit_contractor(contractor_id):
    contractor = Contractor.query.get_or_404(contractor_id)
    departments = Department.query.order_by(Department.name).all()
    managers = Employee.query.order_by(Employee.first_name, Employee.last_name).all()
    if request.method == 'POST':
        data = request.form
        contractor.first_name = data['first_name']
        contractor.last_name = data['last_name']
        contractor.personal_email = data['personal_email']
        contractor.org_email = data.get('org_email')
        contractor.username = data.get('username')
        contractor.id_number = data.get('id_number')
        contractor.tax_id = data['tax_id']
        contractor.start_date = data['start_date']
        contractor.end_date = data.get('end_date') or None
        contractor.company_name = data.get('company_name')
        contractor.department_id = data.get('department_id') or None
        contractor.manager_id = data.get('manager_id') or None
        db.session.commit()
        flash('Contractor updated!')
        return redirect(url_for('contractors'))
    contractor_data = (
        contractor.first_name, contractor.last_name, contractor.personal_email, contractor.org_email, contractor.username, contractor.id_number, contractor.tax_id, contractor.start_date, contractor.end_date, contractor.company_name, contractor.department_id, contractor.manager_id
    )
    return render_template('contractor_form.html', action='Edit', contractor=contractor_data, contractor_id=contractor_id, departments=[(d.department_id, d.name) for d in departments], managers=[(m.employee_id, m.first_name, m.last_name) for m in managers])

@app.route('/contractors/delete/<int:contractor_id>', methods=['POST'])
def delete_contractor(contractor_id):
    contractor = Contractor.query.get_or_404(contractor_id)
    db.session.delete(contractor)
    db.session.commit()
    flash('Contractor deleted!')
    return redirect(url_for('contractors'))


# --- Department Views ---
@app.route('/')
def index():
    departments = Department.query.order_by(Department.department_id).all()
    return render_template('departments.html', departments=departments)

@app.route('/departments/add', methods=['GET', 'POST'])
def add_department():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        dept = Department(name=name, description=description)
        db.session.add(dept)
        db.session.commit()
        flash('Department added!')
        return redirect(url_for('index'))
    return render_template('department_form.html', action='Add')

@app.route('/departments/edit/<int:department_id>', methods=['GET', 'POST'])
def edit_department(department_id):
    dept = Department.query.get_or_404(department_id)
    if request.method == 'POST':
        dept.name = request.form['name']
        dept.description = request.form['description']
        db.session.commit()
        flash('Department updated!')
        return redirect(url_for('index'))
    department = (dept.name, dept.description)
    return render_template('department_form.html', action='Edit', department=department, department_id=department_id)

@app.route('/departments/delete/<int:department_id>', methods=['POST'])
def delete_department(department_id):
    dept = Department.query.get_or_404(department_id)
    db.session.delete(dept)
    db.session.commit()
    flash('Department deleted!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
