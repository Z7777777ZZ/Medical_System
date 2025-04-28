# 医疗系统后端

## 项目结构

```
backend/
├── api/                    # API路由
│   ├── __init__.py
│   ├── auth.py            # 认证路由
│   ├── queue.py           # 队列管理路由
│   └── prescription.py    # 处方管理路由
├── models/                # 数据库模型
│   ├── __init__.py
│   ├── base.py           # 基础模型（包含通用字段）
│   ├── queue.py          # 队列模型
│   └── prescription.py   # 处方模型
├── call_number/          # 叫号系统模块
│   ├── api/              # 队列管理API路由
│   │   ├── __init__.py
│   │   └── queue.py      # 队列API
│   ├── models/           # 队列模型
│   │   └── queue.py      # 队列模型
│   └── services/         # 队列服务
│       └── queue_service.py  # 队列服务实现
├── diagnosis/            # 诊断与处方模块
│   ├── api/              # 诊断API路由
│   │   ├── __init__.py
│   │   └── prescription.py # 处方API
│   ├── models/           # 诊断模型
│   │   └── prescription.py # 处方模型
│   └── services/         # 诊断服务
│       └── prescription_service.py # 处方服务实现
├── config.py             # 配置设置
├── app.py               # 应用程序工厂
├── requirements.txt     # Python依赖项
├── schema.sql          # 数据库架构
└── API_DOCUMENTATION.md # API文档
```

## 安装设置

1. 安装依赖:
```bash
pip install -r requirements.txt
```

2. 设置环境变量:

修改config.py文件中的数据库连接信息和其他配置参数。

```python
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:password@localhost/medical_system'
```

3. 初始化数据库:
```bash
mysql -u 用户名 -p < schema.sql
```

1. 运行应用程序:
```bash
python app.py
```

## API文档

应用程序运行时，可通过`loclhost:5000/docs`端点访问Swagger UI获取API文档。

## API概览

### 叫号系统 API

- `POST /api/call-number/queue/register` - 注册患者进入队列
- `GET /api/call-number/queue/status/<patient_id>` - 获取患者队列状态
- `GET /api/call-number/queue/clinic/<clinic_id>` - 获取诊室信息
- `GET /api/call-number/queue/current` - 获取当前叫号患者
- `GET /api/call-number/queue/list` - 获取当前队列列表
- `POST /api/call-number/queue/refresh/<patient_id>` - 刷新患者队列状态

### 处方系统 API

- `GET /api/diagnosis/prescription/medicines` - 获取所有药品列表
- `GET /api/diagnosis/prescription/medicines/<medicine_id>` - 获取药品详情
- `POST /api/diagnosis/prescription` - 创建新处方
- `GET /api/diagnosis/prescription?patientId=<patient_id>` - 获取患者的所有处方
- `GET /api/diagnosis/prescription/<prescription_id>` - 获取处方详情
- `PUT /api/diagnosis/prescription/<prescription_id>` - 更新处方信息

## 开发指南

1. **代码风格**
   - 遵循PEP 8指南
   - 适当使用类型提示
   - 为所有公共函数和类添加文档

2. **数据库变更**
   - 所有数据库变更应记录在schema.sql中
   - 使用迁移进行数据库架构变更
   - 部署前测试迁移

3. **API开发**
   - 遵循RESTful原则
   - 使用适当的HTTP方法
   - 包含适当的错误处理
   - 记录所有端点

4. **测试**
   - 为所有新功能编写单元测试
   - 使用Postman或类似工具测试API端点
   - 测试数据库操作

## 贡献

1. 为您的功能创建新分支
2. 进行更改
3. 编写测试
4. 更新文档
5. 提交拉取请求

## 许可证

本项目采用MIT许可证。