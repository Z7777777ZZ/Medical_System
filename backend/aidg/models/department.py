from extensions import db

# 科室模型
class Department(db.Model):
    __tablename__ = 'departments'
    department_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    hospital_id = db.Column(db.BigInteger, db.ForeignKey('hospitals.hospital_id'), nullable=False)

    def to_dict(self):
        return {
            'department_id': self.department_id,
            'name': self.name,
            'hospital_id': self.hospital_id
        }