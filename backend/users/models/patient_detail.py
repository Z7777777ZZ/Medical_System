from app import db

class PatientDetail(db.Model):
    __tablename__ = 'patient_details'
    
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), primary_key=True)
    gender = db.Column(db.Enum('male', 'female', 'other'), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    blood_type = db.Column(db.Enum('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'), nullable=True)
    height = db.Column(db.DECIMAL(5, 2), nullable=True)
    weight = db.Column(db.DECIMAL(5, 2), nullable=True)
    emergency_contact = db.Column(db.String(100), nullable=True)
    emergency_phone = db.Column(db.String(20), nullable=True)
    medical_insurance_id = db.Column(db.String(50), nullable=True)
    allergies = db.Column(db.Text, nullable=True)
    chronic_conditions = db.Column(db.Text, nullable=True)
    medications = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            'patientId': self.patient_id,
            'gender': self.gender,
            'dateOfBirth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'bloodType': self.blood_type,
            'height': float(self.height) if self.height else None,
            'weight': float(self.weight) if self.weight else None,
            'emergencyContact': self.emergency_contact,
            'emergencyPhone': self.emergency_phone,
            'medicalInsuranceId': self.medical_insurance_id,
            'allergies': self.allergies,
            'chronicConditions': self.chronic_conditions,
            'medications': self.medications
        }