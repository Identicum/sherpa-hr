import os
from flask import Flask, render_template
from flasgger import Flasgger
from models import db
from schemas import (
    DepartmentSchema,
    PositionSchema,
    PersonSchema,
    PersonDataSchema,
    EmployeeSchema,
    ContractorSchema,
)
import config as config
from blueprints.departments import departments_bp
from blueprints.positions import positions_bp
from blueprints.persons import persons_bp
from blueprints.persondata import persondata_bp
from blueprints.employees import employees_bp
from blueprints.contractors import contractors_bp
from sherpa.utils.basics import Logger

app = Flask(__name__)
log_level = os.environ.get("LOG_LEVEL", "")
# log outputs to /tmp/python-flask.log, redirected to /dev/stdout in the parent image
app.logger = Logger("sherpa-hr", log_level=log_level, log_path="/tmp/python-flask.log")
app.logger.info("Logger initialized with level: {}.", log_level)
app.config.from_object(config)
app.secret_key = app.config.get('SECRET_KEY', 'supersecretkey')
db.init_app(app)

# helper to turn marshmallow schemas into simple swagger definitions
from marshmallow import fields as _fields

def _schema_def(schema_cls):
    props = {}
    for name, field in schema_cls().fields.items():
        fmt = None
        if isinstance(field, _fields.Int):
            typ = 'integer'
        elif isinstance(field, _fields.Str):
            typ = 'string'
        elif isinstance(field, _fields.Date):
            typ = 'string'
            fmt = 'date'
        else:
            typ = 'string'
        entry = {'type': typ}
        if fmt:
            entry['format'] = fmt
        props[name] = entry
    return {'type': 'object', 'properties': props}

swagger = Flasgger(app, template={
    'definitions': {
        'Department': _schema_def(DepartmentSchema),
        'Position': _schema_def(PositionSchema),
        'Person': _schema_def(PersonSchema),
        'PersonData': _schema_def(PersonDataSchema),
        'Employee': _schema_def(EmployeeSchema),
        'Contractor': _schema_def(ContractorSchema),
    }
})

# Register blueprints
app.register_blueprint(departments_bp)
app.register_blueprint(positions_bp)
app.register_blueprint(persons_bp)
app.register_blueprint(persondata_bp)
app.register_blueprint(employees_bp)
app.register_blueprint(contractors_bp)

@app.route('/')
def index():
    app.logger.debug("Index endpoint called.")
    return render_template('index.html')

@app.route('/health')
def getHealth():
    app.logger.trace("Health endpoint called.")
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
