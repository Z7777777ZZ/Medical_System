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
  ShoppingCart
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
    ShoppingCart
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
      router.push('/')
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
      goToPharmacy
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

.user-actions {
  display: flex;
  gap: 10px;
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
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 60px;
  margin-top: 40px;
  width: 100%;
  max-width: 1200px;
}

.function-card {
  height: 300px;
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

.user-actions .el-button {
  border-radius: 8px;
  padding: 8px 20px;
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