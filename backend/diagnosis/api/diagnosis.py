from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from diagnosis.services.diagnosis_service import DiagnosisService

api = Namespace('diagnosis', description='Diagnosis related operations')

# Define models for Swagger documentation
diagnosis_model = api.model('Diagnosis', {
    'id': fields.Integer(description='Diagnosis ID'),
    'patient_id': fields.Integer(required=True, description='Patient ID'),
    'doctor_id': fields.Integer(required=True, description='Doctor ID'),
    'symptoms': fields.String(required=True, description='Patient symptoms'),
    'examination': fields.String(description='Examination results'),
    'diagnosis': fields.String(required=True, description='Diagnosis result'),
    'treatment_plan': fields.String(description='Treatment plan'),
    'follow_up': fields.String(description='Follow up instructions'),
    'template_id': fields.Integer(description='Template ID used for this diagnosis'),
    'created_at': fields.DateTime(description='Creation timestamp'),
    'updated_at': fields.DateTime(description='Last update timestamp')
})

@api.route('/create')
class CreateDiagnosis(Resource):
    @api.doc('create_diagnosis', security='Bearer')
    @api.expect(diagnosis_model)
    @api.marshal_with(diagnosis_model, code=201)
    @api.response(400, 'Invalid input')
    @jwt_required()
    def post(self):
        """Create a new diagnosis record"""
        data = request.get_json()
        diagnosis = DiagnosisService.create_diagnosis(data)
        return diagnosis.to_dict(), 201

@api.route('/<int:diagnosis_id>')
class GetDiagnosis(Resource):
    @api.doc('get_diagnosis', security='Bearer')
    @api.marshal_with(diagnosis_model)
    @api.response(404, 'Diagnosis not found')
    @jwt_required()
    def get(self, diagnosis_id):
        """Get a diagnosis record by ID"""
        diagnosis = DiagnosisService.get_diagnosis(diagnosis_id)
        if not diagnosis:
            api.abort(404, 'Diagnosis not found')
        return diagnosis.to_dict()

@api.route('/patient/<int:patient_id>')
class GetPatientDiagnoses(Resource):
    @api.doc('get_patient_diagnoses', security='Bearer')
    @api.marshal_list_with(diagnosis_model)
    @api.response(404, 'Patient not found')
    @jwt_required()
    def get(self, patient_id):
        """Get all diagnoses for a patient"""
        diagnoses = DiagnosisService.get_patient_diagnoses(patient_id)
        if not diagnoses:
            api.abort(404, 'Patient not found')
        return [diagnosis.to_dict() for diagnosis in diagnoses]

@api.route('/doctor/<int:doctor_id>')
class GetDoctorDiagnoses(Resource):
    @api.doc('get_doctor_diagnoses', security='Bearer')
    @api.marshal_list_with(diagnosis_model)
    @api.response(404, 'Doctor not found')
    @jwt_required()
    def get(self, doctor_id):
        """Get all diagnoses by a doctor"""
        diagnoses = DiagnosisService.get_doctor_diagnoses(doctor_id)
        if not diagnoses:
            api.abort(404, 'Doctor not found')
        return [diagnosis.to_dict() for diagnosis in diagnoses] 