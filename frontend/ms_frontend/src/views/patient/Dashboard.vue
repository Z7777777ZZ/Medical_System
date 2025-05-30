<template>
  <div class="patient-dashboard">
    <el-card class="dashboard-card">
      <template #header>
        <div class="card-header">
          <h3>患者主页</h3>
          <div class="header-actions">
            <el-button type="primary" @click="goToQueue">查看排队</el-button>
            <el-button type="success" @click="goToPrescription">我的处方</el-button>
          </div>
        </div>
      </template>
    </el-card>

    <div class="dashboard-header">
      <h1>欢迎回来，{{ patientName }}</h1>
      <p>{{ currentDate }}</p>
    </div>

    <el-row :gutter="20">
      <el-col :xs="24" :md="12">
        <!-- 近期挂号卡片 -->
        <el-card class="dashboard-card">
          <template #header>
            <div class="card-header">
              <h3>我的挂号</h3>
              <el-button text @click="navigateToQueue">查看更多</el-button>
            </div>
          </template>
          <div class="card-body" v-loading="loadingAppointments">
            <template v-if="upcomingAppointments.length > 0">
              <div v-for="appointment in upcomingAppointments" :key="appointment.id" class="appointment-item">
                <el-row :gutter="10" class="appointment-info">
                  <el-col :span="6">
                    <div class="appointment-date">
                      <div class="date-day">{{ formatAppointmentDay(appointment.date) }}</div>
                      <div class="date-month">{{ formatAppointmentMonth(appointment.date) }}</div>
                    </div>
                  </el-col>
                  <el-col :span="18">
                    <div class="appointment-details">
                      <h4>{{ appointment.departmentName }} - {{ appointment.doctorName }}</h4>
                      <p>时间: {{ formatAppointmentTime(appointment.date) }}</p>
                      <p>号码: {{ appointment.queueNumber }}</p>
                      <p>状态: 
                        <el-tag :type="getStatusType(appointment.status)">
                          {{ getStatusText(appointment.status) }}
                        </el-tag>
                      </p>
                    </div>
                  </el-col>
                </el-row>
                <div class="appointment-actions">
                  <el-button 
                    v-if="appointment.status === 'waiting'" 
                    type="danger" 
                    size="small" 
                    @click="cancelAppointment(appointment.id)"
                  >
                    取消挂号
                  </el-button>
                  <el-button 
                    v-if="appointment.status === 'completed'" 
                    type="primary" 
                    size="small" 
                    @click="viewPrescription(appointment.prescriptionId)"
                  >
                    查看处方
                  </el-button>
                </div>
              </div>
            </template>
            
            <el-empty v-else description="暂无挂号记录" />
          </div>
        </el-card>
      </el-col>

      <el-col :xs="24" :md="12">
        <!-- 健康数据卡片 -->
        <el-card class="dashboard-card">
          <template #header>
            <div class="card-header">
              <h3>健康数据</h3>
              <el-button text @click="refreshHealthData">刷新</el-button>
            </div>
          </template>
          <div class="card-body" v-loading="loadingHealthData">
            <el-tabs>
              <el-tab-pane label="基础信息">
                <div class="health-data-container">
                  <div class="health-data-item">
                    <span class="label">身高</span>
                    <span class="value">{{ healthData.height }} cm</span>
                  </div>
                  <div class="health-data-item">
                    <span class="label">体重</span>
                    <span class="value">{{ healthData.weight }} kg</span>
                  </div>
                  <div class="health-data-item">
                    <span class="label">BMI</span>
                    <span class="value">{{ calculateBMI() }}</span>
                  </div>
                  <div class="health-data-item">
                    <span class="label">血型</span>
                    <span class="value">{{ healthData.bloodType }}</span>
                  </div>
                </div>
              </el-tab-pane>
              <el-tab-pane label="最近检测">
                <div class="health-data-container">
                  <div class="health-data-item">
                    <span class="label">血压</span>
                    <span class="value">{{ healthData.bloodPressure }}</span>
                  </div>
                  <div class="health-data-item">
                    <span class="label">血糖</span>
                    <span class="value">{{ healthData.bloodSugar }} mmol/L</span>
                  </div>
                  <div class="health-data-item">
                    <span class="label">心率</span>
                    <span class="value">{{ healthData.heartRate }} bpm</span>
                  </div>
                  <div class="health-data-item">
                    <span class="label">体温</span>
                    <span class="value">{{ healthData.temperature }} °C</span>
                  </div>
                </div>
                <div class="last-updated">最后更新时间: {{ formatDate(healthData.lastUpdated) }}</div>
              </el-tab-pane>
            </el-tabs>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-20">
      <el-col :xs="24" :md="24">
        <!-- 处方记录卡片 -->
        <el-card class="dashboard-card">
          <template #header>
            <div class="card-header">
              <h3>近期处方</h3>
              <el-button text @click="navigateToPrescription">查看全部</el-button>
            </div>
          </template>
          <div class="card-body" v-loading="loadingPrescriptions">
            <el-table 
              v-if="recentPrescriptions.length > 0"
              :data="recentPrescriptions"
              style="width: 100%"
              @row-click="viewPrescriptionDetails"
            >
              <el-table-column prop="id" label="处方编号" width="140" />
              <el-table-column prop="date" label="开具日期" width="180">
                <template #default="scope">{{ formatDate(scope.row.date) }}</template>
              </el-table-column>
              <el-table-column prop="doctorName" label="医生" width="120" />
              <el-table-column prop="department" label="科室" width="120" />
              <el-table-column prop="diagnosis" label="诊断" show-overflow-tooltip />
              <el-table-column label="操作" width="180" fixed="right">
                <template #default="scope">
                  <el-button type="primary" size="small" @click.stop="viewPrescription(scope.row.id)">
                    查看详情
                  </el-button>
                  <el-button type="info" size="small" @click.stop="printPrescription(scope.row.id)">
                    打印
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
            
            <el-empty v-else description="暂无处方记录" />
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

export default {
  name: 'PatientDashboard',
  setup() {
    const router = useRouter()
    
    // 患者信息
    const patientId = ref('patient123')
    const patientName = ref('张三')
    
    // 加载状态
    const loadingAppointments = ref(false)
    const loadingHealthData = ref(false)
    const loadingPrescriptions = ref(false)
    
    // 当前日期
    const currentDate = computed(() => {
      const now = new Date()
      const options = { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' }
      return now.toLocaleDateString('zh-CN', options)
    })
    
    // 挂号记录
    const upcomingAppointments = ref([
      {
        id: 'apt20250422001',
        departmentId: 'dept001',
        departmentName: '内科',
        doctorId: 'doctor123',
        doctorName: '李医生',
        date: '2025-04-23T10:30:00',
        queueNumber: 'A12',
        status: 'waiting'
      },
      {
        id: 'apt20250415002',
        departmentId: 'dept002',
        departmentName: '外科',
        doctorId: 'doctor456',
        doctorName: '王医生',
        date: '2025-04-18T09:15:00',
        queueNumber: 'B05',
        status: 'completed',
        prescriptionId: 'RX20250418003'
      }
    ])
    
    // 健康数据
    const healthData = ref({
      height: 175,
      weight: 68,
      bloodType: 'O型',
      bloodPressure: '120/80 mmHg',
      bloodSugar: 5.4,
      heartRate: 72,
      temperature: 36.5,
      lastUpdated: '2025-04-20T14:30:00'
    })
    
    // 近期处方
    const recentPrescriptions = ref([
      {
        id: 'RX20250418003',
        patientId: 'patient123',
        doctorId: 'doctor456',
        doctorName: '王医生',
        department: '外科',
        date: '2025-04-18T09:30:00',
        diagnosis: '肌肉拉伤',
        medicines: [
          { name: '扶他林软膏', specification: '20g/支', quantity: 1, usage: '每日涂抹患处2-3次' },
          { name: '布洛芬缓释胶囊', specification: '0.3g*10粒/盒', quantity: 2, usage: '一日两次，饭后服用，一次一粒' }
        ],
        instructions: '避免剧烈运动，保持患处休息'
      },
      {
        id: 'RX20250405001',
        patientId: 'patient123',
        doctorId: 'doctor123',
        doctorName: '李医生',
        department: '内科',
        date: '2025-04-05T14:15:00',
        diagnosis: '感冒',
        medicines: [
          { name: '感冒灵颗粒', specification: '10g*9包/盒', quantity: 1, usage: '一日三次，温开水冲服，一次一包' },
          { name: '维生素C片', specification: '100mg*60片/瓶', quantity: 1, usage: '一日一次，饭后服用，一次一片' }
        ],
        instructions: '多休息，多喝水，避免辛辣食物'
      }
    ])
    
    // 计算BMI
    const calculateBMI = () => {
      const height = healthData.value.height / 100 // 转换为米
      const weight = healthData.value.weight
      if (height && weight) {
        const bmi = (weight / (height * height)).toFixed(1)
        return bmi
      }
      return 'N/A'
    }
    
    // 格式化日期
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
    }
    
    // 格式化挂号日期
    const formatAppointmentDay = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return String(date.getDate()).padStart(2, '0')
    }
    
    const formatAppointmentMonth = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      const months = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月']
      return months[date.getMonth()]
    }
    
    const formatAppointmentTime = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return `${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
    }
    
    // 获取状态类型
    const getStatusType = (status) => {
      switch (status) {
        case 'waiting':
          return 'warning'
        case 'in_progress':
          return 'primary'
        case 'completed':
          return 'success'
        case 'cancelled':
          return 'info'
        default:
          return 'info'
      }
    }
    
    // 获取状态文本
    const getStatusText = (status) => {
      switch (status) {
        case 'waiting':
          return '等待中'
        case 'in_progress':
          return '就诊中'
        case 'completed':
          return '已完成'
        case 'cancelled':
          return '已取消'
        default:
          return '未知状态'
      }
    }
    
    // 取消挂号
    const cancelAppointment = (appointmentId) => {
      // 实际项目中应该调用API取消挂号
      const index = upcomingAppointments.value.findIndex(apt => apt.id === appointmentId)
      if (index !== -1) {
        upcomingAppointments.value[index].status = 'cancelled'
        ElMessage.success('已成功取消挂号')
      }
    }
    
    // 查看处方
    const viewPrescription = (prescriptionId) => {
      router.push(`/patient/prescription?id=${prescriptionId}`)
    }
    
    // 查看处方详情
    const viewPrescriptionDetails = (row) => {
      viewPrescription(row.id)
    }
    
    // 打印处方
    const printPrescription = (prescriptionId) => {
      ElMessage.success(`正在打印处方 ${prescriptionId}`)
      
      // 实际项目中应该调用打印功能
    }
    
    // 刷新健康数据
    const refreshHealthData = () => {
      loadingHealthData.value = true
      
      // 模拟API调用
      setTimeout(() => {
        // 实际项目中应该从服务器获取最新数据
        healthData.value.lastUpdated = new Date().toISOString()
        loadingHealthData.value = false
        ElMessage.success('健康数据已更新')
      }, 1000)
    }
    
    // 导航到挂号页面
    const navigateToQueue = () => {
      router.push('/patient/queue')
    }
    
    // 导航到处方页面
    const navigateToPrescription = () => {
      router.push('/patient/prescription')
    }

    // 导航函数
    const goToQueue = () => {
      router.push('/patient/queue')
    }

    const goToPrescription = () => {
      router.push('/patient/prescription')
    }
    
    // 初始化
    onMounted(() => {
      // 加载挂号记录
      loadingAppointments.value = true
      setTimeout(() => {
        // 实际项目中应该从服务器获取数据
        loadingAppointments.value = false
      }, 800)
      
      // 加载健康数据
      loadingHealthData.value = true
      setTimeout(() => {
        // 实际项目中应该从服务器获取数据
        loadingHealthData.value = false
      }, 1000)
      
      // 加载处方记录
      loadingPrescriptions.value = true
      setTimeout(() => {
        // 实际项目中应该从服务器获取数据
        loadingPrescriptions.value = false
      }, 1200)
    })
    
    return {
      patientId,
      patientName,
      currentDate,
      upcomingAppointments,
      healthData,
      recentPrescriptions,
      loadingAppointments,
      loadingHealthData,
      loadingPrescriptions,
      calculateBMI,
      formatDate,
      formatAppointmentDay,
      formatAppointmentMonth,
      formatAppointmentTime,
      getStatusType,
      getStatusText,
      cancelAppointment,
      viewPrescription,
      viewPrescriptionDetails,
      printPrescription,
      refreshHealthData,
      navigateToQueue,
      navigateToPrescription,
      goToQueue,
      goToPrescription
    }
  }
}
</script>

<style scoped>
.patient-dashboard {
  padding: 20px;
}

.dashboard-header {
  margin-bottom: 20px;
}

.dashboard-header h1 {
  margin: 0 0 10px 0;
  font-size: 24px;
}

.dashboard-header p {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.dashboard-card {
  margin-bottom: 20px;
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
}

.card-body {
  padding: 10px 0;
}

.mt-20 {
  margin-top: 20px;
}

/* 挂号样式 */
.appointment-item {
  border-bottom: 1px solid #ebeef5;
  padding: 15px 0;
}

.appointment-item:last-child {
  border-bottom: none;
}

.appointment-date {
  background-color: #f0f9eb;
  border-radius: 5px;
  padding: 8px 0;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.date-day {
  font-size: 24px;
  font-weight: bold;
  color: #409EFF;
}

.date-month {
  font-size: 12px;
  color: #606266;
}

.appointment-details {
  padding-left: 10px;
}

.appointment-details h4 {
  margin: 0 0 5px 0;
  font-size: 16px;
}

.appointment-details p {
  margin: 5px 0;
  color: #606266;
  font-size: 14px;
}

.appointment-actions {
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;
}

/* 健康数据样式 */
.health-data-container {
  display: flex;
  flex-wrap: wrap;
  padding: 10px 0;
}

.health-data-item {
  width: 50%;
  margin-bottom: 15px;
  padding-right: 10px;
  box-sizing: border-box;
}

.label {
  display: block;
  color: #909399;
  font-size: 13px;
  margin-bottom: 4px;
}

.value {
  display: block;
  font-size: 18px;
  font-weight: 500;
  color: #303133;
}

.last-updated {
  margin-top: 15px;
  text-align: right;
  font-size: 12px;
  color: #909399;
}

@media screen and (max-width: 768px) {
  .health-data-item {
    width: 100%;
  }
}

.header-actions {
  display: flex;
  gap: 10px;
}
</style>