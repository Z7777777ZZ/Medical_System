from datetime import datetime
from models.queue import Queue
from models.call_log import CallLog
from app import db

class QueueService:
    @staticmethod
    def get_doctor_queue(doctor_id):
        """Get all queues for a specific doctor"""
        return Queue.query.filter_by(doctor_id=doctor_id).order_by(Queue.queue_number).all()

    @staticmethod
    def get_patient_queue(patient_id):
        """Get queue status for a specific patient"""
        return Queue.query.filter_by(patient_id=patient_id).first()

    @staticmethod
    def join_queue(patient_id, doctor_id, priority=False, appointment_id=None):
        """Add a patient to the queue"""
        last_queue = Queue.query.filter_by(doctor_id=doctor_id).order_by(Queue.queue_number.desc()).first()
        queue_number = 1 if not last_queue else last_queue.queue_number + 1

        queue = Queue(
            patient_id=patient_id,
            doctor_id=doctor_id,
            queue_number=queue_number,
            priority=priority,
            appointment_id=appointment_id
        )
        queue.save()
        return queue

    @staticmethod
    def call_next_patient(doctor_id):
        """Call the next patient in queue"""
        # First try to get a priority patient
        next_patient = Queue.query.filter_by(
            doctor_id=doctor_id,
            status='waiting',
            priority=True
        ).order_by(Queue.queue_number).first()

        # If no priority patient, get the next normal patient
        if not next_patient:
            next_patient = Queue.query.filter_by(
                doctor_id=doctor_id,
                status='waiting',
                priority=False
            ).order_by(Queue.queue_number).first()

        if not next_patient:
            return None

        next_patient.status = 'called'
        next_patient.save()

        # Create call log
        call_log = CallLog(
            queue_id=next_patient.id,
            doctor_id=doctor_id,
            call_time=datetime.utcnow(),
            status='success'
        )
        call_log.save()

        return next_patient

    @staticmethod
    def finish_diagnosis(queue_id):
        """Finish diagnosis and remove from queue"""
        queue = Queue.query.get_or_404(queue_id)
        queue.delete()
        return True

    @staticmethod
    def get_queue_statistics(doctor_id, start_date, end_date):
        """Get queue statistics for a doctor"""
        queues = Queue.query.filter(
            Queue.doctor_id == doctor_id,
            Queue.created_at.between(start_date, end_date)
        ).all()

        total_patients = len(queues)
        priority_patients = sum(1 for q in queues if q.priority)
        average_wait_time = None  # TODO: Implement wait time calculation

        return {
            'total_patients': total_patients,
            'priority_patients': priority_patients,
            'average_wait_time': average_wait_time
        } 