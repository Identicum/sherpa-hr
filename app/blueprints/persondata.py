from flask import Blueprint, jsonify, current_app, abort
from models import db, PersonData
from schemas import PersonDataSchema

persondata_bp = Blueprint('persondata', __name__)

@persondata_bp.route('/api/persondata', methods=['GET'])
def api_list():
    """
    Get all persons along with their current work relationship
    ---
    tags:
      - PersonData
    responses:
      200:
        description: List of all persons, including workforce_id, work_type, manager_id, start_date, end_date
        schema:
          type: array
          items:
            $ref: '#/definitions/PersonData'
    """
    current_app.logger.debug("Fetching all PersonData from vw_persondata")
    persons = PersonData.query.order_by(PersonData.id).all()
    schema = PersonDataSchema(many=True)
    return jsonify(schema.dump(persons))

@persondata_bp.route('/api/persondata/<int:person_id>', methods=['GET'])
def api_get(person_id):
    """
    Get a specific person along with current work relationship
    ---
    tags:
      - PersonData
    parameters:
      - name: person_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Person details with workforce info
        schema:
          $ref: '#/definitions/PersonData'
      404:
        description: Person not found
    """
    current_app.logger.debug("Fetching PersonData for id: {}", person_id)
    person = PersonData.query.get(person_id)
    if not person:
        current_app.logger.debug("PersonData with id: {} not found", person_id)
        abort(404)
    schema = PersonDataSchema()
    return jsonify(schema.dump(person))
