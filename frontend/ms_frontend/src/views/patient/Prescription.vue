<template>
  <div class="patient-prescription">
    <el-card class="prescription-card">
      <template #header>
        <div class="card-header">
          <h3>我的处方</h3>
          <div class="header-actions">
            <el-button type="primary" @click="goToDashboard">返回主页</el-button>
            <el-button type="success" @click="goToQueue">排队信息</el-button>
          </div>
        </div>
      </template>
      
      <div class="prescription-list-content">
        <el-table
          v-if="prescriptions.length > 0"
          :data="prescriptions"
          style="width: 100%"
          @row-click="handleRowClick">
          <el-table-column prop="id" label="处方编号" width="120" />
          <el-table-column prop="date" label="开具日期" width="180">
            <template #default="scope">
              {{ formatDate(scope.row.date) }}
            </template>
          </el-table-column>
          <el-table-column prop="doctorName" label="医生" />
          <el-table-column prop="department" label="科室" />
          <el-table-column prop="diagnosis" label="诊断" show-overflow-tooltip />
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
                type="primary" 
                size="small" 
                @click.stop="viewPrescription(scope.row)"
              >
                查看
              </el-button>
              <el-button 
                type="success" 
                size="small" 
                @click.stop="downloadPrescription(scope.row)"
              >
                下载
              </el-button>
            </template>
          </el-table-column>
        </el-table>
        
        <div v-else-if="loading" class="loading-placeholder">
          <el-skeleton animated :rows="6" />
        </div>
        
        <el-empty v-else description="暂无处方记录" />
      </div>
    </el-card>
    
    <!-- 处方详情对话框 -->
    <el-dialog
      v-model="prescriptionDialogVisible"
      title="处方详情"
      width="70%"
      destroy-on-close>
      <div v-if="currentPrescription" class="prescription-detail">
        <div class="prescription-header">
          <div class="hospital-info">
            <h2>医疗系统门诊部</h2>
            <p>电子处方笺</p>
          </div>
          <div class="prescription-id">
            <p>处方编号: {{ currentPrescription.id }}</p>
            <p>日期: {{ formatDate(currentPrescription.date) }}</p>
          </div>
        </div>
        
        <el-divider />
        
        <div class="prescription-info">
          <div class="info-row">
            <div class="info-item"><span class="label">患者姓名:</span> {{ patientInfo.name }}</div>
            <div class="info-item"><span class="label">性别:</span> {{ patientInfo.gender === 'male' ? '男' : '女' }}</div>
            <div class="info-item"><span class="label">年龄:</span> {{ patientInfo.age }}岁</div>
          </div>
          <div class="info-row">
            <div class="info-item"><span class="label">诊断:</span> {{ currentPrescription.diagnosis }}</div>
          </div>
        </div>
        
        <el-divider />
        
        <div class="medicine-list">
          <h3>药品清单</h3>
          <el-table
            :data="currentPrescription.medicines"
            style="width: 100%"
            border
            stripe>
            <el-table-column type="index" label="序号" width="60" />
            <el-table-column prop="name" label="药品名称" min-width="180" />
            <el-table-column prop="specification" label="规格" width="150" />
            <el-table-column prop="quantity" label="数量" width="80" />
            <el-table-column prop="usage" label="用法用量" min-width="200" />
          </el-table>
        </div>
        
        <div v-if="currentPrescription.instructions" class="instructions">
          <h3>医嘱</h3>
          <div class="instructions-text">{{ currentPrescription.instructions }}</div>
        </div>
        
        <div class="prescription-footer">
          <div class="doctor-signature">
            <p><span class="label">医生签名:</span> {{ currentPrescription.doctorName }}</p>
            <p><span class="label">医师资格证号:</span> {{ currentPrescription.doctorLicenseNumber || '****' }}</p>
          </div>
          <div class="pharmacy-info">
            <p><span class="label">有效期:</span> 3天（自开具日起计算）</p>
          </div>
        </div>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="downloadPrescription(currentPrescription)">
            下载处方
          </el-button>
          <el-button @click="prescriptionDialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 药物信息对话框 -->
    <el-dialog
      v-model="medicineInfoDialogVisible"
      :title="selectedMedicine ? selectedMedicine.name + '用药指南' : '药品信息'"
      width="50%">
      <div v-if="selectedMedicine" class="medicine-info">
        <div class="medicine-header">
          <h3>{{ selectedMedicine.name }}</h3>
          <p>{{ selectedMedicine.specification }}</p>
        </div>
        
        <el-divider />
        
        <div class="medicine-detail">
          <h4>药品说明</h4>
          <div class="info-section">
            <p><span class="label">药品类型:</span> {{ selectedMedicine.type }}</p>
            <p><span class="label">主要成分:</span> {{ selectedMedicine.ingredients || '未提供' }}</p>
            <p><span class="label">生产厂家:</span> {{ selectedMedicine.manufacturer }}</p>
            <p><span class="label">生产批号:</span> {{ selectedMedicine.batchNumber || '未提供' }}</p>
          </div>
          
          <h4>用法用量</h4>
          <div class="info-section">
            <p>{{ selectedMedicine.usage }}</p>
          </div>
          
          <h4>功能主治</h4>
          <div class="info-section">
            <p>{{ selectedMedicine.indications || '详情请咨询医生或药师' }}</p>
          </div>
          
          <h4>注意事项</h4>
          <div class="info-section">
            <ul class="warning-list">
              <li>请按医嘱服药，勿擅自增减药量或停药</li>
              <li>如出现不良反应，请立即停药并咨询医生</li>
              <li>存放于儿童接触不到的地方</li>
              <li v-if="selectedMedicine.warnings">{{ selectedMedicine.warnings }}</li>
            </ul>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

export default {
  name: 'PatientPrescription',
  setup() {
    const router = useRouter()
    // 移除未使用的 route 变量
    
    // 状态
    const loading = ref(false)
    const prescriptionDialogVisible = ref(false)
    const medicineInfoDialogVisible = ref(false)
    const selectedMedicine = ref(null)
    const currentPrescription = ref(null)
    
    // 患者信息（实际应从用户会话或Store中获取）
    const patientInfo = reactive({
      id: 'patient123',
      name: '张三',
      gender: 'male',
      age: 35
    })
    
    // 处方列表（模拟数据，实际应从API获取）
    const prescriptions = ref([
      {
        id: 'RX20250422001',
        patientId: 'patient123',
        doctorId: '1',
        doctorName: '李医生',
        department: '内科',
        date: '2025-04-20T09:30:00',
        diagnosis: '上呼吸道感染',
        status: 'completed',
        medicines: [
          { id: 1, name: '阿莫西林胶囊', specification: '0.25g*24粒/盒', quantity: 2, usage: '一日三次，饭后半小时服用，一次一粒', type: '抗生素类', manufacturer: '哈药集团' },
          { id: 3, name: '感冒灵颗粒', specification: '10g*9包/盒', quantity: 1, usage: '一日三次，温开水冲服，一次一包', type: '感冒用药', manufacturer: '云南白药集团' }
        ],
        instructions: '注意休息，多喝温水，避免辛辣食物',
        doctorLicenseNumber: 'MD12345678'
      },
      {
        id: 'RX20250419002',
        patientId: 'patient123',
        doctorId: 'doctor456',
        doctorName: '王医生',
        department: '骨科',
        date: '2025-04-19T14:45:00',
        diagnosis: '腰肌劳损',
        status: 'processing',
        medicines: [
          { id: 6, name: '双氯芬酸钠缓释片', specification: '0.1g*12片/盒', quantity: 1, usage: '一日两次，饭后服用，一次一片', type: '解热镇痛药', manufacturer: '扬子江药业' },
          { id: 7, name: '云南白药膏', specification: '20g/盒', quantity: 2, usage: '外用，涂抹于患处，一日两次', type: '外用制剂', manufacturer: '云南白药集团' }
        ],
        instructions: '避免长时间站立或久坐，保持正确坐姿，可适当热敷缓解疼痛',
        doctorLicenseNumber: 'MD87654321'
      }
    ])
    
    // 刷新处方列表
    const refreshPrescriptions = async () => {
      loading.value = true
      
      // 模拟API调用
      setTimeout(() => {
        // 实际项目中应该调用API获取最新数据
        loading.value = false
        ElMessage.success('处方列表已更新')
      }, 1000)
    }
    
    // 格式化日期
    const formatDate = (dateString) => {
      const date = new Date(dateString)
      return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')} ${String(date.getHours()).padStart(2, '0')}:${String(date.getMinutes()).padStart(2, '0')}`
    }
    
    // 获取状态类型
    const getStatusType = (status) => {
      switch (status) {
        case 'completed':
          return 'success'
        case 'processing':
          return 'warning'
        case 'cancelled':
          return 'danger'
        default:
          return 'info'
      }
    }
    
    // 获取状态文本
    const getStatusText = (status) => {
      switch (status) {
        case 'completed':
          return '已完成'
        case 'processing':
          return '处理中'
        case 'cancelled':
          return '已取消'
        default:
          return '未知状态'
      }
    }
    
    // 表格行点击
    const handleRowClick = (row) => {
      viewPrescription(row)
    }
    
    // 查看处方
    const viewPrescription = (prescription) => {
      currentPrescription.value = prescription
      prescriptionDialogVisible.value = true
    }
    
    // 查看药物信息
    const viewMedicineInfo = (medicine) => {
      selectedMedicine.value = medicine
      medicineInfoDialogVisible.value = true
    }
    
    // 下载处方
    const downloadPrescription = (prescription) => {
      // 实际项目中应该调用API下载处方PDF
      ElMessage.success(`处方 ${prescription.id} 下载中...`)
      
      // 模拟下载延迟
      setTimeout(() => {
        ElMessage.success('处方下载完成')
      }, 2000)
    }
    
    // 导航函数
    const goToDashboard = () => {
      router.push('/patient/dashboard')
    }

    const goToQueue = () => {
      router.push('/patient/queue')
    }
    
    // 初始化
    onMounted(() => {
      refreshPrescriptions()
    })
    
    return {
      loading,
      prescriptions,
      prescriptionDialogVisible,
      medicineInfoDialogVisible,
      selectedMedicine,
      currentPrescription,
      patientInfo,
      refreshPrescriptions,
      formatDate,
      getStatusType,
      getStatusText,
      handleRowClick,
      viewPrescription,
      viewMedicineInfo,
      downloadPrescription,
      goToDashboard,
      goToQueue
    }
  }
}
</script>

<style scoped>
.patient-prescription-view {
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

.prescription-list-card {
  margin-bottom: 20px;
}

.prescription-detail {
  padding: 20px;
}

.prescription-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.hospital-info {
  text-align: center;
}

.hospital-info h2 {
  margin-bottom: 5px;
  color: #303133;
}

.prescription-id {
  text-align: right;
}

.prescription-id p {
  margin: 5px 0;
  color: #606266;
}

.prescription-info {
  margin-bottom: 20px;
}

.info-row {
  display: flex;
  margin-bottom: 10px;
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

.medicine-list {
  margin-bottom: 20px;
}

.medicine-list h3, .instructions h3 {
  margin-bottom: 15px;
  color: #303133;
  font-weight: 600;
}

.instructions {
  margin: 20px 0;
}

.instructions-text {
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
  line-height: 1.6;
}

.prescription-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 40px;
}

.doctor-signature, .pharmacy-info {
  max-width: 50%;
}

.doctor-signature p, .pharmacy-info p {
  margin-bottom: 5px;
}

.medicine-info {
  padding: 10px;
}

.medicine-header {
  text-align: center;
  margin-bottom: 15px;
}

.medicine-header h3 {
  margin-bottom: 5px;
  color: #303133;
}

.medicine-header p {
  color: #606266;
}

.medicine-detail h4 {
  margin: 20px 0 10px;
  color: #303133;
  font-weight: 600;
}

.info-section {
  background-color: #f8f9fa;
  padding: 10px;
  border-radius: 4px;
}

.info-section p {
  margin-bottom: 8px;
  line-height: 1.6;
}

.warning-list {
  padding-left: 20px;
}

.warning-list li {
  margin-bottom: 8px;
  color: #f56c6c;
}

.loading-placeholder {
  padding: 20px;
}
</style>