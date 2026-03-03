from flask import abort, Blueprint, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import text
from models import db, Person

persons_bp = Blueprint('persons', __name__)

@persons_bp.route('/api/persons', methods=['GET'])
def api_list():
    """
    Get all persons along with their current work relationship
    ---
    tags:
      - Persons
    responses:
      200:
        description: List of all persons, including workforce_id, work_type, manager_id, start_date, end_date
        schema:
          type: array
          items:
            $ref: '#/definitions/Person'
    """
    # use the view to simplify the query and ensure consistency with vw_person
    sql = text("SELECT * FROM vw_person ORDER BY id")
    result = db.session.execute(sql)
    # SQLAlchemy Row objects support a mapping interface
    persons_data = []
    for row in result.fetchall():
        rowmap = dict(row._mapping)
        persons_data.append(rowmap)
    from schemas import PersonSchema
    return jsonify(PersonSchema(many=True).dump(persons_data))

@persons_bp.route('/api/persons/<int:person_id>', methods=['GET'])
def api_get(person_id):
    """
    Get a specific person along with current work relationship
    ---
    tags:
      - Persons
    parameters:
      - name: person_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Person details with workforce info
        schema:
          $ref: '#/definitions/Person'
      404:
        description: Person not found
    """
    sql = text("SELECT * FROM vw_person WHERE id = :pid")
    row = db.session.execute(sql, {'pid': person_id}).fetchone()
    if row is None:
        abort(404)
    rowmap = dict(row._mapping)
    from schemas import PersonSchema
    return jsonify(PersonSchema().dump(rowmap))

@persons_bp.route('/api/persons/<int:person_id>', methods=['PATCH'])
def api_update(person_id):
    """
    Update person details
    ---
    tags:
      - Persons
    parameters:
      - name: person_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          properties:
            org_email:
              type: string
            username:
              type: string
    responses:
      200:
        description: Updated person details
    """
    person = Person.query.get_or_404(person_id)
    data = request.get_json()
    if 'org_email' in data:
        person.org_email = data['org_email']
    if 'username' in data:
        person.username = data['username']
    db.session.commit()
    return jsonify({
        'org_email': person.org_email,
        'username': person.username
    })

@persons_bp.route('/persons')
def list():
    persons = Person.query.order_by(Person.id).all()
    return render_template('persons.html', persons=persons)

@persons_bp.route('/persons/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form
        person = Person(
            first_name=data['first_name'],
            last_name=data['last_name'],
            personal_email=data['personal_email'],
            id_number=data.get('id_number'),
            tax_id=data.get('tax_id'),
            org_email=data.get('org_email'),
            username=data.get('username')
        )
        db.session.add(person)
        db.session.commit()
        flash('Person added!')
        return redirect(url_for('persons.list'))
    return render_template('person_form.html', action='Add')

@persons_bp.route('/persons/edit/<int:person_id>', methods=['GET', 'POST'])
def update(person_id):
    person = Person.query.get_or_404(person_id)
    if request.method == 'POST':
        data = request.form
        person.first_name = data['first_name']
        person.last_name = data['last_name']
        person.personal_email = data['personal_email']
        person.org_email = data.get('org_email')
        person.username = data.get('username')
        person.id_number = data.get('id_number')
        person.tax_id = data.get('tax_id')
        db.session.commit()
        flash('Person updated!')
        return redirect(url_for('persons.list'))
    return render_template('person_form.html', action='Update', person=person, person_id=person_id)

@persons_bp.route('/persons/delete/<int:person_id>', methods=['POST'])
def delete(person_id):
    person = Person.query.get_or_404(person_id)
    db.session.delete(person)
    db.session.commit()
    flash('Person deleted!')
    return redirect(url_for('persons.list'))
