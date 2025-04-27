from app import db
from models.base import BaseModel

class Medicine(BaseModel):
    __tablename__ = 'medicines'

    name = db.Column(db.String(100), nullable=False)
    specification = db.Column(db.String(100))
    price = db.Column(db.Numeric(10, 2))
    stock = db.Column(db.Integer)
    description = db.Column(db.Text)
    conflicts = db.Column(db.Text)  # 存储与其他药品的冲突信息，JSON格式

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'specification': self.specification,
            'price': float(self.price) if self.price else None,
            'stock': self.stock,
            'description': self.description
        }

class Prescription(BaseModel):
    __tablename__ = 'prescriptions'

    patientId = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctorId = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    instructions = db.Column(db.Text)
    status = db.Column(db.String(20), default='draft')  # draft, completed

    # 移除 relationship 定义

    def to_dict(self):
        # 手动查询关联的处方明细
        from diagnosis.models.prescription import PrescriptionDetail
        details = PrescriptionDetail.query.filter_by(prescriptionId=self.id).all()
        
        return {
            'id': self.id,
            'patientId': self.patientId,
            'doctorId': self.doctorId,
            'date': self.date.isoformat() if self.date else None,
            'instructions': self.instructions,
            'status': self.status,
            'medicines': [detail.to_dict() for detail in details],
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
            'updatedAt': self.updatedAt.isoformat() if self.updatedAt else None
        }

class PrescriptionDetail(BaseModel):
    __tablename__ = 'prescription_details'

    prescriptionId = db.Column(db.Integer, db.ForeignKey('prescriptions.id'), nullable=False)
    medicineId = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    instructions = db.Column(db.Text)

    # 移除 relationship 定义

    def to_dict(self):
        # 手动获取药品信息
        from diagnosis.models.prescription import Medicine
        medicine_obj = Medicine.query.get(self.medicineId)
        medicine = medicine_obj.to_dict() if medicine_obj else None
        
        return {
            'id': self.id,
            'prescriptionId': self.prescriptionId,
            'medicineId': self.medicineId,
            'quantity': self.quantity,
            'usage': self.instructions,
            'medicine': medicine
        }