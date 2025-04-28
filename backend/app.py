from flask import Flask, jsonify, _request_ctx_stack
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restx import Api
from config import Config
from functools import wraps
import os
from dotenv import load_dotenv
import logging

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(level=logging.INFO)

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

# 创建一个自定义的jwt_required装饰器，它总是允许访问
def jwt_always_pass(optional=False):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # 设置一个默认的身份信息
            _request_ctx_stack.top.jwt = {"sub": 1, "role": "doctor"}
            _request_ctx_stack.top.jwt_user = {'id': 1, 'role': 'doctor'}
            return fn(*args, **kwargs)
        return decorator
    return wrapper

import flask_jwt_extended
flask_jwt_extended.jwt_required = jwt_always_pass

authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "输入你的 JWT Token，格式: <code>Bearer &lt;your_token&gt;</code>",
        'default': '11111111'  # 设置默认值
    }
}
api = Api(
    title='Medical System API',
    version='1.0',
    description='Diagnosis and Call API',
    doc='/docs',
    authorizations=authorizations,
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
    from diagnosis.api.prescription import api as prescription_ns
    from call_number.api.queue import api as queue_ns

    # 添加命名空间到API
    api.add_namespace(prescription_ns, path='/api/diagnosis/prescription')
    api.add_namespace(queue_ns, path='/api/call-number/queue')

    # 导入模型以确保它们被创建
    from call_number.models.queue import Queue
    from diagnosis.models.prescription import Prescription, Medicine, PrescriptionDetail
    from users.models.patient import Patient
    from users.models.doctor import Doctor

    # Create database tables
    with app.app_context():
        db.create_all()

    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({'error': 'Server error'}), 500

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)