from flask import Flask, jsonify
from flask_migrate import Migrate
from backend.config import Config
from backend.extensions import db, jwt, cors, migrate
from backend.user_service.api.doctor import bp as doctor_bp
from backend.user_service.api.patient import bp as patient_bp
from backend.user_service.api.hospital import bp as hospital_bp
from backend.user_service.api.department import bp as department_bp
from backend.user_service.utils import ApiResponse

def create_app(config_class=Config):
    """Flask应用工厂函数"""
    
    # 初始化应用
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 配置扩展
    configure_extensions(app)
    
    # 注册蓝图
    register_blueprints(app)

    return app

def configure_extensions(app):
    """初始化第三方扩展"""
    # 数据库
    db.init_app(app)
    
    # JWT
    jwt.init_app(app)

    # CORS
    cors.init_app(app, supports_credentials=True)
    
    # 数据库迁移
    migrate.init_app(app, db)

def register_blueprints(app):
    """注册应用路由"""
    app.register_blueprint(doctor_bp)
    app.register_blueprint(patient_bp)
    app.register_blueprint(hospital_bp)
    app.register_blueprint(department_bp)


if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)