from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, Department, Position

positions_bp = Blueprint('positions', __name__)

@positions_bp.route('/positions')
def positions():
    positions = Position.query.outerjoin(Department).add_entity(Department).order_by(Position.position_id).all()
    return render_template('positions.html', positions=[(p.position_id, p.title, p.description, d.name if d else None) for p, d in positions])

@positions_bp.route('/positions/add', methods=['GET', 'POST'])
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
        return redirect(url_for('positions.positions'))
    return render_template('position_form.html', action='Add', departments=[(d.department_id, d.name) for d in departments])

@positions_bp.route('/positions/edit/<int:position_id>', methods=['GET', 'POST'])
def edit_position(position_id):
    pos = Position.query.get_or_404(position_id)
    departments = Department.query.order_by(Department.name).all()
    if request.method == 'POST':
        pos.title = request.form['title']
        pos.description = request.form['description']
        pos.department_id = request.form['department_id'] or None
        db.session.commit()
        flash('Position updated!')
        return redirect(url_for('positions.positions'))
    position = (pos.title, pos.description, pos.department_id)
    return render_template('position_form.html', action='Edit', position=position, position_id=position_id, departments=[(d.department_id, d.name) for d in departments])

@positions_bp.route('/positions/delete/<int:position_id>', methods=['POST'])
def delete_position(position_id):
    pos = Position.query.get_or_404(position_id)
    db.session.delete(pos)
    db.session.commit()
    flash('Position deleted!')
    return redirect(url_for('positions.positions'))
