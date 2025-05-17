"""
处方数据模型
"""
from backend.service.utils.extensions import db
from datetime import datetime


class Prescription(db.Model):
    """处方模型"""
    __tablename__ = 'prescriptions'
    
    prescription_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    # 关联关系
    patient = db.relationship('Patient', backref='prescriptions')
    doctor = db.relationship('Doctor', backref='prescriptions')
    details = db.relationship('PrescriptionDetail', backref='prescription')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'prescription_id': self.prescription_id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.name if self.patient else None,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name if self.doctor else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'details': [detail.to_dict() for detail in self.details] if hasattr(self, 'details') else []
        }


class PrescriptionDetail(db.Model):
    """处方明细模型"""
    __tablename__ = 'prescription_details'
    
    detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescriptions.prescription_id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.medicine_id'), nullable=False)
    instructions = db.Column(db.Text, nullable=False)  # 用药指导
    
    # 关联关系
    medicine = db.relationship('Medicine', backref='prescription_details')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'detail_id': self.detail_id,
            'prescription_id': self.prescription_id,
            'medicine_id': self.medicine_id,
            'medicine_name': self.medicine.name if self.medicine else None,
            'instructions': self.instructions
        }


class Medicine(db.Model):
    """药品模型"""
    __tablename__ = 'medicines'
    
    medicine_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text)
    
    def to_dict(self):
        """转换为字典"""
        return {
            'medicine_id': self.medicine_id,
            'name': self.name,
            'price': float(self.price) if self.price else 0.0,
            'description': self.description
        } 