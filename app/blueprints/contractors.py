from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Department, Employee, Contractor, Person

contractors_bp = Blueprint('contractors', __name__)

@contractors_bp.route('/contractors')
def list():
    contractors = db.session.query(Contractor, Person, Department).\
        join(Person, Contractor.person_id == Person.person_id).\
        outerjoin(Department, Contractor.department_id == Department.department_id).\
        order_by(Contractor.contractor_id).all()
    def contractor_row(c, p, d):
        return (
            c.contractor_id,
            p.first_name,
            p.last_name,
            c.company_name,
            d.name if d else ''
        )
    return render_template('contractors.html', contractors=[contractor_row(*row) for row in contractors])

@contractors_bp.route('/contractors/add', methods=['GET', 'POST'])
def add():
    persons = Person.query.order_by(Person.last_name, Person.first_name).all()
    departments = Department.query.order_by(Department.name).all()
    managers = Person.query.order_by(Person.last_name, Person.first_name).all()
    if request.method == 'POST':
        data = request.form
        contractor = Contractor(
            person_id=data['person_id'],
            start_date=data['start_date'],
            end_date=data.get('end_date') or None,
            company_name=data.get('company_name'),
            department_id=data.get('department_id') or None,
            manager_id=data.get('manager_id') or None
        )
        db.session.add(contractor)
        db.session.commit()
        flash('Contractor added!')
        return redirect(url_for('contractors.list'))
    return render_template('contractor_form.html', action='Add', persons=[(p.person_id, p.first_name, p.last_name) for p in persons], departments=[(d.department_id, d.name) for d in departments], managers=[(p.person_id, p.first_name, p.last_name) for p in managers if p])

@contractors_bp.route('/contractors/edit/<int:contractor_id>', methods=['GET', 'POST'])
def update(contractor_id):
    contractor = Contractor.query.get_or_404(contractor_id)
    departments = Department.query.order_by(Department.name).all()
    managers = Person.query.order_by(Person.last_name, Person.first_name).all()
    if request.method == 'POST':
        data = request.form
        contractor.start_date = data['start_date']
        contractor.end_date = data.get('end_date') or None
        contractor.company_name = data.get('company_name')
        contractor.department_id = data.get('department_id') or None
        contractor.manager_id = data.get('manager_id') or None
        db.session.commit()
        flash('Contractor updated!')
        return redirect(url_for('contractors.list'))
    return render_template('contractor_form.html', action='Update', contractor=contractor, contractor_id=contractor_id, departments=[(d.department_id, d.name) for d in departments], managers=[(p.person_id, p.first_name, p.last_name) for p in managers if p])

@contractors_bp.route('/contractors/delete/<int:contractor_id>', methods=['POST'])
def delete(contractor_id):
    contractor = Contractor.query.get_or_404(contractor_id)
    db.session.delete(contractor)
    db.session.commit()
    flash('Contractor deleted!')
    return redirect(url_for('contractors.list'))
