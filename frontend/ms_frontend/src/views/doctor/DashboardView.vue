<template>
  <div class="dashboard">
    <!-- 顶部导航栏 -->
    <div class="header">
      <div class="header-content">
        <div class="logo">
          <h1>医院管理系统</h1>
          <el-button type="text" @click="goToHome" class="home-button">
            <el-icon><HomeFilled /></el-icon>
            <span>首页</span>
          </el-button>
        </div>
        <div class="user-info">
          <el-dropdown>
            <span class="user-dropdown">
              <el-avatar :size="32" :src="userAvatar" />
              <span class="username">{{ username }}</span>
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="goToProfile">
                  <el-icon><User /></el-icon>个人信息
                </el-dropdown-item>
                <el-dropdown-item @click="handleLogout">
                  <el-icon><SwitchButton /></el-icon>退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="main-content">
      <router-view v-if="$route.path === '/doctor/dashboard/profile'" />
      <template v-else>
        <div class="welcome-section">
          <h2>医生工作台</h2>
          <p>欢迎使用医院管理系统，请选择您需要的功能</p>
        </div>

        <div class="function-grid">
          <el-card class="function-card" @click="goToCallManagement">
            <div class="card-content">
              <el-icon class="card-icon"><Bell /></el-icon>
              <h3>叫号管理</h3>
              <p>查看和管理患者叫号情况</p>
            </div>
          </el-card>

          <el-card class="function-card" @click="goToDiagnosis">
            <div class="card-content">
              <el-icon class="card-icon"><FirstAidKit /></el-icon>
              <h3>诊断与治疗</h3>
              <p>进行患者诊断和治疗记录</p>
            </div>
          </el-card>

          <el-card class="function-card" @click="goToCaseManagement">
            <div class="card-content">
              <el-icon class="card-icon"><Document /></el-icon>
              <h3>病例编辑</h3>
              <p>查看和编辑患者病例</p>
            </div>
          </el-card>

          <el-card class="function-card" @click="goToPrescription">
            <div class="card-content">
              <el-icon class="card-icon"><Edit /></el-icon>
              <h3>开具处方</h3>
              <p>为患者开具电子处方</p>
            </div>
          </el-card>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  User, 
  SwitchButton, 
  ArrowDown,
  Bell,
  FirstAidKit,
  Document,
  Edit,
  HomeFilled
} from '@element-plus/icons-vue'

export default {
  name: 'DoctorDashboard',
  components: {
    User,
    SwitchButton,
    ArrowDown,
    Bell,
    FirstAidKit,
    Document,
    Edit,
    HomeFilled
  },
  setup() {
    const router = useRouter()
    const username = ref('医生')
    const userAvatar = ref('https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png')

    const handleLogout = () => {
      localStorage.removeItem('token')
      ElMessage.success('已退出登录')
      router.push('/')
    }

    const goToHome = () => {
      router.push('/doctor/dashboard')
    }

    const goToProfile = () => {
      router.push('/doctor/dashboard/profile')
    }

    const goToCallManagement = () => {
      router.push('/doctor/call-management')
    }

    const goToDiagnosis = () => {
      router.push('/doctor/diagnosis')
    }

    const goToCaseManagement = () => {
      router.push('/doctor/case-management')
    }

    const goToPrescription = () => {
      router.push('/doctor/prescription')
    }

    return {
      username,
      userAvatar,
      handleLogout,
      goToHome,
      goToProfile,
      goToCallManagement,
      goToDiagnosis,
      goToCaseManagement,
      goToPrescription
    }
  }
}
</script>

<style scoped>
.dashboard {
  height: 100%;
  background-color: #f5f7fa;
  width: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.header {
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 10px 0;
  width: 100%;
  flex-shrink: 0;
  z-index: 100;
}

.header-content {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 20px;
}

.logo h1 {
  margin: 0;
  color: #409EFF;
  font-size: 24px;
}

.home-button {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 17px;
  color: #606266;
  padding: 0;
  margin: 0;
}

.home-button:hover {
  color: #409EFF;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: 8px 12px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.user-dropdown:hover {
  background-color: #f5f7fa;
}

.username {
  margin: 0 8px;
  font-size: 14px;
  color: #606266;
}

.main-content {
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  overflow: auto;
  padding: 20px;
}

.welcome-section {
  text-align: center;
  margin-top: 40px;
  margin-bottom: 10px;
}

.welcome-section h2 {
  font-size: 28px;
  color: #303133;
  margin-bottom: 10px;
}

.welcome-section p {
  font-size: 16px;
  color: #606266;
}

.function-grid {
  display: flex;
  margin-top: 80px;
  width: 100%;
  max-width: 1200px;
  height: 100%;
  gap: 60px;
}

.function-card {
  flex: 1;
  height: 300px;
  min-width: 240px;
  max-width: 300px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.function-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.card-content {
  text-align: center;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.card-icon {
  font-size: 48px;
  color: #409EFF;
  margin-bottom: 20px;
}

.card-content h3 {
  font-size: 18px;
  color: #303133;
  margin-bottom: 10px;
}

.card-content p {
  font-size: 14px;
  color: #606266;
  line-height: 1.4;
  max-width: 90%;
}

:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: 8px;
}

:deep(.el-dropdown-menu__item .el-icon) {
  font-size: 16px;
}
</style>

<style>
html, body {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

#app {
  height: 100%;
  width: 100%;
}
</style> 