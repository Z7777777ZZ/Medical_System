from flask import Blueprint, request
from backend.extensions import db
from backend.user_service.models.doctor import Hospitals
from backend.user_service.utils import ApiResponse

bp = Blueprint('hospital_api', __name__, url_prefix='/hospitals')

@bp.route('', methods=['GET'])
def get_hospitals():
    print(1)
    hospitals = Hospitals.query.all()
    hospital_list = [{
        "id": hospital.hospital_id,
        "name": hospital.name,
    } for hospital in hospitals]
    return ApiResponse.success(data=hospital_list)