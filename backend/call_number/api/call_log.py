from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.call_log import CallLog
from . import bp

@bp.route('/doctor/<int:doctor_id>', methods=['GET'])
@jwt_required()
def get_doctor_call_logs(doctor_id):
    """Get call logs for a specific doctor"""
    logs = CallLog.query.filter_by(doctor_id=doctor_id).order_by(CallLog.call_time.desc()).all()
    return jsonify([log.to_dict() for log in logs])

@bp.route('/queue/<int:queue_id>', methods=['GET'])
@jwt_required()
def get_queue_call_logs(queue_id):
    """Get call logs for a specific queue"""
    logs = CallLog.query.filter_by(queue_id=queue_id).order_by(CallLog.call_time.desc()).all()
    return jsonify([log.to_dict() for log in logs])

@bp.route('/update/<int:log_id>', methods=['PUT'])
@jwt_required()
def update_call_log(log_id):
    """Update a call log"""
    log = CallLog.query.get_or_404(log_id)
    data = request.get_json()

    if 'status' in data:
        log.status = data['status']
    if 'notes' in data:
        log.notes = data['notes']

    log.save()
    return jsonify(log.to_dict()) 