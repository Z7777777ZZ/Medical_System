from flask import jsonify, request
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
    'isCurrentUser': fields.Boolean(description='是否为当前用户'),
    'queueNumber': fields.Integer(description='队列号码'),
    'priority': fields.Boolean(description='是否优先'),
    'status': fields.String(description='状态')
})

queue_info_model = api.model('QueueInfo', {
    'queueNumber': fields.Integer(required=True, description='队列号码'),
    'ahead': fields.Integer(description='前面等待人数'),
    'estimatedWaitTime': fields.Integer(description='预计等待时间(分钟)'),
    'status': fields.String(description='队列状态(waiting/called)'),
    'createdAt': fields.String(description='创建时间')
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
    @api.doc('register_patient')
    @api.expect(api.model('RegisterForm', {
        'patientId': fields.Integer(required=True, description='患者ID'),
        'doctorId': fields.Integer(required=False, description='医生ID (可选)'),
        'visitReason': fields.String(required=True, description='就诊原因'),
        'department': fields.String(required=True, description='科室'),
        'priority': fields.Boolean(required=False, description='是否优先')
    }))
    @api.marshal_with(queue_info_model, code=201)
    @api.response(400, '无效输入')
    def post(self):
        """将新患者注册到队列中"""
        data = request.get_json()
        
        # 验证必要的参数
        if 'patientId' not in data:
            return {'error': '患者ID是必需的'}, 400
            
        patient_id = data.pop('patientId')  # 提取并移除，避免传给service时重复
        doctor_id = data.pop('doctorId', None)  # 提取并移除医生ID，如果不存在则为None
        
        result = QueueService.register_patient(data, patient_id, doctor_id)
        return result, 201

@api.route('/call')
class CallNextPatient(Resource):
    @api.doc('call_next_patient')
    @api.expect(api.model('CallForm', {
        'doctorId': fields.Integer(required=True, description='医生ID'),
        'patientId': fields.Integer(required=False, description='患者ID (可选，不指定则叫下一位)')
    }))
    @api.marshal_with(patient_model, code=200)
    @api.response(404, '没有等待的患者')
    def post(self):
        """医生叫号"""
        data = request.get_json()
        
        # 验证必要参数
        if 'doctorId' not in data:
            return {'error': '医生ID是必需的'}, 400
            
        doctor_id = data.get('doctorId')
        patient_id = data.get('patientId')  # 可能为None
        
        result, status_code = QueueService.call_next_patient(doctor_id, patient_id)
        return result, status_code

@api.route('/status/<int:patient_id>')
class GetQueueStatus(Resource):
    @api.doc('get_queue_status')
    @api.marshal_with(queue_info_model)
    @api.response(404, '患者未找到')
    def get(self, patient_id):
        """获取患者的队列状态"""
        status = QueueService.get_queue_status(patient_id)
        if not status:
            api.abort(404, '患者未找到')
        return status

@api.route('/clinic/<int:clinic_id>')
class GetClinicInfo(Resource):
    @api.doc('get_clinic_info')
    @api.marshal_with(clinic_info_model)
    @api.response(404, '诊所未找到')
    def get(self, clinic_id):
        """获取诊所信息"""
        info = QueueService.get_clinic_info(clinic_id)
        if not info:
            api.abort(404, '诊所未找到')
        return info

@api.route('/current')
class GetCurrentCalling(Resource):
    @api.doc('get_current_calling')
    @api.marshal_with(patient_model)
    def get(self):
        """获取当前叫号信息"""
        calling = QueueService.get_current_calling()
        return calling

@api.route('/list')
class GetQueueList(Resource):
    @api.doc('get_queue_list')
    @api.marshal_list_with(patient_model)
    def get(self):
        """获取当前队列列表"""
        queue_list = QueueService.get_queue_list()
        return queue_list

@api.route('/refresh/<int:patient_id>')
class RefreshQueueStatus(Resource):
    @api.doc('refresh_queue_status')
    @api.marshal_with(queue_info_model)
    @api.response(404, '患者未找到')
    def post(self, patient_id):
        """刷新患者的队列状态"""
        status = QueueService.refresh_queue_status(patient_id)
        if not status:
            api.abort(404, '患者未找到')
        return status
