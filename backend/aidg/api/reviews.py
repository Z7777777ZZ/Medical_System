from flask import Blueprint, jsonify, request
from extensions import db
from aidg.models.review import DoctorReview
from aidg.models.patient import Patient
from aidg.services.doctor_rating_service import update_single_doctor_rating # 导入服务函数

reviews_bp = Blueprint('reviews_bp', __name__)

@reviews_bp.route('/api/doctors/<int:doctor_id>/reviews', methods=['GET'])
def get_doctor_reviews_route(doctor_id):
    reviews = DoctorReview.query.filter_by(doctor_id=doctor_id)\
        .join(Patient, DoctorReview.patient_id == Patient.patient_id)\
        .add_columns(Patient.name.label('patient_name'))\
        .order_by(DoctorReview.review_date.desc())\
        .all()
    
    return jsonify([{
        'review_id': review.DoctorReview.review_id,
        'patient_name': review.patient_name,
        'rating': review.DoctorReview.rating,
        'comment': review.DoctorReview.comment,
        'review_date': review.DoctorReview.review_date.strftime('%Y-%m-%d %H:%M:%S')
    } for review in reviews])

    # reviews = DoctorReview.query.filter_by(doctor_id=doctor_id).order_by(DoctorReview.review_date.desc()).all()
    # return jsonify([review.to_dict() for review in reviews])

@reviews_bp.route('/api/reviews', methods=['POST'])
def add_review_route():
    data = request.get_json()
    try:
        review = DoctorReview(
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id'],
            rating=data['rating'],
            comment=data.get('comment', '')
        )
        db.session.add(review)
        db.session.commit()

        # 更新医生平均评分
        update_single_doctor_rating(data['doctor_id']) # 使用服务函数

        return jsonify({"message": "评价添加成功"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400