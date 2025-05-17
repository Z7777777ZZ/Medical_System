from flask import Blueprint, request, jsonify
from datetime import datetime
import pymysql
import json

feedback_bp = Blueprint('feedbacks', __name__)

# 数据库连接配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '*****', # 本地数据库密码
    'database': 'medical_system',
    'charset': 'utf8mb4'
}

def get_db_conn():
    return pymysql.connect(**DB_CONFIG)

@feedback_bp.route('/feedbacks', methods=['POST'])
def submit_feedback():
    data = request.json
    conn = get_db_conn()
    try:
        with conn.cursor() as cursor:
            sql = """
                INSERT INTO feedbacks (
                    rating, service_rating, interface_rating, function_rating, performance_rating, content, contact, images, created_at, updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            category = data.get('categoryRatings', {})
            cursor.execute(sql, (
                data.get('rating'),
                category.get('service'),
                category.get('interface'),
                category.get('function'),
                category.get('performance'),
                data.get('content'),
                data.get('contact'),
                json.dumps(data.get('images', [])),
                now,
                now
            ))
            conn.commit()
        return jsonify({'success': True, 'msg': '反馈提交成功'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'msg': f'提交失败: {str(e)}'})
    finally:
        conn.close()

@feedback_bp.route('/feedbacks', methods=['GET'])
def get_feedbacks():
    conn = get_db_conn()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT id, rating, service_rating, interface_rating, function_rating, performance_rating, content, contact, images, created_at
                FROM feedbacks ORDER BY created_at DESC
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            feedbacks = []
            for row in rows:
                feedbacks.append({
                    'id': row[0],
                    'rating': row[1],
                    'categoryRatings': {
                        'service': row[2],
                        'interface': row[3],
                        'function': row[4],
                        'performance': row[5]
                    },
                    'content': row[6],
                    'contact': row[7],
                    'images': json.loads(row[8]) if row[8] else [],
                    'created_at': row[9]
                })
        return jsonify({'success': True, 'data': feedbacks})
    except Exception as e:
        return jsonify({'success': False, 'msg': f'获取失败: {str(e)}'})
    finally:
        conn.close()
