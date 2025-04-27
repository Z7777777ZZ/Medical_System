from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from diagnosis.services.prescription_service import PrescriptionService

api = Namespace('prescription', description='Prescription management operations')

# Define models for Swagger documentation
medicine_model = api.model('Medicine', {
    'id': fields.Integer(description='Medicine ID'),
    'name': fields.String(required=True, description='Medicine name'),
    'specification': fields.String(description='Medicine specification'),
    'price': fields.Float(description='Medicine price'),
    'stock': fields.Integer(description='Medicine stock'),
    'quantity': fields.Integer(description='Prescribed quantity'),
    'usage': fields.String(description='Usage instructions')
})

prescription_model = api.model('Prescription', {
    'id': fields.Integer(description='Prescription ID'),
    'patientId': fields.Integer(required=True, description='Patient ID'),
    'doctorId': fields.Integer(required=True, description='Doctor ID'),
    'date': fields.DateTime(description='Prescription date'),
    'medicines': fields.List(fields.Nested(medicine_model), description='Prescribed medicines'),
    'instructions': fields.String(description='Additional instructions'),
    'status': fields.String(description='Prescription status (draft/completed)'),
    'createdAt': fields.DateTime(description='Creation timestamp'),
    'updatedAt': fields.DateTime(description='Last update timestamp')
})

@api.route('/create')
class CreatePrescription(Resource):
    @api.doc('create_prescription', security='Bearer')
    @api.expect(prescription_model)
    @api.marshal_with(prescription_model, code=201)
    @api.response(400, 'Invalid input')
    @jwt_required()
    def post(self):
        """Create a new prescription"""
        data = request.get_json()
        prescription = PrescriptionService.create_prescription(data)
        return prescription, 201

@api.route('/<int:prescription_id>')
class GetPrescription(Resource):
    @api.doc('get_prescription', security='Bearer')
    @api.marshal_with(prescription_model)
    @api.response(404, 'Prescription not found')
    @jwt_required()
    def get(self, prescription_id):
        """Get a prescription by ID"""
        prescription = PrescriptionService.get_prescription(prescription_id)
        if not prescription:
            api.abort(404, 'Prescription not found')
        return prescription

@api.route('/patient/<int:patient_id>')
class GetPatientPrescriptions(Resource):
    @api.doc('get_patient_prescriptions', security='Bearer')
    @api.marshal_list_with(prescription_model)
    @api.response(404, 'Patient not found')
    @jwt_required()
    def get(self, patient_id):
        """Get all prescriptions for a patient"""
        prescriptions = PrescriptionService.get_patient_prescriptions(patient_id)
        return prescriptions

@api.route('/doctor/<int:doctor_id>')
class GetDoctorPrescriptions(Resource):
    @api.doc('get_doctor_prescriptions', security='Bearer')
    @api.marshal_list_with(prescription_model)
    @api.response(404, 'Doctor not found')
    @jwt_required()
    def get(self, doctor_id):
        """Get all prescriptions by a doctor"""
        prescriptions = PrescriptionService.get_doctor_prescriptions(doctor_id)
        return prescriptions

@api.route('/medicines')
class GetAvailableMedicines(Resource):
    @api.doc('get_available_medicines', security='Bearer')
    @api.marshal_list_with(medicine_model)
    @jwt_required()
    def get(self):
        """Get list of available medicines"""
        medicines = PrescriptionService.get_available_medicines()
        return medicines

@api.route('/update/<int:prescription_id>')
class UpdatePrescription(Resource):
    @api.doc('update_prescription', security='Bearer')
    @api.expect(prescription_model)
    @api.marshal_with(prescription_model)
    @api.response(404, 'Prescription not found')
    @jwt_required()
    def put(self, prescription_id):
        """Update a prescription"""
        data = request.get_json()
        prescription = PrescriptionService.update_prescription(prescription_id, data)
        if not prescription:
            api.abort(404, 'Prescription not found')
        return prescription 