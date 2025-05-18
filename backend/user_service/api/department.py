from flask import Blueprint, request
from backend.extensions import db
from backend.user_service.models.doctor import Departments
from backend.user_service.utils import ApiResponse

bp = Blueprint('department_api', __name__, url_prefix='/departments')

@bp.route('', methods=['GET'])
def get_departments():
    departments = Departments.query.all()
    department_list = [{
        "id": department.department_id,
        "name": department.name,
    } for department in departments]
    return ApiResponse.success(data=department_list)