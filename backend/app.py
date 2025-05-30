
from extensions import db, jwt, cors, migrate
from user_service.utils import ApiResponse

from flask import Flask, jsonify, _request_ctx_stack, request
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

# 【重要】以下 jwt_always_pass 装饰器和对 flask_jwt_extended.jwt_required 的覆盖
# 会导致所有JWT保护的路由绕过实际的Token认证。
# 这在开发阶段可能用于简化测试，但在生产环境中必须移除或注释掉，
# 以确保JWT认证机制正常工作。
#
# # 创建一个自定义的jwt_required装饰器，它总是允许访问
# def jwt_always_pass(optional=False):
#     def wrapper(fn):
#         @wraps(fn)
#         def decorator(*args, **kwargs):
#             # 设置一个默认的身份信息
#             _request_ctx_stack.top.jwt = {"sub": 1, "role": "doctor"}
#             _request_ctx_stack.top.jwt_user = {'id': 1, 'role': 'doctor'}
#             return fn(*args, **kwargs)
#         return decorator
#     return wrapper
#
# import flask_jwt_extended
# flask_jwt_extended.jwt_required = jwt_always_pass

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

    # 确保 JWT_SECRET_KEY 已在配置中设置 (例如, 在 config.py 或环境变量中)
    # 这是 JWT 安全性的核心，例如:
    # app.config['JWT_SECRET_KEY'] = 'your-very-strong-secret-key'
    # 或者最好从环境变量加载:
    # app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    # 设置 CORS，允许跨域请求
    CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], 
                         "allow_headers": ["Content-Type", "Authorization", "Accept"]}})
    jwt.init_app(app)
    api.init_app(app)    
    
    # Register blueprints and namespaces
    from call_number.api import bp as call_number_bp
    app.register_blueprint(call_number_bp, url_prefix='/api/call-number')

    from diagnosis.api import bp as diagnosis_bp
    app.register_blueprint(diagnosis_bp, url_prefix='/api/diagnosis')

    from users.api import bp as users_bp
    app.register_blueprint(users_bp, url_prefix='/api/users')

    from user_service.api import bp as user_service_bp
    app.register_blueprint(user_service_bp, url_prefix='/api/user-service')

    # Import and register namespaces
    from diagnosis.api.prescription import api as prescription_ns
    from call_number.api.queue import api as queue_ns
    from users.api.patient import api as patient_ns
    from users.api.health import api as health_ns
    from user_service.api.doctor import api as doctor_ns
    from user_service.api.hospital import api as hospital_ns
    from user_service.api.department import api as department_ns
    from user_service.api.patient import api as user_service_patient_ns

    # 添加命名空间到API
    api.add_namespace(prescription_ns, path='/api/diagnosis/prescription')
    api.add_namespace(queue_ns, path='/api/call-number/queue')
    api.add_namespace(patient_ns, path='/api/users/patients')
    api.add_namespace(health_ns, path='/api/users/health')
    api.add_namespace(doctor_ns, path='/api/user-service/doctor')
    api.add_namespace(hospital_ns, path='/api/user-service/hospital')
    api.add_namespace(department_ns, path='/api/user-service/department')
    api.add_namespace(user_service_patient_ns, path='/api/user-service/patient')
    
    # 导入模型以确保它们被创建
    from call_number.models.queue import Queue
    from diagnosis.models.prescription import Prescription, Medicine, PrescriptionDetail
    from users.models.patient import Patient
    from users.models.doctor import Doctor
    from users.models.patient_detail import PatientDetail    # Create database tables
    # with app.app_context():
        # db.create_all() # 在开发初期或测试时方便创建表结构。
                        # 对于生产环境和后续的数据库结构变更，
                        # 强烈建议使用 Flask-Migrate 进行数据库迁移管理。
        # pass # 通常在应用启动时不直接调用 create_all()，除非是首次设置或特定场景

    # 数据库连接健康检查中间件
    @app.before_request
    def ensure_db_connection():
        """确保数据库连接在每次请求前是正常的"""
        try:
            # 尝试进行一个简单的查询以验证连接状态
            db.session.execute("SELECT 1")
        except Exception as e:
            logging.error(f"数据库连接检查失败: {e}")
            # 如果当前有活跃的事务，回滚它
            if db.session.is_active:
                db.session.rollback()
            # 主动释放连接回到连接池
            db.session.close()
            return jsonify({'error': '数据库连接暂时不可用，请稍后重试'}), 503

    # 请求后清理资源
    @app.teardown_request
    def shutdown_session(exception=None):
        """确保在请求结束后释放数据库连接"""
        db.session.close()
        
    # 高级错误处理
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found', 'path': request.path}), 404

    @app.errorhandler(500)
    def server_error(error):
        logging.error(f"500错误: {str(error)}")
        return jsonify({'error': 'Server error', 'message': str(error)}), 500
        
    @app.errorhandler(503)
    def service_unavailable(error):
        return jsonify({'error': '服务暂时不可用，请稍后重试'}), 503

    return app



if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)