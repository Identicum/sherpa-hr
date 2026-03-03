from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Department, Position, Contractor

departments_bp = Blueprint('departments', __name__)

@departments_bp.route('/api/departments', methods=['GET'])
def api_list():
    """
    Get all departments
    ---
    tags:
      - Departments
    responses:
      200:
        description: List of all departments
    """
    departments = Department.query.order_by(Department.id).all()
    departments_data = []
    for dept in departments:
        departments_data.append({
            'id': dept.id,
            'name': dept.name,
            'description': dept.description
        })
    return jsonify(departments_data)

@departments_bp.route('/departments')
def list():
    departments = Department.query.order_by(Department.id).all()
    return render_template('departments.html', departments=departments)

@departments_bp.route('/departments/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        dept = Department(name=name, description=description)
        db.session.add(dept)
        db.session.commit()
        flash('Department added!')
        return redirect(url_for('departments.list'))
    return render_template('department_form.html', action='Add')

@departments_bp.route('/departments/edit/<int:department_id>', methods=['GET', 'POST'])
def update(department_id):
    dept = Department.query.get_or_404(department_id)
    if request.method == 'POST':
        dept.name = request.form['name']
        dept.description = request.form['description']
        db.session.commit()
        flash('Department updated!')
        return redirect(url_for('departments.list'))
    department = (dept.name, dept.description)
    return render_template('department_form.html', action='Update', department=department, department_id=department_id)

@departments_bp.route('/departments/delete/<int:department_id>', methods=['POST'])
def delete(department_id):
    dept = Department.query.get_or_404(department_id)
    pos_count = Position.query.filter_by(department_id=department_id).count()
    if pos_count > 0:
        flash('Cannot delete department: it has related positions.')
        return redirect(url_for('departments.list'))
    contractor_count = Contractor.query.filter_by(department_id=department_id).count()
    if contractor_count > 0:
        flash('Cannot delete department: it has assigned contractors.')
        return redirect(url_for('departments.list'))
    db.session.delete(dept)
    db.session.commit()
    flash('Department deleted!')
    return redirect(url_for('departments.list'))
