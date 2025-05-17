"""
配置文件，包含各种系统配置参数
"""
import os

class Config:
    """基础配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-for-medical-system'
    
    # MySQL数据库配置
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_PORT = os.environ.get('MYSQL_PORT') or 3306
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'password'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'medical_system'
    
    # SQLAlchemy配置
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    
    # JWT配置
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-for-medical-system'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 令牌有效期1小时
    
    # 分页配置
    DEFAULT_PAGE_SIZE = 10
    MAX_PAGE_SIZE = 100
    
class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    # 使用SQLite数据库进行开发
    SQLALCHEMY_DATABASE_URI = 'sqlite:///medical_system_dev.db'
    SQLALCHEMY_ECHO = True
    
class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    
class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    JWT_ACCESS_TOKEN_EXPIRES = 1800  # 生产环境令牌有效期30分钟
    
    # 生产环境数据库配置
    # 如需使用MySQL，取消下面注释并配置环境变量
    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DB}"
    
# 根据环境变量选择配置
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    """获取当前环境的配置"""
    config_name = os.environ.get('FLASK_CONFIG') or 'default'
    return config[config_name] 