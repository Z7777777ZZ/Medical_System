<template>
  <div class="doctor-queue-view">
    <el-row :gutter="20">
      <!-- 左侧队列面板 -->
      <el-col :span="16">
        <el-card class="queue-card">
          <template #header>
            <div class="card-header">
              <h3>患者候诊队列</h3>
              <div class="header-actions">
                <el-button type="primary" @click="callNextPatient" :disabled="!queueStore.nextPatient">
                  叫号接诊
                </el-button>
                <el-button @click="refreshQueue">
                  <el-icon><Refresh /></el-icon>刷新
                </el-button>
                <el-button type="primary" @click="goToDashboard">返回工作台</el-button>
                <el-button type="success" @click="goToPrescription">处方管理</el-button>
              </div>
            </div>
          </template>
          
          <div class="queue-content">
            <el-tabs v-model="activeQueueTab">
              <el-tab-pane label="检查后优先队列" name="priority">
                <el-empty v-if="priorityQueue.length === 0" description="暂无检查后优先患者"></el-empty>
                <el-table v-else :data="priorityQueue" style="width: 100%">
                  <el-table-column prop="queueNumber" label="序号" width="80" />
                  <el-table-column prop="name" label="患者姓名" />
                  <el-table-column prop="gender" label="性别" width="80">
                    <template #default="scope">
                      {{ scope.row.gender === 'male' ? '男' : 
                         (scope.row.gender === 'female' ? '女' : '未知') }}
                    </template>
                  </el-table-column>
                  <el-table-column prop="age" label="年龄" width="80" />
                  <el-table-column prop="visitReason" label="就诊原因" />
                  <el-table-column prop="waitingTime" label="等待时间" width="120">
                    <template #default="scope">
                      {{ formatWaitingTime(scope.row.registerTime) }}
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" width="150" fixed="right">
                    <template #default="scope">
                      <el-button 
                        type="primary" 
                        size="small" 
                        @click="callSpecificPatient(scope.row)"
                      >
                        叫号
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>
              
              <el-tab-pane label="普通候诊队列" name="normal">
                <el-empty v-if="normalQueue.length === 0" description="暂无候诊患者"></el-empty>
                <el-table v-else :data="normalQueue" style="width: 100%">
                  <el-table-column prop="queueNumber" label="序号" width="80" />
                  <el-table-column prop="name" label="患者姓名" />
                  <el-table-column prop="gender" label="性别" width="80">
                    <template #default="scope">
                      {{ scope.row.gender === 'male' ? '男' : 
                         (scope.row.gender === 'female' ? '女' : '未知') }}
                    </template>
                  </el-table-column>
                  <el-table-column prop="age" label="年龄" width="80" />
                  <el-table-column prop="visitReason" label="就诊原因" />
                  <el-table-column prop="waitingTime" label="等待时间" width="120">
                    <template #default="scope">
                      {{ formatWaitingTime(scope.row.registerTime) }}
                    </template>
                  </el-table-column>
                  <el-table-column label="操作" width="150" fixed="right">
                    <template #default="scope">
                      <el-button 
                        type="primary" 
                        size="small" 
                        @click="callSpecificPatient(scope.row)"
                      >
                        叫号
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>
            </el-tabs>
          </div>
        </el-card>
      </el-col>
      
      <!-- 右侧当前接诊患者面板 -->
      <el-col :span="8">
        <el-card class="patient-card">
          <template #header>
            <div class="card-header">
              <h3>当前接诊患者</h3>
            </div>
          </template>
          
          <div class="patient-content">
            <el-empty v-if="!currentPatient" description="暂无接诊患者"></el-empty>
            <div v-else class="current-patient-info">
              <div class="patient-avatar">
                <el-avatar :size="80" :icon="UserFilled" />
              </div>
              <div class="patient-details">
                <h2>{{ currentPatient.name || '未知患者' }}</h2>
                <p v-if="currentPatient.gender"><span class="detail-label">性别:</span> {{ currentPatient.gender === 'male' ? '男' : (currentPatient.gender === 'female' ? '女' : '未知') }}</p>
                <p v-if="currentPatient.age"><span class="detail-label">年龄:</span> {{ currentPatient.age }}岁</p>
                <p v-if="currentPatient.visitReason"><span class="detail-label">就诊原因:</span> {{ currentPatient.visitReason }}</p>
                <p v-if="currentPatient.medicalHistory"><span class="detail-label">病史:</span> {{ currentPatient.medicalHistory }}</p>
              </div>
              
              <div class="diagnosis-actions">
                <el-button-group>
                  <el-button type="primary" @click="openPrescriptionDialog">开处方</el-button>
                  <el-button type="warning" @click="sendToExam">去检查</el-button>
                  <el-button type="success" @click="finishDiagnosis">结束诊断</el-button>
                </el-button-group>
              </div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 开处方弹窗 -->
    <el-dialog v-model="prescriptionDialogVisible" title="开具处方" width="60%" @closed="closePrescriptionDialog">
      <prescription-form v-if="prescriptionDialogVisible && currentPatient" :patient="currentPatient" @submit="submitPrescription" />
    </el-dialog>
    
    <!-- 去检查确认弹窗 -->
    <el-dialog v-model="examDialogVisible" title="患者检查" width="30%">
      <p>是否确认 {{ currentPatient?.name }} 需要去做检查?</p>
      <p class="exam-notice">检查完成后，患者将自动进入优先队列</p>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="examDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmExam">确认</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 结束诊断确认弹窗 -->
    <el-dialog v-model="finishDialogVisible" title="结束诊断" width="30%">
      <p>是否确认结束当前患者 {{ currentPatient?.name }} 的诊断?</p>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="finishDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmFinishDiagnosis">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted, defineAsyncComponent } from 'vue'
import { useQueueStore } from '../../stores/queueStore'
import { usePrescriptionStore } from '../../stores/prescriptionStore'
import { UserFilled, Refresh } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { jwtDecode } from 'jwt-decode'

// 异步加载处方表单组件
const PrescriptionForm = defineAsyncComponent(() => 
  import('../../components/doctor/PrescriptionForm.vue')
)

export default {
  name: 'DoctorQueue',
  components: {
    PrescriptionForm,
    UserFilled,
    Refresh
  },
  setup() {
    const router = useRouter()
    const token = localStorage.getItem('token'); // 获取 token
    let doctorId = null;
    let type = null;

    // 从 token 中解析出 doctor_id
    if (token) {
      try {
        const decodedToken = jwtDecode(token);
        // token 中的 payload 应该包含 identity.id
        doctorId = decodedToken.sub.id || decodedToken.id;
        type = decodedToken.sub.type || decodedToken.type;
        if (type !== 'doctor') {
          console.error('Token 中的身份类型不是医生');
          return;
        }
        console.log('从 token 解析出的 doctor_id:', doctorId);
      } catch (error) {
        console.error('解析 token 失败:', error);
      }
    } else {
      // 如果没有 token，可能需要重定向到登录页
      console.error('未找到 token');
    }
    
    // 存储实例
    const queueStore = useQueueStore()
    const prescriptionStore = usePrescriptionStore()
    
    // 激活的队列标签
    const activeQueueTab = ref('normal')
    
    // 提取队列数据
    const normalQueue = computed(() => queueStore.normalQueue)
    const priorityQueue = computed(() => queueStore.priorityQueue)
    const currentPatient = computed(() => queueStore.currentPatient)
    
    // 弹窗状态
    const prescriptionDialogVisible = ref(false)
    const examDialogVisible = ref(false)
    const finishDialogVisible = ref(false)
    
    // 初始化
    onMounted(async () => {
      console.log('组件挂载，准备初始化数据. doctorId:', doctorId)
      if (doctorId) {
        try {
          // 使用初始化数据方法，同时获取队列和当前患者
          await queueStore.initData('doctor', doctorId)
          console.log('初始化数据完成')
        } catch (error) {
          console.error('初始化数据失败:', error)
          ElMessage.error('数据加载失败，请刷新页面重试')
        }
      } else {
        console.error('没有有效的医生ID，无法加载数据')
        ElMessage.warning('请先登录')
      }
    })
    
    // 刷新队列
    const refreshQueue = async () => {
      console.log('Refreshing queue data...')
      try {
        await queueStore.fetchQueueData('doctor', doctorId)
        // 同时刷新当前患者信息
        // await queueStore.fetchCurrentPatient('doctor', doctorId)
        ElMessage.success('刷新成功')
      } catch (error) {
        console.error('刷新队列失败:', error)
        ElMessage.error('刷新失败，请重试')
      }
    }
    
    // 叫下一个患者
    const callNextPatient = async () => {
      if (!queueStore.nextPatient) {
        ElMessage.warning('当前没有等待的患者')
        return
      }
      console.log('正在叫号...')
      try {
        await queueStore.callNextPatient(doctorId) // 使用从token解析出的医生ID
        ElMessage.success('叫号成功')
        // 叫号成功后刷新队列
        await refreshQueue()
      } catch (error) {
        console.error('叫号失败:', error)
        ElMessage.error('叫号失败，请重试')
      }
    }
    
    // 叫特定患者
    const callSpecificPatient = async (patient) => {
      try {
        ElMessage.info(`正在叫号患者: ${patient.name}`)
        // 使用患者ID调用特定患者
        await queueStore.callSpecificPatient(doctorId, patient.id)
        ElMessage.success(`成功叫号患者: ${patient.name}`)
        // 刷新队列
        await refreshQueue()
      } catch (error) {
        console.error('叫号失败:', error)
        ElMessage.error('叫号失败，请重试')
      }
    }
    
    // 格式化等待时间
    const formatWaitingTime = (registerTime) => {
      const now = new Date()
      const registerDate = new Date(registerTime)
      const diffMs = now - registerDate
      const diffMins = Math.floor(diffMs / 60000)
      
      if (diffMins < 60) {
        return `${diffMins} 分钟`
      } else {
        const hours = Math.floor(diffMins / 60)
        const mins = diffMins % 60
        return `${hours} 小时 ${mins} 分钟`
      }
    }
    
    // 开处方
    const openPrescriptionDialog = () => {
      if (!currentPatient.value) {
        ElMessage.warning('请先选择患者')
        return
      }
      
      prescriptionStore.createNewPrescription(
        currentPatient.value.id,
        doctorId // 使用从token解析出的医生ID
      )
      prescriptionDialogVisible.value = true
    }
    
    // 关闭处方弹窗
    const closePrescriptionDialog = () => {
      prescriptionStore.clearCurrentPrescription()
    }
    
    // 提交处方
    const submitPrescription = async () => {
      await prescriptionStore.savePrescription()
      prescriptionDialogVisible.value = false
      ElMessage.success('处方已保存')
    }
    
    // 去检查
    const sendToExam = () => {
      if (!currentPatient.value) {
        ElMessage.warning('请先选择患者')
        return
      }
      
      examDialogVisible.value = true
    }
    
    // 确认去检查
    const confirmExam = async () => {
      if (!currentPatient.value) {
        ElMessage.warning('请先选择患者')
        return
      }
      
      try {
        // await queueStore.returnToQueueAfterExam(currentPatient.value.id, doctorId)
        examDialogVisible.value = false
        // ElMessage.success('患者已去检查，完成后将加入优先队列')
        // 清除当前患者
        queueStore.currentPatient = null
      } catch (error) {
        ElMessage.error('操作失败，请重试')
      }
    }
    
    // 结束诊断
    const finishDiagnosis = () => {
      if (!currentPatient.value) {
        ElMessage.warning('请先选择患者')
        return
      }
      
      finishDialogVisible.value = true
    }
    
    // 确认结束诊断
    const confirmFinishDiagnosis = async () => {
      if (!currentPatient.value) {
        ElMessage.warning('请先选择患者')
        return
      }
      
      try {
        await queueStore.finishDiagnosis(currentPatient.value.id)
        finishDialogVisible.value = false
        ElMessage.success('诊断已结束')
      } catch (error) {
        ElMessage.error('操作失败，请重试')
      }
    }

    // 导航函数
    const goToDashboard = () => {
      router.push('/doctor/dashboard')
    }

    const goToPrescription = () => {
      router.push('/doctor/prescription')
    }
    
    return {
      UserFilled,
      activeQueueTab,
      queueStore,
      normalQueue,
      priorityQueue,
      currentPatient,
      prescriptionDialogVisible,
      examDialogVisible,
      finishDialogVisible,
      refreshQueue,
      callNextPatient,
      callSpecificPatient,
      formatWaitingTime,
      openPrescriptionDialog,
      closePrescriptionDialog,
      submitPrescription,
      sendToExam,
      confirmExam,
      finishDiagnosis,
      confirmFinishDiagnosis,
      goToDashboard,
      goToPrescription
    }
  }
}
</script>

<style scoped>
.doctor-queue-view {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.queue-card {
  margin-bottom: 20px;
}

.queue-content {
  min-height: 400px;
}

.patient-content {
  min-height: 300px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.current-patient-info {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
}

.patient-avatar {
  margin-bottom: 20px;
}

.patient-details {
  width: 100%;
  margin-bottom: 30px;
  text-align: center;
}

.patient-details h2 {
  margin-bottom: 15px;
  color: #303133;
}

.patient-details p {
  margin-bottom: 10px;
  color: #606266;
}

.detail-label {
  font-weight: bold;
  margin-right: 5px;
}

.diagnosis-actions {
  margin-top: 20px;
}

.exam-notice {
  color: #E6A23C;
  font-size: 14px;
  margin-top: 10px;
}
</style>