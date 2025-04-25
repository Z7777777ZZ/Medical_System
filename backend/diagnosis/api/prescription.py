from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from diagnosis.services.diagnosis_service import DiagnosisService
from . import bp

@bp.route('/create', methods=['POST'])
@jwt_required()
def create_prescription():
    """Create a new prescription"""
    data = request.get_json()
    prescription = DiagnosisService.create_prescription(data)
    return jsonify(prescription.to_dict()), 201

@bp.route('/<int:prescription_id>', methods=['GET'])
@jwt_required()
def get_prescription(prescription_id):
    """Get a prescription by ID"""
    prescription = DiagnosisService.get_prescription(prescription_id)
    return jsonify(prescription.to_dict())

@bp.route('/patient/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient_prescriptions(patient_id):
    """Get all prescriptions for a patient"""
    prescriptions = DiagnosisService.get_patient_prescriptions(patient_id)
    return jsonify([prescription.to_dict() for prescription in prescriptions]) 