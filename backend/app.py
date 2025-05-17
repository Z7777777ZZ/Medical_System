"""
医疗系统后端主程序 - 集中式版本
"""
import sys
import os
sys.path.append('..')
from dotenv import load_dotenv

from backend.service.utils.extensions import init_app as init_extensions, db
from backend.service.models.record import Hospital
from backend.service.utils.init_db import init_db
from backend.service.api.patient_api import create_app

# 加载环境变量
load_dotenv()

# 获取配置环境
env = os.environ.get('FLASK_ENV', 'development')

def init_database(app, force_init=False):
    """初始化数据库并加载示例数据
    
    参数：
        app: Flask应用实例
        force_init: 是否强制重新初始化数据库
    """
    print("检查数据库是否需要初始化...")
    with app.app_context():
        # 创建所有表（如果不存在）
        db.create_all()
        
        # 当force_init=True或数据库为空时初始化数据
        if force_init:
            print("强制重新初始化数据库...")
            # 如果需要完全重置数据库，先删除所有表
            try:
                print("删除现有数据库表...")
                db.drop_all()
                print("重新创建数据库表...")
                db.create_all()
                
                # 重新初始化数据
                print("插入新的示例数据...")
                init_db()  # 插入示例数据
                print("数据库初始化完成！")
            except Exception as e:
                print(f"初始化数据时出错: {e}")
        elif Hospital.query.count() == 0:
            print("数据库为空，正在初始化示例数据...")
            try:
                init_db()  # 插入示例数据
                print("数据库初始化完成！")
            except Exception as e:
                print(f"初始化数据时出错: {e}")
        else:
            print("数据库已初始化，跳过初始化步骤。")

if __name__ == '__main__':
    print(f"Starting application in {env} environment")
    
    # 获取命令行参数
    port = 5000  # 默认端口
    force_init_db = False  # 是否强制初始化数据库
    
    # 解析命令行参数
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            if arg == '--init-db' or arg == '-i':
                force_init_db = True
                print("将强制重新初始化数据库")
            elif arg.isdigit():
                port = int(arg)
    
    # 创建应用
    app = create_app(env)
    
    # 初始化数据库（如果需要）
    init_database(app, force_init=force_init_db)
    
    # 启动应用
    print(f"Starting server on port {port}")
    app.run(debug=env=='development', host='0.0.0.0', port=port)