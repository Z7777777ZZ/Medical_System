"""
挂号管理相关模型
"""
from backend.service.utils.extensions import db
from datetime import datetime


class Appointment(db.Model):
    """预约挂号模型"""
    __tablename__ = 'appointments'
    
    appointment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum('pending', 'confirmed', 'cancelled'), nullable=False, default='pending')
    
    # 关联关系
    patient = db.relationship('Patient', backref='appointments')
    doctor = db.relationship('Doctor', backref='appointments')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'appointment_id': self.appointment_id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.name if self.patient else None,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name if self.doctor else None,
            'department_name': self.doctor.department.name if self.doctor and self.doctor.department else None,
            'appointment_time': self.appointment_time.strftime('%Y-%m-%d %H:%M:%S') if self.appointment_time else None,
            'status': self.status
        }


class RegistrationStatus(db.Model):
    """挂号状态模型"""
    __tablename__ = 'registration_status'
    
    status_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.appointment_id'), nullable=False)
    status = db.Column(db.Enum('registered', 'paid', 'visiting', 'completed', 'cancelled'), nullable=False)
    status_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    notes = db.Column(db.Text)
    
    # 关联关系
    appointment = db.relationship('Appointment', backref='registration_statuses')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'status_id': self.status_id,
            'appointment_id': self.appointment_id,
            'status': self.status,
            'status_time': self.status_time.strftime('%Y-%m-%d %H:%M:%S') if self.status_time else None,
            'notes': self.notes
        }


class PatientVisitFlow(db.Model):
    """患者就诊流程模型"""
    __tablename__ = 'patient_visit_flows'
    
    flow_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.appointment_id'), nullable=False)
    registration_time = db.Column(db.DateTime)
    payment_time = db.Column(db.DateTime)
    visit_time = db.Column(db.DateTime)
    medical_record_id = db.Column(db.Integer, db.ForeignKey('medical_records.record_id'))
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.payment_id'))
    status = db.Column(db.Enum(
        'registered', 'payment_pending', 'payment_completed', 
        'in_consultation', 'consultation_completed', 
        'consultation_payment_pending', 'consultation_payment_completed', 
        'completed'
    ), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    
    # 关联关系
    patient = db.relationship('Patient', backref='visit_flows')
    appointment = db.relationship('Appointment', backref='visit_flow')
    medical_record = db.relationship('MedicalRecord', backref='visit_flow')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'flow_id': self.flow_id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.name if self.patient else None,
            'appointment_id': self.appointment_id,
            'registration_time': self.registration_time.strftime('%Y-%m-%d %H:%M:%S') if self.registration_time else None,
            'payment_time': self.payment_time.strftime('%Y-%m-%d %H:%M:%S') if self.payment_time else None,
            'visit_time': self.visit_time.strftime('%Y-%m-%d %H:%M:%S') if self.visit_time else None,
            'medical_record_id': self.medical_record_id,
            'payment_id': self.payment_id,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        }


class Queue(db.Model):
    """排队模型"""
    __tablename__ = 'queues'
    
    queue_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.doctor_id'), nullable=False)
    queue_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum('waiting', 'called'), nullable=False, default='waiting')
    
    # 关联关系
    patient = db.relationship('Patient', backref='queues')
    doctor = db.relationship('Doctor', backref='queues')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'queue_id': self.queue_id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.name if self.patient else None,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name if self.doctor else None,
            'queue_number': self.queue_number,
            'status': self.status
        } 