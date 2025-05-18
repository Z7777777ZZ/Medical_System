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
   cd frontend/ms_frontend
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

# 医疗系统后端项目

## 项目简介
这是一个基于 Flask 的医疗系统后端项目，提供 RESTful API 接口服务。

## 环境要求
- Python 3.8+
- MySQL 5.7+
- pip (Python 包管理器)

## 技术栈
- Flask: Web 框架
- SQLAlchemy: ORM 框架
- PyMySQL: MySQL 数据库驱动
- Flask-JWT-Extended: JWT 认证
- Flask-Migrate: 数据库迁移
- Flask-CORS: 跨域支持

## 安装步骤

1. 创建并激活虚拟环境（推荐）
   ```bash
   # 创建虚拟环境
   python -m venv venv
   
   # 在 Windows 上激活虚拟环境
   venv\Scripts\activate
   
   # 在 macOS/Linux 上激活虚拟环境
   source venv/bin/activate
   ```

2. 安装项目依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 配置数据库
   - 确保 MySQL 服务已启动
   - 创建数据库
   - 修改 `config.py` 中的数据库配置

4. 初始化数据库
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

## 开发运行

1. 启动开发服务器
   ```bash
   flask run
   ```
   或
   ```bash
   python -m backend.app
   ```

2. 默认情况下，服务器将在 http://localhost:5000 运行

## 项目结构
```
backend/
├── app.py              # 应用入口文件
├── config.py           # 配置文件
├── extensions.py       # Flask 扩展初始化
├── requirements.txt    # 项目依赖
├── migrations/         # 数据库迁移文件
└── user_service/       # 用户服务模块
```

## API 文档
主要 API 端点：
- 用户认证相关
  - POST /api/auth/login
  - POST /api/auth/register
  - GET /api/auth/profile

## 开发规范
- 遵循 PEP 8 编码规范
- 使用 Flask 蓝图组织路由
- 使用 SQLAlchemy 进行数据库操作
- 实现适当的错误处理和日志记录

## 数据库迁移
当修改了数据模型后，需要执行以下命令：
```bash
flask db migrate -m "描述变更内容"
flask db upgrade
```

## 注意事项
- 确保数据库配置正确
- 开发时注意跨域配置
- 生产环境部署时注意修改密钥
- 定期备份数据库

## 常见问题解决

1. 数据库连接问题
   - 检查 MySQL 服务是否运行
   - 验证数据库配置是否正确
   - 确保数据库用户有适当权限

2. 依赖安装问题
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. 端口占用问题
   - 可以在 `app.py` 中修改端口配置
   - 或使用 `flask run -p <端口号>`