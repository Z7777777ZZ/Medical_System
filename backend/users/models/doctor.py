from datetime import datetime, date
from app import db

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    doctor_id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.hospital_id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def calculate_age(self):
        """计算医生年龄"""
        if not hasattr(self, 'birthday') or not self.birthday:
            return None
        today = date.today()
        return today.year - self.birthday.year - ((today.month, today.day) < (self.birthday.month, self.birthday.day))
    
    def to_dict(self):
        return {
            'id': self.doctor_id,
            'name': self.name,
            'specialty': self.specialty,
            'phone': self.phone,
            'hospital_id': self.hospital_id,
            'department_id': self.department_id,
            'bio': self.bio,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }