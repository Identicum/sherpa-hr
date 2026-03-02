import os
from flask import Flask, render_template
from flasgger import Flasgger
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
swagger = Flasgger(app)

# Register blueprints
app.register_blueprint(departments_bp)
app.register_blueprint(positions_bp)
app.register_blueprint(employees_bp)
app.register_blueprint(contractors_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def getHealth():
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
