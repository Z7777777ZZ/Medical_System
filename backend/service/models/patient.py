"""
患者数据模型
"""
from backend.service.utils.extensions import db
from datetime import datetime


class Patient(db.Model):
    """患者模型"""
    __tablename__ = 'patients'
    
    patient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    # 关联
    patient_details = db.relationship('PatientDetail', backref='patient', uselist=False)
    
    def to_dict(self):
        """转换为字典"""
        data = {
            'patient_id': self.patient_id,
            'phone': self.phone,
            'email': self.email,
            'name': self.name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
        
        # 如果有详细信息，添加进来
        if self.patient_details:
            patient_details = self.patient_details.to_dict()
            # 移除重复的patient_id
            patient_details.pop('patient_id', None)
            data.update(patient_details)
            
        return data


class PatientDetail(db.Model):
    """患者详细信息模型"""
    __tablename__ = 'patient_details'
    
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), primary_key=True)
    gender = db.Column(db.Enum('male', 'female', 'other'), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    blood_type = db.Column(db.Enum('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'), nullable=True)
    height = db.Column(db.Numeric(5, 2), nullable=True)
    weight = db.Column(db.Numeric(5, 2), nullable=True)
    emergency_contact = db.Column(db.String(100), nullable=True)
    emergency_phone = db.Column(db.String(20), nullable=True)
    medical_insurance_id = db.Column(db.String(50), nullable=True)
    allergies = db.Column(db.Text, nullable=True)
    chronic_conditions = db.Column(db.Text, nullable=True)
    medications = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'patient_id': self.patient_id,
            'gender': self.gender,
            'date_of_birth': self.date_of_birth.strftime('%Y-%m-%d') if self.date_of_birth else None,
            'blood_type': self.blood_type,
            'height': float(self.height) if self.height else None,
            'weight': float(self.weight) if self.weight else None,
            'emergency_contact': self.emergency_contact,
            'emergency_phone': self.emergency_phone,
            'medical_insurance_id': self.medical_insurance_id,
            'allergies': self.allergies,
            'chronic_conditions': self.chronic_conditions,
            'medications': self.medications
        } 