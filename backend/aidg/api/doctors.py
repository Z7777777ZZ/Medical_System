from flask import Blueprint, jsonify, request
from extensions import db
from aidg.models.doctor import Doctor
from aidg.models.hospital import Hospital
from aidg.models.department import Department
from aidg.models.review import DoctorReview

doctors_bp = Blueprint('doctors_bp', __name__, url_prefix='/api/doctors')

@doctors_bp.route('/search', methods=['GET'])
def search_doctors_route():
    search_term = request.args.get('query', '').strip().lower()
    # hospital_id = request.args.get('hospital_id', type=int)
    hospital_name = request.args.get('hospital')
    department_name = request.args.get('department')
    sort_by = request.args.get('sort_by', 'default')  # 新增排序参数: rating, review_count
    print(hospital_name, department_name)
    
    # if not search_term:
    #     doctors = Doctor.query.all()
    #     return jsonify([doctor.to_dict() for doctor in doctors])
    #     # return jsonify({"error": "查询参数不能为空"}), 400

    # query = Doctor.query.join(Hospital).join(Department)
    query = Doctor.query.join(Hospital).join(Department, Doctor.department_id == Department.department_id)
    # print(query)

    # 添加筛选条件
    if hospital_name:
        query = query.filter(Hospital.name == hospital_name)
    
    if department_name:
        query = query.filter(Department.name == department_name)
    
    # print(query)

    # 关键词搜索
    if search_term:
        query = query.filter(
            db.or_(
                Doctor.name.ilike(f'%{search_term}%'),
                Hospital.name.ilike(f'%{search_term}%'),
                Department.name.ilike(f'%{search_term}%'),
                Doctor.specialty.ilike(f'%{search_term}%')
            )
        )

    # 添加排序逻辑
    if sort_by == 'rating':
        query = query.order_by(Doctor.average_rating.desc())
    elif sort_by == 'review_count':
        query = query.order_by(Doctor.review_count.desc())
    else:
        query = query.order_by(Doctor.doctor_id.asc())

    doctors = query.all()
    # return jsonify([doctor.to_dict() for doctor in doctors])
    return jsonify([{
        'doctor_id': doctor.doctor_id,
        'name': doctor.name,
        'phone': doctor.phone,
        'hospital': doctor.hospital.name if doctor.hospital else None,
        'department': doctor.department.name if doctor.department else None,
        'specialty': doctor.specialty,
        'bio': doctor.bio,
        'average_rating': float(doctor.average_rating) if doctor.average_rating else 0,
        'review_count': doctor.review_count if doctor.review_count else 0
    } for doctor in doctors])

@doctors_bp.route('/<int:doctor_id>', methods=['GET'])
def get_doctor_route(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    # return jsonify(doctor.to_dict())
    return jsonify({
        'doctor_id': doctor.doctor_id,
        'name': doctor.name,
        'phone': doctor.phone,
        'hospital': doctor.hospital.name if doctor.hospital else None,
        'department': doctor.department.name if doctor.department else None,
        'specialty': doctor.specialty,
        'bio': doctor.bio,
        'average_rating': float(doctor.average_rating) if doctor.average_rating else 0,
        'review_count': doctor.review_count if doctor.review_count else 0
    })

@doctors_bp.route('/<int:doctor_id>/rating', methods=['GET'])
def get_doctor_rating_route(doctor_id):
    avg_rating = db.session.query(
        db.func.avg(DoctorReview.rating).label('average')
    ).filter(DoctorReview.doctor_id == doctor_id).scalar()
    
    review_count = DoctorReview.query.filter_by(doctor_id=doctor_id).count()
    
    return jsonify({
        'doctor_id': doctor_id,
        'average_rating': float(avg_rating) if avg_rating else 0,
        'review_count': review_count
    })