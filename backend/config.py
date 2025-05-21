import os

class Config:
    # DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
    # DEEPSEEK_API_URL = os.getenv('DEEPSEEK_API_URL', 'https://api.deepseek.com')

    # DEEPSEEK_API_KEY = 'sk-205fdc1afaab4936b346136629e4d146'
    # DEEPSEEK_API_URL = 'https://api.deepseek.com/chat/completions'
    # DEEPSEEK_API_URL = 'https://api.deepseek.com/'

    API_KEY = 'sk-1eac2c03ec0e4cbba82ed465aea18962'
    API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    # 数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              "mysql+pymysql://root:123456@localhost:3306/medical_system"
    SQLALCHEMY_TRACK_MODIFICATIONS = False