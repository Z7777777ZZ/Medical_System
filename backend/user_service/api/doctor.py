from flask import Blueprint, request
from flask_jwt_extended import create_access_token
from backend.extensions import db
from backend.user_service.models.doctor import Doctors
from backend.user_service.models.doctor import Hospitals
from backend.user_service.models.doctor import Departments
from backend.user_service.utils import ApiResponse
from backend.user_service.utils.password import get_password_hash, verify_password

bp = Blueprint('doctor_api', __name__, url_prefix='/doctor')

# 医生注册
@bp.route('/register', methods=['POST'])
def register_doctor():
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

# 医生登录
@bp.route('/login', methods=['POST'])
def login_doctor():
    data = request.get_json()
    print(data)
    
    # 基础验证
    if 'phone' not in data or 'password' not in data:
        return ApiResponse.error("需要手机号和密码", 400)

    doctor = Doctors.query.filter_by(phone=data['phone']).first()

    print(doctor.password_hash)
    # 验证用户存在性和密码
    if not doctor or not verify_password(data['password'], doctor.password_hash):
        return ApiResponse.error("手机号或密码错误", 401)

    # 生成访问令牌
    access_token = create_access_token(identity={
        'id': doctor.doctor_id,
        'type': 'doctor'
    })

    return ApiResponse.success({
        'token': access_token,
        'doctor_id': doctor.doctor_id
    })

# 获取医生个人信息
@bp.route('/<int:doctor_id>/profile', methods=['GET'])
def get_doctor_profile(doctor_id):
    doctor = Doctors.query.get_or_404(doctor_id)
    
    profile_data = {
        "doctor_id": doctor.doctor_id,
        "phone": doctor.phone,
        "name": doctor.name,
        "hospital": doctor.hospital_id,
        "department": doctor.department_id,
        "specialty": doctor.specialty,
        "bio": doctor.bio,
        "created_at": doctor.created_at.isoformat()
    }
    
    return ApiResponse.success(profile_data)

@bp.route('/<int:doctor_id>/profile', methods=['PUT'])
def update_doctor_profile(doctor_id):
    data = request.get_json()

    print(data)

    try:
        doctor = Doctors.query.get_or_404(doctor_id)
        # 更新医生记录
        for key, value in data.items():
            setattr(doctor, key, value)

        db.session.commit()
        return ApiResponse.success(message="信息更新成功")
        
    except Exception as e:
        db.session.rollback()
        return ApiResponse.error("更新失败: {}".format(str(e)), 500)