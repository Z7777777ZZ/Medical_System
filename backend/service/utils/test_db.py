"""
测试数据库连接
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask
from backend.service.utils.config import get_config
from backend.service.utils.extensions import db
from backend.service.models.record import Hospital

# 创建Flask应用
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(get_config())

# 确保instance目录存在
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

# 初始化数据库
db.init_app(app)

# 测试数据库连接和表创建
with app.app_context():
    # 打印SQLite数据库文件路径
    print(f"数据库URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    
    # 创建所有表
    db.create_all()
    print("已创建所有表")
    
    # 添加测试数据
    test_hospital = Hospital(hospital_id=1, name='测试医院', address='测试地址')
    db.session.add(test_hospital)
    db.session.commit()
    print("已添加测试数据")
    
    # 验证数据
    hospital = Hospital.query.first()
    if hospital:
        print(f"查询到医院: {hospital.name}, 地址: {hospital.address}")
    else:
        print("未查询到数据") 