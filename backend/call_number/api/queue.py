from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from call_number.services.queue_service import QueueService
from . import bp

@bp.route('/doctor/<int:doctor_id>', methods=['GET'])
@jwt_required()
def get_doctor_queue(doctor_id):
    """Get queue for a specific doctor"""
    queues = QueueService.get_doctor_queue(doctor_id)
    return jsonify([queue.to_dict() for queue in queues])

@bp.route('/patient/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient_queue(patient_id):
    """Get queue status for a specific patient"""
    queue = QueueService.get_patient_queue(patient_id)
    if not queue:
        return jsonify({'message': 'No queue found'}), 404
    return jsonify(queue.to_dict())

@bp.route('/join', methods=['POST'])
@jwt_required()
def join_queue():
    """Join the queue"""
    data = request.get_json()
    patient_id = data.get('patient_id')
    doctor_id = data.get('doctor_id')
    priority = data.get('priority', False)
    appointment_id = data.get('appointment_id')

    queue = QueueService.join_queue(patient_id, doctor_id, priority, appointment_id)
    return jsonify(queue.to_dict()), 201

@bp.route('/call-next', methods=['POST'])
@jwt_required()
def call_next_patient():
    """Call next patient in queue"""
    data = request.get_json()
    doctor_id = data.get('doctor_id')
    
    next_patient = QueueService.call_next_patient(doctor_id)
    if not next_patient:
        return jsonify({'message': 'No patients in queue'}), 404

    return jsonify(next_patient.to_dict())

@bp.route('/finish/<int:queue_id>', methods=['POST'])
@jwt_required()
def finish_diagnosis(queue_id):
    """Finish diagnosis and remove from queue"""
    QueueService.finish_diagnosis(queue_id)
    return jsonify({'message': 'Diagnosis finished'})

@bp.route('/statistics/<int:doctor_id>', methods=['GET'])
@jwt_required()
def get_queue_statistics(doctor_id):
    """Get queue statistics for a doctor"""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    if not start_date or not end_date:
        return jsonify({'message': 'Start date and end date are required'}), 400

    statistics = QueueService.get_queue_statistics(doctor_id, start_date, end_date)
    return jsonify(statistics) 