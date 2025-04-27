from datetime import datetime
from app import db
from call_number.models.queue import Queue
from flask import current_app
import random

class QueueService:
    @staticmethod
    def register_patient(data):
        """注册患者进入队列"""
        # 获取当前排队人数，生成队列号
        patient_id = 1  # 模拟获取当前用户ID，实际应从JWT获取
        doctor_id = 1  # 模拟分配医生，实际应根据科室分配
        
        # 生成队列号: 科室代码 + 日期 + 序号
        department_code = data.get('department', 'GEN')[:3].upper()
        date_code = datetime.now().strftime('%Y%m%d')
        sequence = random.randint(1, 100)  # 模拟序号，实际应从数据库获取
        queue_number = f"{department_code}{date_code}{sequence:03d}"
        
        # 创建队列记录
        queue = Queue(
            patient_id=patient_id,
            doctor_id=doctor_id,
            queue_number=queue_number,
            status='waiting',
            visit_reason=data.get('visitReason', ''),
            department=data.get('department', '')
        )
        
        db.session.add(queue)
        db.session.commit()
        
        # 返回队列信息
        return {
            'queueNumber': queue_number,
            'ahead': 5,  # 模拟前面等待人数
            'estimatedWaitTime': 25,  # 模拟等待时间，实际应计算
            'status': 'waiting',
            'registerTime': queue.register_time.isoformat()
        }
    
    @staticmethod
    def get_queue_status(patient_id):
        """获取患者的队列状态"""
        queue = Queue.query.filter_by(patient_id=patient_id, status='waiting').order_by(Queue.register_time.desc()).first()
        
        if not queue:
            return None
        
        # 计算前面等待人数
        ahead_count = Queue.query.filter(
            Queue.doctor_id == queue.doctor_id,
            Queue.register_time < queue.register_time,
            Queue.status == 'waiting'
        ).count()
        
        # 估算等待时间（每人约5分钟）
        estimated_wait_time = ahead_count * 5
        
        return {
            'queueNumber': queue.queue_number,
            'ahead': ahead_count,
            'estimatedWaitTime': estimated_wait_time,
            'status': queue.status,
            'registerTime': queue.register_time.isoformat()
        }
    
    @staticmethod
    def get_clinic_info(clinic_id):
        """获取诊所信息"""
        # 模拟诊所信息，实际应从数据库获取
        return {
            'name': f'诊室 {clinic_id}',
            'location': f'门诊楼 {clinic_id//10 + 1} 楼 {clinic_id % 10 + 1} 号诊室',
            'doctorName': '张医生',
            'specialty': '内科',
            'workingHours': '8:00-17:00',
            'notice': '请患者按顺序进入诊室',
            'mapX': 120 + clinic_id,
            'mapY': 85 + clinic_id,
            'locationDirections': '从大厅电梯出来右转直走200米'
        }
    
    @staticmethod
    def get_current_calling():
        """获取当前正在叫号的患者信息"""
        # 模拟当前叫号患者，实际应从数据库获取
        return {
            'id': 101,
            'name': '张三',
            'age': 45,
            'gender': '男',
            'symptom': '头痛、发热',
            'waitingTime': 15,
            'examResult': '体温38.5°C',
            'isCurrentUser': False
        }
    
    @staticmethod
    def get_queue_list():
        """获取当前队列列表"""
        # 模拟队列列表，实际应从数据库获取并根据医生ID筛选
        patients = []
        for i in range(1, 6):
            patients.append({
                'id': 100 + i,
                'name': f'患者{i}',
                'age': 20 + i * 5,
                'gender': '男' if i % 2 == 0 else '女',
                'symptom': '常见症状描述',
                'waitingTime': i * 10,
                'examResult': '' if i > 2 else '检查结果描述',
                'isCurrentUser': False
            })
        return patients
    
    @staticmethod
    def refresh_queue_status(patient_id):
        """刷新患者的队列状态"""
        return QueueService.get_queue_status(patient_id)
