from flask import Flask, Blueprint, request, jsonify
from flask_cors import CORS
import click
from datetime import datetime

from backend.service.utils.config import get_config
from backend.service.utils.extensions import init_app as init_extensions, db
from backend.service.models.record import MedicalRecord, Doctor, Department, Hospital
from backend.service.models.patient import Patient, PatientDetail
from backend.service.models.prescription import Prescription, PrescriptionDetail, Medicine
from backend.service.models.registration import Appointment
from backend.service.models.payment import Payment, PaymentDetail
from backend.service.utils.validators import validate_pagination_params
from backend.service.utils.init_db import init_db


def create_app(config_name=None):
    """创建Flask应用"""
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(get_config())
    
    # 允许跨域
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    
    # 初始化扩展
    init_extensions(app)
    
    # 注册API蓝图，所有路由都在/api前缀下
    api_bp = Blueprint('api', __name__, url_prefix='/api')
    patient_bp = Blueprint('patient', __name__, url_prefix='/patient')
    api_bp.register_blueprint(patient_bp)
    
    # ============ 集中式API路由定义 ============
    
    # 测试API连接 - 添加一个根级别的测试路由
    @app.route('/patient/test', methods=['GET', 'OPTIONS'])
    def test_connection_root():
        """根级别的测试API连接"""
        return jsonify({
            'status': 'success',
            'message': '后端API连接成功 (根路径)',
            'timestamp': datetime.now().isoformat()
        })
    
    # 测试API连接
    @patient_bp.route('/test', methods=['GET', 'OPTIONS'])
    def test_connection():
        """测试API连接"""
        return jsonify({
            'status': 'success',
            'message': '后端API连接成功',
            'timestamp': datetime.now().isoformat()
        })
    
    # 获取所有患者列表接口
    @api_bp.route('/patients', methods=['GET'])
    def get_all_patients():
        """获取所有患者列表"""
        try:
            patients = Patient.query.all()
            return jsonify({
                'status': 'success',
                'message': '获取患者列表成功',
                'data': [patient.to_dict() for patient in patients]
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'获取患者列表失败: {str(e)}',
                'data': None
            }), 500
    
    # 获取单个患者信息接口
    @patient_bp.route('/<int:patient_id>', methods=['GET'])
    def get_patient_by_id(patient_id):
        """获取单个患者信息
        
        Args:
            patient_id (int): 患者ID
            
        Returns:
            JSON: 患者信息
        """
        try:
            patient = Patient.query.get(patient_id)
            if not patient:
                return jsonify({
                    'status': 'error',
                    'message': '未找到患者信息',
                    'data': None
                }), 404
                
            # 获取患者详细信息
            patient_data = patient.to_dict()
            
            # 如果有详细信息，加入返回数据中
            patient_detail = PatientDetail.query.filter_by(patient_id=patient_id).first()
            if patient_detail:
                patient_data.update({
                    'gender': patient_detail.gender,
                    'date_of_birth': patient_detail.date_of_birth.strftime('%Y-%m-%d') if patient_detail.date_of_birth else None,
                    'blood_type': patient_detail.blood_type,
                    'height': float(patient_detail.height) if patient_detail.height else None,
                    'weight': float(patient_detail.weight) if patient_detail.weight else None,
                    'emergency_contact': patient_detail.emergency_contact,
                    'emergency_phone': patient_detail.emergency_phone,
                    'medical_insurance_id': patient_detail.medical_insurance_id,
                    'allergies': patient_detail.allergies,
                    'chronic_conditions': patient_detail.chronic_conditions,
                    'medications': patient_detail.medications
                })
                
            return jsonify({
                'status': 'success',
                'message': '获取患者信息成功',
                'data': patient_data
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'获取患者信息失败: {str(e)}',
                'data': None
            }), 500
    
    # 获取所有医生列表接口
    @api_bp.route('/doctors', methods=['GET'])
    def get_all_doctors():
        """获取所有医生列表"""
        try:
            doctors = Doctor.query.all()
            return jsonify({
                'status': 'success',
                'message': '获取医生列表成功',
                'data': [doctor.to_dict() for doctor in doctors]
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'获取医生列表失败: {str(e)}',
                'data': None
            }), 500
    
    # 病例查询API
    @patient_bp.route('/records/latest', methods=['GET'])
    def get_latest_record():
        """获取患者所有病例"""
        patient_id = request.args.get('patient_id', 1, type=int)
        
        # 查询患者的所有病例记录
        records = MedicalRecord.query.filter_by(patient_id=patient_id) \
            .order_by(MedicalRecord.created_at.desc()).all()
        
        if not records:
            return jsonify({
                'status': 'success',
                'message': '未找到病例记录',
                'data': []
            }), 200
        
        # 格式化所有病例记录
        record_list = []
        for record in records:
            # 获取病例相关信息
            record_dict = record.to_dict()
            
            # 获取处方详情
            if record.prescription:
                prescription_dict = record.prescription.to_dict()
                medicines = []
                for detail in record.prescription.details:
                    medicine_info = {
                        'name': detail.medicine.name if detail.medicine else None,
                        'instructions': detail.instructions
                    }
                    medicines.append(medicine_info)
                prescription_dict['medicines'] = medicines
                record_dict['prescription'] = prescription_dict
            
            # 获取科室信息
            doctor = record.doctor
            if doctor and doctor.department:
                record_dict['department_name'] = doctor.department.name
                
            record_list.append(record_dict)
        
        return jsonify({
            'status': 'success',
            'message': '获取成功',
            'data': record_list
        })
    
    @patient_bp.route('/records/history', methods=['GET'])
    def get_record_history():
        """获取患者病例历史"""
        patient_id = request.args.get('patient_id', 1, type=int)
        
        # 分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        page, per_page = validate_pagination_params(page, per_page)
        
        # 查询病例历史
        pagination = MedicalRecord.query.filter_by(patient_id=patient_id) \
            .order_by(MedicalRecord.visit_date.desc()) \
            .paginate(page=page, per_page=per_page, error_out=False)
        
        records = pagination.items
        
        # 格式化返回数据
        record_list = []
        for record in records:
            record_data = {
                'record_id': record.record_id,
                'visit_date': record.visit_date.strftime('%Y-%m-%d') if record.visit_date else None,
                'doctor_name': record.doctor.name if record.doctor else None,
                'department_name': record.doctor.department.name if record.doctor and record.doctor.department else None,
                'diagnosis': record.diagnosis
            }
            record_list.append(record_data)
        
        return jsonify({
            'status': 'success',
            'message': '获取成功',
            'data': {
                'total': pagination.total,
                'page': page,
                'per_page': per_page,
                'records': record_list
            }
        })
    
    @patient_bp.route('/records/<int:record_id>', methods=['GET'])
    def get_record_detail(record_id):
        """获取病例详情"""
        patient_id = request.args.get('patient_id', 1, type=int)
        
        # 查询指定病例
        record = MedicalRecord.query.filter_by(record_id=record_id, patient_id=patient_id).first()
        
        if not record:
            return jsonify({
                'status': 'error',
                'message': '未找到病例记录或无权访问',
                'data': None
            }), 404
        
        # 获取病例相关信息
        record_dict = record.to_dict()
        
        # 获取处方详情
        if record.prescription:
            prescription_dict = record.prescription.to_dict()
            medicines = []
            for detail in record.prescription.details:
                medicine_info = {
                    'name': detail.medicine.name if detail.medicine else None,
                    'instructions': detail.instructions
                }
                medicines.append(medicine_info)
            prescription_dict['medicines'] = medicines
            record_dict['prescription'] = prescription_dict
        
        # 获取科室信息
        doctor = record.doctor
        if doctor and doctor.department:
            record_dict['department_name'] = doctor.department.name
        
        return jsonify({
            'status': 'success',
            'message': '获取成功',
            'data': record_dict
        })

    @patient_bp.route('/payments/history', methods=['GET'])
    def get_payment_history():
        """获取支付记录
        
        Args:
            page (int): 页码
            per_page (int): 每页数量
            
        Returns:
            JSON: 支付记录列表
        """
        patient_id = request.args.get('patient_id', 1, type=int)
        print("patient_id", patient_id)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        page, per_page = validate_pagination_params(page, per_page)
        
        # 查询支付记录
        pagination = Payment.query.filter_by(patient_id=patient_id) \
            .order_by(Payment.created_at.desc()) \
            .paginate(page=page, per_page=per_page, error_out=False)
        
        payments = pagination.items
        print("payments", payments)

        # 格式化返回数据
        payment_list = []
        for payment in payments:
            # 获取详情信息
            details = ''
            if payment.details:
                detail = payment.details[0]  # 获取第一条详情
                details = detail.description
            
            payment_data = {
                'payment_id': payment.payment_id,
                'payment_time': payment.payment_time.strftime('%Y-%m-%d %H:%M:%S') if payment.payment_time else None,
                'amount': float(payment.amount),
                'type': payment.type,
                'status': payment.status,
                'details': details,
                'created_at': payment.created_at.strftime('%Y-%m-%d %H:%M:%S') if payment.created_at else None,
                'payment_method': payment.payment_method,
                'transaction_id': payment.transaction_id
            }
            payment_list.append(payment_data)
            print("payment_data", payment_data)
        
        return jsonify({
            'status': 'success',
            'message': '获取成功',
            'data': {
                'total': pagination.total,
                'page': page,
                'per_page': per_page,
                'payments': payment_list
            }
        })

    # 预约挂号相关接口
    @patient_bp.route('/registration/hospitals', methods=['GET'])
    def get_hospitals():
        """获取医院列表
        
        Returns:
            JSON: 医院列表
        """
        try:
            hospitals = Hospital.query.all()
            return jsonify({
                'status': 'success',
                'message': '获取医院列表成功',
                'data': [hospital.to_dict() for hospital in hospitals]
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'获取医院列表失败: {str(e)}',
                'data': None
            }), 500

    @patient_bp.route('/registration/departments', methods=['GET'])
    def get_departments():
        """获取科室列表
        
        Args:
            hospital_id (int): 医院ID
            
        Returns:
            JSON: 科室列表
        """
        hospital_id = request.args.get('hospital_id', type=int)
        if not hospital_id:
            return jsonify({
                'status': 'error',
                'message': '医院ID不能为空',
                'data': None
            }), 400
            
        try:
            departments = Department.query.filter_by(hospital_id=hospital_id).all()
            return jsonify({
                'status': 'success',
                'message': '获取科室列表成功',
                'data': [department.to_dict() for department in departments]
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'获取科室列表失败: {str(e)}',
                'data': None
            }), 500

    @patient_bp.route('/registration/doctors', methods=['GET'])
    def get_doctors_by_department():
        """获取科室医生列表
        
        Args:
            hospital_id (int): 医院ID
            department_id (int): 科室ID
            
        Returns:
            JSON: 医生列表
        """
        hospital_id = request.args.get('hospital_id', type=int)
        department_id = request.args.get('department_id', type=int)
        
        if not hospital_id or not department_id:
            return jsonify({
                'status': 'error',
                'message': '医院ID和科室ID不能为空',
                'data': None
            }), 400
            
        try:
            doctors = Doctor.query.filter_by(
                hospital_id=hospital_id, 
                department_id=department_id
            ).all()
            return jsonify({
                'status': 'success',
                'message': '获取医生列表成功',
                'data': [doctor.to_dict() for doctor in doctors]
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'获取医生列表失败: {str(e)}',
                'data': None
            }), 500
    
    @patient_bp.route('/registration/appointments', methods=['POST'])
    def create_appointment():
        """创建预约
        
        Body:
            patient_id (int): 患者ID
            doctor_id (int): 医生ID
            appointment_time (str): 预约时间
            hospital_id (int): 医院ID
            department_id (int): 科室ID
            status (str): 状态
            
        Returns:
            JSON: 创建结果
        """
        try:
            data = request.get_json()
            
            # 验证必要字段
            required_fields = ['patient_id', 'doctor_id', 'appointment_time']
            for field in required_fields:
                if field not in data:
                    return jsonify({
                        'status': 'error',
                        'message': f'缺少必要字段: {field}',
                        'data': None
                    }), 400
            
            # 创建预约
            appointment = Appointment(
                patient_id=data.get('patient_id'),
                doctor_id=data.get('doctor_id'),
                appointment_time=datetime.strptime(data.get('appointment_time'), '%Y-%m-%d %H:%M'),
                status=data.get('status', 'pending')
            )
            
            # 保存到数据库
            db.session.add(appointment)
            db.session.commit()
            
            # 返回结果
            return jsonify({
                'status': 'success',
                'message': '预约创建成功',
                'data': {
                    'appointment_id': appointment.appointment_id
                }
            })
        except Exception as e:
            # 回滚事务
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': f'创建预约失败: {str(e)}',
                'data': None
            }), 500
    
    @patient_bp.route('/registration/appointments', methods=['GET'])
    def get_patient_appointments():
        """获取患者的预约记录
        
        Args:
            patient_id (int): 患者ID
            
        Returns:
            JSON: 预约记录列表
        """
        # 用于存储查询结果的列表
        appointment_list = []
        
        # 使用显式会话管理
        session = db.session()
        try:
            patient_id = request.args.get('patient_id', type=int)
            if not patient_id:
                return jsonify({
                    'status': 'error',
                    'message': '患者ID不能为空',
                    'data': None
                }), 400
                
            # 查询患者的预约记录
            appointments = session.query(Appointment).filter_by(patient_id=patient_id).order_by(Appointment.appointment_time.desc()).all()
            
            # 格式化返回数据
            for appointment in appointments:
                doctor = session.query(Doctor).get(appointment.doctor_id)
                department = session.query(Department).get(doctor.department_id) if doctor else None
                hospital = session.query(Hospital).get(doctor.hospital_id) if doctor else None
                
                # 添加所需的字段，包括created_at
                appointment_data = {
                    'appointment_id': appointment.appointment_id,
                    'patient_id': appointment.patient_id,
                    'doctor_id': appointment.doctor_id,
                    'doctor_name': doctor.name if doctor else None,
                    'department_name': department.name if department else None,
                    'hospital_name': hospital.name if hospital else None,
                    'appointment_time': appointment.appointment_time.strftime('%Y-%m-%d %H:%M') if appointment.appointment_time else None,
                    'status': appointment.status,
                    'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # 添加一个创建时间，因为前端期望这个字段
                    'description': '预约挂号'  # 添加一个默认描述
                }
                appointment_list.append(appointment_data)
                
            # 成功获取数据后，提交会话
            session.commit()
            
            return jsonify({
                'status': 'success',
                'message': '获取预约记录成功',
                'data': appointment_list
            })
        except Exception as e:
            # 发生异常时回滚会话
            session.rollback()
            print(f"获取预约记录失败: {str(e)}")  # 打印错误信息以便调试
            return jsonify({
                'status': 'error',
                'message': f'获取预约记录失败: {str(e)}',
                'data': None
            }), 500
        finally:
            # 确保会话关闭
            session.close()
    
    @patient_bp.route('/payment/orders', methods=['POST'])
    def create_payment():
        """创建支付单
        
        Body:
            patient_id (int): 患者ID
            amount (float): 金额
            type (str): 类型
            status (str): 状态
            appointment_id (int): 预约ID
            
        Returns:
            JSON: 创建结果
        """
        try:
            data = request.get_json()
            
            # 验证必要字段
            required_fields = ['patient_id', 'type']
            for field in required_fields:
                if field not in data:
                    return jsonify({
                        'status': 'error',
                        'message': f'缺少必要字段: {field}',
                        'data': None
                    }), 400
            
            # 确保金额字段存在且是数值类型
            if 'amount' not in data:
                data['amount'] = 0.0  # 默认值
            
            # 如果amount为0，设置一个默认值（避免数据库约束问题）
            amount = float(data.get('amount', 0.0))
            if amount <= 0:
                amount = 30.0  # 设置默认挂号费为30元
            
            # 获取下一个可用的payment_id
            max_id_query = db.session.query(db.func.max(Payment.payment_id)).scalar()
            next_id = 1 if max_id_query is None else max_id_query + 1
            
            # 创建支付记录
            payment = Payment(
                payment_id=next_id,  # 手动设置ID
                patient_id=data.get('patient_id'),
                amount=amount,
                type=data.get('type'),
                status=data.get('status', 'pending'),
                created_at=datetime.now()  # 确保有创建时间
            )
            
            # 保存到数据库
            db.session.add(payment)
            db.session.flush()  # 确保ID已分配
            
            # 如果有详情信息，创建支付详情
            appointment_id = data.get('appointment_id')
            if appointment_id:
                description = f"预约挂号费用: 预约ID {appointment_id}"
                
                # 获取下一个可用的detail_id
                max_detail_id = db.session.query(db.func.max(PaymentDetail.detail_id)).scalar()
                next_detail_id = 1 if max_detail_id is None else max_detail_id + 1
                
                payment_detail = PaymentDetail(
                    detail_id=next_detail_id,  # 手动设置ID
                    payment_id=payment.payment_id,
                    fee_type='registration_fee',
                    amount=amount,
                    description=description
                )
                db.session.add(payment_detail)
            
            # 提交事务
            db.session.commit()
            
            # 返回结果
            return jsonify({
                'status': 'success',
                'message': '支付单创建成功',
                'data': {
                    'payment_id': payment.payment_id,
                    'amount': float(payment.amount)
                }
            })
        except Exception as e:
            # 回滚事务
            db.session.rollback()
            print(f"创建支付单失败: {str(e)}")  # 打印错误信息以便调试
            return jsonify({
                'status': 'error',
                'message': f'创建支付单失败: {str(e)}',
                'data': None
            }), 500
    
    @patient_bp.route('/records', methods=['POST'])
    def create_medical_record():
        """创建病历记录
        
        Body:
            patient_id (int): 患者ID
            doctor_id (int): 医生ID
            visit_date (str): 就诊日期
            diagnosis (str): 诊断结果
            treatment (str): 治疗方案
            
        Returns:
            JSON: 创建结果
        """
        try:
            data = request.get_json()
            
            # 验证必要字段
            required_fields = ['patient_id', 'doctor_id']
            for field in required_fields:
                if field not in data:
                    return jsonify({
                        'status': 'error',
                        'message': f'缺少必要字段: {field}',
                        'data': None
                    }), 400
            
            # 处理日期字段
            visit_date = None
            if data.get('visit_date'):
                # 尝试解析日期字符串
                try:
                    if ' ' in data.get('visit_date'):
                        visit_date = datetime.strptime(data.get('visit_date'), '%Y-%m-%d %H:%M')
                    else:
                        visit_date = datetime.strptime(data.get('visit_date'), '%Y-%m-%d')
                except ValueError:
                    visit_date = datetime.now()
            else:
                visit_date = datetime.now()
                
            # 创建病历记录
            record = MedicalRecord(
                patient_id=data.get('patient_id'),
                doctor_id=data.get('doctor_id'),
                visit_date=visit_date,
                diagnosis=data.get('diagnosis', '初诊'),
                treatment=data.get('treatment', '待医生诊断'),
                discription=data.get('discription', '患者初次就诊')
            )
            
            # 保存到数据库
            db.session.add(record)
            db.session.commit()
            
            # 返回结果
            return jsonify({
                'status': 'success',
                'message': '病历记录创建成功',
                'data': {
                    'record_id': record.record_id
                }
            })
        except Exception as e:
            # 回滚事务
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': f'创建病历记录失败: {str(e)}',
                'data': None
            }), 500

    # 医生获取患者列表接口
    @patient_bp.route('/doctor/patients', methods=['GET'])
    def get_doctor_patients():
        """获取医生的患者列表
        
        Args:
            doctor_id (int): 医生ID
            
        Returns:
            JSON: 患者列表及其基本信息
        """
        try:
            doctor_id = request.args.get('doctor_id', type=int)
            if not doctor_id:
                return jsonify({
                    'status': 'error',
                    'message': '医生ID不能为空',
                    'data': None
                }), 400
                
            # 查询该医生的所有病历记录
            records = MedicalRecord.query.filter_by(doctor_id=doctor_id).all()
            
            # 用集合去重患者ID
            patient_ids = set()
            for record in records:
                patient_ids.add(record.patient_id)
            
            # 查询患者详细信息
            patients_data = []
            for patient_id in patient_ids:
                # 查询患者基本信息
                patient = Patient.query.get(patient_id)
                if not patient:
                    continue
                    
                # 查询患者详情
                patient_detail = PatientDetail.query.filter_by(patient_id=patient_id).first()
                
                # 查询该患者最新的病历记录
                latest_record = MedicalRecord.query.filter_by(
                    patient_id=patient_id, 
                    doctor_id=doctor_id
                ).order_by(MedicalRecord.created_at.desc()).first()
                
                # 查询该患者的预约信息
                appointment = Appointment.query.filter_by(
                    patient_id=patient_id,
                    doctor_id=doctor_id
                ).order_by(Appointment.appointment_time.desc()).first()
                
                # 构建患者数据
                patient_data = {
                    'patient_id': patient.patient_id,
                    'name': patient.name,
                    'gender': patient_detail.gender if patient_detail else None,
                    'date_of_birth': patient_detail.date_of_birth.strftime('%Y-%m-%d') if patient_detail and patient_detail.date_of_birth else None,
                    'height': float(patient_detail.height) if patient_detail and patient_detail.height else None,
                    'weight': float(patient_detail.weight) if patient_detail and patient_detail.weight else None,
                    'record_id': latest_record.record_id if latest_record else None,
                    'appointment_id': appointment.appointment_id if appointment else None,
                    'visit_date': latest_record.visit_date.strftime('%Y-%m-%d') if latest_record and latest_record.visit_date else None,
                    'status': appointment.status if appointment else None
                }
                
                patients_data.append(patient_data)
            
            return jsonify({
                'status': 'success',
                'message': '获取医生患者列表成功',
                'data': patients_data
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'获取医生患者列表失败: {str(e)}',
                'data': None
            }), 500
    
    # 医生更新病历记录接口
    @patient_bp.route('/records/update', methods=['PUT'])
    def update_medical_record():
        """更新病历记录
        
        Body:
            record_id (int): 病历ID
            doctor_id (int): 医生ID
            patient_id (int): 患者ID
            discription (str): 主诉
            diagnosis (str): 诊断结果
            treatment (str): 治疗方案
            medicines (list): 药品列表，每个包含id和instructions
            
        Returns:
            JSON: 更新结果
        """
        try:
            print("收到更新病历请求")
            data = request.get_json()
            print("请求数据:", data)
            
            # 验证必要字段
            required_fields = ['doctor_id', 'patient_id']
            for field in required_fields:
                if field not in data:
                    return jsonify({
                        'status': 'error',
                        'message': f'缺少必要字段: {field}',
                        'data': None
                    }), 400
            
            # 获取或创建病历记录
            record = None
            if data.get('record_id'):
                record = MedicalRecord.query.get(data.get('record_id'))
                print("找到现有病历:", record.record_id if record else None)
            
            if not record:
                # 如果没有找到病历记录，创建一个新的
                print("创建新病历记录")
                record = MedicalRecord(
                    patient_id=data.get('patient_id'),
                    doctor_id=data.get('doctor_id'),
                    visit_date=datetime.now(),
                    diagnosis='初诊',
                    treatment='待治疗',
                    discription='初次就诊',
                    created_at=datetime.now()
                )
                db.session.add(record)
                db.session.flush()  # 确保获取ID
                print("新病历ID:", record.record_id)
            
            # 更新病历信息
            if 'discription' in data and data.get('discription'):
                record.discription = data.get('discription')
            if 'diagnosis' in data and data.get('diagnosis'):
                record.diagnosis = data.get('diagnosis')
            if 'treatment' in data and data.get('treatment'):
                record.treatment = data.get('treatment')
            
            # 处理处方和药品
            medicines = data.get('medicines', [])
            if medicines:
                prescription = None
                # 检查是否已有处方
                if record.prescription_id:
                    # 使用现有处方
                    prescription = Prescription.query.get(record.prescription_id)
                    print("使用现有处方:", prescription.prescription_id)
                
                if not prescription:
                    # 创建新处方
                    print("创建新处方")
                    prescription = Prescription(
                        patient_id=data.get('patient_id'),
                        doctor_id=data.get('doctor_id'),
                        created_at=datetime.now()
                    )
                    db.session.add(prescription)
                    db.session.flush()  # 确保ID已分配
                    
                    # 更新病历的处方ID
                    record.prescription_id = prescription.prescription_id
                    print("新处方ID:", prescription.prescription_id)
                
                # 计算总药品费用
                total_amount = 0
                
                # 添加处方明细
                for medicine_data in medicines:
                    medicine_id = medicine_data.get('medicine_id')
                    if not medicine_id:
                        continue
                        
                    instructions = medicine_data.get('instructions', '')
                    
                    # 查询药品信息
                    medicine = Medicine.query.get(medicine_id)
                    if not medicine:
                        print(f"未找到药品ID {medicine_id}")
                        continue
                    
                    print(f"添加药品: {medicine.name}, 价格: {medicine.price}")
                    
                    # 累加药品费用
                    total_amount += float(medicine.price)
                    
                    # 创建处方明细
                    detail = PrescriptionDetail(
                        prescription_id=prescription.prescription_id,
                        medicine_id=medicine_id,
                        instructions=instructions
                    )
                    db.session.add(detail)
                
                # 创建支付记录
                if total_amount > 0:
                    print(f"创建支付记录，总金额: {total_amount}")
                    # 获取下一个可用的payment_id
                    max_id_query = db.session.query(db.func.max(Payment.payment_id)).scalar()
                    next_id = 1 if max_id_query is None else max_id_query + 1
                    
                    payment = Payment(
                        payment_id=next_id,  # 手动设置ID
                        patient_id=data.get('patient_id'),
                        amount=total_amount,
                        type='药品费用',
                        status='pending',
                        created_at=datetime.now()
                    )
                    db.session.add(payment)
                
                # 更新预约状态
                if data.get('appointment_id'):
                    appointment = Appointment.query.get(data.get('appointment_id'))
                    if appointment:
                        print(f"更新预约状态为confirmed, 预约ID: {appointment.appointment_id}")
                        appointment.status = 'confirmed'
            
            # 保存所有更改
            db.session.commit()
            print("成功保存所有更改")
            
            return jsonify({
                'status': 'success',
                'message': '病历记录更新成功',
                'data': {
                    'record_id': record.record_id,
                    'prescription_id': record.prescription_id
                }
            })
        except Exception as e:
            # 回滚事务
            db.session.rollback()
            print(f"更新病历记录失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'status': 'error',
                'message': f'更新病历记录失败: {str(e)}',
                'data': None
            }), 500
    
    # 获取所有药品列表接口
    @patient_bp.route('/medicines', methods=['GET'])
    def get_medicines():
        """获取所有药品列表"""
        try:
            medicines = Medicine.query.all()
            return jsonify({
                'status': 'success',
                'message': '获取药品列表成功',
                'data': [
                    {
                        'medicine_id': medicine.medicine_id,
                        'name': medicine.name,
                        'price': float(medicine.price),
                        'description': medicine.description
                    } 
                    for medicine in medicines
                ]
            })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'获取药品列表失败: {str(e)}',
                'data': None
            }), 500

    # 支付完成接口
    @patient_bp.route('/payments/<int:payment_id>/complete', methods=['PUT', 'OPTIONS'])
    def complete_payment(payment_id):
        """完成支付
        
        Args:
            payment_id (int): 支付ID
            
        Returns:
            JSON: 更新结果
        """
        # 处理OPTIONS请求（CORS预检请求）
        if request.method == 'OPTIONS':
            return '', 200
            
        try:
            # 查询支付记录
            payment = Payment.query.get(payment_id)
            if not payment:
                return jsonify({
                    'status': 'error',
                    'message': '未找到支付记录',
                    'data': None
                }), 404
            
            # 更新支付状态
            payment.status = 'paid'
            payment.payment_time = datetime.now()
            
            # 可以在这里添加支付方式和交易号（如果前端提供）
            data = request.get_json() or {}
            if 'payment_method' in data:
                payment.payment_method = data.get('payment_method')
            if 'transaction_id' in data:
                payment.transaction_id = data.get('transaction_id')
                
            # 保存更改
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': '支付状态更新成功',
                'data': {
                    'payment_id': payment.payment_id,
                    'status': payment.status,
                    'payment_time': payment.payment_time.strftime('%Y-%m-%d %H:%M:%S') if payment.payment_time else None
                }
            })
        except Exception as e:
            # 回滚事务
            db.session.rollback()
            print(f"更新支付状态失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return jsonify({
                'status': 'error',
                'message': f'更新支付状态失败: {str(e)}',
                'data': None
            }), 500

    # ============ 集中式API路由定义结束 ============
    
    # 注册API蓝图
    app.register_blueprint(api_bp)
    
    # 注册根路由
    @app.route('/')
    def home():
        return "医疗系统API服务已启动"
    
    # 添加命令行命令
    @app.cli.command('init-db')
    def init_db_command():
        """初始化数据库命令"""
        click.echo('正在初始化数据库...')
        db.create_all()
        
        # 导入并执行数据库初始化函数
        init_db()
        
        click.echo('数据库初始化完成.')
    
    return app
