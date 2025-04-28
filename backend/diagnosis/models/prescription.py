from datetime import datetime
from app import db

class Medicine(db.Model):
    __tablename__ = 'medicines'
    
    medicine_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specification = db.Column(db.String(1024), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.medicine_id,
            'name': self.name,
            'specification': self.specification,
            'price': self.price,
            'stock': self.stock,
            'description': self.description
        }

class Prescription(db.Model):
    __tablename__ = 'prescriptions'
    
    prescription_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    instructions = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, completed, cancelled
    
    def to_dict(self):
        return {
            'id': self.prescription_id,
            'patientId': self.patient_id,
            'doctorId': self.doctor_id,
            'date': self.created_at.isoformat() if self.created_at else None,
            'instructions': self.instructions,
            'status': self.status,
            'medicines': []  # 这里返回一个空列表，药品信息将在API层手动添加
        }

class PrescriptionDetail(db.Model):
    __tablename__ = 'prescription_details'
    
    detail_id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescriptions.prescription_id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.medicine_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    instructions = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.medicine_id,
            'quantity': self.quantity,
            'usage': self.instructions
        }
