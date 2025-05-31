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
          <el-button type="text" @click="goToUserExperience" class="nav-button">
            <el-icon><Star /></el-icon>
            <span>用户体验</span>
          </el-button>
        </div>
        <div class="user-actions" v-if="!isLoggedIn">
          <el-button type="primary" @click="goToLogin">登录</el-button>
          <el-button @click="goToRegister">注册</el-button>
        </div>
        <div class="user-info" v-else>
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
      <router-view v-if="$route.path === '/patient/dashboard/profile'" />
      <template v-else>
        <div class="welcome-section">
          <h2>患者服务</h2>
          <p>欢迎使用医院管理系统，请选择您需要的服务</p>
        </div>

        <div class="function-grid">
          <el-card class="function-card" @click="goToCaseView">
            <div class="card-content">
              <el-icon class="card-icon"><Document /></el-icon>
              <h3>病例查看</h3>
              <p>查看您的就诊记录和检查报告</p>
            </div>
          </el-card>

          <el-card class="function-card" @click="goToAppointment">
            <div class="card-content">
              <el-icon class="card-icon"><Calendar /></el-icon>
              <h3>预约挂号</h3>
              <p>在线预约医生门诊</p>
            </div>
          </el-card>

          <el-card class="function-card" @click="goToPayment">
            <div class="card-content">
              <el-icon class="card-icon"><Money /></el-icon>
              <h3>线上缴费</h3>
              <p>在线支付医疗费用</p>
            </div>
          </el-card>

          <el-card class="function-card" @click="goToConsultation">
            <div class="card-content">
              <el-icon class="card-icon"><ChatDotRound /></el-icon>
              <h3>智慧问诊</h3>
              <p>在线咨询医生</p>
            </div>
          </el-card>

          <el-card class="function-card" @click="goToDoctorSearch">
            <div class="card-content">
              <el-icon class="card-icon"><Search /></el-icon>
              <h3>查找医生</h3>
              <p>查找合适的医生</p>
            </div>
          </el-card>

          <el-card class="function-card" @click="goToPharmacy">
            <div class="card-content">
              <el-icon class="card-icon"><ShoppingCart /></el-icon>
              <h3>线上购药</h3>
              <p>在线购买药品</p>
            </div>
          </el-card>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  User, 
  SwitchButton, 
  ArrowDown,
  HomeFilled,
  Document,
  Calendar,
  Money,
  ChatDotRound,
  Search,
  ShoppingCart,
  Star
} from '@element-plus/icons-vue'

export default {
  name: 'PatientDashboard',
  components: {
    User,
    SwitchButton,
    ArrowDown,
    HomeFilled,
    Document,
    Calendar,
    Money,
    ChatDotRound,
    Search,
    ShoppingCart,
    Star
  },
  setup() {
    const router = useRouter()
    const username = ref('患者')
    const userAvatar = ref('https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png')
    const isLoggedIn = computed(() => !!localStorage.getItem('token'))
    //const isLoggedIn=true
    //localStorage.setItem('patient_id',12345)
    const handleLogout = () => {
      localStorage.removeItem('patient_id')
      //localStorage.removeItem('doctor_id')
      localStorage.removeItem('token')
      ElMessage.success('已退出登录')
      router.push('/home')
    }

    const goToHome = () => {
      //localStorage.setItem('patient_id',12345)
      router.push('/patient/dashboard')
    }

    const goToLogin = () => {
      router.push('/login?type=patient')
    }

    const goToRegister = () => {
      router.push('/patient/register')
    }

    const goToProfile = () => {
      router.push('/patient/dashboard/profile')
    }

    const goToCaseView = () => {
      if (!isLoggedIn.value) {
        ElMessage.warning('请先登录')
        return
      }
      router.push('/patient/case-view')
    }

    const goToAppointment = () => {
      if (!isLoggedIn.value) {
        ElMessage.warning('请先登录')
        return
      }
      router.push('/patient/appointment')
    }

    const goToPayment = () => {
      if (!isLoggedIn.value) {
        ElMessage.warning('请先登录')
        return
      }
      router.push('/patient/payment')
    }

    const goToConsultation = () => {
      if (!isLoggedIn.value) {
        ElMessage.warning('请先登录')
        return
      }
      router.push('/patient/consultation')
    }

    const goToDoctorSearch = () => {
      router.push('/patient/doctor-search')
    }

    const goToPharmacy = () => {
      if (!isLoggedIn.value) {
        ElMessage.warning('请先登录')
        return
      }
      router.push('/patient/pharmacy')
    }

    const goToUserExperience = () => {
      router.push('/ue')
    }

    return {
      username,
      userAvatar,
      isLoggedIn,
      handleLogout,
      goToHome,
      goToLogin,
      goToRegister,
      goToProfile,
      goToCaseView,
      goToAppointment,
      goToPayment,
      goToConsultation,
      goToDoctorSearch,
      goToPharmacy,
      goToUserExperience
    }
  }
}
</script>

<style scoped>
.dashboard {
  width: 100%;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--bg-color, #ffffff);
}

.header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  height: 70px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--border-lighter, #EBEEF5);
  box-shadow: var(--shadow-light, 0 2px 4px rgba(0, 0, 0, 0.05));
}

.header-content {
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 var(--spacing-lg, 24px);
  max-width: 1200px;
  margin: 0 auto;
}

.logo {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg, 24px);
}

.logo h1 {
  font-size: 24px;
  margin: 0;
  color: var(--text-primary, #303133);
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary-color, #409EFF) 0%, var(--success-color, #67C23A) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.home-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs, 4px);
  font-size: 17px;
  color: var(--text-regular, #606266);
  padding: 0;
  margin: 0;
}

.home-button:hover {
  color: var(--primary-color, #409EFF);
}

.nav-button {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs, 4px);
  font-size: 17px;
  color: var(--text-regular, #606266);
  padding: 0;
  margin: 0;
}

.nav-button:hover {
  color: var(--primary-color, #409EFF);
}

.user-actions {
  display: flex;
  gap: var(--spacing-sm, 8px);
}

.user-info {
  display: flex;
  align-items: center;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
  padding: var(--spacing-sm, 8px) var(--spacing-md, 16px);
  border-radius: var(--border-radius-sm, 4px);
  transition: background-color var(--transition-fast, 0.2s ease);
}

.user-dropdown:hover {
  background-color: var(--bg-light, #f8fafe);
}

.username {
  margin: 0 var(--spacing-sm, 8px);
  font-size: 14px;
  color: var(--text-regular, #606266);
}

.main-content {
  width: 100%;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  padding: calc(70px + var(--spacing-xl, 32px)) var(--spacing-lg, 24px) var(--spacing-xxl, 48px);
  background: linear-gradient(180deg, var(--bg-lighter, #fafbfc) 0%, var(--bg-light, #f5f7fa) 100%);
  overflow-y: auto;
  overflow-x: hidden;
}

.welcome-section {
  text-align: center;
  margin-bottom: var(--spacing-xl, 32px);
  padding: var(--spacing-xxl, 48px) var(--spacing-xl, 32px);
  background: linear-gradient(135deg, var(--bg-light, #f8fafe) 0%, #e3f2fd 100%);
  border-radius: var(--border-radius-xl, 16px);
  box-shadow: var(--shadow-base, 0 4px 12px rgba(0, 0, 0, 0.08));
  max-width: 800px;
  width: 100%;
  position: relative;
  overflow: hidden;
}

.welcome-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary-color, #409EFF), var(--success-color, #67C23A), var(--warning-color, #E6A23C));
}

.welcome-section h2 {
  font-size: 32px;
  color: var(--text-primary, #2c3e50);
  margin-bottom: var(--spacing-md, 16px);
  font-weight: 700;
  background: linear-gradient(135deg, var(--primary-color, #409EFF) 0%, var(--success-color, #67C23A) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.welcome-section p {
  font-size: 18px;
  color: var(--text-regular, #5a6c7d);
  line-height: 1.6;
  margin: 0;
}

.function-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--spacing-xl, 32px);
  margin-top: var(--spacing-xxl, 48px);
  width: 100%;
  max-width: 1100px;
  padding: var(--spacing-lg, 24px);
}

.function-card {
  width: 100%;
  height: 280px;
  cursor: pointer;
  transition: all var(--transition-base, 0.3s ease);
  border-radius: var(--border-radius-lg, 12px);
  overflow: hidden;
  box-shadow: var(--shadow-light, 0 4px 12px rgba(0, 0, 0, 0.05));
  border: 1px solid var(--border-lighter, #f0f0f0);
}

.function-card:hover {
  transform: translateY(-8px);
  box-shadow: var(--shadow-dark, 0 12px 32px rgba(64, 158, 255, 0.15));
  border-color: var(--primary-color, #409EFF);
}

.card-content {
  text-align: center;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xl, 32px) var(--spacing-lg, 24px);
  background: linear-gradient(135deg, var(--bg-color, #ffffff) 0%, var(--bg-light, #f8fafe) 100%);
  position: relative;
}

.card-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, var(--primary-color, #409EFF), var(--success-color, #67C23A));
  transform: scaleX(0);
  transition: transform var(--transition-base, 0.3s ease);
}

.function-card:hover .card-content::before {
  transform: scaleX(1);
}

.card-icon {
  font-size: 56px;
  color: var(--primary-color, #409EFF);
  margin-bottom: var(--spacing-lg, 24px);
  transition: all var(--transition-base, 0.3s ease);
}

.function-card:hover .card-icon {
  color: var(--success-color, #67C23A);
  transform: scale(1.1);
}

.card-content h3 {
  font-size: 20px;
  color: var(--text-primary, #2c3e50);
  margin-bottom: var(--spacing-md, 16px);
  font-weight: 600;
  transition: color var(--transition-base, 0.3s ease);
}

.function-card:hover .card-content h3 {
  color: var(--primary-color, #409EFF);
}

.card-content p {
  font-size: 14px;
  color: var(--text-regular, #6c757d);
  line-height: 1.6;
  max-width: 90%;
  transition: color var(--transition-base, 0.3s ease);
}

.function-card:hover .card-content p {
  color: var(--text-secondary, #495057);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .function-grid {
    max-width: 900px;
    gap: var(--spacing-lg, 24px);
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  }
  
  .function-card {
    height: 260px;
  }
  
  .card-icon {
    font-size: 48px;
  }
  
  .card-content h3 {
    font-size: 18px;
  }
}

@media (max-width: 900px) {
  .main-content {
    padding: calc(70px + var(--spacing-lg, 24px)) var(--spacing-md, 16px) var(--spacing-xl, 32px);
  }
  
  .function-grid {
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: var(--spacing-lg, 24px);
    max-width: 600px;
    padding: var(--spacing-md, 16px);
  }
  
  .welcome-section {
    padding: var(--spacing-xl, 32px) var(--spacing-lg, 24px);
  }
  
  .welcome-section h2 {
    font-size: 28px;
  }
  
  .welcome-section p {
    font-size: 16px;
  }
}

@media (max-width: 640px) {
  .header-content {
    padding: 0 var(--spacing-md, 16px);
  }
  
  .logo {
    gap: var(--spacing-md, 16px);
  }
  
  .logo h1 {
    font-size: 20px;
  }
  
  .main-content {
    padding: calc(70px + var(--spacing-md, 16px)) var(--spacing-sm, 8px) var(--spacing-lg, 24px);
  }
  
  .function-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-md, 16px);
    max-width: 400px;
    padding: var(--spacing-sm, 8px);
  }
  
  .function-card {
    height: 220px;
  }
  
  .card-content {
    padding: var(--spacing-lg, 24px) var(--spacing-md, 16px);
  }
  
  .card-icon {
    font-size: 40px;
    margin-bottom: var(--spacing-md, 16px);
  }
  
  .card-content h3 {
    font-size: 16px;
    margin-bottom: var(--spacing-sm, 8px);
  }
  
  .card-content p {
    font-size: 13px;
  }
  
  .welcome-section {
    padding: var(--spacing-lg, 24px) var(--spacing-md, 16px);
  }
  
  .welcome-section h2 {
    font-size: 24px;
  }
  
  .welcome-section p {
    font-size: 14px;
  }
}

.user-actions .el-button {
  border-radius: var(--border-radius-md, 8px);
  padding: var(--spacing-sm, 8px) var(--spacing-lg, 24px);
  font-weight: 500;
}

.user-actions .el-button--primary {
  background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
  border: none;
}

.user-actions .el-button--primary:hover {
  background: linear-gradient(135deg, #2980b9 0%, #3498db 100%);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.2);
}

:deep(.el-dropdown-menu__item) {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm, 8px);
}

:deep(.el-dropdown-menu__item .el-icon) {
  font-size: 16px;
}

/* 页面加载动画 */
.welcome-section {
  animation: fadeInDown 0.6s ease-out;
}

.function-grid {
  animation: fadeInUp 0.8s ease-out 0.2s both;
}

.function-card:nth-child(1) { animation: fadeInScale 0.6s ease-out 0.3s both; }
.function-card:nth-child(2) { animation: fadeInScale 0.6s ease-out 0.4s both; }
.function-card:nth-child(3) { animation: fadeInScale 0.6s ease-out 0.5s both; }
.function-card:nth-child(4) { animation: fadeInScale 0.6s ease-out 0.6s both; }
.function-card:nth-child(5) { animation: fadeInScale 0.6s ease-out 0.7s both; }
.function-card:nth-child(6) { animation: fadeInScale 0.6s ease-out 0.8s both; }

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fadeInScale {
  from {
    opacity: 0;
    transform: scale(0.8) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
</style>

<style>
html, body {
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 0;
}

#app {
  height: 100%;
  width: 100%;
}
</style> 