from datetime import datetime
from extensions import db

class Doctors(db.Model):
    __tablename__ = 'doctors'

    doctor_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    hospital_id = db.Column(db.BigInteger, db.ForeignKey('hospitals.hospital_id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    department_id = db.Column(db.BigInteger, db.ForeignKey('departments.department_id', onupdate='CASCADE', ondelete='RESTRICT'), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(1024), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<doctors {self.name}>'
    
    @property
    def basic_info(self):
        """返回基础信息的字典格式"""
        return {
            "doctor_id": self.doctor_id,
            "name": self.name,
            "hospital": self.hospital.name if self.hospital else "",
            "department": self.department.name if self.department else "",
            "specialty": self.specialty,
            "bio": self.bio
        }
    
class Hospitals(db.Model):
    __tablename__ = 'hospitals'

    hospital_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<hospitals {self.name}>'
    
class Departments(db.Model):
    __tablename__ = 'departments'
    department_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    hospital_id = db.Column(db.BigInteger, db.ForeignKey('hospitals.hospital_id'))

    def __repr__(self):
        return f'<departments {self.name}>'