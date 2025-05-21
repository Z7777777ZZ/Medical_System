from extensions import db
from aidg.models.patient import Patient
from aidg.models.doctor import Doctor

class DoctorReview(db.Model):
    __tablename__ = 'doctor_reviews'
    review_id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey('patients.patient_id'), nullable=False)
    doctor_id = db.Column(db.BigInteger, db.ForeignKey('doctors.doctor_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5星
    comment = db.Column(db.Text)
    review_date = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    # 定义关系
    patient = db.relationship('Patient', backref='reviews')
    doctor = db.relationship('Doctor', backref='reviews')

    def to_dict(self):
        return {
            'review_id': self.review_id,
            # 'patient_id': self.patient_id,
            'patient_name': self.patient.name if self.patient else None,
            # 'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name if self.doctor else None,
            'rating': self.rating,
            'comment': self.comment,
            'review_date': self.review_date.strftime('%Y-%m-%d %H:%M:%S')
        }