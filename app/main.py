import os
from flask import Flask
from models import db
import config as config
from blueprints.departments import departments_bp
from blueprints.positions import positions_bp
from blueprints.employees import employees_bp
from blueprints.contractors import contractors_bp

app = Flask(__name__)
app.config.from_object(config)
app.secret_key = app.config.get('SECRET_KEY', 'supersecretkey')
db.init_app(app)

# Register blueprints
app.register_blueprint(departments_bp)
app.register_blueprint(positions_bp)
app.register_blueprint(employees_bp)
app.register_blueprint(contractors_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
