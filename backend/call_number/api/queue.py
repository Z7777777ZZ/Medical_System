from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from call_number.services.queue_service import QueueService

api = Namespace('queue', description='Queue management operations')

# Define models for Swagger documentation
patient_model = api.model('Patient', {
    'id': fields.Integer(description='Patient ID'),
    'name': fields.String(required=True, description='Patient name'),
    'age': fields.Integer(description='Patient age'),
    'gender': fields.String(description='Patient gender'),
    'symptom': fields.String(description='Patient symptoms'),
    'waitingTime': fields.Integer(description='Waiting time in minutes'),
    'examResult': fields.String(description='Examination result'),
    'isCurrentUser': fields.Boolean(description='Whether this is the current user')
})

queue_info_model = api.model('QueueInfo', {
    'queueNumber': fields.String(required=True, description='Queue number'),
    'ahead': fields.Integer(description='Number of patients ahead'),
    'estimatedWaitTime': fields.Integer(description='Estimated wait time in minutes'),
    'status': fields.String(description='Queue status (waiting/calling/exam/completed)'),
    'registerTime': fields.DateTime(description='Registration time')
})

clinic_info_model = api.model('ClinicInfo', {
    'name': fields.String(required=True, description='Clinic name'),
    'location': fields.String(description='Clinic location'),
    'doctorName': fields.String(description='Doctor name'),
    'specialty': fields.String(description='Doctor specialty'),
    'workingHours': fields.String(description='Working hours'),
    'notice': fields.String(description='Clinic notice'),
    'mapX': fields.Integer(description='Map X coordinate'),
    'mapY': fields.Integer(description='Map Y coordinate'),
    'locationDirections': fields.String(description='Location directions')
})

@api.route('/register')
class RegisterPatient(Resource):
    @api.doc('register_patient', security='Bearer')
    @api.expect(api.model('RegisterForm', {
        'visitReason': fields.String(required=True, description='Visit reason'),
        'department': fields.String(required=True, description='Department')
    }))
    @api.marshal_with(queue_info_model, code=201)
    @api.response(400, 'Invalid input')
    @jwt_required()
    def post(self):
        """Register a new patient in the queue"""
        data = request.get_json()
        result = QueueService.register_patient(data)
        return result, 201

@api.route('/status/<int:patient_id>')
class GetQueueStatus(Resource):
    @api.doc('get_queue_status', security='Bearer')
    @api.marshal_with(queue_info_model)
    @api.response(404, 'Patient not found')
    @jwt_required()
    def get(self, patient_id):
        """Get queue status for a patient"""
        status = QueueService.get_queue_status(patient_id)
        if not status:
            api.abort(404, 'Patient not found')
        return status

@api.route('/clinic/<int:clinic_id>')
class GetClinicInfo(Resource):
    @api.doc('get_clinic_info', security='Bearer')
    @api.marshal_with(clinic_info_model)
    @api.response(404, 'Clinic not found')
    @jwt_required()
    def get(self, clinic_id):
        """Get clinic information"""
        info = QueueService.get_clinic_info(clinic_id)
        if not info:
            api.abort(404, 'Clinic not found')
        return info

@api.route('/current')
class GetCurrentCalling(Resource):
    @api.doc('get_current_calling', security='Bearer')
    @api.marshal_with(patient_model)
    @jwt_required()
    def get(self):
        """Get current calling information"""
        calling = QueueService.get_current_calling()
        return calling

@api.route('/list')
class GetQueueList(Resource):
    @api.doc('get_queue_list', security='Bearer')
    @api.marshal_list_with(patient_model)
    @jwt_required()
    def get(self):
        """Get the current queue list"""
        queue_list = QueueService.get_queue_list()
        return queue_list

@api.route('/refresh/<int:patient_id>')
class RefreshQueueStatus(Resource):
    @api.doc('refresh_queue_status', security='Bearer')
    @api.marshal_with(queue_info_model)
    @api.response(404, 'Patient not found')
    @jwt_required()
    def post(self, patient_id):
        """Refresh queue status for a patient"""
        status = QueueService.refresh_queue_status(patient_id)
        if not status:
            api.abort(404, 'Patient not found')
        return status 