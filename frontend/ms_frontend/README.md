# 医疗系统前端项目

## 项目简介
这是一个基于 Vue 3 + Vite + Element Plus 的医疗系统前端项目。

## 环境要求
- Node.js: ^20.17.0 或 >=22.9.0
- npm: ^10.8.0

## 技术栈
- Vue 3
- Vite
- Element Plus
- Vue Router
- Axios

## 安装步骤

1. 确保已安装正确版本的 Node.js
   ```bash
   node -v  # 应显示 v20.17.0 或更高版本
   ```

2. 安装项目依赖
   ```bash
   npm install
   ```

3. 如果遇到权限问题，请执行：
   ```bash
   chmod -R 755 node_modules
   ```

## 开发运行

1. 启动开发服务器
   ```bash
   npm run dev
   ```

2. 构建生产版本
   ```bash
   npm run build
   ```

3. 预览生产构建
   ```bash
   npm run preview
   ```

## 项目结构
```
ms_frontend/
├── src/            # 源代码目录
├── public/         # 静态资源目录
├── node_modules/   # 依赖包目录
├── index.html      # 入口 HTML 文件
├── vite.config.js  # Vite 配置文件
└── package.json    # 项目配置文件
```

## 常见问题解决

1. 如果遇到权限问题：
   ```bash
   chmod -R 755 node_modules
   ```

2. 如果依赖安装失败：
   ```bash
   npm cache clean --force
   npm install
   ```

3. 如果端口被占用，可以在 vite.config.js 中修改端口配置

## 开发规范
- 使用 Vue 3 组合式 API
- 遵循 Element Plus 的设计规范
- 使用 ESLint 进行代码规范检查

## 注意事项
- 确保 Node.js 版本符合要求
- 开发时注意跨域配置
- 提交代码前进行代码格式化

# 门诊系统前端

## 项目概述
这是一个门诊系统的前端项目，包含患者端和医生端两个子系统，用于实现医院门诊的排队、叫号、处方管理等功能。

## 项目安装与运行

### 安装依赖
```
npm install
```

### 开发环境运行
```
npm run serve
```

### 生产环境构建
```
npm run build
```

### 代码格式检查
```
npm run lint
```

## 项目结构及文件功能说明

### 主要文件目录

```
frontend/
  ms_frontend/
    public/                   # 静态资源目录
    src/                      # 源代码目录
      assets/                 # 静态资源
        images/               # 图片资源
        styles/               # 样式资源
      components/             # 组件
        common/               # 公共组件
        doctor/               # 医生端组件
        patient/              # 患者端组件
      layouts/                # 布局组件
      router/                 # 路由配置
      stores/                 # 状态管理
      views/                  # 视图页面
        doctor/               # 医生端页面
        patient/              # 患者端页面
```

### 核心文件功能说明

#### 入口文件
- `src/main.js` - 应用程序入口文件，初始化Vue应用
- `src/App.vue` - 根组件，包含应用的最外层结构

#### 路由配置
- `src/router/index.js` - 定义了整个应用的路由系统，包括医生端和患者端的路由

#### 布局组件
- `src/layouts/DoctorLayout.vue` - 医生端布局，包含侧边栏菜单和整体页面结构
- `src/layouts/PatientLayout.vue` - 患者端布局，包含侧边栏菜单和整体页面结构

#### 状态管理
- `src/stores/queueStore.js` - 管理患者队列数据的状态存储
- `src/stores/prescriptionStore.js` - 管理处方数据的状态存储

#### 医生端视图
- `src/views/doctor/Dashboard.vue` - 医生工作台，显示当日工作概览
- `src/views/doctor/Queue.vue` - 患者队列管理，用于叫号和安排患者就诊
- `src/views/doctor/Prescription.vue` - 处方管理，用于开具和查看处方

#### 患者端视图
- `src/views/patient/Dashboard.vue` - 患者主页，显示个人信息和就医概览
- `src/views/patient/Queue.vue` - 排队信息，显示患者在队列中的位置和等待状态
- `src/views/patient/Prescription.vue` - 处方查询，用于查看历史处方信息

#### 组件
- `src/components/doctor/PrescriptionForm.vue` - 处方表单组件，用于医生开具处方

## 路由URL说明

### 医生端路由
- `/doctor/dashboard` - 医生工作台页面
- `/doctor/queue` - 医生端队列管理页面，默认首页
- `/doctor/prescription` - 医生端处方管理页面

### 患者端路由
- `/patient/dashboard` - 患者主页
- `/patient/queue` - 患者排队信息页面
- `/patient/prescription` - 患者处方查询页面

## 后端开发需要修改的静态数据位置

### queueStore.js
文件路径: `src/stores/queueStore.js`

包含以下静态数据，需替换为实际API调用：
- `normalQueue` - 普通患者等待队列数据
- `priorityQueue` - 检查后优先队列数据
- `actions` 中的模拟API调用
  - `fetchQueueData()` - 获取队列数据
  - `callNextPatient()` - 医生叫号接诊
  - `returnToQueueAfterExam()` - 患者检查完毕重新加入队列
  - `finishDiagnosis()` - 结束当前患者诊断

### prescriptionStore.js
文件路径: `src/stores/prescriptionStore.js`

假设包含以下静态数据，需替换为实际API调用：
- 处方列表数据
- 处方详情数据
- 处方创建、更新和查询等操作

### 患者队列页面
文件路径: `src/views/patient/Queue.vue`

包含以下静态数据：
- `myQueueInfo` - 当前患者的排队信息
- `currentCalling` - 当前叫号信息
- `clinicInfo` - 诊室信息
- `queueList` - 候诊队列列表
- `refreshStatus()` 方法中的模拟数据更新
- `submitRegister()` 方法中的模拟挂号处理

### 医生队列页面
文件路径: `src/views/doctor/Queue.vue`

包含患者队列管理相关的静态数据，需要替换为与后端API的实际交互。

### 处方相关页面
文件路径:
- `src/views/doctor/Prescription.vue`
- `src/views/patient/Prescription.vue`

包含处方管理和查询相关的静态数据，需要替换为与后端API的实际交互。

## API开发指南

后端需要实现的主要API功能包括：

1. **用户认证**
   - 用户登录
   - 获取当前用户信息

2. **队列管理**
   - 获取当前队列状态
   - 患者排队/挂号
   - 医生叫号
   - 患者检查管理
   - 结束诊断

3. **处方管理**
   - 创建处方
   - 获取处方列表
   - 查询处方详情
   - 更新处方状态

每个API端点应返回与前端静态数据结构匹配的JSON数据，以确保无缝集成。

## 注意事项

1. 本项目前端暂时使用静态数据模拟，不包含实时Socket通信功能，后续可根据需要添加
2. 所有页面间的导航使用Vue Router实现，通过点击相应按钮进行页面跳转
3. 开发后端API时请参考前端中的数据结构，保持字段名称和数据类型的一致性

