from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Department

departments_bp = Blueprint('departments', __name__)

@departments_bp.route('/')
def list():
    departments = Department.query.order_by(Department.department_id).all()
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
    db.session.delete(dept)
    db.session.commit()
    flash('Department deleted!')
    return redirect(url_for('departments.list'))
