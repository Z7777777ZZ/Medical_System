from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from backend.extensions import db
from backend.user_service.models.patient import Patients, Patient_details
from backend.user_service.utils import ApiResponse
from backend.user_service.utils.password import get_password_hash, verify_password

bp = Blueprint('patient_api', __name__, url_prefix='/patient')

# 患者注册
@bp.route('/register', methods=['POST'])
def register_patient():
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

# 患者登录
@bp.route('/login', methods=['POST'])
def login_patient():
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

# 获取患者个人信息（需要登录）
@bp.route('/<int:patient_id>/profile', methods=['GET'])
def get_patient_profile(patient_id):
    patient = Patients.query.get_or_404(patient_id)
    print(patient.details)
    profile_data = {
        "patient_id": patient.patient_id,
        "phone": patient.phone,
        "email": patient.email,
        "name": patient.name,
        "created_at": patient.created_at.isoformat()
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
            "allergies":patient_details.allergies,
            "chronic_conditions": patient_details.chronic_conditions,
            "medications": patient_details.medications
        }
    print(profile_data)
    return ApiResponse.success(profile_data)

# 更新患者详细信息
@bp.route('/<int:patient_id>/profile', methods=['PUT'])
def update_patient_profile(patient_id):
    data = request.get_json()

    print(data)
    # 过滤无效字段

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
        return ApiResponse.error("更新失败: {}".format(str(e)), 500)