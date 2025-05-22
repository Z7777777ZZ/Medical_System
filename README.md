# 医疗系统

一个综合性的医疗管理平台，包含患者、医生、病历、支付和预约管理功能。

## 项目结构

开发手册是大组开发组给出的，第二小组详细架构设计-更新.md文档包括概述、功能模块、技术栈、项目结构、数据库额外设计、子系统API设计、额外导入的库、页面跳转逻辑等内容。

项目代码结构如下：

```
medical-system/
├── backend/
│   ├── app.py                    # Flask 主程序  
│   ├── config.py                 # 配置文件
│   ├── extensions.py             # 扩展配置(SQLAlchemy, JWT等)
│   ├── requirements.txt          # Python 依赖
│   ├── aidg/
│   │   ├── __init__.py
│   │   ├── models/
│   │   │   ├── department.py      # 科室模型
│   │   │   ├── doctor.py        # 医生模型扩展
│   │   │   ├── hospital.py      # 医院模型
│   │   │   ├── patient.py      # 患者模型
│   │   │   └── review.py       # 医生评论模型
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── ai_diagnosis.py   # AI问诊API
│   │   │   ├── department.py     # 获取所有科室API
│   │   │   ├── doctors.py        # 医生查询API
│   │   │   ├── hospitals.py      # 获取所有医院API
│   │   │   ├── reviews.py        # 医生评论查询与新增API
│   │   ├── services/
│   │   │   ├── ai_service.py     # AI服务封装
│   │   │   └── doctor_rating_service.py  # 医生评分更新服务
│   │   ├── database/
│   │   │   └── aidg.sql  # 相关表结构
│   │   └── utils/
│   │       └── /
│   └── /
└──  frontend/ms_frontend/
    ├── src/
    │   ├── app.vue  # 主组件文件
    │   ├── main.js  # 主程序入口
    │   ├── components/
    │   │   └── DoctorDetailDialog.vue     # 医生详情会话框组件
    │   ├── views/
    │   │   ├── AIDiagnosisView.vue  # AI问诊页面
    │   │   └── DoctorSearchView.vue # 医生搜索页面
    │   ├── store/
    │   │   └── /
    │   └── assets/
    │       ├── aidg-icons/     # 相关图标图片
    │       └── aidg-css/          # 相关css文件
    └── package.json             # 前端依赖
```

## 功能特性

- **智慧问诊系统**

  - **AI症状分析**：基于用户输入的症状进行初步诊断分析
  - **医生推荐**：根据症状分析结果推荐合适的专科医生

  **医生查找系统**

  - **医生筛选**：支持按名字、科室、医院、专长等多维度筛选
  - **医生详情**：展示医生详细信息，包括医院、科室、评分、评价等

## 技术栈

### 后端
- Python 3.9
- Flask (Web 框架)
- SQLAlchemy (ORM)

### 前端
- Vue.js
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
   安装其他所需依赖项
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

### 医院 API

- `GET /api/hospitals` - 获取所有医院信息

### 科室 API

- `GET /api/departments` - 获取所有科室信息（已去重）

### 医生 API

- `GET /api/doctors/search` - 搜索医生（支持按关键词、医院、科室筛选，并按评分或评价数量排序）
- `GET /api/doctors/<int:doctor_id>` - 通过 ID 获取医生详细信息
- `GET /api/doctors/<int:doctor_id>/rating` - 获取指定医生的平均评分和评价数量

### 评价 API

- `GET /api/doctors/<int:doctor_id>/reviews` - 获取指定医生的所有评价列表
- `POST /api/reviews` - 添加新的医生评价

### AI 智能诊断 API

- `POST /api/aidiagnosis` - 提交症状描述进行智能分析，并获取可能的疾病、建议、紧急程度及推荐医生

## 开发

该项目遵循模块化架构，便于维护和扩展：

- 后端 API 分组为独立模块
- 前端使用基于组件的结构以提高可重用性
- 处理跨域 API 访问的 CORS 配置
