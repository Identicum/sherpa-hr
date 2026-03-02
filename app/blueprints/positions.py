from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Department, Employee, Position

positions_bp = Blueprint('positions', __name__)

@positions_bp.route('/api/positions', methods=['GET'])
def api_list():
    """
    Get all positions
    ---
    tags:
      - Positions
    responses:
      200:
        description: List of all positions
    """
    positions = Position.query.outerjoin(Department).add_entity(Department).order_by(Position.position_id).all()
    positions_data = []
    for pos, dept in positions:
        positions_data.append({
            'position_id': pos.position_id,
            'title': pos.title,
            'description': pos.description,
            'department_id': dept.department_id if dept else None,
            'department_name': dept.name if dept else None
        })
    return jsonify(positions_data)

@positions_bp.route('/positions')
def list():
    positions = Position.query.outerjoin(Department).add_entity(Department).order_by(Position.position_id).all()
    return render_template('positions.html', positions=[(p.position_id, p.title, p.description, d.name if d else None) for p, d in positions])

@positions_bp.route('/positions/add', methods=['GET', 'POST'])
def add():
    departments = Department.query.order_by(Department.name).all()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        department_id = request.form['department_id'] or None
        pos = Position(title=title, description=description, department_id=department_id)
        db.session.add(pos)
        db.session.commit()
        flash('Position added!')
        return redirect(url_for('positions.list'))
    return render_template('position_form.html', action='Add', departments=[(d.department_id, d.name) for d in departments])

@positions_bp.route('/positions/edit/<int:position_id>', methods=['GET', 'POST'])
def update(position_id):
    pos = Position.query.get_or_404(position_id)
    departments = Department.query.order_by(Department.name).all()
    if request.method == 'POST':
        pos.title = request.form['title']
        pos.description = request.form['description']
        pos.department_id = request.form['department_id'] or None
        db.session.commit()
        flash('Position updated!')
        return redirect(url_for('positions.list'))
    position = (pos.title, pos.description, pos.department_id)
    return render_template('position_form.html', action='Update', position=position, position_id=position_id, departments=[(d.department_id, d.name) for d in departments])

@positions_bp.route('/positions/delete/<int:position_id>', methods=['POST'])
def delete(position_id):
    pos = Position.query.get_or_404(position_id)
    employee_count = Employee.query.filter_by(position_id=position_id).count()
    if employee_count > 0:
        flash('Cannot delete position: it has related employees.')
        return redirect(url_for('positions.list'))
    db.session.delete(pos)
    db.session.commit()
    flash('Position deleted!')
    return redirect(url_for('positions.list'))
