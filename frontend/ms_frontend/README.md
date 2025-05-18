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
