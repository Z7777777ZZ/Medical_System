from extensions import db
from aidg.models.doctor import Doctor
from aidg.models.review import DoctorReview

def update_single_doctor_rating(doctor_id):
    """更新单个医生的平均评分和评论数量"""
    # 计算新的平均评分
    avg_rating = db.session.query(
        db.func.avg(DoctorReview.rating).label('average')
    ).filter(DoctorReview.doctor_id == doctor_id).scalar()
    
    review_count = DoctorReview.query.filter_by(doctor_id=doctor_id).count()
    
    # 更新医生表的评分信息
    doctor = Doctor.query.get(doctor_id)
    if doctor:
        doctor.average_rating = float(avg_rating) if avg_rating else 0
        doctor.review_count = review_count
        db.session.commit()

def update_all_doctors_ratings_on_startup(app):
    """更新所有医生的平均评分和评论数量 (在应用上下文中执行)"""
    with app.app_context():
        doctors = Doctor.query.all()
        for doctor in doctors:
            # 计算平均评分
            avg_rating = db.session.query(
                db.func.avg(DoctorReview.rating)
            ).filter(DoctorReview.doctor_id == doctor.doctor_id).scalar()
            
            # 计算评论数量
            review_count = db.session.query(
                db.func.count(DoctorReview.review_id)
            ).filter(DoctorReview.doctor_id == doctor.doctor_id).scalar()
            
            # 更新医生记录
            doctor.average_rating = float(avg_rating) if avg_rating else 0
            doctor.review_count = review_count if review_count else 0
        
        db.session.commit()
        # print(f"已更新 {len(doctors)} 位医生的评分数据")
        app.logger.info(f"已更新 {len(doctors)} 位医生的评分数据") # 使用 app.logger