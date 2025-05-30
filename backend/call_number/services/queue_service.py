from datetime import datetime
from app import db
from call_number.models.queue import Queue
from flask import current_app
import random

class QueueService:    
    @staticmethod
    def register_patient(data, patient_id, doctor_id=None):
        """
        注册患者进入队列
        :param data: 包含就诊信息的字典
        :param patient_id: 患者ID (必选)
        :param doctor_id: 医生ID (可选，如果未指定就分配)
        """
        from users.models.doctor import Doctor
        from users.models.patient import Patient
        
        # 验证患者是否存在
        patient = Patient.query.get(patient_id)
        if not patient:
            return {"error": "患者不存在"}, 404
            
        # 如果指定了医生，检查医生是否存在
        if doctor_id is not None:
            doctor = Doctor.query.get(doctor_id)
            if not doctor:
                return {"error": f"医生ID {doctor_id} 不存在"}, 404
        else:
            # 如果未指定医生，尝试根据科室分配医生
            department = data.get('department')
            if department:
                # 根据科室查询医生
                from sqlalchemy import text
                query = text("SELECT doctor_id FROM doctors WHERE department_id = (SELECT department_id FROM departments WHERE name = :dept LIMIT 1) LIMIT 1")
                result = db.session.execute(query, {"dept": department}).fetchone()
                
                if result:
                    doctor_id = result[0]
                else:
                    # 如果找不到对应科室的医生，随机选择一个存在的医生
                    doctor = Doctor.query.order_by(Doctor.doctor_id).first()
                    if doctor:
                        doctor_id = doctor.doctor_id
                    else:
                        return {"error": "未找到指定科室，且系统中没有可用的医生"}, 404
            else:
                # 如果没有指定科室，随机选择一个有效的医生ID
                doctor = Doctor.query.order_by(Doctor.doctor_id).first()
                if doctor:
                    doctor_id = doctor.doctor_id
                else:
                    return {"error": "系统中没有医生可分配"}, 404
        
        # 生成队列号: 科室代码 + 日期 + 序号
        department_code = data.get('department', 'GEN')[:3].upper()
        date_code = datetime.now().strftime('%Y%m%d')
        
        # 使用显式查询获取当天同科室的队列数量
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        queue_count = Queue.query.filter(
            Queue.doctor_id == doctor_id,
            Queue.created_at >= today_start
        ).count()
        
        # 生成序号，使用实际计数值
        sequence = queue_count + 1
        queue_number = sequence  # 使用整数队列号
        
        # 创建队列记录
        queue = Queue(
            patient_id=patient_id,
            doctor_id=doctor_id,
            queue_number=queue_number,
            status='waiting',
            priority=data.get('priority', False)
        )
        
        db.session.add(queue)
        db.session.commit()
        
        # 计算前面等待人数
        ahead_count = Queue.query.filter(
            Queue.doctor_id == queue.doctor_id,
            Queue.created_at < queue.created_at,
            Queue.status == 'waiting'
        ).count()
        
        # 估算等待时间（每人约5分钟）
        estimated_wait_time = ahead_count * 5
        
        # 返回队列信息
        return {
            'queueNumber': queue_number,
            'ahead': ahead_count,
            'estimatedWaitTime': estimated_wait_time,
            'status': 'waiting',
            'createdAt': queue.created_at.isoformat() if queue.created_at else None
        }
    
    @staticmethod
    def call_next_patient(doctor_id, patient_id=None):
        """
        医生叫号
        :param doctor_id: 医生ID
        :param patient_id: 指定叫号的患者ID (可选)
        :return: 被叫的患者信息
        """
        print(f"调用叫号函数: doctor_id={doctor_id}, patient_id={patient_id}")
        
        # 如果指定了患者ID，则叫指定患者
        if patient_id:
            queue = Queue.query.filter_by(
                doctor_id=doctor_id,
                patient_id=patient_id,
                status='waiting'
            ).first()
            
            if not queue:
                print(f"未找到指定患者 ID={patient_id} 在医生 ID={doctor_id} 的等待队列中")
                return {"error": "指定的患者不在等待队列中"}, 404
            print(f"找到指定患者: {queue.patient_id}")
        else:
            # 否则叫下一位排队的患者
            queue = Queue.query.filter_by(
                doctor_id=doctor_id,
                status='waiting'
            ).order_by(Queue.priority.desc(), Queue.created_at.asc()).first()
            
            if not queue:
                print(f"医生 ID={doctor_id} 没有等待的患者")
                return {"error": "没有等待的患者"}, 404
        
        # 将队列状态更新为"called"
        queue.status = 'called'
        db.session.commit()
        print(f"已更新队列状态为 'called': 患者ID={queue.patient_id}")
        
        # 获取患者信息
        from user_service.models.patient import Patients
        patient = Patients.query.get(queue.patient_id)
        
        if not patient:
            print(f"找不到患者信息: ID={queue.patient_id}")
            return {"error": "找不到患者信息"}, 404
        
        # 计算等待时间（分钟）
        waiting_time = 0
        if queue.created_at:
            from datetime import datetime  # 在需要的地方导入datetime
            delta = datetime.utcnow() - queue.created_at
            waiting_time = int(delta.total_seconds() / 60)
        
        # 尝试获取患者详细信息
        gender = None
        age = None
        try:
            # 尝试获取patient_details表中的性别信息
            if hasattr(patient, 'details') and patient.details:
                gender = patient.details.gender
                # 计算年龄
                if patient.details.date_of_birth:
                    from datetime import datetime
                    today = datetime.today()
                    born = patient.details.date_of_birth
                    age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        except Exception as e:
            print(f"获取患者详细信息时出错: {e}")
        
        return {
            'id': queue.patient_id,
            'name': patient.name,
            'gender': gender,
            'age': age,
            'queueNumber': queue.queue_number,
            'waitingTime': waiting_time,
            'priority': queue.priority,
            'status': queue.status,
            'visitReason': queue.visit_reason if hasattr(queue, 'visit_reason') else None,
            'medicalHistory': None  # 可以在未来添加病历获取逻辑
        }, 200
    
    @staticmethod
    def get_queue_status(patient_id):
        """获取患者的队列状态"""
        queue = Queue.query.filter_by(patient_id=patient_id, status='waiting').order_by(Queue.created_at.desc()).first()
        
        if not queue:
            return None
        
        # 计算前面等待人数
        ahead_count = Queue.query.filter(
            Queue.doctor_id == queue.doctor_id,
            Queue.created_at < queue.created_at,
            Queue.status == 'waiting'
        ).count()
        
        # 估算等待时间（每人约5分钟）
        estimated_wait_time = ahead_count * 5
        
        return {
            'queueNumber': queue.queue_number,
            'ahead': ahead_count,
            'estimatedWaitTime': estimated_wait_time,
            'status': queue.status,
            'registerTime': queue.created_at.isoformat()
        }
    
    @staticmethod
    def get_clinic_info(clinic_id):
        """获取诊室信息"""
        # 模拟诊室信息，实际应从数据库获取
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
    def get_current_calling(user_type=None, user_id=None):
        """获取当前正在叫号的患者信息
        
        Args:
            user_type (str, optional): 用户类型，'doctor' 或 'patient'
            user_id (int, optional): 用户ID
        """
        # 查询当前正在叫号的患者
        if user_type == 'patient':
            return {"error": "患者不能查看当前叫号信息"}, 403
        from users.models.patient import Patient  # 引入患者模型
        
        # 构建基本查询
        query = Queue.query.filter_by(status='calling')
        
        # 如果是医生类型且有用户ID，则添加医生ID过滤
        if user_type == 'doctor' and user_id:
            query = query.filter_by(doctor_id=user_id)
            
        # 获取排序后的第一条记录
        current_queue = query.order_by(Queue.created_at).first()
        if not current_queue:
            return None
            
        # 获取患者基本信息
        patient = Patient.query.get(current_queue.patient_id)
        if not patient:
            return None
            
        # 计算等待时间（分钟）
        waiting_time = 0
        if current_queue.created_at:
            import datetime
            delta = datetime.datetime.utcnow() - current_queue.created_at
            waiting_time = int(delta.total_seconds() / 60)
            
        # 获取可能的检查结果
        from diagnosis.models.medical_record import MedicalExam
        exam_result = MedicalExam.query.filter_by(patient_id=patient.id).order_by(MedicalExam.exam_time.desc()).first()
        
        is_current_user = False
        return {
            'id': patient.patient_id,
            'name': patient.name,
            'age': patient.calculate_age() if hasattr(patient, 'calculate_age') else None,
            'gender': None,  # 暂不获取性别信息，因为它在patient_details表中
            'symptom': current_queue.visit_reason if hasattr(current_queue, 'visit_reason') else None,
            'waitingTime': waiting_time,
            'examResult': exam_result.result if exam_result else '',
            'isCurrentUser': is_current_user
        }
    
    @staticmethod
    def get_queue_list(user_type=None, user_id=None):
        """获取当前队列列表
        
        Args:
            user_type (str, optional): 用户类型，'doctor' 或 'patient'
            user_id (int, optional): 用户ID
        """
        from users.models.patient import Patient  # 引入患者模型
        
        # 获取等待中的队列
        queues = Queue.query.filter_by(status='waiting').order_by(Queue.created_at).all()
        patients = []

        for queue in queues:
            # 获取患者基本信息
            patient = Patient.query.get(queue.patient_id)
            if not patient:
                continue
                
            # 计算等待时间（分钟）
            waiting_time = 0
            if queue.created_at:
                import datetime
                delta = datetime.datetime.utcnow() - queue.created_at
                waiting_time = int(delta.total_seconds() / 60)
                
            # 判断是否为当前用户
            is_current_user = False
                # 检查用户类型和 ID
            if user_type == 'patient':
                # 患者只能查看自己的排队信息
                is_current_user = str(user_id) == str(patient.patient_id)
                if not is_current_user:
                    continue  # 如果不是当前患者，跳过此记录
                
            elif user_type == 'doctor' and user_id:
                # 如果是医生类型，检查是否为当前医生的患者
                # print(f"当前医生ID: {user_id}, 队列医生ID: {queue.doctor_id}, 是否匹配: {int(queue.doctor_id) == int(user_id)}")
                if int(queue.doctor_id) != int(user_id):
                    continue  # 如果不是当前医生的患者，跳过此记录
                is_current_user = False  # 医生查看时不需要标记自己
                
            else:
                # 如果不是医生，不返回任何列表项
                continue

                # 添加患者信息到列表
            patients.append({
                'id': patient.patient_id,
                'name': patient.name,
                'age': patient.calculate_age() if hasattr(patient, 'calculate_age') else None,
                'gender': None,  # 暂不获取性别信息，因为它在patient_details表中
                'symptom': queue.visit_reason if hasattr(queue, 'visit_reason') else None,
                'waitingTime': waiting_time,
                'priority': queue.priority,
                'queueNumber': queue.queue_number,
                'status': queue.status,
                'examResult': '',  # 排队中的患者通常没有检查结果
                'isCurrentUser': is_current_user
            })
            
        print(f"获取到 {len(patients)} 个患者的排队信息")
        return patients
    
    @staticmethod
    def refresh_queue_status(patient_id):
        """刷新患者的队列状态"""
        return QueueService.get_queue_status(patient_id)

    # get_queue_stats
    @staticmethod
    def get_queue_stats(doctor_id=None):
        """获取队列统计信息：今日就诊患者数量和当前等待患者数量
        
        Args:
            doctor_id (int, optional): 医生ID，如果提供则仅获取该医生的统计信息
            
        Returns:
            dict: 包含 todayPatients 和 waitingPatients 的字典
        """
        try:
            from datetime import datetime, time
            
            # 获取今天的开始时间（00:00:00）
            today_start = datetime.combine(datetime.today(), time.min)
            
            # 基础查询条件
            base_conditions = [Queue.created_at >= today_start]
            waiting_conditions = [Queue.status == 'waiting']
            
            # 如果指定了医生ID，则添加筛选条件
            if doctor_id:
                base_conditions.append(Queue.doctor_id == doctor_id)
                waiting_conditions.append(Queue.doctor_id == doctor_id)
            
            # 查询今日就诊的患者数量（包括已经被叫号的和正在等待的患者）
            today_patients_count = Queue.query.filter(*base_conditions).count()
            
            # 查询当前等待中的患者数量
            waiting_patients_count = Queue.query.filter(*waiting_conditions).count()
            
            print(f"医生ID {doctor_id} 的统计信息: 今日患者 {today_patients_count}, 等待患者 {waiting_patients_count}")
            
            return {
                'todayPatients': today_patients_count,
                'waitingPatients': waiting_patients_count
            }
            
        except Exception as e:
            import logging
            logging.error(f"获取队列统计信息失败: {e}")
            # 返回默认值
            return {
                'todayPatients': 0,
                'waitingPatients': 0
            }

    @staticmethod
    def update_patient_priority(patient_id, doctor_id):
        """
        更新患者优先级状态
        将已经叫号的患者重新置为等待状态并设置优先级
        :param patient_id: 患者ID
        :param doctor_id: 医生ID
        :return: 更新后的患者队列信息
        """
        try:
            # 查找该医生已叫号的指定患者
            queue = Queue.query.filter_by(
                patient_id=patient_id,
                doctor_id=doctor_id,
                status='called'
            ).first()
            
            if not queue:
                return {"error": "未找到已叫号的指定患者"}, 404
            
            # 更新状态为等待，并设置优先级为True
            queue.status = 'waiting'
            queue.priority = True
            db.session.commit()
            
            
            return {
                'message': '患者已重新设置为优先等待状态'
            }, 200

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"更新患者优先级状态失败: {e}")
            return {"error": f"更新患者优先级状态失败: {str(e)}"}, 500