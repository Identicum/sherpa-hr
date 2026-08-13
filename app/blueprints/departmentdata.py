from flask import Blueprint, jsonify, current_app, abort
from models import db, DepartmentData
from schemas import DepartmentDataSchema

departmentdata_bp = Blueprint('departmentdata', __name__)

@departmentdata_bp.route('/api/departmentdata', methods=['GET'])
def api_list():
    """
    Get all departments along with their manager info
    ---
    tags:
      - DepartmentData
    responses:
      200:
        description: List of all departments, including parent_name, department_type_name, manager_person_id
        schema:
          type: array
          items:
            $ref: '#/definitions/DepartmentData'
    """
    current_app.logger.debug("Fetching all DepartmentData from vw_department")
    departments = DepartmentData.query.order_by(DepartmentData.id).all()
    schema = DepartmentDataSchema(many=True)
    return jsonify(schema.dump(departments))

@departmentdata_bp.route('/api/departmentdata/<int:department_id>', methods=['GET'])
def api_get(department_id):
    """
    Get a specific department along with its manager info
    ---
    tags:
      - DepartmentData
    parameters:
      - name: department_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Department details with manager info
        schema:
          $ref: '#/definitions/DepartmentData'
      404:
        description: Department not found
    """
    current_app.logger.debug("Fetching DepartmentData for id: {}", department_id)
    department = DepartmentData.query.get(department_id)
    if not department:
        current_app.logger.debug("DepartmentData with id: {} not found", department_id)
        abort(404)
    schema = DepartmentDataSchema()
    return jsonify(schema.dump(department))
