from extensions import db
from aidg.models.hospital import Hospital
from aidg.models.department import Department

# 医生模型 SQLAlchemy 默认使用 ​​类名的小写蛇形命名（snake_case）​​ 作为表名
class Doctor(db.Model):
    __tablename__ = 'doctors' # 显式指定该模型对应的数据库表名为 doctors
    doctor_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    hospital_id = db.Column(db.BigInteger, db.ForeignKey('hospitals.hospital_id'), nullable=False)
    department_id = db.Column(db.BigInteger, db.ForeignKey('departments.department_id'), nullable=False)
    specialty = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    
    average_rating = db.Column(db.Float, default=0)  # 平均评分
    review_count = db.Column(db.Integer, default=0)   # 评价数量

    # 定义关系
    hospital = db.relationship('Hospital', backref='doctors')
    department = db.relationship('Department', backref='doctors')

    def to_dict(self):
        return {
            'doctor_id': self.doctor_id,
            'phone': self.phone,
            'name': self.name,
            # 'hospital_id': self.hospital_id,
            'hospital': self.hospital.name if self.hospital else None,
            # 'department_id': self.department_id,
            'department': self.department.name if self.department else None,
            'specialty': self.specialty,
            'bio': self.bio,
            # 'password_hash': self.password_hash,
            # 'created_at': self.created_at,
            'average_rating': self.average_rating,
            'review_count': self.review_count
        }