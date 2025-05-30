from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
from user_service.models.doctor import Doctors
from user_service.models.doctor import Hospitals
from user_service.models.doctor import Departments
from user_service.utils import ApiResponse
from user_service.utils.password import get_password_hash, verify_password

from flask import Blueprint, jsonify, request
from flask_restx import Namespace, Resource, fields


# 创建Namespace
api = Namespace('doctor', description='医生相关操作')

# 定义登录模型
login_model = api.model('DoctorLogin', {
    'phone': fields.String(required=True, description='手机号码'),
    'password': fields.String(required=True, description='密码')
})

# 定义注册模型
register_model = api.model('DoctorRegister', {
    'name': fields.String(required=True, description='医生姓名'),
    'phone': fields.String(required=True, description='手机号码'),
    'password': fields.String(required=True, description='密码'),
    'department_id': fields.String(required=True, description='科室ID'),
    'hospital_id': fields.String(required=True, description='医院ID'),
    'specialty': fields.String(description='专长'),
    'bio': fields.String(description='个人简介')
})

# 定义医生资料模型
doctor_profile_model = api.model('DoctorProfile', {
    'doctor_id': fields.Integer(description='医生ID'),
    'phone': fields.String(description='手机号码'),
    'name': fields.String(description='医生姓名'),
    'hospital': fields.Integer(description='医院ID'),
    'department': fields.Integer(description='科室ID'),
    'specialty': fields.String(description='专长'),
    'bio': fields.String(description='个人简介'),
    'created_at': fields.String(description='创建时间')
})

# 定义医生资料更新模型
doctor_update_model = api.model('DoctorUpdate', {
    'name': fields.String(description='医生姓名'),
    'phone': fields.String(description='手机号码'),
    'specialty': fields.String(description='专长'),
    'bio': fields.String(description='个人简介')
})

# 定义API响应模型
response_model = api.model('ApiResponse', {
    'status': fields.String(description='响应状态', enum=['success', 'error']),
    'message': fields.String(description='响应消息'),
    'data': fields.Raw(description='响应数据')
})



@api.route('/login')
class DoctorLogin(Resource):
    @api.doc('doctor_login', description='医生登录接口')
    @api.expect(login_model)
    @api.response(200, '登录成功', response_model)
    @api.response(400, '参数错误')
    @api.response(401, '登录失败')
    @api.marshal_with(response_model)
    def post(self):
        """医生登录"""
        data = request.get_json()
        print(data)
        
        # 基础验证
        if 'phone' not in data or 'password' not in data:
            return ApiResponse.error("需要手机号和密码", 400)

        doctor = Doctors.query.filter_by(phone=data['phone']).first()

        # 验证用户存在性和密码
        if not doctor or not verify_password(data['password'], doctor.password_hash):
            return ApiResponse.error("手机号或密码错误", 401)
        print(doctor.password_hash)

        # 生成访问令牌
        access_token = create_access_token(identity={
            'id': doctor.doctor_id,
            'type': 'doctor'
        })

        return ApiResponse.success({
            'token': access_token,
            'doctor_id': doctor.doctor_id
        })

@api.route('/register')
class DoctorRegister(Resource):
    @api.doc('doctor_register', description='医生注册')
    @api.expect(register_model)
    @api.response(201, '注册成功', response_model)
    @api.response(400, '参数错误')
    @api.response(409, '手机号已注册')
    @api.response(500, '服务器内部错误')
    @api.marshal_with(response_model)
    def post(self):
        """医生注册"""
        data = request.get_json()
        print(data)
        
        # 验证必填字段
        required_fields = ['phone', 'name', 'hospital_id', 'department_id', 'specialty', 'password']
        if not all(field in data for field in required_fields):
            return ApiResponse.error("缺少必要字段", 400)

        # 验证手机号唯一性
        if Doctors.query.filter_by(phone=data['phone']).first():
            return ApiResponse.error("该手机号已注册", 409)

        # 验证医院和科室有效性
        hospital = Hospitals.query.get(data['hospital_id'])
        department = Departments.query.get(data['department_id'])
        
        if not hospital:
            return ApiResponse.error("无效的医院ID", 400)
        if not department or department.hospital_id != hospital.hospital_id:
            return ApiResponse.error("无效的科室ID", 400)

        try:
            new_doctor = Doctors(
                phone=data['phone'],
                name=data['name'],
                hospital_id=hospital.hospital_id,
                department_id=department.department_id,
                specialty=data['specialty'],
                bio=data.get('bio', '无'),
                password_hash=get_password_hash(data['password'])
            )
            db.session.add(new_doctor)
            db.session.commit()

            # 生成访问令牌
            access_token = create_access_token(identity={
                'id': new_doctor.doctor_id,
                'type': 'doctor'
            })

            return ApiResponse.success({
                'doctor_id': new_doctor.doctor_id,
                'token': access_token
            }, "注册成功", 201)

        except Exception as e:
            db.session.rollback()
            return ApiResponse.error("服务器内部错误", 500)

@api.route('/<int:doctor_id>/profile')
class DoctorProfile(Resource):
    @api.doc('get_doctor_profile', description='获取医生个人资料')
    @api.response(200, '获取成功', response_model)
    @api.response(404, '医生不存在')
    @api.marshal_with(response_model)
    def get(self, doctor_id):
        """获取医生个人资料"""
        doctor = Doctors.query.get_or_404(doctor_id)
        
        profile_data = {
            "doctor_id": doctor.doctor_id,
            "phone": doctor.phone,
            "name": doctor.name,
            "hospital": doctor.hospital_id,
            "department": doctor.department_id,
            "specialty": doctor.specialty,
            "bio": doctor.bio,
            "created_at": doctor.created_at.isoformat() if doctor.created_at else None
        }
        
        return ApiResponse.success(profile_data)

    @api.doc('update_doctor_profile', description='更新医生个人资料')
    @api.expect(doctor_update_model)
    @api.response(200, '更新成功', response_model)
    @api.response(404, '医生不存在')
    @api.response(500, '更新失败')
    @api.marshal_with(response_model)
    def put(self, doctor_id):
        """更新医生个人资料"""
        data = request.get_json()
        print(f"更新医生个人资料: {data}")

        try:
            doctor = Doctors.query.get_or_404(doctor_id)
            # 更新医生记录
            for key, value in data.items():
                setattr(doctor, key, value)

            db.session.commit()
            return ApiResponse.success(message="信息更新成功")
            
        except Exception as e:
            db.session.rollback()
            return ApiResponse.error(f"更新失败: {str(e)}", 500)