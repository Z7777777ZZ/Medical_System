from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from diagnosis.services.diagnosis_service import DiagnosisService
from . import bp

@bp.route('/create', methods=['POST'])
@jwt_required()
def create_diagnosis():
    """Create a new diagnosis record"""
    data = request.get_json()
    diagnosis = DiagnosisService.create_diagnosis(data)
    return jsonify(diagnosis.to_dict()), 201

@bp.route('/<int:diagnosis_id>', methods=['GET'])
@jwt_required()
def get_diagnosis(diagnosis_id):
    """Get a diagnosis record by ID"""
    diagnosis = DiagnosisService.get_diagnosis(diagnosis_id)
    return jsonify(diagnosis.to_dict())

@bp.route('/patient/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient_diagnoses(patient_id):
    """Get all diagnoses for a patient"""
    diagnoses = DiagnosisService.get_patient_diagnoses(patient_id)
    return jsonify([diagnosis.to_dict() for diagnosis in diagnoses])

@bp.route('/doctor/<int:doctor_id>', methods=['GET'])
@jwt_required()
def get_doctor_diagnoses(doctor_id):
    """Get all diagnoses by a doctor"""
    diagnoses = DiagnosisService.get_doctor_diagnoses(doctor_id)
    return jsonify([diagnosis.to_dict() for diagnosis in diagnoses]) 