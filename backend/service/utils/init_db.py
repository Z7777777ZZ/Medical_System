"""
数据库初始化脚本
用于插入示例数据
"""
import os
import sys
from datetime import datetime, timedelta, date
from flask import Flask
from sqlalchemy.exc import IntegrityError
from backend.service.utils.extensions import db
from backend.service.models.record import Department, Doctor, MedicalRecord, Hospital
from backend.service.models.patient import Patient, PatientDetail
from backend.service.models.registration import Appointment, Queue
from backend.service.models.payment import Payment
from backend.service.models.prescription import Prescription, PrescriptionDetail, Medicine

def init_db():
    """初始化数据库"""
    print("正在初始化示例数据...")
    
    try:
        # 创建医院数据
        hospitals = [
            Hospital(hospital_id=1, name='北京协和医院', address='北京市东城区帅府园1号'),
            Hospital(hospital_id=2, name='上海瑞金医院', address='上海市黄浦区瑞金二路197号'),
            Hospital(hospital_id=3, name='广州南方医院', address='广州市白云区广花路1838号')
        ]
        
        db.session.add_all(hospitals)
        db.session.commit()
        print(f"已添加 {len(hospitals)} 个医院")
        
        # 创建科室数据
        departments = [
            Department(department_id=1, name='内科', hospital_id=1),
            Department(department_id=2, name='外科', hospital_id=1),
            Department(department_id=3, name='妇产科', hospital_id=1),
            Department(department_id=4, name='儿科', hospital_id=1),
            Department(department_id=5, name='骨科', hospital_id=2),
            Department(department_id=6, name='心脏内科', hospital_id=2),
            Department(department_id=7, name='神经内科', hospital_id=2),
            Department(department_id=8, name='急诊科', hospital_id=3),
            Department(department_id=9, name='肿瘤科', hospital_id=3),
            Department(department_id=10, name='眼科', hospital_id=3)
        ]
        
        db.session.add_all(departments)
        db.session.commit()
        print(f"已添加 {len(departments)} 个科室")
        
        # 创建医生数据
        doctors = [
            Doctor(doctor_id=1, phone='13800001111', name='张伟', hospital_id=1, department_id=1, 
                   specialty='呼吸系统疾病', bio='毕业于北京医科大学，从事呼吸系统疾病研究20年', 
                   password_hash='password123', created_at=datetime(2023, 1, 15, 9, 0, 0)),
            Doctor(doctor_id=2, phone='13800002222', name='王芳', hospital_id=1, department_id=3, 
                   specialty='妇科肿瘤', bio='妇科肿瘤专家，擅长妇科恶性肿瘤的诊断与治疗', 
                   password_hash='password123', created_at=datetime(2023, 1, 16, 10, 30, 0)),
            Doctor(doctor_id=3, phone='13800003333', name='李明', hospital_id=1, department_id=2, 
                   specialty='胃肠外科', bio='擅长微创手术和胃肠道肿瘤手术', 
                   password_hash='password123', created_at=datetime(2023, 2, 1, 8, 45, 0)),
            Doctor(doctor_id=4, phone='13800004444', name='赵华', hospital_id=2, department_id=5, 
                   specialty='骨折创伤', bio='专注于复杂骨折和创伤修复', 
                   password_hash='password123', created_at=datetime(2023, 2, 10, 14, 0, 0)),
            Doctor(doctor_id=5, phone='13800005555', name='刘洋', hospital_id=2, department_id=6, 
                   specialty='冠心病', bio='心脏介入治疗专家', 
                   password_hash='password123', created_at=datetime(2023, 3, 5, 11, 20, 0)),
            Doctor(doctor_id=6, phone='13800006666', name='陈晓', hospital_id=3, department_id=9, 
                   specialty='肺癌治疗', bio='肺癌靶向治疗和免疫治疗专家', 
                   password_hash='password123', created_at=datetime(2023, 3, 15, 16, 40, 0)),
            Doctor(doctor_id=7, phone='13800007777', name='杨红', hospital_id=3, department_id=10, 
                   specialty='白内障手术', bio='高级眼科医师，擅长各类眼科疾病诊疗', 
                   password_hash='password123', created_at=datetime(2023, 4, 1, 9, 15, 0))
        ]
        
        db.session.add_all(doctors)
        db.session.commit()
        print(f"已添加 {len(doctors)} 名医生")
        
        # 创建患者数据
        patients = [
            Patient(patient_id=1, phone='13900001111', email='patient1@example.com', 
                    name='张三', password_hash='patientpwd1', 
                    created_at=datetime(2023, 5, 1, 10, 0, 0)),
            Patient(patient_id=2, phone='13900002222', email='patient2@example.com', 
                    name='李四', password_hash='patientpwd2', 
                    created_at=datetime(2023, 5, 2, 11, 30, 0)),
            Patient(patient_id=3, phone='13900003333', email='patient3@example.com', 
                    name='王五', password_hash='patientpwd3', 
                    created_at=datetime(2023, 5, 3, 14, 20, 0)),
            Patient(patient_id=4, phone='13900004444', email='patient4@example.com', 
                    name='赵六', password_hash='patientpwd4', 
                    created_at=datetime(2023, 5, 4, 16, 45, 0)),
            Patient(patient_id=5, phone='13900005555', email='patient5@example.com', 
                    name='孙七', password_hash='patientpwd5', 
                    created_at=datetime(2023, 5, 5, 9, 15, 0)),
            Patient(patient_id=6, phone='13900006666', email='patient6@example.com', 
                    name='周八', password_hash='patientpwd6', 
                    created_at=datetime(2023, 5, 6, 13, 40, 0)),
            Patient(patient_id=7, phone='13900007777', email='patient7@example.com', 
                    name='吴九', password_hash='patientpwd7', 
                    created_at=datetime(2023, 5, 7, 15, 10, 0)),
            Patient(patient_id=8, phone='13900008888', email='patient8@example.com', 
                    name='郑十', password_hash='patientpwd8', 
                    created_at=datetime(2023, 5, 8, 10, 50, 0))
        ]
        
        db.session.add_all(patients)
        db.session.commit()
        print(f"已添加 {len(patients)} 名患者")
        
        # 创建患者详细信息
        patient_details = [
            PatientDetail(patient_id=1, gender='male', date_of_birth=date(1980, 6, 15), blood_type='A+', 
                         height=178.5, weight=75.0, emergency_contact='张太太', emergency_phone='13911112222', 
                         medical_insurance_id='INS123456', allergies='青霉素', 
                         chronic_conditions='高血压', medications='络活喜 5mg 每日一次'),
            PatientDetail(patient_id=2, gender='female', date_of_birth=date(1985, 3, 22), blood_type='B+', 
                         height=165.0, weight=55.0, emergency_contact='李先生', emergency_phone='13922223333', 
                         medical_insurance_id='INS234567', allergies='无', 
                         chronic_conditions='糖尿病', medications='二甲双胍 500mg 每日两次'),
            PatientDetail(patient_id=3, gender='male', date_of_birth=date(1975, 11, 10), blood_type='O+', 
                         height=182.0, weight=80.0, emergency_contact='王妻子', emergency_phone='13933334444', 
                         medical_insurance_id='INS345678', allergies='磺胺类药物', 
                         chronic_conditions='冠心病', medications='阿司匹林 100mg 每日一次'),
            PatientDetail(patient_id=4, gender='female', date_of_birth=date(1990, 8, 5), blood_type='AB+', 
                         height=160.0, weight=50.0, emergency_contact='赵母亲', emergency_phone='13944445555', 
                         medical_insurance_id='INS456789', allergies='花粉过敏', 
                         chronic_conditions='无', medications='无'),
            PatientDetail(patient_id=5, gender='male', date_of_birth=date(1965, 1, 20), blood_type='A-', 
                         height=175.0, weight=70.0, emergency_contact='孙妻子', emergency_phone='13955556666', 
                         medical_insurance_id='INS567890', allergies='无', 
                         chronic_conditions='高血脂', medications='立普妥 20mg 每晚一次'),
            PatientDetail(patient_id=6, gender='female', date_of_birth=date(1988, 4, 30), blood_type='O-', 
                         height=168.0, weight=58.0, emergency_contact='周丈夫', emergency_phone='13966667777', 
                         medical_insurance_id='INS678901', allergies='海鲜', 
                         chronic_conditions='哮喘', medications='舒利迭 100mcg 每日两次'),
            PatientDetail(patient_id=7, gender='male', date_of_birth=date(1982, 9, 18), blood_type='B-', 
                         height=180.0, weight=85.0, emergency_contact='吴父亲', emergency_phone='13977778888', 
                         medical_insurance_id='INS789012', allergies='无', 
                         chronic_conditions='无', medications='无'),
            PatientDetail(patient_id=8, gender='female', date_of_birth=date(1995, 12, 25), blood_type='AB-', 
                         height=163.0, weight=52.0, emergency_contact='郑母亲', emergency_phone='13988889999', 
                         medical_insurance_id='INS890123', allergies='乳糖不耐', 
                         chronic_conditions='贫血', medications='铁剂补充剂 每日一次')
        ]
        
        db.session.add_all(patient_details)
        db.session.commit()
        print(f"已添加 {len(patient_details)} 条患者详细信息")
        
        # 创建药品数据
        medicines = [
            Medicine(medicine_id=1, name='阿莫西林胶囊', price=15.50, 
                    description='广谱青霉素类抗生素，用于敏感菌引起的感染'),
            Medicine(medicine_id=2, name='奥美拉唑肠溶胶囊', price=22.80, 
                    description='质子泵抑制剂，用于消化性溃疡和胃食管反流病'),
            Medicine(medicine_id=3, name='辛伐他汀片', price=35.60, 
                    description='他汀类调脂药，用于高胆固醇血症'),
            Medicine(medicine_id=4, name='盐酸二甲双胍片', price=12.40, 
                    description='口服降糖药，用于2型糖尿病'),
            Medicine(medicine_id=5, name='硝苯地平控释片', price=18.90, 
                    description='钙通道阻滞剂，用于高血压和心绞痛'),
            Medicine(medicine_id=6, name='复方甲硝唑阴道凝胶', price=26.50, 
                    description='抗菌药，用于细菌性阴道病和滴虫性阴道炎'),
            Medicine(medicine_id=7, name='布洛芬缓释胶囊', price=9.80, 
                    description='非甾体抗炎药，用于缓解疼痛和发热'),
            Medicine(medicine_id=8, name='氯雷他定片', price=16.70, 
                    description='抗组胺药，用于过敏性鼻炎和荨麻疹')
        ]
        
        db.session.add_all(medicines)
        db.session.commit()
        print(f"已添加 {len(medicines)} 种药品")
        
        # 创建预约数据
        appointments = [
            Appointment(appointment_id=1, patient_id=1, doctor_id=1, 
                       appointment_time=datetime(2023, 6, 1, 9, 30, 0), status='confirmed'),
            Appointment(appointment_id=2, patient_id=2, doctor_id=2, 
                       appointment_time=datetime(2023, 6, 1, 10, 0, 0), status='confirmed'),
            Appointment(appointment_id=3, patient_id=3, doctor_id=3, 
                       appointment_time=datetime(2023, 6, 1, 14, 0, 0), status='confirmed'),
            Appointment(appointment_id=4, patient_id=4, doctor_id=4, 
                       appointment_time=datetime(2023, 6, 2, 11, 30, 0), status='confirmed'),
            Appointment(appointment_id=5, patient_id=5, doctor_id=5, 
                       appointment_time=datetime(2023, 6, 2, 15, 45, 0), status='confirmed'),
            Appointment(appointment_id=6, patient_id=6, doctor_id=6, 
                       appointment_time=datetime(2023, 6, 3, 9, 15, 0), status='confirmed'),
            Appointment(appointment_id=7, patient_id=7, doctor_id=7, 
                       appointment_time=datetime(2023, 6, 3, 16, 0, 0), status='confirmed'),
            Appointment(appointment_id=8, patient_id=8, doctor_id=1, 
                       appointment_time=datetime(2023, 6, 4, 10, 30, 0), status='pending'),
            Appointment(appointment_id=9, patient_id=1, doctor_id=5, 
                       appointment_time=datetime(2023, 6, 5, 14, 30, 0), status='pending'),
            Appointment(appointment_id=10, patient_id=3, doctor_id=6, 
                       appointment_time=datetime(2023, 6, 6, 11, 0, 0), status='pending')
        ]
        
        db.session.add_all(appointments)
        db.session.commit()
        print(f"已添加 {len(appointments)} 条预约记录")
        
        # 创建排队数据
        queues = [
            Queue(queue_id=1, patient_id=1, doctor_id=1, queue_number=1, status='called'),
            Queue(queue_id=2, patient_id=2, doctor_id=2, queue_number=1, status='called'),
            Queue(queue_id=3, patient_id=3, doctor_id=3, queue_number=1, status='called'),
            Queue(queue_id=4, patient_id=4, doctor_id=4, queue_number=1, status='waiting'),
            Queue(queue_id=5, patient_id=5, doctor_id=5, queue_number=1, status='waiting'),
            Queue(queue_id=6, patient_id=6, doctor_id=6, queue_number=1, status='waiting'),
            Queue(queue_id=7, patient_id=7, doctor_id=7, queue_number=1, status='waiting')
        ]
        
        db.session.add_all(queues)
        db.session.commit()
        print(f"已添加 {len(queues)} 条排队数据")
        
        # 创建处方数据
        prescriptions = [
            Prescription(prescription_id=1, patient_id=1, doctor_id=1, 
                         created_at=datetime(2023, 6, 1, 10, 15, 0)),
            Prescription(prescription_id=2, patient_id=2, doctor_id=2, 
                         created_at=datetime(2023, 6, 1, 10, 45, 0)),
            Prescription(prescription_id=3, patient_id=3, doctor_id=3, 
                         created_at=datetime(2023, 6, 1, 14, 30, 0)),
            Prescription(prescription_id=4, patient_id=4, doctor_id=4, 
                         created_at=datetime(2023, 6, 2, 12, 0, 0)),
            Prescription(prescription_id=5, patient_id=5, doctor_id=5, 
                         created_at=datetime(2023, 6, 2, 16, 15, 0))
        ]
        
        db.session.add_all(prescriptions)
        db.session.commit()
        print(f"已添加 {len(prescriptions)} 个处方")
        
        # 创建处方详情
        prescription_details = [
            PrescriptionDetail(detail_id=1, prescription_id=1, medicine_id=1, 
                              instructions='一次1粒，一日3次，饭后服用，疗程5天'),
            PrescriptionDetail(detail_id=2, prescription_id=1, medicine_id=7, 
                              instructions='一次1粒，一日3次，饭后服用，需要时服用'),
            PrescriptionDetail(detail_id=3, prescription_id=2, medicine_id=6, 
                              instructions='每晚睡前使用一次，连续使用7天'),
            PrescriptionDetail(detail_id=4, prescription_id=3, medicine_id=2, 
                              instructions='一次1粒，一日2次，早晚饭前30分钟服用，疗程4周'),
            PrescriptionDetail(detail_id=5, prescription_id=3, medicine_id=3, 
                              instructions='一次1粒，每晚睡前服用，长期服用'),
            PrescriptionDetail(detail_id=6, prescription_id=4, medicine_id=5, 
                              instructions='一次1粒，一日1次，早饭后服用，长期服用'),
            PrescriptionDetail(detail_id=7, prescription_id=5, medicine_id=4, 
                              instructions='一次1粒，一日2次，早晚饭后服用，长期服用'),
            PrescriptionDetail(detail_id=8, prescription_id=5, medicine_id=8, 
                              instructions='一次1粒，一日1次，需要时服用')
        ]
        
        db.session.add_all(prescription_details)
        db.session.commit()
        print(f"已添加 {len(prescription_details)} 条处方详情")
        
        # 创建电子病历数据
        records = [
            MedicalRecord(
                record_id=1,
                patient_id=1, 
                doctor_id=1, 
                visit_date=date(2023, 6, 1),
                discription='患者出现发热、咳嗽、咽痛症状3天',
                diagnosis='上呼吸道感染',
                prescription_id=1,
                treatment='对症治疗，多休息，多饮水',
                created_at=datetime(2023, 6, 1, 10, 30, 0)
            ),
            MedicalRecord(
                record_id=2,
                patient_id=2, 
                doctor_id=2, 
                visit_date=date(2023, 6, 1),
                discription='患者出现白带异常、外阴瘙痒症状1周',
                diagnosis='细菌性阴道炎',
                prescription_id=2,
                treatment='局部用药治疗，保持局部清洁干燥',
                created_at=datetime(2023, 6, 1, 11, 0, 0)
            ),
            MedicalRecord(
                record_id=3,
                patient_id=3, 
                doctor_id=3, 
                visit_date=date(2023, 6, 1),
                discription='患者出现上腹部疼痛、反酸、烧心症状2周',
                diagnosis='胃食管反流病',
                prescription_id=3,
                treatment='药物治疗，调整饮食习惯，避免辛辣刺激食物',
                created_at=datetime(2023, 6, 1, 14, 45, 0)
            ),
            MedicalRecord(
                record_id=4,
                patient_id=4, 
                doctor_id=4, 
                visit_date=date(2023, 6, 2),
                discription='患者左踝关节扭伤，出现肿胀、疼痛',
                photo='ankle_sprain.jpg',
                diagnosis='踝关节扭伤',
                prescription_id=4,
                treatment='抬高患肢，冰敷，制动，药物治疗',
                created_at=datetime(2023, 6, 2, 12, 15, 0)
            ),
            MedicalRecord(
                record_id=5,
                patient_id=5, 
                doctor_id=5, 
                visit_date=date(2023, 6, 2),
                discription='患者出现头晕、乏力，血压测量160/95mmHg',
                diagnosis='高血压',
                prescription_id=5,
                treatment='药物治疗，低盐饮食，规律运动，定期监测血压',
                created_at=datetime(2023, 6, 2, 16, 30, 0)
            )
        ]
        
        db.session.add_all(records)
        db.session.commit()
        print(f"已添加 {len(records)} 条电子病历")
        
        # 创建支付数据
        payments = [
            Payment(payment_id=1, patient_id=1, amount=55.30, type='医保支付', status='paid'),
            Payment(payment_id=2, patient_id=2, amount=26.50, type='现金支付', status='paid'),
            Payment(payment_id=3, patient_id=3, amount=78.40, type='微信支付', status='paid'),
            Payment(payment_id=4, patient_id=4, amount=28.70, type='医保支付', status='paid'),
            Payment(payment_id=5, patient_id=5, amount=31.30, type='支付宝支付', status='paid'),
            Payment(payment_id=6, patient_id=6, amount=0.00, type='待诊', status='pending'),
            Payment(payment_id=7, patient_id=7, amount=0.00, type='待诊', status='pending'),
            Payment(payment_id=8, patient_id=8, amount=0.00, type='待诊', status='pending')
        ]
        
        db.session.add_all(payments)
        db.session.commit()
        print(f"已添加 {len(payments)} 条支付数据")
        
        print("数据库初始化完成")
        
    except Exception as e:
        db.session.rollback()
        print(f"初始化数据错误: {str(e)}")
        raise e

if __name__ == '__main__':
    app = Flask(__name__)
    with app.app_context():
        init_db() 