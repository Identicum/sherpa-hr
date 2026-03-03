from flask import abort, Blueprint, current_app, flash, jsonify, render_template, request, redirect, url_for
from models import db, Department, Employee, Position
from schemas import PositionSchema

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
        schema:
          type: array
          items:
            $ref: '#/definitions/Position'
    """
    positions = Position.query.outerjoin(Department).add_entity(Department).order_by(Position.id).all()
    positions_data = []
    for pos, dept in positions:
        positions_data.append({
            'id': pos.id,
            'name': pos.name,
            'description': pos.description,
            'department_id': dept.id if dept else None,
            'department_name': dept.name if dept else None
        })
    current_app.logger.debug("Returning list of {} positions", len(positions_data))
    return jsonify(PositionSchema(many=True).dump(positions_data))

@positions_bp.route('/api/positions/<int:position_id>', methods=['GET'])
def api_get(position_id):
    """
    Get a specific position
    ---
    tags:
      - Positions
    parameters:
      - name: position_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Position details
        schema:
          $ref: '#/definitions/Position'
      404:
        description: Position not found
    """
    pos = Position.query.outerjoin(Department).add_entity(Department).filter(Position.id == position_id).first()
    if pos is None:
        current_app.logger.debug("Position with id: {} not found", position_id)
        abort(404)
    position_obj, dept_obj = pos
    position_data = {
        'id': position_obj.id,
        'name': position_obj.name,
        'description': position_obj.description,
        'department_id': dept_obj.id if dept_obj else None,
        'department_name': dept_obj.name if dept_obj else None
    }
    current_app.logger.debug("Returning position data for id: {}", position_id)
    return jsonify(PositionSchema().dump(position_data))

@positions_bp.route('/positions')
def list():
    positions = Position.query.outerjoin(Department).add_entity(Department).order_by(Position.id).all()
    return render_template('positions.html', positions=[(p.id, p.name, p.description, d.name if d else None) for p, d in positions])

@positions_bp.route('/positions/add', methods=['GET', 'POST'])
def add():
    departments = Department.query.order_by(Department.name).all()
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        department_id = request.form['department_id'] or None
        pos = Position(name=name, description=description, department_id=department_id)
        db.session.add(pos)
        db.session.commit()
        flash('Position added!')
        return redirect(url_for('positions.list'))
    return render_template('position_form.html', action='Add', departments=[(d.id, d.name) for d in departments])

@positions_bp.route('/positions/edit/<int:position_id>', methods=['GET', 'POST'])
def update(position_id):
    pos = Position.query.get_or_404(position_id)
    departments = Department.query.order_by(Department.name).all()
    if request.method == 'POST':
        pos.name = request.form['name']
        pos.description = request.form['description']
        pos.department_id = request.form['department_id'] or None
        db.session.commit()
        flash('Position updated!')
        return redirect(url_for('positions.list'))
    position = (pos.name, pos.description, pos.department_id)
    return render_template('position_form.html', action='Update', position=position, position_id=position_id, departments=[(d.id, d.name) for d in departments])

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
