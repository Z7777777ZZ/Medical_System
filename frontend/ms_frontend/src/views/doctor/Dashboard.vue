<template>
  <div class="doctor-dashboard">
    <el-row :gutter="20">
      <!-- 医生信息卡片 -->
      <el-col :span="24">
        <el-card class="info-card">
          <template #header>
            <div class="card-header">
              <h3>医生工作台</h3>
            </div>
          </template>
          
          <div class="doctor-info">
            <div class="avatar-section">
              <el-avatar :size="100" :icon="UserFilled" />
            </div>
            
            <div class="info-section">
              <div class="info-row">
                <div class="info-item"><span class="label">姓名:</span> {{ doctorInfo.name }}</div>
                <div class="info-item"><span class="label">工号:</span> {{ doctorInfo.staffId }}</div>
                <div class="info-item"><span class="label">科室:</span> {{ doctorInfo.department }}</div>
              </div>
              <div class="info-row">
                <div class="info-item"><span class="label">职称:</span> {{ doctorInfo.title }}</div>
                <div class="info-item"><span class="label">专长:</span> {{ doctorInfo.specialty }}</div>
              </div>
            </div>
            
            <div class="stats-section">
              <div class="stat-item">
                <div class="stat-value">{{ stats.todayPatients }}</div>
                <div class="stat-label">今日接诊</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ stats.waitingPatients }}</div>
                <div class="stat-label">等待接诊</div>
              </div>
              <div class="stat-item">
                <div class="stat-value">{{ stats.todayPrescriptions }}</div>
                <div class="stat-label">今日处方</div>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
      
      <!-- 快速操作卡片 -->
      <el-col :span="12">
        <el-card class="quick-actions-card">
          <template #header>
            <div class="card-header">
              <h3>快速操作</h3>
            </div>
          </template>
          
          <div class="quick-actions">
            <el-row :gutter="20">
              <el-col :span="8">
                <div class="action-item" @click="goToQueue">
                  <el-icon :size="32" color="#409EFF"><el-icon-user /></el-icon>
                  <span>患者队列</span>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="action-item" @click="goToPrescription">
                  <el-icon :size="32" color="#67C23A"><el-icon-document /></el-icon>
                  <span>处方管理</span>
                </div>
              </el-col>
              <el-col :span="8">
                <div class="action-item" @click="goToSchedule">
                  <el-icon :size="32" color="#E6A23C"><el-icon-calendar /></el-icon>
                  <span>排班查询</span>
                </div>
              </el-col>
            </el-row>
          </div>
        </el-card>
      </el-col>
      
      <!-- 通知卡片 -->
      <el-col :span="12">
        <el-card class="notification-card">
          <template #header>
            <div class="card-header">
              <h3>最近通知</h3>
              <el-button type="text" @click="refreshNotifications">刷新</el-button>
            </div>
          </template>
          
          <div v-if="notifications.length > 0" class="notification-list">
            <div 
              v-for="notification in notifications" 
              :key="notification.id" 
              class="notification-item"
              :class="{ unread: !notification.read }"
            >
              <div class="notification-content">
                <div class="notification-title">{{ notification.title }}</div>
                <div class="notification-message">{{ notification.message }}</div>
                <div class="notification-time">{{ formatTime(notification.time) }}</div>
              </div>
              <div class="notification-actions">
                <el-button type="text" size="small" @click="markAsRead(notification)">
                  {{ notification.read ? '标为未读' : '标为已读' }}
                </el-button>
              </div>
            </div>
          </div>
          
          <el-empty v-else description="暂无通知" />
        </el-card>
      </el-col>
      
      <!-- 今日工作摘要 -->
      <el-col :span="24">
        <el-card class="work-summary-card">
          <template #header>
            <div class="card-header">
              <h3>今日工作摘要</h3>
              <div class="date-display">{{ currentDate }}</div>
            </div>
          </template>
          
          <el-table 
            :data="recentPatients" 
            style="width: 100%"
            :max-height="400"
          >
            <el-table-column prop="time" label="时间" width="120" />
            <el-table-column prop="patientName" label="患者姓名" width="120" />
            <el-table-column prop="patientInfo" label="患者信息" width="180" />
            <el-table-column prop="diagnosis" label="诊断结果" />
            <el-table-column prop="status" label="状态" width="120">
              <template #default="scope">
                <el-tag :type="getStatusType(scope.row.status)">
                  {{ getStatusText(scope.row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="180" fixed="right">
              <template #default="scope">
                <el-button 
                  v-if="scope.row.status === 'waiting'"
                  type="primary" 
                  size="small" 
                  @click="callPatient(scope.row)"
                >
                  叫号
                </el-button>
                <el-button 
                  v-else-if="scope.row.status === 'completed'"
                  type="info" 
                  size="small" 
                  @click="viewRecord(scope.row)"
                >
                  查看病历
                </el-button>
                <el-button 
                  v-else
                  type="success" 
                  size="small" 
                  @click="goToPrescriptionWithPatient(scope.row)"
                >
                  开处方
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useQueueStore } from '../../stores/queueStore'
import { usePrescriptionStore } from '../../stores/prescriptionStore'
import { ElMessage } from 'element-plus'
import { UserFilled } from '@element-plus/icons-vue'

export default {
  name: 'DoctorDashboard',
  setup() {
    const router = useRouter()
    /* eslint-disable no-unused-vars */
    const queueStore = useQueueStore()
    const prescriptionStore = usePrescriptionStore()
    /* eslint-enable no-unused-vars */
    
    // 医生信息（模拟数据，实际应从用户会话或Store中获取）
    const doctorInfo = reactive({
      id: 'doctor123',
      staffId: 'D00123',
      name: '李医生',
      department: '内科',
      title: '主治医师',
      specialty: '呼吸系统疾病'
    })
    
    // 统计数据
    const stats = reactive({
      todayPatients: 12,
      waitingPatients: 5,
      todayPrescriptions: 8
    })
    
    // 当前日期
    const currentDate = computed(() => {
      const now = new Date()
      return `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日`
    })
    
    // 通知列表
    const notifications = ref([
      {
        id: 1,
        title: '系统通知',
        message: '今日下午2点将进行系统维护，请做好工作安排',
        time: new Date(new Date().setHours(new Date().getHours() - 2)),
        read: false
      },
      {
        id: 2,
        title: '排班变更',
        message: '您的下周二上午的排班已调整为周三上午',
        time: new Date(new Date().setDate(new Date().getDate() - 1)),
        read: true
      }
    ])
    
    // 最近患者
    const recentPatients = ref([
      {
        id: 'visit001',
        time: '09:30',
        patientName: '张三',
        patientInfo: '男, 45岁, 发热咳嗽',
        diagnosis: '上呼吸道感染',
        status: 'completed'
      },
      {
        id: 'visit002',
        time: '10:15',
        patientName: '李四',
        patientInfo: '女, 32岁, 头痛',
        diagnosis: '偏头痛',
        status: 'completed'
      },
      {
        id: 'visit003',
        time: '11:00',
        patientName: '王五',
        patientInfo: '男, 28岁, 腹痛',
        diagnosis: '胃炎',
        status: 'in-progress'
      },
      {
        id: 'visit004',
        time: '待叫号',
        patientName: '赵六',
        patientInfo: '女, 50岁, 关节疼痛',
        diagnosis: '待诊断',
        status: 'waiting'
      }
    ])
    
    // 刷新通知
    const refreshNotifications = () => {
      // 实际项目中应该调用API获取最新通知
      ElMessage.success('通知已更新')
    }
    
    // 标记通知已读/未读
    const markAsRead = (notification) => {
      notification.read = !notification.read
      // 实际项目中应该调用API更新通知状态
      ElMessage.success(`通知已标记为${notification.read ? '已读' : '未读'}`)
    }
    
    // 格式化时间
    const formatTime = (time) => {
      const now = new Date()
      const notificationTime = new Date(time)
      const diffMs = now - notificationTime
      const diffMins = Math.floor(diffMs / 60000)
      
      if (diffMins < 60) {
        return `${diffMins} 分钟前`
      } else if (diffMins < 1440) {
        const hours = Math.floor(diffMins / 60)
        return `${hours} 小时前`
      } else {
        const days = Math.floor(diffMins / 1440)
        return `${days} 天前`
      }
    }
    
    // 获取状态类型
    const getStatusType = (status) => {
      switch (status) {
        case 'completed':
          return 'success'
        case 'in-progress':
          return 'warning'
        case 'waiting':
          return 'info'
        default:
          return 'info'
      }
    }
    
    // 获取状态文本
    const getStatusText = (status) => {
      switch (status) {
        case 'completed':
          return '已完成'
        case 'in-progress':
          return '就诊中'
        case 'waiting':
          return '等待中'
        default:
          return '未知状态'
      }
    }
    
    // 叫号患者
    // eslint-disable-next-line no-unused-vars
    const callPatient = (patient) => {
      router.push('/doctor/queue')
    }
    
    // 查看病历
    const viewRecord = (patient) => {
      ElMessage.info(`查看患者 ${patient.patientName} 的病历`)
    }
    
    // 跳转到患者队列页面
    const goToQueue = () => {
      router.push('/doctor/queue')
    }
    
    // 跳转到处方管理页面
    const goToPrescription = () => {
      router.push('/doctor/prescription')
    }
    
    // 跳转到排班查询页面
    const goToSchedule = () => {
      ElMessage.info('排班查询功能尚未实现')
    }
    
    // 跳转到处方页面并带上患者信息
    // eslint-disable-next-line no-unused-vars
    const goToPrescriptionWithPatient = (patient) => {
      router.push({
        path: '/doctor/prescription',
        query: { patientId: patient.id }
      })
    }
    
    // 初始化
    onMounted(() => {
      // 实际项目中，应该从API获取数据
    })
    
    return {
      doctorInfo,
      stats,
      notifications,
      recentPatients,
      currentDate,
      UserFilled,
      refreshNotifications,
      markAsRead,
      formatTime,
      getStatusType,
      getStatusText,
      callPatient,
      viewRecord,
      goToQueue,
      goToPrescription,
      goToSchedule,
      goToPrescriptionWithPatient
    }
  }
}
</script>

<style scoped>
.doctor-dashboard {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-card {
  margin-bottom: 20px;
}

.doctor-info {
  display: flex;
  flex-wrap: wrap;
}

.avatar-section {
  margin-right: 40px;
  margin-bottom: 20px;
}

.info-section {
  flex: 1;
  min-width: 300px;
  margin-bottom: 20px;
}

.stats-section {
  display: flex;
  margin-left: auto;
}

.info-row {
  display: flex;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.info-item {
  margin-right: 30px;
  margin-bottom: 5px;
}

.label {
  font-weight: bold;
  color: #303133;
  margin-right: 5px;
}

.stat-item {
  text-align: center;
  margin: 0 20px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #409EFF;
}

.stat-label {
  margin-top: 5px;
  color: #606266;
}

.quick-actions, .notification-list {
  padding: 10px 0;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.action-item:hover {
  background-color: #f0f2f5;
}

.action-item span {
  margin-top: 10px;
  color: #606266;
}

.notification-item {
  display: flex;
  justify-content: space-between;
  padding: 15px 10px;
  border-bottom: 1px solid #EBEEF5;
}

.notification-item:last-child {
  border-bottom: none;
}

.notification-item.unread {
  background-color: #ecf5ff;
}

.notification-title {
  font-weight: 500;
  color: #303133;
  margin-bottom: 5px;
}

.notification-message {
  color: #606266;
  margin-bottom: 5px;
}

.notification-time {
  font-size: 12px;
  color: #909399;
}

.work-summary-card {
  margin-top: 20px;
}

.date-display {
  font-size: 14px;
  color: #606266;
}

@media (max-width: 768px) {
  .doctor-info {
    flex-direction: column;
  }
  
  .avatar-section {
    margin-right: 0;
    align-self: center;
  }
  
  .stats-section {
    margin-left: 0;
    justify-content: space-around;
    width: 100%;
  }
}
</style>