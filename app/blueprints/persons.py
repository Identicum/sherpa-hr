from flask import abort, Blueprint, current_app, flash, jsonify, render_template, request, redirect, url_for
from models import db, Person, Employee, Contractor
from sqlalchemy import text
from schemas import PersonSchema

persons_bp = Blueprint('persons', __name__)

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
        current_app.logger.debug("Updating org_email for person id: {}", person_id)
        person.org_email = data['org_email']
    if 'username' in data:
        current_app.logger.debug("Updating username for person id: {}", person_id)
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
    employee_count = Employee.query.filter_by(person=person_id).count()
    if employee_count > 0:
        flash('Cannot delete person: it has related employees.')
        return redirect(url_for('persons.list'))
    contractor_count = Contractor.query.filter_by(person=person_id).count()
    if contractor_count > 0:
        flash('Cannot delete person: it has related contractors.')
        return redirect(url_for('persons.list'))
    db.session.delete(person)
    db.session.commit()
    flash('Person deleted!')
    return redirect(url_for('persons.list'))
