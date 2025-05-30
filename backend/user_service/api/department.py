from flask import Blueprint, request, jsonify
from extensions import db
from user_service.models.doctor import Departments
from user_service.utils import ApiResponse
from flask_restx import Namespace, Resource, fields


# 创建Namespace
api = Namespace('department', description='科室相关操作')

# 定义Swagger文档模型
department_model = api.model('Department', {
    'id': fields.Integer(description='科室ID'),
    'name': fields.String(description='科室名称'),
    'hospital_id': fields.Integer(description='所属医院ID')
})

@api.route('')
class DepartmentList(Resource):
    @api.doc('get_all_departments')
    @api.marshal_list_with(department_model)
    def get(self):
        """获取所有科室"""
        departments = Departments.query.all()
        department_list = [{
            "id": department.department_id,
            "name": department.name,
            "hospital_id": department.hospital_id
        } for department in departments]
        return department_list

# @api.route('/<int:hospital_id>')
# class HospitalDepartments(Resource):
#     @api.doc('get_departments_by_hospital')
#     @api.marshal_list_with(department_model)
#     def get(self, hospital_id):
#         """获取指定医院的科室列表"""
#         departments = Departments.query.filter_by(hospital_id=hospital_id).all()
#         department_list = [{
#             "id": department.department_id,
#             "name": department.name,
#             "hospital_id": department.hospital_id
#         } for department in departments]
#         return department_list