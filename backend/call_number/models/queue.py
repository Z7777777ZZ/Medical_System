from app import db
from models.base import Base
from datetime import datetime

class Queue(Base):
    """排队模型"""
    __tablename__ = 'queues'
    
    queue_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'), nullable=False)
    queue_number = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Enum('waiting', 'calling', 'exam', 'completed'), default='waiting')
    register_time = db.Column(db.DateTime, default=datetime.utcnow)
    visit_reason = db.Column(db.String(255))
    department = db.Column(db.String(100))
    priority = db.Column(db.Integer, default=0)  # 优先级，数字越大优先级越高
    
    # 关系
    patient = db.relationship('Patient', backref='queues')
    doctor = db.relationship('Doctor', backref='queues')
    
    def to_dict(self):
        """转换为API响应格式，使用驼峰命名"""
        return {
            'queueId': self.queue_id,
            'patientId': self.patient_id,
            'doctorId': self.doctor_id,
            'queueNumber': self.queue_number,
            'status': self.status,
            'registerTime': self.register_time.isoformat() if self.register_time else None,
            'visitReason': self.visit_reason,
            'department': self.department,
            'priority': self.priority
        }
