from flask import Blueprint, request, jsonify
from ..services.doctor_service import search_doctors

doctor_find_bp = Blueprint('doctor_find', __name__)

@doctor_find_bp.route('/search', methods=['GET'])
def search_doctors_api():
    search_term = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    
    doctors, total = search_doctors(search_term, page, page_size)
    
    return jsonify({
        "status": "success",
        "data": {
            "total": total,
            "doctors": doctors
        }
    })