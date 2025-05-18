import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_COOKIE_SECURE = True
    JWT_COOKIE_CSRF_PROTECT = True

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:yuer0822@localhost:3306/medical_system'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'max_overflow': 10,
        'pool_recycle': 3600
    }

    CORS_ORIGINS = ["http://localhost:5173"]  # 允许的前端地址
    CORS_SUPPORTS_CREDENTIALS = True          # 允许携带Cookie