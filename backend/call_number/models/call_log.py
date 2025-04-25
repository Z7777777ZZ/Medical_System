from app import db
from models.base import BaseModel

class CallLog(BaseModel):
    __tablename__ = 'call_logs'

    queue_id = db.Column(db.Integer, db.ForeignKey('queues.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    call_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='success')  # success, failed, cancelled

    # Relationships
    queue = db.relationship('Queue', backref='call_logs')
    doctor = db.relationship('Doctor', backref='call_logs')

    def to_dict(self):
        return {
            'id': self.id,
            'queueId': self.queue_id,
            'doctorId': self.doctor_id,
            'callTime': self.call_time.isoformat() if self.call_time else None,
            'status': self.status,
            'patientName': self.queue.patient.name if self.queue and self.queue.patient else None,
            'queueNumber': self.queue.queue_number if self.queue else None,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        } 