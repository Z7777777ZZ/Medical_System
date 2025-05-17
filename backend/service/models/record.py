"""
病例记录数据模型
"""
from backend.service.utils.extensions import db
from datetime import datetime
from backend.service.models.patient import Patient
from backend.service.models.prescription import Prescription


class MedicalRecord(db.Model):
    """电子病历模型"""
    __tablename__ = 'medical_records'
    
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'), nullable=False)
    visit_date = db.Column(db.Date, nullable=False)
    discription = db.Column(db.Text)  # 患者自述
    photo = db.Column(db.Text)  # 检查照片URL，多个用回车分隔
    diagnosis = db.Column(db.Text, nullable=False)  # 诊断结果
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescriptions.prescription_id'))
    treatment = db.Column(db.Text)  # 治疗方案
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    # 关联关系
    patient = db.relationship('Patient', backref='medical_records')
    doctor = db.relationship('Doctor', backref='medical_records')
    prescription = db.relationship('Prescription', backref='medical_record')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'record_id': self.record_id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name if self.doctor else None,
            'visit_date': self.visit_date.strftime('%Y-%m-%d') if self.visit_date else None,
            'discription': self.discription,
            'photo': self.photo.split('\n') if self.photo else [],
            'diagnosis': self.diagnosis,
            'prescription_id': self.prescription_id,
            'treatment': self.treatment,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }


class Doctor(db.Model):
    """医生模型"""
    __tablename__ = 'doctors'
    
    doctor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.hospital_id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    title = db.Column(db.String(20))  # 职称
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    # 关联关系
    hospital = db.relationship('Hospital', backref='doctors')
    department = db.relationship('Department', backref='doctors')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'doctor_id': self.doctor_id,
            'phone': self.phone,
            'name': self.name,
            'hospital_id': self.hospital_id,
            'hospital_name': self.hospital.name if self.hospital else None,
            'department_id': self.department_id,
            'department_name': self.department.name if self.department else None,
            'specialty': self.specialty,
            'title': self.title,
            'bio': self.bio,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }


class Department(db.Model):
    """科室模型"""
    __tablename__ = 'departments'
    
    department_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.hospital_id'), nullable=False)
    description = db.Column(db.Text)  # 科室描述
    
    # 关联关系
    hospital = db.relationship('Hospital', backref='departments')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'department_id': self.department_id,
            'name': self.name,
            'hospital_id': self.hospital_id,
            'hospital_name': self.hospital.name if self.hospital else None,
            'description': self.description
        }


class Hospital(db.Model):
    """医院模型"""
    __tablename__ = 'hospitals'
    
    hospital_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'hospital_id': self.hospital_id,
            'name': self.name,
            'address': self.address
        }


# Prescription、PrescriptionDetail 和 Medicine 类已经在 prescription.py 中定义 