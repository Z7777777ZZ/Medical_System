import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'dev-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root@localhost/medical_system'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'max_overflow': 10,
        'pool_recycle': 3600
    }

    RESTX_MASK_SWAGGER = False  # 禁用Swagger UI中的掩码功能
    RESTX_MASK_HEADER = None    # 移除X-Fields头信息
      #SQL连接池 - 优化配置，解决"Too many connections"错误
    SQLALCHEMY_POOL_SIZE = 10          # 连接池大小 (降低以适应MySQL默认最大连接数)
    SQLALCHEMY_MAX_OVERFLOW = 5        # 最大溢出数量
    SQLALCHEMY_POOL_TIMEOUT = 30       # 获取连接超时(秒)
    SQLALCHEMY_POOL_RECYCLE = 60       # 连接回收时间(秒) - 在空闲60秒后回收
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,         # 连接前ping测试连接是否可用
        'pool_use_lifo': True,          # 使用LIFO策略，提高连接复用率
        'pool_size': 5,
        'max_overflow': 10,
        'pool_recycle': 3600
    }

    # CORS_ORIGINS = ["http://localhost:5173"]  # 允许的前端地址
    CORS_SUPPORTS_CREDENTIALS = True          # 允许携带Cookie