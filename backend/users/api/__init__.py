from flask import Blueprint

bp = Blueprint('users', __name__)

# 导入路由定义
from users.api import patient, health