from flask import jsonify, request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from users.models.patient import Patient
from users.models.patient_detail import PatientDetail
from call_number.models.queue import Queue
from call_number.services.queue_service import QueueService
import logging

# 创建命名空间
api = Namespace('patients', description='患者操作')

# 定义Swagger文档模型
queue_info_model = api.model('QueueInfo', {
    'queueNumber': fields.Integer(required=True, description='队列号码'),
    'ahead': fields.Integer(description='前面等待人数'),
    'estimatedWaitTime': fields.Integer(description='预计等待时间(分钟)'),
    'status': fields.String(description='队列状态(waiting/called)'),
    'createdAt': fields.String(description='创建时间')
})

register_model = api.model('RegisterForm', {
    'doctorId': fields.Integer(required=False, description='医生ID (可选)'),
    'visitReason': fields.String(required=True, description='就诊原因'),
    'department': fields.String(required=True, description='科室'),
    'priority': fields.Boolean(required=False, description='是否优先')
})

@api.route('/register')
class RegisterQueue(Resource):
    @jwt_required()    
    @api.doc('register_queue')
    @api.expect(register_model)
    @api.marshal_with(queue_info_model, code=201)
    @api.response(400, '无效输入')
    @api.response(404, '患者不存在或医生不存在或科室不存在')
    def post(self):
        """患者排队挂号"""
        data = request.get_json()
        
        # 获取当前用户ID
        patient_id = get_jwt_identity()
        
        # 验证必要的参数
        if 'visitReason' not in data or 'department' not in data:
            return {'error': '就诊原因和科室是必需的'}, 400
        doctor_id = data.pop('doctorId', None)  # 提取并移除医生ID，如果不存在则为None
        
        result = QueueService.register_patient(data, patient_id, doctor_id)
        
        # 处理错误情况：如果返回的是元组，说明包含错误状态码
        if isinstance(result, tuple) and len(result) == 2:
            return result  # 直接返回错误信息和状态码
        
        # 如果是正常结果，返回201状态码
        return result, 201

@api.route('/cancel_register/<int:queue_id>')
class CancelRegister(Resource):
    @jwt_required()
    @api.doc('cancel_register')
    @api.response(200, '取消挂号成功')
    @api.response(404, '未找到挂号记录')
    @api.response(403, '无权限取消此挂号')
    def delete(self, queue_id):
        """取消挂号"""
        # 获取当前用户ID
        patient_id = get_jwt_identity()
        
        try:
            # 查找对应的队列记录 - 使用正确的字段名
            queue = Queue.query.filter_by(queue_id=queue_id).first()
            
            if not queue:
                return {'error': '未找到挂号记录'}, 404
                
            # 验证是否是当前患者的挂号
            if queue.patient_id != patient_id:
                return {'error': '无权限取消此挂号'}, 403
                
            # 如果状态已经是called，则不能取消
            if queue.status == 'called':
                return {'error': '已经被叫号，不能取消'}, 400
                
            # 删除队列记录
            db.session.delete(queue)
            db.session.commit()
            return {'message': '挂号已成功取消'}, 200
        except Exception as e:
            db.session.rollback()
            logging.error(f"取消挂号时发生错误: {str(e)}")
            return {'error': f'取消挂号失败: {str(e)}'}, 500

@api.route('/queue_status')
class QueueStatus(Resource):
    @jwt_required()
    @api.doc('get_queue_status')
    @api.marshal_with(queue_info_model)
    @api.response(404, '未找到挂号记录')
    def get(self):
        """获取当前患者的排队状态"""
        # 获取当前用户ID
        patient_id = get_jwt_identity()
        
        status = QueueService.get_queue_status(patient_id)
        if not status:
            return {'error': '未找到挂号记录'}, 404
            
        return status
        
@api.route('/refresh_queue_status')
class RefreshQueueStatus(Resource):
    @jwt_required()
    @api.doc('refresh_queue_status')
    @api.marshal_with(queue_info_model)
    @api.response(404, '未找到挂号记录')
    def get(self):
        """刷新当前患者的排队状态"""
        # 获取当前用户ID
        patient_id = get_jwt_identity()
        
        status = QueueService.refresh_queue_status(patient_id)
        if not status:
            return {'error': '未找到挂号记录'}, 404
            
        return status