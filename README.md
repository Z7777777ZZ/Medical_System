# 医疗系统

一个综合性的医疗管理平台，包含患者、医生、病历、支付和预约管理功能。

## 项目结构

```
Medical_System/
├── backend/                    # 后端服务器代码
│   ├── app.py                  # 主应用程序入口点
│   ├── __init__.py             # 包初始化
│   ├── requirements.txt        # Python 依赖项
│   └── service/                # 服务模块
│       ├── __init__.py         # 模块初始化
│       ├── api/                # API 端点
│       │   ├── __init__.py     # API 初始化
│       │   ├── patient_api.py  # API 定义
│       ├── models/             # 数据库模型
│       └── utils/              # 工具函数
└── frontend/                   # 前端应用
    └── ms_frontend/            # Vue.js 前端应用
        ├── public/             # 公共静态文件
        ├── src/                # 源代码
        │   ├── assets/         # 静态资源
        │   ├── components/     # 可重用组件
        │   ├── router/         # 路由定义
        │   ├── store/          # Pinia 状态管理
        │   └── views/          # 页面组件
        └── package.json        # 前端依赖项
```

## 功能特性

- **患者管理**：患者信息的存储和检索
- **医疗记录**：创建、查看和编辑患者的医疗记录
- **医生咨询**：医生-患者互动及记录更新
- **预约系统**：安排和管理患者预约
- **支付处理**：处理和跟踪医疗支付
- **药品处方**：管理和开具药品处方

## 技术栈

### 后端
- Python 3.x
- Flask (Web 框架)
- SQLAlchemy (ORM)
- SQLite (数据库，可配置为其他数据库)

### 前端
- Vue.js
- Pinia (状态管理)
- Vue Router
- Axios (HTTP 客户端)
- Element Plus (UI 组件库)

## 安装说明

### 后端设置

1. 切换到后端目录：
   ```
   cd backend
   ```

2. 安装依赖项：
   ```
   pip install -r requirements.txt
   ```

3. 初始化数据库并运行：
   ```
   python app.py --init-db
   ```

4. 运行服务器：
   ```
   python app.py
   ```
   服务器默认将在 http://localhost:5000 上运行。

### 前端设置

1. 切换到前端目录：
   ```
   cd frontend/ms_frontend
   ```

2. 安装依赖项：
   ```
   npm install
   ```

3. 运行开发服务器：
   ```
   npm run serve
   ```
   前端将在 http://localhost:8080 上可用。

## API 端点

后端 API 结构化为几个模块：

### 患者 API
- `GET /api/patients` - 获取所有患者
- `GET /api/patient/:id` - 通过 ID 获取患者

### 医疗记录 API
- `GET /api/patient/records/latest` - 获取患者最新记录
- `GET /api/patient/records/history` - 获取患者的记录历史
- `GET /api/patient/records/:id` - 获取特定记录详情
- `POST /api/patient/records` - 创建新的医疗记录
- `PUT /api/patient/records/update` - 更新医疗记录

### 挂号 API
- `GET /api/patient/registration/hospitals` - 获取医院列表
- `GET /api/patient/registration/departments` - 获取科室列表
- `GET /api/patient/registration/doctors` - 按科室获取医生
- `POST /api/patient/registration/appointments` - 创建预约
- `GET /api/patient/registration/appointments` - 获取患者预约

### 支付 API
- `GET /api/patient/payments/history` - 获取支付历史
- `POST /api/patient/payment/orders` - 创建支付订单
- `PUT /api/patient/payments/:id/complete` - 完成支付

### 药品 API
- `GET /api/patient/medicines` - 获取所有药品

## 开发

该项目遵循模块化架构，便于维护和扩展：

- 后端 API 按功能分组为独立模块
- 前端使用基于组件的结构以提高可重用性
- 实现身份验证和授权以保证安全性
- 处理跨域 API 访问的 CORS 配置
