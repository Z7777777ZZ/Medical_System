from flask import Blueprint, jsonify
from extensions import db
from aidg.models.department import Department

departments_bp = Blueprint('departments_bp', __name__, url_prefix='/api/departments')

@departments_bp.route('', methods=['GET'])
def get_departments_route():
    # 使用 distinct 对科室名称进行去重
    departments = db.session.query(
        Department.department_id,
        Department.name
    ).distinct(Department.name).all()
    # departments = Department.query.all()
    return jsonify([{
        'department_id': d.department_id,
        'name': d.name,
        # 'hospital_id': d.hospital_id
    } for d in departments])