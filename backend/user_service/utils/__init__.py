class ApiResponse:
    @staticmethod
    def success(data=None, message="操作成功", status_code=200):
        return {
            "status": "success",
            "message": message,
            "data": data
        }, status_code

    @staticmethod
    def error(message="发生错误", status_code=400, data=None):
        return {
            "status": "error",
            "message": message,
            "data": data
        }, status_code