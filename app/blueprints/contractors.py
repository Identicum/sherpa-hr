from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Department, Employee, Contractor

contractors_bp = Blueprint('contractors', __name__)

@contractors_bp.route('/contractors')
def contractors():
    contractors = db.session.query(Contractor, Department, Employee).\
        outerjoin(Department, Contractor.department_id == Department.department_id).\
        outerjoin(Employee, Contractor.manager_id == Employee.employee_id).\
        order_by(Contractor.contractor_id).all()
    def contractor_row(c, d, m):
        return (
            c.contractor_id, c.first_name, c.last_name, c.personal_email, c.company_name,
            d.name if d else '',
            (m.first_name if m else None), (m.last_name if m else None)
        )
    return render_template('contractors.html', contractors=[contractor_row(*row) for row in contractors])

@contractors_bp.route('/contractors/add', methods=['GET', 'POST'])
def add_contractor():
    departments = Department.query.order_by(Department.name).all()
    managers = Employee.query.order_by(Employee.first_name, Employee.last_name).all()
    if request.method == 'POST':
        data = request.form
        contractor = Contractor(
            first_name=data['first_name'],
            last_name=data['last_name'],
            personal_email=data['personal_email'],
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
        return redirect(url_for('contractors.contractors'))
    return render_template('contractor_form.html', action='Add', departments=[(d.department_id, d.name) for d in departments], managers=[(m.employee_id, m.first_name, m.last_name) for m in managers])

@contractors_bp.route('/contractors/edit/<int:contractor_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('contractors.contractors'))
    contractor_data = (
        contractor.first_name, contractor.last_name, contractor.personal_email, contractor.org_email, contractor.username, contractor.id_number, contractor.tax_id, contractor.start_date, contractor.end_date, contractor.company_name, contractor.department_id, contractor.manager_id
    )
    return render_template('contractor_form.html', action='Edit', contractor=contractor_data, contractor_id=contractor_id, departments=[(d.department_id, d.name) for d in departments], managers=[(m.employee_id, m.first_name, m.last_name) for m in managers])

@contractors_bp.route('/contractors/delete/<int:contractor_id>', methods=['POST'])
def delete_contractor(contractor_id):
    contractor = Contractor.query.get_or_404(contractor_id)
    db.session.delete(contractor)
    db.session.commit()
    flash('Contractor deleted!')
    return redirect(url_for('contractors.contractors'))
