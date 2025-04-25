from app import db
from models.base import BaseModel

class Queue(BaseModel):
    __tablename__ = 'queues'

    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    queue_number = db.Column(db.Integer, nullable=False)
    priority = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='waiting')
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=True)
    waiting_time = db.Column(db.Integer, default=0)  # in minutes

    # Relationships
    patient = db.relationship('Patient', backref='queues')
    doctor = db.relationship('Doctor', backref='queues')
    appointment = db.relationship('Appointment', backref='queues')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.patient.name if self.patient else None,
            'age': self.patient.age if self.patient else None,
            'gender': self.patient.gender if self.patient else None,
            'symptom': self.appointment.symptoms if self.appointment else None,
            'waitingTime': self.waiting_time,
            'examResult': self.appointment.exam_result if self.appointment else None,
            'status': self.status,
            'queueNumber': self.queue_number,
            'priority': self.priority,
            'patientId': self.patient_id,
            'doctorId': self.doctor_id,
            'appointmentId': self.appointment_id,
            'createdAt': self.created_at.isoformat() if self.created_at else None,
            'updatedAt': self.updated_at.isoformat() if self.updated_at else None
        } 