from app import db
from models.base import BaseModel

class Prescription(BaseModel):
    __tablename__ = 'prescriptions'

    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    diagnosis_id = db.Column(db.Integer, db.ForeignKey('diagnosis_records.id'), nullable=True)
    notes = db.Column(db.Text)

    # Relationships
    patient = db.relationship('Patient', backref='prescriptions')
    doctor = db.relationship('Doctor', backref='prescriptions')
    diagnosis = db.relationship('DiagnosisRecord', backref='prescription')
    details = db.relationship('PrescriptionDetail', backref='prescription', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'diagnosis_id': self.diagnosis_id,
            'notes': self.notes,
            'details': [detail.to_dict() for detail in self.details],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class PrescriptionDetail(BaseModel):
    __tablename__ = 'prescription_details'

    prescription_id = db.Column(db.Integer, db.ForeignKey('prescriptions.id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.medicine_id'), nullable=False)
    dosage = db.Column(db.String(50), nullable=False)
    frequency = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.String(50), nullable=False)
    instructions = db.Column(db.Text)
    quantity = db.Column(db.Integer, nullable=False)

    # Relationships
    medicine = db.relationship('Medicine', backref='prescription_details')

    def to_dict(self):
        return {
            'id': self.id,
            'prescription_id': self.prescription_id,
            'medicine_id': self.medicine_id,
            'dosage': self.dosage,
            'frequency': self.frequency,
            'duration': self.duration,
            'instructions': self.instructions,
            'quantity': self.quantity,
            'medicine': self.medicine.to_dict() if self.medicine else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 