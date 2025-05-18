#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, request, jsonify
from datetime import datetime
import json
import pymysql
import logging
import os
import uuid
import hashlib
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 创建蓝图
api = Blueprint('api', __name__)

# 数据库连接函数
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='zsj031128',
        db='medical_system',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

# 日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 错误处理
def handle_error(e):
    logger.error(f"API错误: {str(e)}")
    return jsonify({
        'status': 'error',
        'message': str(e)
    }), 500

# ==================== 用户反馈接口 ====================

@api.route('/feedbacks', methods=['POST'])
def create_feedback():
    try:
        data = request.json
        
        # 验证必填字段
        required_fields = ['patient_id', 'rating', 'service_rating', 'interface_rating', 
                         'function_rating', 'performance_rating', 'content']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'缺少必填字段: {field}'}), 400
        
        # 插入数据库
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO feedbacks 
                (rating, service_rating, interface_rating, function_rating, performance_rating, 
                 content, contact, images)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                images_json = json.dumps(data.get('images', [])) if data.get('images') else None
                cursor.execute(sql, (
                    data['rating'],
                    data['service_rating'],
                    data['interface_rating'],
                    data['function_rating'],
                    data['performance_rating'],
                    data['content'],
                    data.get('contact'),
                    images_json
                ))
                feedback_id = cursor.lastrowid
            
            # 记录用户行为
            record_user_activity(
                data['patient_id'],
                'feedback',
                '提交了系统反馈',
                {'feedback_id': feedback_id}
            )
            
            conn.commit()
            return jsonify({
                'status': 'success',
                'message': '反馈提交成功',
                'data': {'id': feedback_id}
            })
        finally:
            conn.close()
    except Exception as e:
        return handle_error(e)

@api.route('/treatment-feedbacks', methods=['POST'])
def create_treatment_feedback():
    try:
        data = request.json
        
        # 验证必填字段
        required_fields = ['patient_id', 'appointment_id', 'treatment_rating', 
                         'doctor_rating', 'hospital_rating', 'waiting_rating', 'content']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'缺少必填字段: {field}'}), 400
        
        # 插入数据库
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO treatment_feedbacks 
                (patient_id, appointment_id, treatment_rating, doctor_rating, 
                 hospital_rating, waiting_rating, content)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    data['patient_id'],
                    data['appointment_id'],
                    data['treatment_rating'],
                    data['doctor_rating'],
                    data['hospital_rating'],
                    data['waiting_rating'],
                    data['content']
                ))
                feedback_id = cursor.lastrowid
            
            # 记录用户行为
            record_user_activity(
                data['patient_id'],
                'feedback',
                '提交了就诊体验反馈',
                {'feedback_id': feedback_id, 'appointment_id': data['appointment_id']}
            )
            
            conn.commit()
            return jsonify({
                'status': 'success',
                'message': '反馈提交成功',
                'data': {'id': feedback_id}
            })
        finally:
            conn.close()
    except Exception as e:
        return handle_error(e)

@api.route('/recovery-feedbacks', methods=['POST'])
def create_recovery_feedback():
    try:
        data = request.json
        
        # 验证必填字段
        required_fields = ['patient_id', 'medical_record_id', 'recovery_status', 
                         'symptom_description', 'medication_adherence']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'缺少必填字段: {field}'}), 400
        
        # 插入数据库
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO recovery_feedbacks 
                (patient_id, medical_record_id, recovery_status, symptom_description, 
                 medication_adherence, side_effects, content)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(sql, (
                    data['patient_id'],
                    data['medical_record_id'],
                    data['recovery_status'],
                    data['symptom_description'],
                    data['medication_adherence'],
                    data.get('side_effects'),
                    data.get('content')
                ))
                feedback_id = cursor.lastrowid
            
            # 记录用户行为
            record_user_activity(
                data['patient_id'],
                'feedback',
                '提交了康复情况反馈',
                {'feedback_id': feedback_id, 'medical_record_id': data['medical_record_id']}
            )
            
            conn.commit()
            return jsonify({
                'status': 'success',
                'message': '反馈提交成功',
                'data': {'id': feedback_id}
            })
        finally:
            conn.close()
    except Exception as e:
        return handle_error(e)

# ==================== 消息通知接口 ====================

@api.route('/notifications/<int:patient_id>', methods=['GET'])
def get_notifications(patient_id):
    try:
        limit = int(request.args.get('limit', 20))
        offset = int(request.args.get('offset', 0))
        notification_type = request.args.get('type')
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # 查询条件构建
                conditions = ["patient_id = %s"]
                params = [patient_id]
                
                if notification_type and notification_type != 'all':
                    conditions.append("type = %s")
                    params.append(notification_type)
                
                # 查询通知
                sql = f"""
                SELECT * FROM notifications 
                WHERE {' AND '.join(conditions)}
                ORDER BY scheduled_time DESC
                LIMIT %s OFFSET %s
                """
                params.extend([limit, offset])
                cursor.execute(sql, params)
                notifications = cursor.fetchall()
                
                # 查询未读数量
                sql = """
                SELECT COUNT(*) as unread_count FROM notifications 
                WHERE patient_id = %s AND status != 'read'
                """
                cursor.execute(sql, (patient_id,))
                unread_count = cursor.fetchone()['unread_count']
                
                # 记录用户行为
                record_user_activity(
                    patient_id,
                    'view_record',
                    '查看了消息列表',
                    None
                )
                
                return jsonify({
                    'status': 'success',
                    'data': {
                        'notifications': notifications,
                        'unread_count': unread_count
                    }
                })
        finally:
            conn.close()
    except Exception as e:
        return handle_error(e)

@api.route('/notifications/<int:notification_id>/read', methods=['POST'])
def mark_notification_read(notification_id):
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # 更新通知状态
                sql = """
                UPDATE notifications 
                SET status = 'read', read_time = %s
                WHERE id = %s AND status != 'read'
                """
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                cursor.execute(sql, (now, notification_id))
                
                # 获取通知信息
                sql = "SELECT patient_id FROM notifications WHERE id = %s"
                cursor.execute(sql, (notification_id,))
                notification = cursor.fetchone()
                
                if notification:
                    # 记录用户行为
                    record_user_activity(
                        notification['patient_id'],
                        'view_record',
                        '阅读了一条消息',
                        {'notification_id': notification_id}
                    )
            
            conn.commit()
            return jsonify({
                'status': 'success',
                'message': '已标记为已读'
            })
        finally:
            conn.close()
    except Exception as e:
        return handle_error(e)

@api.route('/notifications/settings/<int:patient_id>', methods=['GET', 'POST'])
def notification_settings(patient_id):
    try:
        conn = get_db_connection()
        try:
            if request.method == 'GET':
                with conn.cursor() as cursor:
                    # 查询通知设置
                    sql = """
                    SELECT * FROM notification_settings
                    WHERE patient_id = %s
                    """
                    cursor.execute(sql, (patient_id,))
                    settings = cursor.fetchone()
                    
                    # 如果没有设置，返回默认设置
                    if not settings:
                        settings = {
                            'patient_id': patient_id,
                            'app_enabled': 1,
                            'sms_enabled': 1,
                            'email_enabled': 1
                        }
                    
                    return jsonify({
                        'status': 'success',
                        'data': settings
                    })
            else:  # POST
                data = request.json
                
                with conn.cursor() as cursor:
                    # 检查是否已存在设置
                    sql = """
                    SELECT id FROM notification_settings
                    WHERE patient_id = %s
                    """
                    cursor.execute(sql, (patient_id,))
                    existing = cursor.fetchone()
                    
                    if existing:
                        # 更新设置
                        sql = """
                        UPDATE notification_settings 
                        SET app_enabled = %s, sms_enabled = %s, email_enabled = %s
                        WHERE patient_id = %s
                        """
                        cursor.execute(sql, (
                            data.get('app_enabled', 1),
                            data.get('sms_enabled', 1),
                            data.get('email_enabled', 1),
                            patient_id
                        ))
                    else:
                        # 创建设置
                        sql = """
                        INSERT INTO notification_settings 
                        (patient_id, app_enabled, sms_enabled, email_enabled)
                        VALUES (%s, %s, %s, %s)
                        """
                        cursor.execute(sql, (
                            patient_id,
                            data.get('app_enabled', 1),
                            data.get('sms_enabled', 1),
                            data.get('email_enabled', 1)
                        ))
                
                conn.commit()
                return jsonify({
                    'status': 'success',
                    'message': '设置已保存'
                })
        finally:
            conn.close()
    except Exception as e:
        return handle_error(e)

# ==================== 用户引导接口 ====================

@api.route('/guides/progress/<int:patient_id>', methods=['GET'])
def get_guide_progress(patient_id):
    try:
        guide_key = request.args.get('guide_key')
        if not guide_key:
            return jsonify({'status': 'error', 'message': '缺少guide_key参数'}), 400
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # 查询引导进度
                sql = """
                SELECT * FROM guide_progress
                WHERE patient_id = %s AND guide_key = %s
                """
                cursor.execute(sql, (patient_id, guide_key))
                progress = cursor.fetchone()
                
                # 如果没有进度记录，返回默认值
                if not progress:
                    progress = {
                        'patient_id': patient_id,
                        'guide_key': guide_key,
                        'current_step': 0,
                        'is_completed': 0
                    }
                
                return jsonify({
                    'status': 'success',
                    'data': progress
                })
        finally:
            conn.close()
    except Exception as e:
        return handle_error(e)

@api.route('/guides/progress', methods=['POST'])
def update_guide_progress():
    try:
        data = request.json
        
        # 验证必填字段
        required_fields = ['patient_id', 'guide_key', 'current_step']
        for field in required_fields:
            if field not in data:
                return jsonify({'status': 'error', 'message': f'缺少必填字段: {field}'}), 400
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # 检查是否已存在进度
                sql = """
                SELECT id FROM guide_progress
                WHERE patient_id = %s AND guide_key = %s
                """
                cursor.execute(sql, (data['patient_id'], data['guide_key']))
                existing = cursor.fetchone()
                
                if existing:
                    # 更新进度
                    sql = """
                    UPDATE guide_progress 
                    SET current_step = %s, is_completed = %s
                    WHERE patient_id = %s AND guide_key = %s
                    """
                    cursor.execute(sql, (
                        data['current_step'],
                        data.get('is_completed', 0),
                        data['patient_id'],
                        data['guide_key']
                    ))
                else:
                    # 创建进度记录
                    sql = """
                    INSERT INTO guide_progress 
                    (patient_id, guide_key, current_step, is_completed)
                    VALUES (%s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        data['patient_id'],
                        data['guide_key'],
                        data['current_step'],
                        data.get('is_completed', 0)
                    ))
            
            conn.commit()
            return jsonify({
                'status': 'success',
                'message': '进度已更新'
            })
        finally:
            conn.close()
    except Exception as e:
        return handle_error(e)

# ==================== 用户行为时间轴接口 ====================

@api.route('/activities/<int:patient_id>', methods=['GET'])
def get_activities(patient_id):
    try:
        limit = int(request.args.get('limit', 20))
        offset = int(request.args.get('offset', 0))
        activity_type = request.args.get('type')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        sort_order = request.args.get('sort', 'desc')
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                # 查询条件构建
                conditions = ["patient_id = %s"]
                params = [patient_id]
                
                if activity_type and activity_type != 'all':
                    conditions.append("activity_type = %s")
                    params.append(activity_type)
                
                if start_date:
                    conditions.append("created_at >= %s")
                    params.append(f"{start_date} 00:00:00")
                
                if end_date:
                    conditions.append("created_at <= %s")
                    params.append(f"{end_date} 23:59:59")
                
                # 确定排序方式
                order_by = "created_at DESC" if sort_order.lower() == 'desc' else "created_at ASC"
                
                # 查询活动列表
                sql = f"""
                SELECT * FROM user_activities 
                WHERE {' AND '.join(conditions)}
                ORDER BY {order_by}
                LIMIT %s OFFSET %s
                """
                params.extend([limit, offset])
                cursor.execute(sql, params)
                activities = cursor.fetchall()
                
                # 查询总数
                sql = f"""
                SELECT COUNT(*) as total FROM user_activities 
                WHERE {' AND '.join(conditions)}
                """
                cursor.execute(sql, params[:-2])  # 去掉limit和offset参数
                total = cursor.fetchone()['total']
                
                # 记录用户行为
                record_user_activity(
                    patient_id,
                    'view_record',
                    '查看了行为时间轴',
                    None
                )
                
                return jsonify({
                    'status': 'success',
                    'data': {
                        'activities': activities,
                        'total': total
                    }
                })
        finally:
            conn.close()
    except Exception as e:
        return handle_error(e)

# ==================== 健康贴士接口 ====================

@api.route('/health-tips', methods=['GET'])
def get_health_tips():
    try:
        limit = int(request.args.get('limit', 10))
        random_order = request.args.get('random', 'false').lower() == 'true'
        
        try:
            conn = get_db_connection()
            try:
                with conn.cursor() as cursor:
                    # 构建查询SQL
                    order_by = "RAND()" if random_order else "publish_date DESC"
                    
                    sql = f"""
                    SELECT * FROM health_tips 
                    WHERE is_active = 1
                    ORDER BY {order_by}
                    LIMIT %s
                    """
                    cursor.execute(sql, (limit,))
                    tips = cursor.fetchall()
                    
                    if tips and len(tips) > 0:
                        return jsonify({
                            'status': 'success',
                            'data': tips
                        })
                    else:
                        # 如果数据库中没有数据，使用模拟数据
                        logger.info("数据库中没有健康贴士数据，使用模拟数据")
                        mock_tips = generate_mock_health_tips(limit)
                        return jsonify({
                            'status': 'success',
                            'message': '使用模拟数据',
                            'data': mock_tips
                        })
            finally:
                conn.close()
        except Exception as db_error:
            logger.error(f"数据库连接失败，使用模拟数据: {str(db_error)}")
            # 如果数据库连接失败，返回模拟数据
            mock_tips = generate_mock_health_tips(limit)
            return jsonify({
                'status': 'success',
                'message': '使用模拟数据',
                'data': mock_tips
            })
    except Exception as e:
        return handle_error(e)

# 生成模拟健康贴士数据
def generate_mock_health_tips(limit=10):
    mock_tips = [
        {
            'id': 1,
            'title': '保持充足睡眠的重要性',
            'content': '研究表明，成年人每晚应保持7-8小时的睡眠时间，良好的睡眠有助于提高免疫力，降低心脏病和抑郁症风险。',
            'source': '中国睡眠研究会',
            'publish_date': '2023-10-15',
            'is_active': 1
        },
        {
            'id': 2,
            'title': '饮食均衡与健康',
            'content': '每天摄入足够的蔬菜、水果和全谷物，限制高糖、高盐和加工食品的摄入，有助于维持健康体重和预防慢性疾病。',
            'source': '中国营养学会',
            'publish_date': '2023-10-20',
            'is_active': 1
        },
        {
            'id': 3,
            'title': '适度运动的益处',
            'content': '每周至少进行150分钟中等强度有氧运动，如快走、游泳或骑自行车，可以显著降低患心脏病、糖尿病和某些癌症的风险。',
            'source': '世界卫生组织',
            'publish_date': '2023-10-25',
            'is_active': 1
        },
        {
            'id': 4,
            'title': '减轻压力的方法',
            'content': '长期压力可能导致多种健康问题。尝试通过冥想、深呼吸练习或瑜伽等方式来减轻压力，保持心理健康。',
            'source': '中国心理卫生协会',
            'publish_date': '2023-11-01',
            'is_active': 1
        },
        {
            'id': 5,
            'title': '合理用眼保护视力',
            'content': '长时间使用电子设备可能导致视力问题。请记住20-20-20法则：每20分钟，看20英尺外的物体20秒钟，以减轻眼睛疲劳。',
            'source': '中国医师协会眼科医师分会',
            'publish_date': '2023-11-05',
            'is_active': 1
        },
        {
            'id': 6,
            'title': '预防感冒的小技巧',
            'content': '勤洗手、保持社交距离、避免触摸面部是预防感冒和流感的简单有效方法。确保接种流感疫苗也是保护自己的重要措施。',
            'source': '中国疾病预防控制中心',
            'publish_date': '2023-11-10',
            'is_active': 1
        },
        {
            'id': 7,
            'title': '控制血压的健康生活方式',
            'content': '减少盐分摄入、规律运动、限制酒精摄入、戒烟、保持健康体重都是控制血压的有效方法。高血压患者应定期监测血压。',
            'source': '中国高血压联盟',
            'publish_date': '2023-11-15',
            'is_active': 1
        },
        {
            'id': 8,
            'title': '保护关节健康',
            'content': '保持健康体重、进行低冲击运动、避免过度使用关节、加强肌肉力量训练都有助于保护关节健康，预防关节炎。',
            'source': '中国康复医学会',
            'publish_date': '2023-11-20',
            'is_active': 1
        },
        {
            'id': 9,
            'title': '健康饮水习惯',
            'content': '每天饮用足够的水对维持身体正常功能至关重要。成年人应每天饮用约2升水，根据活动量和气候适当调整。',
            'source': '中国营养学会',
            'publish_date': '2023-11-25',
            'is_active': 1
        },
        {
            'id': 10,
            'title': '预防腰背痛的正确姿势',
            'content': '保持良好的坐姿和站姿、避免长时间保持同一姿势、正确搬抬重物、加强核心肌群训练都有助于预防腰背痛。',
            'source': '中国康复医学会',
            'publish_date': '2023-12-01',
            'is_active': 1
        }
    ]
    
    # 如果要求随机排序
    if random.random() > 0.5:
        random.shuffle(mock_tips)
    
    # 返回指定数量的贴士
    return mock_tips[:min(limit, len(mock_tips))]

@api.route('/health-tips/<int:tip_id>', methods=['GET'])
def get_health_tip(tip_id):
    try:
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                SELECT * FROM health_tips 
                WHERE id = %s AND is_active = 1
                """
                cursor.execute(sql, (tip_id,))
                tip = cursor.fetchone()
                
                if not tip:
                    return jsonify({'status': 'error', 'message': '未找到健康贴士'}), 404
                
                return jsonify({
                    'status': 'success',
                    'data': tip
                })
        finally:
            conn.close()
    except Exception as e:
        return handle_error(e)

# ==================== 文件上传接口 ====================

@api.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'status': 'error', 'message': '未找到上传文件'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'status': 'error', 'message': '未选择文件'}), 400
        
        # 验证文件类型
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if '.' not in file.filename or \
           file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({'status': 'error', 'message': '不支持的文件类型'}), 400
        
        # 创建保存目录
        upload_folder = os.path.join(os.getcwd(), 'uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        # 生成文件名并保存文件
        filename = f"{uuid.uuid4().hex}.{file.filename.rsplit('.', 1)[1].lower()}"
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        
        # 返回文件URL
        file_url = f"/uploads/{filename}"
        return jsonify({
            'status': 'success',
            'data': {
                'url': file_url
            }
        })
    except Exception as e:
        return handle_error(e)

# ==================== 工具函数 ====================

def record_user_activity(patient_id, activity_type, description, metadata=None):
    """
    记录用户活动
    """
    try:
        # 获取客户端信息
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')
        
        conn = get_db_connection()
        try:
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO user_activities 
                (patient_id, activity_type, description, metadata, ip_address, user_agent)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                metadata_json = json.dumps(metadata) if metadata else None
                cursor.execute(sql, (
                    patient_id,
                    activity_type,
                    description,
                    metadata_json,
                    ip_address,
                    user_agent
                ))
            conn.commit()
        finally:
            conn.close()
    except Exception as e:
        logger.error(f"记录用户活动失败: {str(e)}") 