from flask import Blueprint, jsonify
from aidg.models.hospital import Hospital

hospitals_bp = Blueprint('hospitals_bp', __name__, url_prefix='/api/hospitals')

@hospitals_bp.route('', methods=['GET'])
def get_hospitals_route():
    # 从数据库中查询所有医院信息
    hospitals = Hospital.query.all()
    # 将医院信息转换为json格式，并返回
    # return jsonify([h.to_dict() for h in hospitals])
    return jsonify([{
        'hospital_id': h.hospital_id,
        'name': h.name,
        'address': h.address
    } for h in hospitals])