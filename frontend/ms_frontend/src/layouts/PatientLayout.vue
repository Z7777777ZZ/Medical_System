<template>
  <div class="patient-layout">
    <el-container>
      <el-aside width="250px">
        <div class="logo-container">
          <h2>门诊患者系统</h2>
        </div>
        <el-menu
          router
          default-active="/patient/dashboard"
          class="el-menu-vertical"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF">
          <el-menu-item index="/patient/dashboard">
            <el-icon><el-icon-odometer /></el-icon>
            <span>患者主页</span>
          </el-menu-item>
          <el-menu-item index="/patient/queue">
            <el-icon><el-icon-time /></el-icon>
            <span>排队信息</span>
          </el-menu-item>
          <el-menu-item index="/patient/prescription">
            <el-icon><el-icon-document /></el-icon>
            <span>处方查询</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-container>
        <el-header height="60px">
          <div class="header-right">
            <el-dropdown>
              <span class="el-dropdown-link">
                患者姓名<el-icon class="el-icon--right"><el-icon-arrow-down /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>个人信息</el-dropdown-item>
                  <el-dropdown-item>修改密码</el-dropdown-item>
                  <el-dropdown-item divided>退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        
        <el-main>
          <div class="main-container">
            <router-view />
          </div>
        </el-main>
        
        <el-footer height="50px">
          <div class="footer-content">
            © {{ currentYear }} 医疗系统 - 门诊服务平台
          </div>
        </el-footer>
      </el-container>
    </el-container>
    
    <!-- 叫号提醒弹窗 -->
    <el-dialog
      v-model="showCallNotification"
      title="叫号通知"
      width="30%"
      :show-close="false"
      center>
      <div class="call-notification-content">
        <el-icon class="notification-icon" :size="64" color="#409EFF"><el-icon-bell /></el-icon>
        <h2>您好，{{ patientName }}!</h2>
        <p>请前往{{ doctorRoom }}诊室就诊</p>
        <p class="doctor-name">{{ doctorName }}医生正在等待您</p>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="acknowledgeCall">确定</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useQueueStore } from '../stores/queueStore'

export default {
  name: 'PatientLayout',
  setup() {
    const route = useRoute()
    const queueStore = useQueueStore()
    
    // 当前激活的菜单项
    const activeIndex = computed(() => route.path)
    
    // 当前年份（用于页脚版权信息）
    const currentYear = new Date().getFullYear()
    
    // 叫号提醒相关状态
    const showCallNotification = ref(false)
    const patientName = ref('')
    const doctorName = ref('')
    const doctorRoom = ref('')
    
    // 确认叫号通知
    const acknowledgeCall = () => {
      showCallNotification.value = false
    }
    
    onMounted(() => {
      // 初始化队列数据
      queueStore.initData()
    })
    
    return {
      activeIndex,
      currentYear,
      showCallNotification,
      patientName,
      doctorName,
      doctorRoom,
      acknowledgeCall
    }
  }
}
</script>

<style scoped>
.patient-layout {
  height: 100vh;
}

.logo-container {
  height: 60px;
  background-color: #263445;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.el-header {
  background-color: #fff;
  color: #333;
  line-height: 60px;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
}

.el-menu-vertical {
  height: calc(100vh - 60px);
  border-right: none;
}

.el-aside {
  background-color: #304156;
  color: #fff;
}

.el-main {
  background-color: #f0f2f5;
  padding: 20px;
}

.el-dropdown-link {
  cursor: pointer;
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #333;
}

.main-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.el-footer {
  background-color: #304156;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.footer-content {
  text-align: center;
}

.call-notification-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.notification-icon {
  margin-bottom: 20px;
}

.doctor-name {
  margin-top: 10px;
  color: #409EFF;
  font-weight: bold;
}

::v-deep .el-menu--horizontal > .el-menu-item {
  height: 60px;
  line-height: 60px;
}
</style>