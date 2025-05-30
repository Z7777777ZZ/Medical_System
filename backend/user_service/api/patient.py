from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
from user_service.models.patient import Patients, Patient_details
from user_service.utils import ApiResponse
from user_service.utils.password import get_password_hash, verify_password

from flask import Blueprint, jsonify, request
from flask_restx import Namespace, Resource, fields


# 创建Namespace
api = Namespace('patient', description='患者相关操作')

# 定义登录模型
login_model = api.model('PatientLogin', {
    'phone': fields.String(required=True, description='手机号码'),
    'password': fields.String(required=True, description='密码')
})

# 定义注册模型
register_model = api.model('PatientRegister', {
    'name': fields.String(required=True, description='患者姓名'),
    'phone': fields.String(required=True, description='手机号码'),
    'email': fields.String(required=True, description='电子邮箱'),
    'password': fields.String(required=True, description='密码'),
    'birthday': fields.String(description='出生日期'),
    'gender': fields.String(description='性别'),
    'address': fields.String(description='地址'),
    'id_card': fields.String(description='身份证号')
})

# 定义患者资料模型
patient_profile_model = api.model('PatientProfile', {
    'patient_id': fields.Integer(description='患者ID'),
    'phone': fields.String(description='手机号码'),
    'email': fields.String(description='电子邮箱'),
    'name': fields.String(description='患者姓名'),
    'created_at': fields.String(description='创建时间'),
    'details': fields.Nested(api.model('PatientDetails', {
        'gender': fields.String(description='性别'),
        'date_of_birth': fields.String(description='出生日期'),
        'blood_type': fields.String(description='血型'),
        'height': fields.Float(description='身高(cm)'),
        'weight': fields.Float(description='体重(kg)'),
        'emergency_contact': fields.String(description='紧急联系人'),
        'emergency_phone': fields.String(description='紧急联系电话'),
        'medical_insurance_id': fields.String(description='医保ID'),
        'allergies': fields.String(description='过敏史'),
        'chronic_conditions': fields.String(description='慢性病史'),
        'medications': fields.String(description='当前用药')
    }))
})

# 定义患者资料更新模型
patient_update_model = api.model('PatientUpdate', {
    'name': fields.String(description='患者姓名'),
    'phone': fields.String(description='手机号码'),
    'email': fields.String(description='电子邮箱'),
    'details': fields.Nested(api.model('PatientDetailsUpdate', {
        'gender': fields.String(description='性别'),
        'date_of_birth': fields.String(description='出生日期'),
        'blood_type': fields.String(description='血型'),
        'height': fields.Float(description='身高(cm)'),
        'weight': fields.Float(description='体重(kg)'),
        'emergency_contact': fields.String(description='紧急联系人'),
        'emergency_phone': fields.String(description='紧急联系电话'),
        'medical_insurance_id': fields.String(description='医保ID'),
        'allergies': fields.String(description='过敏史'),
        'chronic_conditions': fields.String(description='慢性病史'),
        'medications': fields.String(description='当前用药')
    }))
})

# 定义API响应模型
response_model = api.model('PatientApiResponse', {
    'status': fields.String(description='响应状态', enum=['success', 'error']),
    'message': fields.String(description='响应消息'),
    'data': fields.Raw(description='响应数据')
})

@api.route('/login')
class PatientLogin(Resource):
    @api.doc('patient_login', description='患者登录接口')
    @api.expect(login_model)
    @api.response(200, '登录成功', response_model)
    @api.response(400, '参数错误')
    @api.response(401, '登录失败')
    @api.marshal_with(response_model)
    def post(self):
        """患者登录"""
        data = request.get_json()

        if 'phone' not in data or 'password' not in data:
            return ApiResponse.error("需要手机号和密码", 400)

        patient = Patients.query.filter_by(phone=data['phone']).first()

        if not patient or not verify_password(data['password'], patient.password_hash):
            return ApiResponse.error("手机号或密码错误", 401)

        access_token = create_access_token(identity={
            'id': patient.patient_id,
            'type': 'patient'
        })

        return ApiResponse.success({
            'token': access_token,
            'patient_id': patient.patient_id
        })


@api.route('/register')
class PatientRegister(Resource):
    @api.doc('patient_register', description='患者注册接口')
    @api.expect(register_model)
    @api.response(201, '注册成功', response_model)
    @api.response(400, '参数错误')
    @api.response(409, '手机号或邮箱已注册')
    @api.response(500, '服务器内部错误')
    @api.marshal_with(response_model)
    def post(self):
        """患者注册"""
        data = request.get_json()
        
        # 验证必填字段
        required_fields = ['phone', 'email', 'password', 'name']
        if not all(field in data for field in required_fields):
            return ApiResponse.error("缺少必要字段: phone, email, password, name", 400)

        # 验证手机号和邮箱唯一性
        if Patients.query.filter_by(phone=data['phone']).first():
            return ApiResponse.error("手机号已注册", 409)
        if Patients.query.filter_by(email=data['email']).first():
            return ApiResponse.error("邮箱已注册", 409)

        try:
            # 创建患者主记录
            new_patient = Patients(
                phone=data['phone'],
                email=data['email'],
                name=data['name'],
                password_hash=get_password_hash(data['password'])
            )
            db.session.add(new_patient)
            
            # 创建患者详情记录
            #patient_detail = Patient_details(patient_id=new_patient.patient_id)
            #db.session.add(patient_detail)

            db.session.commit()

            # 生成访问令牌
            access_token = create_access_token(identity={
                'id': new_patient.patient_id,
                'type': 'patient'
            })

            return ApiResponse.success({
                'patient_id': new_patient.patient_id,
                'token': access_token
            }, "注册成功", 201)

        except Exception as e:
            db.session.rollback()
            return ApiResponse.error("注册失败: {}".format(str(e)), 500)

@api.route('/<int:patient_id>/profile')
class PatientProfile(Resource):
    @api.doc('get_patient_profile', description='获取患者个人资料')
    @api.response(200, '获取成功', response_model)
    @api.response(404, '患者不存在')
    @api.marshal_with(response_model)
    def get(self, patient_id):
        """获取患者个人资料"""
        patient = Patients.query.get_or_404(patient_id)
        print(patient.details)
        profile_data = {
            "patient_id": patient.patient_id,
            "phone": patient.phone,
            "email": patient.email,
            "name": patient.name,
            "created_at": patient.created_at.isoformat() if patient.created_at else None
        }
        # 处理患者详情
        if patient.details:
            patient_details = patient.details
            profile_data["details"] = {
                "gender": patient_details.gender,
                "date_of_birth": patient_details.date_of_birth.strftime('%Y-%m-%d') if patient_details.date_of_birth else None,
                "blood_type": patient_details.blood_type,
                "height": float(patient_details.height) if patient_details.height else None,
                "weight": float(patient_details.weight) if patient_details.weight else None,
                "emergency_contact": patient_details.emergency_contact,
                "emergency_phone": patient_details.emergency_phone,
                "medical_insurance_id": patient_details.medical_insurance_id,
                "allergies": patient_details.allergies,
                "chronic_conditions": patient_details.chronic_conditions,
                "medications": patient_details.medications
            }
        print(profile_data)
        return ApiResponse.success(profile_data)
    
    @api.doc('update_patient_profile')
    def put(self, patient_id):
        """更新患者个人资料"""
        data = request.get_json()
        print(f"更新患者个人资料: {data}")

        try:
            patient = Patients.query.get_or_404(patient_id)
            # 更新患者主记录
            for key, value in data.items():
                if key in ['phone', 'email', 'name']:
                    setattr(patient, key, value)
            db.session.commit()
            
            # 获取或创建患者详情
            patient_detail = Patient_details.query.get(patient_id)
            if not patient_detail:
                patient_detail = Patient_details(patient_id=patient_id)
                db.session.add(patient_detail)
            
            # 更新患者详情
            if 'details' in data:
                for key, value in data['details'].items():
                    setattr(patient_detail, key, value)
            
            db.session.commit()
            return ApiResponse.success(message="信息更新成功")
            
        except Exception as e:
            db.session.rollback()
            return ApiResponse.error(f"更新失败: {str(e)}", 500)
