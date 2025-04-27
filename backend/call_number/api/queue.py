from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restx import Namespace, Resource, fields
from call_number.services.queue_service import QueueService

api = Namespace('queue', description='队列管理操作')

# 定义Swagger文档模型
patient_model = api.model('Patient', {
    'id': fields.Integer(description='患者ID'),
    'name': fields.String(required=True, description='患者姓名'),
    'age': fields.Integer(description='患者年龄'),
    'gender': fields.String(description='患者性别'),
    'symptom': fields.String(description='患者症状'),
    'waitingTime': fields.Integer(description='等待时间(分钟)'),
    'examResult': fields.String(description='检查结果'),
    'isCurrentUser': fields.Boolean(description='是否为当前用户')
})

queue_info_model = api.model('QueueInfo', {
    'queueNumber': fields.String(required=True, description='队列号码'),
    'ahead': fields.Integer(description='前面等待人数'),
    'estimatedWaitTime': fields.Integer(description='预计等待时间(分钟)'),
    'status': fields.String(description='队列状态(waiting/calling/exam/completed)'),
    'registerTime': fields.DateTime(description='挂号时间')
})

clinic_info_model = api.model('ClinicInfo', {
    'name': fields.String(required=True, description='诊所名称'),
    'location': fields.String(description='诊所位置'),
    'doctorName': fields.String(description='医生姓名'),
    'specialty': fields.String(description='医生专长'),
    'workingHours': fields.String(description='工作时间'),
    'notice': fields.String(description='诊所公告'),
    'mapX': fields.Integer(description='地图X坐标'),
    'mapY': fields.Integer(description='地图Y坐标'),
    'locationDirections': fields.String(description='位置指引')
})

@api.route('/register')
class RegisterPatient(Resource):
    @api.doc('register_patient', security='Bearer')
    @api.expect(api.model('RegisterForm', {
        'visitReason': fields.String(required=True, description='就诊原因'),
        'department': fields.String(required=True, description='科室')
    }))
    @api.marshal_with(queue_info_model, code=201)
    @api.response(400, '无效输入')
    @jwt_required()
    def post(self):
        """将新患者注册到队列中"""
        data = request.get_json()
        result = QueueService.register_patient(data)
        return result, 201

@api.route('/status/<int:patient_id>')
class GetQueueStatus(Resource):
    @api.doc('get_queue_status', security='Bearer')
    @api.marshal_with(queue_info_model)
    @api.response(404, '患者未找到')
    @jwt_required()
    def get(self, patient_id):
        """获取患者的队列状态"""
        status = QueueService.get_queue_status(patient_id)
        if not status:
            api.abort(404, '患者未找到')
        return status

@api.route('/clinic/<int:clinic_id>')
class GetClinicInfo(Resource):
    @api.doc('get_clinic_info', security='Bearer')
    @api.marshal_with(clinic_info_model)
    @api.response(404, '诊所未找到')
    @jwt_required()
    def get(self, clinic_id):
        """获取诊所信息"""
        info = QueueService.get_clinic_info(clinic_id)
        if not info:
            api.abort(404, '诊所未找到')
        return info

@api.route('/current')
class GetCurrentCalling(Resource):
    @api.doc('get_current_calling', security='Bearer')
    @api.marshal_with(patient_model)
    @jwt_required()
    def get(self):
        """获取当前叫号信息"""
        calling = QueueService.get_current_calling()
        return calling

@api.route('/list')
class GetQueueList(Resource):
    @api.doc('get_queue_list', security='Bearer')
    @api.marshal_list_with(patient_model)
    @jwt_required()
    def get(self):
        """获取当前队列列表"""
        queue_list = QueueService.get_queue_list()
        return queue_list

@api.route('/refresh/<int:patient_id>')
class RefreshQueueStatus(Resource):
    @api.doc('refresh_queue_status', security='Bearer')
    @api.marshal_with(queue_info_model)
    @api.response(404, '患者未找到')
    @jwt_required()
    def post(self, patient_id):
        """刷新患者的队列状态"""
        status = QueueService.refresh_queue_status(patient_id)
        if not status:
            api.abort(404, '患者未找到')
        return status
