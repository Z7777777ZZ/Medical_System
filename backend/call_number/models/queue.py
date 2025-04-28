from datetime import datetime
from app import db

class Queue(db.Model):
    __tablename__ = 'queues'
    
    queue_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'), nullable=False)
    queue_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('waiting', 'called'), nullable=False, default='waiting')
    priority = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.queue_id,
            'patientId': self.patient_id,
            'doctorId': self.doctor_id,
            'queueNumber': self.queue_number,
            'status': self.status,
            'priority': self.priority,
            'createdAt': self.created_at.isoformat() if self.created_at else None
        }
