from datetime import datetime
from app import db

class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    
    record_id = db.Column(db.Integer, primary_key=True)  # 更正主键名
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)  # 更新外键
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'), nullable=False)  # 更新外键
    visit_date = db.Column(db.Date, nullable=False)
    discription = db.Column(db.Text, nullable=True)  # 与数据库字段匹配
    photo = db.Column(db.Text, nullable=True)
    diagnosis = db.Column(db.Text, nullable=False)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescriptions.prescription_id'), nullable=True)  # 更新外键
    treatment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.record_id,  # 返回的API仍然使用id
            'patientId': self.patient_id,
            'doctorId': self.doctor_id,
            'visitDate': self.visit_date.isoformat() if self.visit_date else None,
            'description': self.discription,  # API中使用description
            'photo': self.photo,
            'diagnosis': self.diagnosis,
            'prescriptionId': self.prescription_id,
            'treatment': self.treatment,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }
