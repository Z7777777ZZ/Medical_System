from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from users.models.patient import Patient
from users.models.patient_detail import PatientDetail

# 创建命名空间
api = Namespace('health', description='患者健康数据操作')

# 定义Swagger文档模型
health_data_model = api.model('HealthData', {
    'patientId': fields.Integer(description='患者ID'),
    'gender': fields.String(description='性别'),
    'dateOfBirth': fields.String(description='出生日期'),
    'bloodType': fields.String(description='血型'),
    'height': fields.Float(description='身高(cm)'),
    'weight': fields.Float(description='体重(kg)'),
    'bmi': fields.Float(description='BMI指数'),
    'allergies': fields.String(description='过敏史'),
    'chronicConditions': fields.String(description='慢性病'),
    'medications': fields.String(description='正在服用的药物')
})

location_model = api.model('Location', {
    'name': fields.String(required=True, description='位置名称'),
    'location': fields.String(description='详细位置'),
    'mapX': fields.Integer(description='地图X坐标'),
    'mapY': fields.Integer(description='地图Y坐标'),
    'locationDirections': fields.String(description='位置指引')
})

@api.route('/data')
class HealthData(Resource):
    @jwt_required()
    @api.doc('get_health_data')
    @api.marshal_with(health_data_model)
    @api.response(404, '未找到患者健康数据')
    def get(self):
        """获取患者健康数据"""
        # 获取当前用户ID
        patient_id = get_jwt_identity()
        
        # 查询患者基本信息
        patient = Patient.query.get(patient_id)
        if not patient:
            return {'error': '未找到患者'}, 404
        
        # 查询患者详细健康信息
        health_data = PatientDetail.query.get(patient_id)
        if not health_data:
            return {'error': '未找到健康数据'}, 404
        
        # 计算BMI
        bmi = None
        if health_data.height and health_data.weight:
            height_m = float(health_data.height) / 100  # 转换为米
            bmi = float(health_data.weight) / (height_m * height_m)
            bmi = round(bmi, 2)  # 保留两位小数
        
        # 返回健康数据
        return {
            'patientId': patient_id,
            'gender': health_data.gender,
            'dateOfBirth': health_data.date_of_birth.isoformat() if health_data.date_of_birth else None,
            'bloodType': health_data.blood_type,
            'height': float(health_data.height) if health_data.height else None,
            'weight': float(health_data.weight) if health_data.weight else None,
            'bmi': bmi,
            'allergies': health_data.allergies,
            'chronicConditions': health_data.chronic_conditions,
            'medications': health_data.medications
        }

@api.route('/refresh')
class RefreshHealthData(Resource):
    @jwt_required()
    @api.doc('refresh_health_data')
    @api.marshal_with(health_data_model)
    @api.response(404, '未找到患者健康数据')
    def get(self):
        """刷新患者健康数据"""
        # 这个API的逻辑和get_health_data相同，只是提供了一个单独的端点用于刷新按钮
        return HealthData().get()

@api.route('/update')
class UpdateHealthData(Resource):
    @jwt_required()
    @api.doc('update_health_data')
    @api.expect(health_data_model)
    @api.marshal_with(health_data_model)
    @api.response(404, '未找到患者')
    @api.response(400, '无效输入')
    def put(self):
        """更新患者健康数据"""
        # 获取当前用户ID
        patient_id = get_jwt_identity()
        
        # 查询患者是否存在
        patient = Patient.query.get(patient_id)
        if not patient:
            return {'error': '未找到患者'}, 404
        
        data = request.get_json()
        
        # 查询患者详细健康信息
        health_data = PatientDetail.query.get(patient_id)
        
        # 如果不存在则创建新记录
        if not health_data:
            health_data = PatientDetail(patient_id=patient_id)
            db.session.add(health_data)
        
        # 更新健康数据
        if 'gender' in data:
            health_data.gender = data['gender']
        if 'dateOfBirth' in data and data['dateOfBirth']:
            from datetime import datetime
            health_data.date_of_birth = datetime.fromisoformat(data['dateOfBirth']).date()
        if 'bloodType' in data:
            health_data.blood_type = data['bloodType']
        if 'height' in data:
            health_data.height = data['height']
        if 'weight' in data:
            health_data.weight = data['weight']
        if 'allergies' in data:
            health_data.allergies = data['allergies']
        if 'chronicConditions' in data:
            health_data.chronic_conditions = data['chronicConditions']
        if 'medications' in data:
            health_data.medications = data['medications']
        
        db.session.commit()
        
        # 返回更新后的数据
        return HealthData().get()

@api.route('/location/<string:type>')
class Location(Resource):
    @jwt_required()
    @api.doc('get_location')
    @api.marshal_with(location_model)
    @api.response(404, '未找到位置信息')
    def get(self, type):
        """获取医院特定位置信息
        
        可用的位置类型:
        * registration - 挂号处
        * pharmacy - 药房
        * laboratory - 化验室
        * radiology - 放射科
        * emergency - 急诊
        * cashier - 收银处
        """
        # 模拟不同位置的信息，实际应用中应从数据库获取
        locations = {
            "registration": {
                "name": "挂号处",
                "location": "门诊楼一楼大厅",
                "mapX": 120,
                "mapY": 85,
                "locationDirections": "从正门进入后直走200米"
            },
            "pharmacy": {
                "name": "药房",
                "location": "门诊楼一楼东侧",
                "mapX": 180,
                "mapY": 85,
                "locationDirections": "从挂号处向东走50米"
            },
            "laboratory": {
                "name": "化验室",
                "location": "门诊楼二楼",
                "mapX": 120,
                "mapY": 150,
                "locationDirections": "乘坐1号电梯到二楼后向北走30米"
            },
            "radiology": {
                "name": "放射科",
                "location": "门诊楼地下一层",
                "mapX": 120,
                "mapY": 20,
                "locationDirections": "乘坐2号电梯到地下一层"
            },
            "emergency": {
                "name": "急诊",
                "location": "急诊楼一楼",
                "mapX": 250,
                "mapY": 85,
                "locationDirections": "从停车场侧门直接进入"
            },
            "cashier": {
                "name": "收银处",
                "location": "门诊楼一楼大厅",
                "mapX": 140,
                "mapY": 85,
                "locationDirections": "位于挂号处旁边"
            }
        }
        
        if type in locations:
            return locations[type]
        else:
            return {'error': '未找到该位置信息'}, 404