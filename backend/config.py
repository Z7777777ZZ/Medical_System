import os
from dotenv import load_dotenv

# 加载.env文件中的环境变量
load_dotenv()

class Config:
    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root@localhost/medical_system'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'dev-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1小时
    
    # 应用配置
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DEBUG = True
    
    # Flask-RestX配置
    RESTX_MASK_SWAGGER = False  # 禁用Swagger UI中的掩码功能
    RESTX_MASK_HEADER = None    # 移除X-Fields头信息
      #SQL连接池 - 优化配置，解决"Too many connections"错误
    SQLALCHEMY_POOL_SIZE = 10          # 连接池大小 (降低以适应MySQL默认最大连接数)
    SQLALCHEMY_MAX_OVERFLOW = 5        # 最大溢出数量
    SQLALCHEMY_POOL_TIMEOUT = 30       # 获取连接超时(秒)
    SQLALCHEMY_POOL_RECYCLE = 60       # 连接回收时间(秒) - 在空闲60秒后回收
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,         # 连接前ping测试连接是否可用
        'pool_use_lifo': True          # 使用LIFO策略，提高连接复用率
    }
