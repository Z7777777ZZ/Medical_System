from extensions import db

class Patient(db.Model):
    __tablename__ = 'patients'
    patient_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    def to_dict(self): # 根据需要添加
        return {
            'patient_id': self.patient_id,
            'phone': self.phone,
            'email': self.email,
            'name': self.name,
        }