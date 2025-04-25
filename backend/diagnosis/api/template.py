from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from diagnosis.services.diagnosis_service import DiagnosisService
from . import bp

@bp.route('/department/<int:department_id>', methods=['GET'])
@jwt_required()
def get_templates(department_id):
    """Get all diagnosis templates for a department"""
    templates = DiagnosisService.get_diagnosis_templates(department_id)
    return jsonify([template.to_dict() for template in templates])

@bp.route('/create', methods=['POST'])
@jwt_required()
def create_template():
    """Create a new diagnosis template"""
    data = request.get_json()
    template = DiagnosisService.create_diagnosis_template(data)
    return jsonify(template.to_dict()), 201 