from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restx import Api
from config import Config

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
api = Api(
    title='Medical System API(Diagnosis and Call)',
    version='1.0',
    description='A medical system API with Swagger documentation',
    doc='/docs'
)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    jwt.init_app(app)
    api.init_app(app)

    # Register blueprints and namespaces
    from call_number.api import bp as call_number_bp
    app.register_blueprint(call_number_bp, url_prefix='/api/call-number')

    from diagnosis.api import bp as diagnosis_bp
    app.register_blueprint(diagnosis_bp, url_prefix='/api/diagnosis')

    # Import and register namespaces
    from diagnosis.api.diagnosis import api as diagnosis_ns
    from diagnosis.api.prescription import api as prescription_ns
    from call_number.api.queue import api as queue_ns

    api.add_namespace(diagnosis_ns, path='/api/diagnosis')
    api.add_namespace(prescription_ns, path='/api/diagnosis/prescription')
    api.add_namespace(queue_ns, path='/api/call-number/queue')

    # Create database tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)