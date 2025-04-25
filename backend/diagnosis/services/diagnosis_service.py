from models.diagnosis_record import DiagnosisRecord, DiagnosisTemplate
from models.prescription import Prescription, PrescriptionDetail
from app import db

class DiagnosisService:
    @staticmethod
    def create_diagnosis(data):
        """Create a new diagnosis record"""
        diagnosis = DiagnosisRecord(
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id'],
            symptoms=data['symptoms'],
            examination=data.get('examination'),
            diagnosis=data['diagnosis'],
            treatment_plan=data.get('treatment_plan'),
            follow_up=data.get('follow_up'),
            template_id=data.get('template_id')
        )
        diagnosis.save()
        return diagnosis

    @staticmethod
    def get_diagnosis(diagnosis_id):
        """Get a diagnosis record by ID"""
        return DiagnosisRecord.query.get_or_404(diagnosis_id)

    @staticmethod
    def get_patient_diagnoses(patient_id):
        """Get all diagnoses for a patient"""
        return DiagnosisRecord.query.filter_by(patient_id=patient_id).order_by(DiagnosisRecord.created_at.desc()).all()

    @staticmethod
    def get_doctor_diagnoses(doctor_id):
        """Get all diagnoses by a doctor"""
        return DiagnosisRecord.query.filter_by(doctor_id=doctor_id).order_by(DiagnosisRecord.created_at.desc()).all()

    @staticmethod
    def create_prescription(data):
        """Create a new prescription"""
        prescription = Prescription(
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id'],
            diagnosis_id=data.get('diagnosis_id'),
            notes=data.get('notes')
        )
        prescription.save()

        # Add prescription details
        for detail in data.get('details', []):
            prescription_detail = PrescriptionDetail(
                prescription_id=prescription.id,
                medicine_id=detail['medicine_id'],
                dosage=detail['dosage'],
                frequency=detail['frequency'],
                duration=detail['duration'],
                instructions=detail.get('instructions'),
                quantity=detail['quantity']
            )
            prescription_detail.save()

        return prescription

    @staticmethod
    def get_prescription(prescription_id):
        """Get a prescription by ID"""
        return Prescription.query.get_or_404(prescription_id)

    @staticmethod
    def get_patient_prescriptions(patient_id):
        """Get all prescriptions for a patient"""
        return Prescription.query.filter_by(patient_id=patient_id).order_by(Prescription.created_at.desc()).all()

    @staticmethod
    def get_diagnosis_templates(department_id):
        """Get all diagnosis templates for a department"""
        return DiagnosisTemplate.query.filter_by(department_id=department_id).all()

    @staticmethod
    def create_diagnosis_template(data):
        """Create a new diagnosis template"""
        template = DiagnosisTemplate(
            name=data['name'],
            description=data.get('description'),
            symptoms_template=data['symptoms_template'],
            examination_template=data.get('examination_template'),
            diagnosis_template=data['diagnosis_template'],
            treatment_template=data.get('treatment_template'),
            department_id=data['department_id']
        )
        template.save()
        return template 