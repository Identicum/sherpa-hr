from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Department, DepartmentType, Employee, Contractor
from schemas import DepartmentSchema

departments_bp = Blueprint('departments', __name__)

def _descendant_ids(dept):
    ids = set()
    stack = [*dept.children]
    while stack:
        child = stack.pop()
        if child.id not in ids:
            ids.add(child.id)
            stack.extend(child.children)
    return ids

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
        schema:
          type: array
          items:
            $ref: '#/definitions/Department'
    """
    departments = Department.query.order_by(Department.id).all()
    result = DepartmentSchema(many=True).dump(departments)
    return jsonify(result)

@departments_bp.route('/departments')
def list():
    departments = Department.query.filter_by(top_level=True).order_by(Department.id).all()
    return render_template('departments.html', departments=departments)

@departments_bp.route('/departments/<int:department_id>')
def detail(department_id):
    dept = Department.query.get_or_404(department_id)
    return render_template('department_detail.html', department=dept)

@departments_bp.route('/departments/add', methods=['GET', 'POST'])
def add():
    department_types = DepartmentType.query.order_by(DepartmentType.name).all()
    departments = Department.query.order_by(Department.name).all()
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        description = request.form['description']
        department_type_id = request.form['department_type_id']
        top_level = 'top_level' in request.form
        parent_id = request.form.get('parent_id') or None
        if not top_level and not parent_id:
            flash('Parent department is required unless this is a top level department.')
            return render_template('department_form.html', action='Add',
                                    departments=[(d.id, d.name) for d in departments],
                                    department_types=[(dt.id, dt.name) for dt in department_types])
        if top_level:
            parent_id = None
        dept = Department(name=name, code=code, description=description,
                           department_type_id=department_type_id,
                           top_level=top_level, parent_id=parent_id)
        db.session.add(dept)
        db.session.commit()
        flash('Department added!')
        return redirect(url_for('departments.list'))
    return render_template('department_form.html', action='Add',
                            departments=[(d.id, d.name) for d in departments],
                            department_types=[(dt.id, dt.name) for dt in department_types])

@departments_bp.route('/departments/edit/<int:department_id>', methods=['GET', 'POST'])
def update(department_id):
    dept = Department.query.get_or_404(department_id)
    department_types = DepartmentType.query.order_by(DepartmentType.name).all()
    excluded_parent_ids = _descendant_ids(dept) | {dept.id}
    departments = [d for d in Department.query.order_by(Department.name).all() if d.id not in excluded_parent_ids]
    if request.method == 'POST':
        name = request.form['name']
        code = request.form['code']
        description = request.form['description']
        department_type_id = request.form['department_type_id']
        top_level = 'top_level' in request.form
        parent_id = request.form.get('parent_id') or None
        if not top_level:
            if not parent_id or int(parent_id) in excluded_parent_ids:
                flash('Choose a valid parent department: it must be set and cannot be this department or one of its descendants.')
                return render_template('department_form.html', action='Update', department=(name, code, description, department_type_id, top_level, dept.parent_id), department_id=department_id,
                                        departments=[(d.id, d.name) for d in departments],
                                        department_types=[(dt.id, dt.name) for dt in department_types])
        else:
            parent_id = None
        dept.name = name
        dept.code = code
        dept.description = description
        dept.department_type_id = department_type_id
        dept.top_level = top_level
        dept.parent_id = parent_id
        db.session.commit()
        flash('Department updated!')
        return redirect(url_for('departments.detail', department_id=department_id))
    department = (dept.name, dept.code, dept.description, dept.department_type_id, dept.top_level, dept.parent_id)
    return render_template('department_form.html', action='Update', department=department, department_id=department_id,
                            departments=[(d.id, d.name) for d in departments],
                            department_types=[(dt.id, dt.name) for dt in department_types])

@departments_bp.route('/departments/delete/<int:department_id>', methods=['POST'])
def delete(department_id):
    dept = Department.query.get_or_404(department_id)
    employee_count = Employee.query.filter_by(department_id=department_id).count()
    if employee_count > 0:
        flash('Cannot delete department: it has assigned employees.')
        return redirect(url_for('departments.detail', department_id=department_id))
    contractor_count = Contractor.query.filter_by(department_id=department_id).count()
    if contractor_count > 0:
        flash('Cannot delete department: it has assigned contractors.')
        return redirect(url_for('departments.detail', department_id=department_id))
    child_count = Department.query.filter_by(parent_id=department_id).count()
    if child_count > 0:
        flash('Cannot delete department: it has child departments.')
        return redirect(url_for('departments.detail', department_id=department_id))
    parent_id = dept.parent_id
    db.session.delete(dept)
    db.session.commit()
    flash('Department deleted!')
    if parent_id:
        return redirect(url_for('departments.detail', department_id=parent_id))
    return redirect(url_for('departments.list'))
