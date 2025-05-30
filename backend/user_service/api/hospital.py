from flask import Blueprint, request, jsonify
from extensions import db
from user_service.models.doctor import Hospitals
from user_service.utils import ApiResponse
from flask_restx import Namespace, Resource, fields


# 创建Namespace
api = Namespace('hospital', description='医院相关操作')

# 定义Swagger文档模型
hospital_model = api.model('Hospital', {
    'id': fields.Integer(description='医院ID'),
    'name': fields.String(description='医院名称'),
    'address': fields.String(description='医院地址'),
    'tel': fields.String(description='联系电话'),
    'level': fields.String(description='医院等级')
})

@api.route('')
class HospitalList(Resource):
    @api.doc('get_all_hospitals')
    @api.marshal_list_with(hospital_model)
    def get(self):
        """获取所有医院"""
        hospitals = Hospitals.query.all()
        hospital_list = [{
            "id": hospital.hospital_id,
            "name": hospital.name,
            "address": hospital.address if hasattr(hospital, 'address') else None,
            "tel": hospital.tel if hasattr(hospital, 'tel') else None,
            "level": hospital.level if hasattr(hospital, 'level') else None
        } for hospital in hospitals]
        return hospital_list

# @api.route('/<int:hospital_id>')
# class HospitalDetail(Resource):
#     @api.doc('get_hospital_detail')
#     @api.marshal_with(hospital_model)
#     def get(self, hospital_id):
#         """获取指定医院的详细信息"""
#         hospital = Hospitals.query.get_or_404(hospital_id)
#         return {
#             "id": hospital.hospital_id,
#             "name": hospital.name,
#             "address": hospital.address if hasattr(hospital, 'address') else None,
#             "tel": hospital.tel if hasattr(hospital, 'tel') else None,
#             "level": hospital.level if hasattr(hospital, 'level') else None
#         }
