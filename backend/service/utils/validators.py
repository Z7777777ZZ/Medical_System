"""
数据验证工具
"""
from datetime import datetime
from decimal import Decimal
import re


class ValidationError(Exception):
    """验证错误异常"""
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Validator:
    """验证器基类"""
    @staticmethod
    def validate_required(data, fields, name=""):
        """验证必填字段"""
        for field in fields:
            if field not in data or data[field] is None:
                raise ValidationError(f"{name}{field} 字段是必填的")
                
    @staticmethod
    def validate_date_format(date_str, format="%Y-%m-%d"):
        """验证日期格式"""
        try:
            datetime.strptime(date_str, format)
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_datetime_format(datetime_str, format="%Y-%m-%d %H:%M:%S"):
        """验证日期时间格式"""
        try:
            datetime.strptime(datetime_str, format)
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_decimal(value):
        """验证decimal值"""
        try:
            decimal_value = Decimal(str(value))
            return decimal_value >= 0
        except:
            return False


class AppointmentValidator(Validator):
    """预约挂号验证器"""
    @classmethod
    def validate_create(cls, data):
        """验证创建预约数据"""
        cls.validate_required(data, ['doctor_id', 'appointment_time'], "预约")
        
        # 验证预约时间格式
        if 'appointment_time' in data:
            if not cls.validate_datetime_format(data['appointment_time']):
                raise ValidationError("预约时间格式不正确，请使用 YYYY-MM-DD HH:MM:SS 格式")
        
        # 验证预约时间是否在未来
        if 'appointment_time' in data:
            appointment_time = datetime.strptime(data['appointment_time'], "%Y-%m-%d %H:%M:%S")
            if appointment_time < datetime.now():
                raise ValidationError("预约时间必须在未来")
                
        return True
        
    @classmethod
    def validate_reschedule(cls, data):
        """验证改期预约数据"""
        cls.validate_required(data, ['appointment_time'], "改期")
        
        # 验证预约时间格式
        if 'appointment_time' in data:
            try:
                appointment_time = datetime.strptime(data['appointment_time'], "%Y-%m-%dT%H:%M:%S")
            except ValueError:
                raise ValidationError("预约时间格式不正确，请使用 YYYY-MM-DDThh:mm:ss 格式")
        
        # 验证预约时间是否在未来
        if appointment_time < datetime.now():
            raise ValidationError("预约时间必须在未来")
                
        return True


class PaymentValidator(Validator):
    """支付验证器"""
    @classmethod
    def validate_create(cls, data):
        """验证创建支付数据"""
        cls.validate_required(data, ['appointment_id', 'fee_type'], "支付")
        
        # 验证费用类型
        if 'fee_type' in data and data['fee_type'] not in ['registration_fee', 'consultation_fee', 'medicine_fee', 'examination_fee']:
            raise ValidationError("费用类型不正确")
            
        return True
        
    @classmethod
    def validate_complete(cls, data):
        """验证完成支付数据"""
        cls.validate_required(data, ['transaction_id'], "支付完成")
        
        return True


def validate_pagination_params(page, per_page, max_per_page=100):
    """验证分页参数
    
    Args:
        page (int): 页码
        per_page (int): 每页数量
        max_per_page (int): 最大每页数量
        
    Returns:
        tuple: (page, per_page)
    """
    try:
        page = int(page) if page is not None else 1
        per_page = int(per_page) if per_page is not None else 10
    except ValueError:
        page = 1
        per_page = 10
    
    if page < 1:
        page = 1
    if per_page < 1:
        per_page = 10
    if per_page > max_per_page:
        per_page = max_per_page
    
    return page, per_page


def validate_id(id_value):
    """验证ID是否为正整数
    
    Args:
        id_value: ID值
        
    Returns:
        bool: 是否合法
    """
    try:
        id_int = int(id_value)
        return id_int > 0
    except (ValueError, TypeError):
        return False 