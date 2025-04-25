from app import db
from models.base import BaseModel

class DiagnosisRecord(BaseModel):
    __tablename__ = 'diagnosis_records'

    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    examination = db.Column(db.Text)
    diagnosis = db.Column(db.Text, nullable=False)
    treatment_plan = db.Column(db.Text)
    follow_up = db.Column(db.Text)
    template_id = db.Column(db.Integer, db.ForeignKey('diagnosis_templates.id'), nullable=True)

    # Relationships
    patient = db.relationship('Patient', backref='diagnosis_records')
    doctor = db.relationship('Doctor', backref='diagnosis_records')
    template = db.relationship('DiagnosisTemplate', backref='diagnosis_records')

    def to_dict(self):
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'doctor_id': self.doctor_id,
            'symptoms': self.symptoms,
            'examination': self.examination,
            'diagnosis': self.diagnosis,
            'treatment_plan': self.treatment_plan,
            'follow_up': self.follow_up,
            'template_id': self.template_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class DiagnosisTemplate(BaseModel):
    __tablename__ = 'diagnosis_templates'

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    symptoms_template = db.Column(db.Text)
    examination_template = db.Column(db.Text)
    diagnosis_template = db.Column(db.Text)
    treatment_template = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'), nullable=False)

    # Relationships
    department = db.relationship('Department', backref='diagnosis_templates')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'symptoms_template': self.symptoms_template,
            'examination_template': self.examination_template,
            'diagnosis_template': self.diagnosis_template,
            'treatment_template': self.treatment_template,
            'department_id': self.department_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        } 