"""
Flask扩展模块，集中管理所有扩展
"""
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# 数据库ORM
db = SQLAlchemy()

# 跨域支持
cors = CORS()

# JWT认证
jwt = JWTManager()

def init_app(app):
    """初始化所有扩展"""
    db.init_app(app)
    cors.init_app(app)
    jwt.init_app(app) 