from flask import Blueprint, request, jsonify
import pymysql
from werkzeug.exceptions import BadRequest

message_bp = Blueprint('messages', __name__)

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # 本地数据库密码
    'database': 'medical_system',
    'charset': 'utf8mb4'
}

def get_db_conn():
    return pymysql.connect(**DB_CONFIG)

@message_bp.route('/messages', methods=['GET'])
def get_messages():
    """获取消息列表(简略信息)"""
    conn = get_db_conn()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 查询简略信息
            sql = """
                SELECT id, title, publish_time
                FROM push_messages
                ORDER BY publish_time DESC
            """
            cursor.execute(sql)
            messages = cursor.fetchall()
            
        return jsonify({
            'success': True,
            'data': messages
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取消息列表失败: {str(e)}'
        }), 500
    finally:
        conn.close()

@message_bp.route('/messages/<int:message_id>', methods=['GET'])
def get_message_detail(message_id):
    """获取单条消息详情(全部内容)"""
    conn = get_db_conn()
    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = """
                SELECT id, title, content, publish_time
                FROM push_messages
                WHERE id = %s
            """
            cursor.execute(sql, (message_id,))
            message = cursor.fetchone()
            
            if not message:
                return jsonify({
                    'success': False,
                    'message': '消息不存在'
                }), 404
                
        return jsonify({
            'success': True,
            'data': message
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取消息详情失败: {str(e)}'
        }), 500
    finally:
        conn.close()

@message_bp.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    """删除单条消息"""
    conn = get_db_conn()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM push_messages WHERE id = %s"
            cursor.execute(sql, (message_id,))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({'success': False, 'message': '消息不存在'}), 404
        return jsonify({'success': True, 'message': '消息已删除'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': f'删除消息失败: {str(e)}'}), 500
    finally:
        conn.close()