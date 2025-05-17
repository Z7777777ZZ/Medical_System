"""
统一响应格式工具
"""
from flask import jsonify


def success_response(data=None, message="操作成功"):
    """成功响应
    
    Args:
        data: 响应数据
        message (str): 响应消息
        
    Returns:
        flask.Response: JSON响应
    """
    response = {
        "status": "success",
        "message": message,
        "data": data
    }
    return jsonify(response)


def error_response(message="操作失败", code=400):
    """错误响应
    
    Args:
        message (str): 错误消息
        code (int): HTTP状态码
        
    Returns:
        flask.Response: JSON响应
    """
    response = {
        "status": "error",
        "message": message,
        "data": None
    }
    return jsonify(response), code


def pagination_meta(page, per_page, total):
    """生成分页元数据
    
    Args:
        page (int): 当前页码
        per_page (int): 每页数量
        total (int): 总数据量
        
    Returns:
        dict: 分页元数据
    """
    return {
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": (total + per_page - 1) // per_page
    } 