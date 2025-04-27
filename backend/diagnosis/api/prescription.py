from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from diagnosis.services.prescription_service import PrescriptionService

api = Namespace('prescription', description='处方管理操作')

# 定义Swagger文档模型
medicine_model = api.model('Medicine', {
    'id': fields.Integer(description='药品ID'),
    'name': fields.String(required=True, description='药品名称'),
    'price': fields.Float(description='药品价格'),
    'description': fields.String(description='药品描述')
})

prescription_detail_model = api.model('PrescriptionDetail', {
    'id': fields.Integer(description='明细ID'),
    'medicineId': fields.Integer(required=True, description='药品ID'),
    'medicineName': fields.String(description='药品名称'),
    'dosage': fields.String(description='剂量'),
    'frequency': fields.String(description='频率'),
    'duration': fields.String(description='持续时间'),
    'instructions': fields.String(description='用药说明'),
    'price': fields.Float(description='药品价格')
})

prescription_model = api.model('Prescription', {
    'id': fields.Integer(description='处方ID'),
    'patientId': fields.Integer(required=True, description='患者ID'),
    'doctorId': fields.Integer(description='医生ID'),
    'patientName': fields.String(description='患者姓名'),
    'doctorName': fields.String(description='医生姓名'),
    'diagnosis': fields.String(description='诊断结果'),
    'createdAt': fields.DateTime(description='创建时间'),
    'status': fields.String(description='状态(draft/confirmed/dispensed)'),
    'medicines': fields.List(fields.Nested(prescription_detail_model), description='药品明细')
})

@api.route('/medicines')
class MedicineList(Resource):
    @api.doc('list_medicines', security='Bearer')
    @api.marshal_list_with(medicine_model)
    @jwt_required()
    def get(self):
        """获取所有可用药品列表"""
        medicines = PrescriptionService.get_medicines()
        return medicines

@api.route('/medicines/<int:medicine_id>')
class MedicineDetail(Resource):
    @api.doc('get_medicine', security='Bearer')
    @api.marshal_with(medicine_model)
    @api.response(404, '药品未找到')
    @jwt_required()
    def get(self, medicine_id):
        """获取药品详情"""
        medicine = PrescriptionService.get_medicine(medicine_id)
        if not medicine:
            api.abort(404, '药品未找到')
        return medicine

@api.route('')
class PrescriptionList(Resource):
    @api.doc('create_prescription', security='Bearer')
    @api.expect(prescription_model)
    @api.marshal_with(prescription_model, code=201)
    @api.response(400, '无效输入')
    @jwt_required()
    def post(self):
        """创建新处方"""
        data = request.get_json()
        result = PrescriptionService.create_prescription(data)
        if not result:
            api.abort(400, '创建处方失败')
        return result, 201
    
    @api.doc('list_prescriptions', security='Bearer')
    @api.marshal_list_with(prescription_model)
    @jwt_required()
    def get(self):
        """获取当前患者的所有处方"""
        patient_id = request.args.get('patientId', None)
        if not patient_id:
            api.abort(400, '缺少必要的患者ID参数')
        
        prescriptions = PrescriptionService.get_patient_prescriptions(patient_id)
        return prescriptions

@api.route('/<int:prescription_id>')
class PrescriptionDetail(Resource):
    @api.doc('get_prescription', security='Bearer')
    @api.marshal_with(prescription_model)
    @api.response(404, '处方未找到')
    @jwt_required()
    def get(self, prescription_id):
        """获取处方详情"""
        prescription = PrescriptionService.get_prescription(prescription_id)
        print('ok1')
        if not prescription:
            api.abort(404, '处方未找到')
        return prescription
    
    @api.doc('update_prescription', security='Bearer')
    @api.expect(prescription_model)
    @api.marshal_with(prescription_model)
    @api.response(404, '处方未找到')
    @jwt_required()
    def put(self, prescription_id):
        """更新处方信息"""
        data = request.get_json()
        result = PrescriptionService.update_prescription(prescription_id, data)
        if not result:
            api.abort(404, '处方未找到或更新失败')
        return result
