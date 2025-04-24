<template>
  <div class="patient-queue">
    <el-card class="queue-card">
      <template #header>
        <div class="card-header">
          <h3>排队信息</h3>
          <div class="header-actions">
            <el-button type="primary" @click="goToDashboard">返回主页</el-button>
            <el-button type="success" @click="goToPrescription">我的处方</el-button>
          </div>
        </div>
      </template>

      <div class="patient-queue-view">
        <el-row :gutter="20">
          <!-- 左侧排队状态卡片 -->
          <el-col :span="16">
            <el-card class="queue-status-card">
              <template #header>
                <div class="card-header">
                  <h3>我的排队状态</h3>
                  <el-button @click="refreshStatus" :loading="loading">
                    <el-icon><el-icon-refresh /></el-icon>刷新
                  </el-button>
                </div>
              </template>
              
              <div class="queue-status-content">
                <div v-if="myQueueInfo" class="queue-info">
                  <div class="queue-number">
                    <span>您的排队号</span>
                    <div class="number">{{ myQueueInfo.queueNumber }}</div>
                  </div>
                  
                  <el-divider />
                  
                  <div class="status-info">
                    <div class="status-item">
                      <div class="item-label">前面等待</div>
                      <div class="item-value">{{ myQueueInfo.ahead }} 人</div>
                    </div>
                    <div class="status-item">
                      <div class="item-label">预计等待</div>
                      <div class="item-value">{{ myQueueInfo.estimatedWaitTime }} 分钟</div>
                    </div>
                    <div class="status-item">
                      <div class="item-label">目前状态</div>
                      <div class="item-value" :class="'status-' + myQueueInfo.status">
                        {{ getStatusText(myQueueInfo.status) }}
                      </div>
                    </div>
                  </div>
                  
                  <el-divider />
                  
                  <div class="current-calling">
                    <h4>当前叫号</h4>
                    <div v-if="currentCalling" class="calling-number">
                      {{ currentCalling.queueNumber }}
                    </div>
                    <div v-else class="no-calling">
                      暂无叫号
                    </div>
                  </div>
                </div>
                
                <div v-else-if="loading" class="loading-placeholder">
                  <el-skeleton animated :rows="6" />
                </div>
                
                <el-empty v-else description="您当前不在排队队列中">
                  <el-button type="primary" @click="showRegisterDialog">立即挂号</el-button>
                </el-empty>
              </div>
            </el-card>
          </el-col>
          
          <!-- 右侧诊室信息卡片 -->
          <el-col :span="8">
            <el-card class="clinic-info-card">
              <template #header>
                <div class="card-header">
                  <h3>诊室信息</h3>
                </div>
              </template>
              
              <div class="clinic-info-content">
                <div v-if="clinicInfo" class="clinic-details">
                  <h4>{{ clinicInfo.name }}</h4>
                  <p><span class="info-label">位置:</span> {{ clinicInfo.location }}</p>
                  <p><span class="info-label">医生:</span> {{ clinicInfo.doctorName }}</p>
                  <p><span class="info-label">专科:</span> {{ clinicInfo.specialty }}</p>
                  <p><span class="info-label">工作时间:</span> {{ clinicInfo.workingHours }}</p>
                  <p v-if="clinicInfo.notice"><span class="info-label">公告:</span> {{ clinicInfo.notice }}</p>
                  
                  <div class="clinic-actions">
                    <el-button type="primary" @click="showClinicLocation">查看位置</el-button>
                  </div>
                </div>
                
                <div v-else-if="loading" class="loading-placeholder">
                  <el-skeleton animated :rows="4" />
                </div>
                
                <el-empty v-else description="暂无诊室信息" />
              </div>
            </el-card>
            
            <el-card class="notice-card">
              <template #header>
                <div class="card-header">
                  <h3>就诊须知</h3>
                </div>
              </template>
              
              <div class="notice-content">
                <ul class="notice-list">
                  <li>请保持手机畅通，以便及时收到叫号通知</li>
                  <li>叫号后请携带身份证或就诊卡前往指定诊室</li>
                  <li>如需取消排队，请提前操作以减少他人等待时间</li>
                  <li>如需检查，请遵医嘱前往相应科室</li>
                  <li>检查完成后请尽快返回诊室继续就诊</li>
                </ul>
              </div>
            </el-card>
          </el-col>
        </el-row>
        
        <!-- 全部队列展示 -->
        <el-card class="queue-list-card">
          <template #header>
            <div class="card-header">
              <h3>当前候诊队列</h3>
            </div>
          </template>
          
          <div class="queue-list-content">
            <el-table 
              v-if="queueList.length > 0"
              :data="queueList" 
              style="width: 100%"
              max-height="400">
              <el-table-column prop="queueNumber" label="排队号" width="100" />
              <el-table-column prop="patientName" label="患者姓名">
                <template #default="scope">
                  <span v-if="scope.row.isCurrentUser" class="current-user">
                    {{ scope.row.patientName }} (我)
                  </span>
                  <span v-else>{{ maskName(scope.row.patientName) }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="visitReason" label="就诊原因" />
              <el-table-column prop="status" label="状态">
                <template #default="scope">
                  <el-tag :type="getStatusTagType(scope.row.status)">
                    {{ getStatusText(scope.row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="waitingTime" label="等待时间" width="120" />
            </el-table>
            
            <div v-else-if="loading" class="loading-placeholder">
              <el-skeleton animated :rows="6" />
            </div>
            
            <el-empty v-else description="当前没有患者在排队" />
          </div>
        </el-card>
        
        <!-- 挂号对话框 -->
        <el-dialog v-model="registerDialogVisible" title="门诊挂号" width="30%">
          <el-form :model="registerForm" label-width="80px" :rules="registerRules" ref="registerFormRef">
            <el-form-item label="就诊原因" prop="visitReason">
              <el-input v-model="registerForm.visitReason" placeholder="请简要描述就诊原因"></el-input>
            </el-form-item>
            <el-form-item label="科室" prop="department">
              <el-select v-model="registerForm.department" placeholder="请选择科室" style="width: 100%">
                <el-option v-for="dept in departments" :key="dept.value" :label="dept.label" :value="dept.value"></el-option>
              </el-select>
            </el-form-item>
          </el-form>
          <template #footer>
            <span class="dialog-footer">
              <el-button @click="registerDialogVisible = false">取消</el-button>
              <el-button type="primary" @click="submitRegister" :loading="registerLoading">
                确认挂号
              </el-button>
            </span>
          </template>
        </el-dialog>
        
        <!-- 诊室位置对话框 -->
        <el-dialog v-model="locationDialogVisible" title="诊室位置" width="50%">
          <div class="location-map">
            <img src="../../assets/images/clinic-map.png" alt="诊室位置图" class="clinic-map-img" />
            <div class="map-marker" :style="mapMarkerStyle"></div>
          </div>
          <div class="location-directions">
            <h4>位置指引</h4>
            <p>{{ clinicInfo?.locationDirections || '请从一楼大厅进入，乘坐电梯至2楼，沿指示牌前往相应诊室。' }}</p>
          </div>
        </el-dialog>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
// import { useQueueStore } from '../../stores/queueStore'
import { ElMessage } from 'element-plus'

export default {
  name: 'PatientQueue',
  setup() {
    const router = useRouter()
    // const queueStore = useQueueStore() - 不再使用store，改为静态数据
    
    // 状态
    const loading = ref(false)
    const registerDialogVisible = ref(false)
    const locationDialogVisible = ref(false)
    const registerLoading = ref(false)
    
    // 静态测试数据
    const myQueueInfo = ref({
      queueNumber: 'A016',
      ahead: 5,
      estimatedWaitTime: 25,
      status: 'waiting', // waiting, exam, calling, completed
      registerTime: new Date(Date.now() - 1800000) // 30分钟前
    })
    
    const currentCalling = ref({
      queueNumber: 'A012',
      patientName: '张**'
    })
    
    const clinicInfo = ref({
      name: '内科诊室 3号',
      location: '2楼 B区 205室',
      doctorName: '李医生',
      specialty: '内科/呼吸科',
      workingHours: '上午8:00-12:00, 下午13:30-17:30',
      notice: '目前患者较多，请耐心等待',
      mapX: 60,
      mapY: 40,
      locationDirections: '从一楼大厅进入，乘坐电梯至2楼，沿指示牌前往B区205室。'
    })
    
    const queueList = ref([
      { queueNumber: 'A012', patientName: '张三', visitReason: '发热', status: 'calling', waitingTime: '45分钟', isCurrentUser: false },
      { queueNumber: 'A013', patientName: '李四', visitReason: '咳嗽', status: 'waiting', waitingTime: '40分钟', isCurrentUser: false },
      { queueNumber: 'A014', patientName: '王五', visitReason: '头痛', status: 'exam', waitingTime: '35分钟', isCurrentUser: false },
      { queueNumber: 'A015', patientName: '赵六', visitReason: '腹痛', status: 'waiting', waitingTime: '30分钟', isCurrentUser: false },
      { queueNumber: 'A016', patientName: '陈七', visitReason: '感冒', status: 'waiting', waitingTime: '25分钟', isCurrentUser: true }
    ])
    
    // 挂号表单
    const registerFormRef = ref(null)
    const registerForm = reactive({
      visitReason: '',
      department: ''
    })
    
    // 表单验证规则
    const registerRules = {
      visitReason: [
        { required: true, message: '请输入就诊原因', trigger: 'blur' },
        { min: 2, max: 50, message: '长度应为2到50个字符', trigger: 'blur' }
      ],
      department: [
        { required: true, message: '请选择科室', trigger: 'change' }
      ]
    }
    
    // 科室列表 - 静态数据
    const departments = [
      { label: '内科', value: 'internal' },
      { label: '外科', value: 'surgery' },
      { label: '儿科', value: 'pediatrics' },
      { label: '妇产科', value: 'obstetrics' },
      { label: '眼科', value: 'ophthalmology' },
      { label: '耳鼻喉科', value: 'ent' },
      { label: '口腔科', value: 'dental' },
      { label: '皮肤科', value: 'dermatology' }
    ]
    
    // 刷新排队状态 - 使用静态数据模拟
    const refreshStatus = async () => {
      loading.value = true
      
      // 模拟API调用
      setTimeout(() => {
        // 随机更新一些数据来模拟刷新效果
        myQueueInfo.value.ahead = Math.max(0, myQueueInfo.value.ahead - Math.floor(Math.random() * 2));
        myQueueInfo.value.estimatedWaitTime = myQueueInfo.value.ahead * 5;
        
        if (myQueueInfo.value.ahead === 0 && myQueueInfo.value.status === 'waiting') {
          myQueueInfo.value.status = 'calling';
          currentCalling.value.queueNumber = myQueueInfo.value.queueNumber;
        }
        
        loading.value = false
        ElMessage.success('排队状态已更新')
      }, 1000)
    }
    
    // 获取状态文本描述
    const getStatusText = (status) => {
      switch (status) {
        case 'waiting':
          return '等待中'
        case 'calling':
          return '正在叫号'
        case 'exam':
          return '检查中'
        case 'completed':
          return '已完成'
        default:
          return '未知状态'
      }
    }
    
    // 获取状态标签类型
    const getStatusTagType = (status) => {
      switch (status) {
        case 'waiting':
          return 'info'
        case 'calling':
          return 'danger'
        case 'exam':
          return 'warning'
        case 'completed':
          return 'success'
        default:
          return 'info'
      }
    }
    
    // 隐藏姓名部分字符
    const maskName = (name) => {
      if (!name) return ''
      if (name.length <= 1) return name
      
      return name.charAt(0) + '*'.repeat(name.length - 1)
    }
    
    // 诊室位置标记样式
    const mapMarkerStyle = computed(() => {
      return {
        left: `${clinicInfo.value?.mapX || 0}%`,
        top: `${clinicInfo.value?.mapY || 0}%`
      }
    })
    
    // 显示挂号对话框
    const showRegisterDialog = () => {
      registerDialogVisible.value = true
    }
    
    // 提交挂号 - 使用静态数据模拟
    const submitRegister = async () => {
      if (!registerFormRef.value) return
      
      await registerFormRef.value.validate(async (valid) => {
        if (!valid) return
        
        registerLoading.value = true
        
        // 模拟API调用
        setTimeout(() => {
          registerLoading.value = false
          registerDialogVisible.value = false
          
          // 生成新的排队号
          const newQueueNumber = 'A' + (Number(queueList.value[queueList.value.length - 1].queueNumber.substring(1)) + 1).toString().padStart(3, '0');
          
          // 模拟成功挂号后的数据更新
          myQueueInfo.value = {
            queueNumber: newQueueNumber,
            ahead: queueList.value.length,
            estimatedWaitTime: queueList.value.length * 5,
            status: 'waiting',
            registerTime: new Date()
          }
          
          // 添加到队列末尾
          queueList.value.push({
            queueNumber: newQueueNumber,
            patientName: '当前用户',
            visitReason: registerForm.visitReason,
            status: 'waiting',
            waitingTime: '刚刚',
            isCurrentUser: true
          })
          
          // 重置旧的"我"的标记
          queueList.value.forEach(item => {
            if (item.queueNumber !== newQueueNumber) {
              item.isCurrentUser = false
            }
          })
          
          ElMessage.success('挂号成功，请留意叫号提醒')
          
          // 重置表单
          registerForm.visitReason = '';
          registerForm.department = '';
        }, 1500)
      })
    }
    
    // 显示诊室位置
    const showClinicLocation = () => {
      locationDialogVisible.value = true
    }
    
    // 导航函数
    const goToDashboard = () => {
      router.push('/patient/dashboard')
    }

    const goToPrescription = () => {
      router.push('/patient/prescription')
    }
    
    // 初始化
    onMounted(() => {
      // 不再初始化Socket连接
      // queueStore.initSocket()
      
      // 初始加载数据
      refreshStatus()
    })
    
    return {
      loading,
      myQueueInfo,
      currentCalling,
      clinicInfo,
      queueList,
      registerDialogVisible,
      locationDialogVisible,
      registerLoading,
      registerForm,
      registerFormRef,
      registerRules,
      departments,
      mapMarkerStyle,
      refreshStatus,
      getStatusText,
      getStatusTagType,
      maskName,
      showRegisterDialog,
      submitRegister,
      showClinicLocation,
      goToDashboard,
      goToPrescription
    }
  }
}
</script>

<style scoped>
.patient-queue-view {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.queue-status-card {
  margin-bottom: 20px;
}

.queue-info {
  padding: 10px;
  text-align: center;
}

.queue-number {
  margin-bottom: 20px;
}

.queue-number span {
  font-size: 16px;
  color: #606266;
}

.queue-number .number {
  font-size: 60px;
  font-weight: bold;
  color: #409EFF;
  line-height: 1.2;
}

.status-info {
  display: flex;
  justify-content: space-around;
  margin: 20px 0;
}

.status-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.item-label {
  font-size: 14px;
  color: #606266;
  margin-bottom: 5px;
}

.item-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.status-waiting {
  color: #409EFF;
}

.status-calling {
  color: #F56C6C;
}

.status-exam {
  color: #E6A23C;
}

.status-completed {
  color: #67C23A;
}

.current-calling {
  margin: 20px 0;
}

.current-calling h4 {
  font-size: 16px;
  color: #606266;
  margin-bottom: 10px;
}

.calling-number {
  font-size: 36px;
  color: #F56C6C;
  font-weight: bold;
}

.no-calling {
  color: #909399;
  font-size: 16px;
}

.notice-card {
  margin-top: 20px;
}

.notice-list {
  padding-left: 20px;
}

.notice-list li {
  margin-bottom: 10px;
  color: #606266;
  line-height: 1.5;
}

.queue-list-card {
  margin-top: 20px;
}

.clinic-info-content {
  padding: 10px;
}

.clinic-details h4 {
  font-size: 18px;
  color: #303133;
  margin-bottom: 15px;
}

.clinic-details p {
  margin-bottom: 10px;
  color: #606266;
}

.info-label {
  font-weight: bold;
  color: #303133;
  margin-right: 5px;
}

.clinic-actions {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.current-user {
  color: #409EFF;
  font-weight: bold;
}

.loading-placeholder {
  padding: 20px;
}

.location-map {
  position: relative;
  width: 100%;
  height: 300px;
  border: 1px solid #DCDFE6;
  overflow: hidden;
}

.clinic-map-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.map-marker {
  position: absolute;
  width: 20px;
  height: 20px;
  background-color: #F56C6C;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  animation: pulse 1.5s infinite;
}

.location-directions {
  margin-top: 20px;
  padding: 10px;
  background-color: #F8F9FA;
  border-radius: 4px;
}

.location-directions h4 {
  margin-bottom: 10px;
  color: #303133;
}

@keyframes pulse {
  0% {
    box-shadow: 0 0 0 0 rgba(245, 108, 108, 0.6);
  }
  70% {
    box-shadow: 0 0 0 10px rgba(245, 108, 108, 0);
  }
  100% {
    box-shadow: 0 0 0 0 rgba(245, 108, 108, 0);
  }
}

.header-actions {
  display: flex;
  gap: 10px;
}
</style>