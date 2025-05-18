from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pymysql
import json
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import time
import logging
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import uuid
from api_endpoints import api
import concurrent.futures
import threading
import multiprocessing
import psutil
import requests

app = Flask(__name__)
CORS(app)

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'zsj031128',
    'db': 'medical_system',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# 文件上传配置
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# 压力测试配置
STRESS_TEST_DURATION = 60  # 压力测试默认持续时间（秒）
STRESS_TEST_CONCURRENT = 10  # 默认并发用户数
STRESS_TEST_RUNNING = False  # 测试运行状态
STRESS_TEST_RESULTS = {}  # 存储测试结果

# 确保上传目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 数据库连接函数
def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

# 检查文件扩展名
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 记录用户活动
def log_user_activity(patient_id, activity_type, description, metadata=None, request=None):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        ip_address = request.remote_addr if request else None
        user_agent = request.headers.get('User-Agent') if request else None
        
        cursor.execute(
            "INSERT INTO user_activities (patient_id, activity_type, description, metadata, ip_address, user_agent) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (patient_id, activity_type, description, json.dumps(metadata) if metadata else None, 
             ip_address, user_agent)
        )
        conn.commit()
    except Exception as e:
        logger.error(f"Error logging user activity: {e}")
    finally:
        if 'conn' in locals() and conn is not None:
            conn.close()

# 发送邮件通知
def send_email_notification(email, subject, message):
    try:
        # 这里配置你的SMTP服务器信息
        smtp_server = "smtp.example.com"
        smtp_port = 587
        smtp_username = "your_email@example.com"
        smtp_password = "your_password"
        
        msg = MIMEMultipart()
        msg['From'] = smtp_username
        msg['To'] = email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(message, 'html'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

# 发送短信通知（模拟）
def send_sms_notification(phone, message):
    try:
        # 这里应该集成实际的短信发送服务
        # 目前仅记录日志模拟发送
        logger.info(f"SMS sent to {phone}: {message}")
        return True
    except Exception as e:
        logger.error(f"Error sending SMS: {e}")
        return False

# 获取系统资源使用情况
def get_system_resources():
    return {
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'threads': threading.active_count(),
        'time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    }

# 注册API蓝图
app.register_blueprint(api, url_prefix='/api')

# 静态文件服务
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# 数据库连接测试
@app.route('/api/test-db-connection')
def test_db_connection():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        conn.close()
        return jsonify({
            'status': 'success',
            'message': '数据库连接成功',
            'result': result
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'数据库连接失败: {str(e)}'
        }), 500

# 根路由
@app.route('/')
def index():
    return jsonify({
        'status': 'success',
        'message': '医疗系统API服务正在运行'
    })

# 测试接口，用于诊断前端连接问题
@app.route('/api/test')
def test_api():
    return jsonify({
        'status': 'success',
        'message': 'API连接成功',
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': '请求的资源不存在'
    }), 404

@app.errorhandler(500)
def server_error(error):
    logger.error(f"服务器错误: {str(error)}")
    return jsonify({
        'status': 'error',
        'message': '服务器内部错误'
    }), 500

# 启动入口
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)