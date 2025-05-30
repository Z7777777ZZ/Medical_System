from datetime import timedelta
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    verify_jwt_in_request
)
from flask import current_app
from functools import wraps

class TokenService:
    @staticmethod
    def create_token(user_id: int, user_type: str) -> dict:
        """
        创建访问令牌和刷新令牌
        :param user_id: 用户ID
        :param user_type: 用户类型（patient/doctor）
        :return: 包含令牌的字典
        """
        identity = {
            'id': user_id,
            'type': user_type
        }
        return {
            'access_token': create_access_token(
                identity=identity,
                expires_delta=timedelta(minutes=current_app.config['JWT_ACCESS_TOKEN_EXPIRES'])
            ),
            'refresh_token': create_refresh_token(
                identity=identity,
                expires_delta=timedelta(days=7)
            )
        }

    @staticmethod
    def get_current_user():
        """
        获取当前认证用户信息
        :return: (user_id, user_type)
        """
        try:
            verify_jwt_in_request()
            identity = get_jwt_identity()
            return identity['id'], identity['type']
        except:
            return None, None

    @staticmethod
    def doctor_required(fn):
        """医生角色校验装饰器"""
        @wraps(fn)
        def wrapper(*args, **kwargs):
            _, user_type = TokenService.get_current_user()
            if user_type != 'doctor':
                return {'message': 'Doctor access required'}, 403
            return fn(*args, **kwargs)
        return wrapper

    @staticmethod
    def patient_required(fn):
        """患者角色校验装饰器"""
        @wraps(fn)
        def wrapper(*args, **kwargs):
            _, user_type = TokenService.get_current_user()
            if user_type != 'patient':
                return {'message': 'Patient access required'}, 403
            return fn(*args, **kwargs)
        return wrapper