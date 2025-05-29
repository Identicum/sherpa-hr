from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Department

departments_bp = Blueprint('departments', __name__)

@departments_bp.route('/')
def index():
    departments = Department.query.order_by(Department.department_id).all()
    return render_template('departments.html', departments=departments)

@departments_bp.route('/departments/add', methods=['GET', 'POST'])
def add_department():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        dept = Department(name=name, description=description)
        db.session.add(dept)
        db.session.commit()
        flash('Department added!')
        return redirect(url_for('departments.index'))
    return render_template('department_form.html', action='Add')

@departments_bp.route('/departments/edit/<int:department_id>', methods=['GET', 'POST'])
def edit_department(department_id):
    dept = Department.query.get_or_404(department_id)
    if request.method == 'POST':
        dept.name = request.form['name']
        dept.description = request.form['description']
        db.session.commit()
        flash('Department updated!')
        return redirect(url_for('departments.index'))
    department = (dept.name, dept.description)
    return render_template('department_form.html', action='Edit', department=department, department_id=department_id)

@departments_bp.route('/departments/delete/<int:department_id>', methods=['POST'])
def delete_department(department_id):
    dept = Department.query.get_or_404(department_id)
    db.session.delete(dept)
    db.session.commit()
    flash('Department deleted!')
    return redirect(url_for('departments.index'))
