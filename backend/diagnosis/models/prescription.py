from app import db
from models.base import Base
from datetime import datetime

class Medicine(Base):
    """药品模型"""
    __tablename__ = 'medicines'
    
    medicine_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    
    def to_dict(self):
        """转换为API响应格式，使用驼峰命名"""
        return {
            'id': self.medicine_id,
            'name': self.name,
            'price': self.price,
            'description': self.description
        }

class Prescription(Base):
    """处方模型"""
    __tablename__ = 'prescriptions'
    
    prescription_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'), nullable=False)
    diagnosis = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.Enum('draft', 'confirmed', 'dispensed'), default='draft')
    
    # 关系
    patient = db.relationship('Patient', backref='prescriptions')
    doctor = db.relationship('Doctor', backref='prescriptions')
    details = db.relationship('PrescriptionDetail', backref='prescription', cascade='all, delete-orphan')
    
    def to_dict(self):
        """转换为API响应格式，使用驼峰命名"""
        details = [detail.to_dict() for detail in self.details]
        
        return {
            'id': self.prescription_id,
            'patientId': self.patient_id,
            'doctorId': self.doctor_id,
            'patientName': self.patient.name if self.patient else None,
            'doctorName': self.doctor.name if self.doctor else None,
            'diagnosis': self.diagnosis,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'status': self.status,
            'medicines': details
        }

class PrescriptionDetail(Base):
    """处方明细模型"""
    __tablename__ = 'prescription_details'
    
    detail_id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescriptions.prescription_id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.medicine_id'), nullable=False)
    dosage = db.Column(db.String(100))
    frequency = db.Column(db.String(100))
    duration = db.Column(db.String(100))
    instructions = db.Column(db.Text)
    
    # 关系
    medicine = db.relationship('Medicine')
    
    def to_dict(self):
        """转换为API响应格式，使用驼峰命名"""
        return {
            'id': self.detail_id,
            'medicineId': self.medicine_id,
            'medicineName': self.medicine.name if self.medicine else None,
            'dosage': self.dosage,
            'frequency': self.frequency,
            'duration': self.duration,
            'instructions': self.instructions,
            'price': self.medicine.price if self.medicine else 0
        }
