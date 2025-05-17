"""
缴费管理相关模型
"""
from backend.service.utils.extensions import db
from datetime import datetime
from decimal import Decimal


class Payment(db.Model):
    """支付表模型"""
    __tablename__ = 'payments'
    
    payment_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey('patients.patient_id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Enum('pending', 'paid'), nullable=False, default='pending')
    transaction_id = db.Column(db.String(100))
    payment_method = db.Column(db.String(50))
    payment_time = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    
    # 关联关系
    patient = db.relationship('Patient', backref='payments')
    details = db.relationship('PaymentDetail', backref='payment')
    
    def to_dict(self):
        """转换为字典"""
        return {
            'payment_id': self.payment_id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.name if self.patient else None,
            'amount': float(self.amount) if self.amount else 0.0,
            'type': self.type,
            'status': self.status,
            'transaction_id': self.transaction_id,
            'payment_method': self.payment_method,
            'payment_time': self.payment_time.strftime('%Y-%m-%d %H:%M:%S') if self.payment_time else None,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'details': [detail.to_dict() for detail in self.details]
        }


class PaymentDetail(db.Model):
    """缴费详情表模型"""
    __tablename__ = 'payment_details'
    
    detail_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    payment_id = db.Column(db.BigInteger, db.ForeignKey('payments.payment_id'), nullable=False)
    fee_type = db.Column(db.Enum('registration_fee', 'consultation_fee', 'medicine_fee', 'examination_fee'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(255))
    
    def to_dict(self):
        """转换为字典"""
        return {
            'detail_id': self.detail_id,
            'payment_id': self.payment_id,
            'fee_type': self.fee_type,
            'amount': float(self.amount) if self.amount else 0.0,
            'description': self.description
        } 