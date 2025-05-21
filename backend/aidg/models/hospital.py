from extensions import db

# 医院模型
class Hospital(db.Model):
    __tablename__ = 'hospitals'
    hospital_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'hospital_id': self.hospital_id,
            'name': self.name,
            'address': self.address
        }