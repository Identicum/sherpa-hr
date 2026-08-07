from flask import abort, Blueprint, current_app, flash, jsonify, render_template, request, redirect, url_for
from models import db, Employee, Position
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
    positions = Position.query.order_by(Position.id).all()
    current_app.logger.debug("Returning list of {} positions", len(positions))
    return jsonify(PositionSchema(many=True).dump(positions))

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
    pos = Position.query.get(position_id)
    if pos is None:
        current_app.logger.debug("Position with id: {} not found", position_id)
        abort(404)
    current_app.logger.debug("Returning position data for id: {}", position_id)
    return jsonify(PositionSchema().dump(pos))

@positions_bp.route('/positions')
def list():
    positions = Position.query.order_by(Position.id).all()
    return render_template('positions.html', positions=[(p.id, p.name, p.description) for p in positions])

@positions_bp.route('/positions/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        pos = Position(name=name, description=description)
        db.session.add(pos)
        db.session.commit()
        flash('Position added!')
        return redirect(url_for('positions.list'))
    return render_template('position_form.html', action='Add')

@positions_bp.route('/positions/edit/<int:position_id>', methods=['GET', 'POST'])
def update(position_id):
    pos = Position.query.get_or_404(position_id)
    if request.method == 'POST':
        pos.name = request.form['name']
        pos.description = request.form['description']
        db.session.commit()
        flash('Position updated!')
        return redirect(url_for('positions.list'))
    position = (pos.name, pos.description)
    return render_template('position_form.html', action='Update', position=position, position_id=position_id)

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
