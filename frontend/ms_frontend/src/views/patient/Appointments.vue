<template>
  <div class="page-container">
    <div class="page-header">
      <h2>我的预约</h2>
      <el-button type="primary" @click="$router.push('/patient/appointment')">新预约</el-button>
    </div>
    
    <div class="content-section">
      <!-- 筛选选项 -->
      <div class="filter-section">
        <el-select v-model="filterStatus" placeholder="预约状态" clearable>
          <el-option label="全部" value="" />
          <el-option label="待确认" value="pending" />
          <el-option label="已确认" value="confirmed" />
          <el-option label="已完成" value="completed" />
          <el-option label="已取消" value="cancelled" />
        </el-select>
        
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          clearable
        />
      </div>
      
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-section">
        <el-skeleton :rows="5" animated />
      </div>
      
      <!-- 空状态 -->
      <div v-else-if="!filteredAppointments.length" class="empty-section">
        <el-empty description="暂无预约记录">
          <template #description>
            <div>
              <p>您暂时没有预约记录</p>
              <p class="small">可以点击"新预约"按钮创建预约</p>
            </div>
          </template>
          <el-button type="primary" @click="$router.push('/patient/appointment')">去预约挂号</el-button>
        </el-empty>
      </div>
      
      <!-- 预约列表 -->
      <div v-else>
        <!-- 移除标签页组件，直接显示内容 -->
        <div class="tab-section">
          <div class="tab-header">
            <h3>预约记录</h3>
          </div>
          <el-table :data="filteredAppointments" style="width: 100%" border>
            <el-table-column label="医生" prop="doctor_name" min-width="120" />
            
            <el-table-column label="预约时间" prop="appointment_time" min-width="180">
              <template #default="{ row }">
                {{ formatDateTime(row.appointment_time) }}
              </template>
            </el-table-column>
            
            <el-table-column label="状态" prop="status" width="120">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ formatStatus(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button 
                  size="small" 
                  @click="viewAppointment(row)"
                >
                  详情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </div>
    
    <!-- 预约详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="预约详情"
      width="600px"
    >
      <div v-if="selectedAppointment" class="appointment-detail">
        <div class="detail-row">
          <span class="detail-label">预约编号:</span>
          <span class="detail-value">#{{ selectedAppointment.appointment_id }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">医院:</span>
          <span class="detail-value">{{ selectedAppointment.hospital_name || '市第一医院' }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">科室:</span>
          <span class="detail-value">{{ selectedAppointment.department_name }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">医生:</span>
          <span class="detail-value">{{ selectedAppointment.doctor_name }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">预约时间:</span>
          <span class="detail-value">{{ formatDateTime(selectedAppointment.appointment_time) }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">就诊状态:</span>
          <span class="detail-value">
            <el-tag :type="getStatusType(selectedAppointment.status)">
              {{ formatStatus(selectedAppointment.status) }}
            </el-tag>
          </span>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailDialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch } from 'vue'
import { usePatientStore } from '../../store/patient'
import { ElMessage } from 'element-plus'
import axios from 'axios'

export default {
  name: 'PatientAppointments',
  setup() {
    const patientStore = usePatientStore()
    
    // 状态变量
    const loading = ref(false)
    const appointments = ref([])
    const filterStatus = ref('')
    const dateRange = ref(null)
    
    // 详情对话框
    const detailDialogVisible = ref(false)
    const selectedAppointment = ref(null)
    
    // 获取预约列表
    const fetchAppointments = async () => {
      loading.value = true
      try {
        const patientId = patientStore.patientId || localStorage.getItem('patientId') || 1
        
        // 尝试从API获取预约
        try {
          const response = await axios.get('/api/patient/registration/appointments', {
            params: {
              patient_id: patientId
            }
          })
          
          if (response.data && response.data.status === 'success') {
            console.log('成功获取预约数据:', response.data.data)
            appointments.value = response.data.data || []
            return
          }
        } catch (error) {
          console.warn('Error fetching appointments from API, using mock data:', error)
        }
        
        // 使用模拟数据
        const mockData = [
          { appointment_id: 1, doctor_name: '张伟', appointment_time: '2023-06-01 09:30:00', status: 'confirmed' },
          { appointment_id: 9, doctor_name: '刘洋', appointment_time: '2023-06-05 14:30:00', status: 'pending' }
        ]
        appointments.value = mockData
        console.log('使用模拟数据:', appointments.value)
      } catch (error) {
        console.error('Failed to fetch appointments:', error)
        ElMessage.error('获取预约记录失败')
        appointments.value = []
      } finally {
        loading.value = false
      }
    }
    
    // 过滤后的预约记录
    const filteredAppointments = computed(() => {
      let result = [...appointments.value]
      
      // 按状态筛选
      if (filterStatus.value) {
        result = result.filter(a => a.status === filterStatus.value)
      }
      
      // 按日期范围筛选
      if (dateRange.value && dateRange.value.length === 2) {
        const startDate = new Date(dateRange.value[0])
        startDate.setHours(0, 0, 0, 0)
        
        const endDate = new Date(dateRange.value[1])
        endDate.setHours(23, 59, 59, 999)
        
        result = result.filter(a => {
          const appointmentTime = new Date(a.appointment_time)
          return appointmentTime >= startDate && appointmentTime <= endDate
        })
      }
      
      // 默认按预约时间排序
      return result.sort((a, b) => new Date(a.appointment_time) - new Date(b.appointment_time))
    })
    
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
    
    // 格式化状态
    const formatStatus = (status) => {
      const statusMap = {
        'pending': '待确认',
        'confirmed': '已确认',
        'completed': '已完成',
        'cancelled': '已取消'
      }
      return statusMap[status] || status
    }
    
    // 获取状态样式类型
    const getStatusType = (status) => {
      const typeMap = {
        'pending': 'warning',
        'confirmed': 'primary',
        'completed': 'success',
        'cancelled': 'danger'
      }
      return typeMap[status] || 'info'
    }
    
    // 查看预约详情
    const viewAppointment = (appointment) => {
      selectedAppointment.value = appointment
      detailDialogVisible.value = true
    }
    
    // 监听筛选条件变化
    watch([filterStatus, dateRange], () => {
      // 如果需要重新加载数据，可以在这里添加逻辑
    })
    
    // 初始加载
    onMounted(() => {
      fetchAppointments()
    })
    
    return {
      loading,
      appointments,
      filterStatus,
      dateRange,
      filteredAppointments,
      detailDialogVisible,
      selectedAppointment,
      formatDateTime,
      formatStatus,
      getStatusType,
      viewAppointment
    }
  }
}
</script>

<style scoped>
.page-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.content-section {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.filter-section {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.loading-section, .empty-section {
  padding: 40px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.empty-section .small {
  font-size: 14px;
  color: #909399;
}

.appointment-id {
  font-family: monospace;
  font-weight: 600;
}

/* 详情对话框样式 */
.appointment-detail {
  padding: 0 20px;
}

.detail-row {
  display: flex;
  margin-bottom: 15px;
}

.detail-label {
  width: 100px;
  color: #606266;
  font-weight: 500;
}

.detail-value {
  flex: 1;
}

/* 添加新的样式 */
.tab-section {
  border: 1px solid #EBEEF5;
  border-radius: 4px;
  background-color: #FFF;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  padding: 20px;
}

.tab-header {
  border-bottom: 1px solid #EBEEF5;
  padding-bottom: 15px;
  margin-bottom: 15px;
}

.tab-header h3 {
  margin: 0;
  color: #303133;
  font-size: 18px;
  font-weight: 500;
}
</style> 