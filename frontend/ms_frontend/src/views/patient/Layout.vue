<template>
  <div class="layout-container">
    <el-container>
      <el-header class="main-header">
        <div class="header-left">
          <div class="logo">
            <h2>医疗系统 - 患者端</h2>
          </div>
          <el-menu
            mode="horizontal"
            router
            :default-active="$route.path"
            class="nav-menu"
          >
            <el-menu-item index="/patient/appointment">
              <el-icon><Calendar /></el-icon>
              <span>预约挂号</span>
            </el-menu-item>
            
            <el-menu-item index="/patient/records">
              <el-icon><Document /></el-icon>
              <span>病历查询</span>
            </el-menu-item>
            
            <el-menu-item index="/patient/payment-history">
              <el-icon><Wallet /></el-icon>
              <span>支付记录</span>
            </el-menu-item>
            
            <el-menu-item index="/patient/appointments">
              <el-icon><Notification /></el-icon>
              <span>我的预约</span>
            </el-menu-item>
          </el-menu>
        </div>
        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-profile">
              <el-avatar :size="32">{{ userInitial }}</el-avatar>
              <span class="username">{{ userName }}</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                <el-dropdown-item command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      
      <el-main class="main-content">
        <!-- 移除提醒区域 -->
        <!-- <div v-if="upcomingAppointments.length > 0" class="reminder-section">
          <el-alert
            v-for="appointment in upcomingAppointments"
            :key="appointment.appointment_id"
            type="info"
            :closable="false"
            class="appointment-reminder"
          >
            <el-icon><Alarm /></el-icon>
            <span class="reminder-text">
              您有一个预约：{{ formatDateTime(appointment.appointment_time) }} 
              在{{ appointment.department_name }} {{ appointment.doctor_name }}
            </span>
            <el-button size="small" type="primary" @click="viewAppointment(appointment)">查看详情</el-button>
          </el-alert>
        </div> -->
        
        <router-view />
      </el-main>
      
      <el-footer class="main-footer">
        <div class="footer-content">
          &copy; {{ new Date().getFullYear() }} 医疗系统 - 患者就诊流程管理子系统
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { Calendar, Document, Wallet, Notification } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'PatientLayout',
  components: {
    Calendar,
    Document,
    Wallet, 
    Notification
  },
  setup() {
    const router = useRouter()
    const userName = ref('患者用户')
    
    const userInitial = computed(() => {
      return userName.value.charAt(0)
    })
    
    // 获取患者信息
    const fetchPatientInfo = () => {
      // 从localStorage获取患者ID和姓名
      const patientId = localStorage.getItem('patientId') || 1
      const storedName = localStorage.getItem('patientName')
      
      // 如果已有存储的姓名，直接使用
      if (storedName) {
        userName.value = storedName
        return
      }
      
      // 否则尝试从服务器获取患者信息
      axios.get(`/api/patient/${patientId}`).then(response => {
        if (response.data && response.data.status === 'success' && response.data.data && response.data.data.name) {
          userName.value = response.data.data.name
          // 存储到localStorage以便下次使用
          localStorage.setItem('patientName', response.data.data.name)
        } else {
          // 使用模拟数据
          userName.value = `患者${patientId}`
          localStorage.setItem('patientName', `患者${patientId}`)
        }
      }).catch(error => {
        console.warn('Error fetching patient info:', error)
        // 使用模拟数据
        userName.value = `患者${patientId}`
        localStorage.setItem('patientName', `患者${patientId}`)
      })
    }
    
    // 格式化时间
    const formatDateTime = (dateString) => {
      if (!dateString) return ''
      
      try {
        const date = new Date(dateString)
        return date.toLocaleString('zh-CN', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        })
      } catch {
        return dateString
      }
    }
    
    // 查看预约详情
    const viewAppointment = (appointment) => {
      router.push({
        path: '/patient/appointments', 
        query: { id: appointment.appointment_id }
      })
    }
    
    // 处理下拉菜单命令
    const handleCommand = (command) => {
      if (command === 'logout') {
        ElMessageBox.confirm(
          '确定要退出登录吗？',
          '提示',
          {
            confirmButtonText: '确定',
            cancelButtonText: '取消',
            type: 'warning'
          }
        ).then(() => {
          // 清除登录状态
          localStorage.removeItem('token')
          localStorage.removeItem('patientId')
          localStorage.removeItem('patientName')
          
          // 返回首页
          router.push('/')
          ElMessage.success('已退出登录')
        }).catch(() => {})
      } else if (command === 'profile') {
        // 个人信息页面（如果有的话）
        ElMessage.info('个人信息功能暂未开放')
      }
    }
    
    onMounted(() => {
      // 获取患者信息
      fetchPatientInfo()
    })
    
    return {
      userName,
      userInitial,
      formatDateTime,
      viewAppointment,
      handleCommand
    }
  }
}
</script>

<style scoped>
.layout-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-header {
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  height: auto !important;
}

.header-left {
  display: flex;
  align-items: center;
}

.logo {
  margin-right: 40px;
}

.logo h2 {
  margin: 0;
  color: #409EFF;
}

.nav-menu {
  border-bottom: none;
}

.user-profile {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.username {
  margin-left: 8px;
  font-size: 14px;
}

.main-content {
  padding: 20px;
  background-color: #f5f7fa;
  flex: 1;
}

.reminder-section {
  margin-bottom: 20px;
}

.appointment-reminder {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.reminder-text {
  flex: 1;
  margin: 0 10px;
}

.main-footer {
  background-color: #fff;
  text-align: center;
  padding: 15px 0;
  color: #909399;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}
</style> 