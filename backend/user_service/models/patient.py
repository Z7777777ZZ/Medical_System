from datetime import datetime
from extensions import db

class Patients(db.Model):
    __tablename__ = 'patients'

    patient_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    details = db.relationship('Patient_details', backref='patient', uselist=False)

    def __repr__(self):
        return f'<patients {self.name}>'
    
class Patient_details(db.Model):
    __tablename__ = 'patient_details'

    patient_id = db.Column(db.BigInteger, db.ForeignKey('patients.patient_id'), primary_key=True)
    gender = db.Column(db.Enum('male', 'female', 'other'), nullable=False)
    date_of_birth = db.Column(db.String(20), nullable=False)
    blood_type = db.Column(db.Enum('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'), nullable=False)
    height = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    emergency_contact = db.Column(db.String(100), nullable=False)
    emergency_phone = db.Column(db.String(20), nullable=False)
    medical_insurance_id = db.Column(db.String(50), nullable=False)
    allergies = db.Column(db.String(1024), nullable=False)
    chronic_conditions = db.Column(db.String(1024), nullable=False)
    medications = db.Column(db.String(1024), nullable=False)