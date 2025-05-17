<template>
  <div class="home-container">
    <div class="header">
      <h1 class="title">医疗管理系统</h1>
      <h2 class="subtitle">患者就诊流程管理子系统</h2>
    </div>
    
    <div class="content">
      <div class="card">
        <h3>请选择您的身份</h3>
        
        <!-- 患者入口 -->
        <div class="section">
          <h4>患者入口</h4>
          <div class="buttons-container">
            <el-skeleton v-if="patientsLoading" :rows="1" animated />
            <div v-else-if="patients.length === 0" class="empty-data">暂无患者数据</div>
            <div v-else class="buttons-grid">
              <el-button 
                v-for="patient in patients" 
                :key="patient.patient_id"
                type="primary" 
                size="large" 
                @click="enterPatientSystem(patient)"
              >
                {{ patient.name }}
              </el-button>
            </div>
          </div>
        </div>
        
        <!-- 医生入口 -->
        <div class="section">
          <h4>医生入口</h4>
          <div class="buttons-container">
            <el-skeleton v-if="doctorsLoading" :rows="1" animated />
            <div v-else-if="doctors.length === 0" class="empty-data">暂无医生数据</div>
            <div v-else class="buttons-grid">
              <el-button 
                v-for="doctor in doctors" 
                :key="doctor.doctor_id"
                type="success" 
                size="large" 
                @click="enterDoctorSystem(doctor)"
              >
                {{ doctor.name }}
                <small class="department">({{ doctor.department_name }})</small>
              </el-button>
            </div>
          </div>
        </div>
        
        <!-- 使用新的BackendTest组件 -->
        <BackendTest class="api-test" />
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../store/auth'
import { usePatientStore } from '../store/patient'
import { useDoctorStore } from '../store/doctor'
import BackendTest from '../components/BackendTest.vue'
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'HomePage',
  components: {
    BackendTest
  },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const patientStore = usePatientStore()
    const doctorStore = useDoctorStore()
    
    // 患者和医生数据
    const patients = ref([])
    const doctors = ref([])
    const patientsLoading = ref(true)
    const doctorsLoading = ref(true)
    
    // 加载患者列表
    const loadPatients = async () => {
      try {
        patientsLoading.value = true
        const response = await axios.get('/api/patients')
        if (response.data.status === 'success') {
          patients.value = response.data.data
        } else {
          ElMessage.error('获取患者列表失败: ' + response.data.message)
        }
      } catch (error) {
        console.error('获取患者列表出错:', error)
        ElMessage.error('获取患者列表失败: ' + (error.response?.data?.message || error.message))
      } finally {
        patientsLoading.value = false
      }
    }
    
    // 加载医生列表
    const loadDoctors = async () => {
      try {
        doctorsLoading.value = true
        const response = await axios.get('/api/doctors')
        if (response.data.status === 'success') {
          doctors.value = response.data.data
        } else {
          ElMessage.error('获取医生列表失败: ' + response.data.message)
        }
      } catch (error) {
        console.error('获取医生列表出错:', error)
        ElMessage.error('获取医生列表失败: ' + (error.response?.data?.message || error.message))
      } finally {
        doctorsLoading.value = false
      }
    }
    
    // 进入患者系统
    const enterPatientSystem = (patient) => {
      authStore.setUserData({
        token: `patient-token-${patient.patient_id}`,
        user: patient,
        userType: 'patient'
      })
      // 设置当前患者ID
      patientStore.setPatientId(patient.patient_id)
      router.push('/patient/medical-records')
    }
    
    // 进入医生系统
    const enterDoctorSystem = (doctor) => {
      authStore.setUserData({
        token: `doctor-token-${doctor.doctor_id}`,
        user: doctor,
        userType: 'doctor'
      })
      // 设置当前医生ID
      doctorStore.setDoctorId(doctor.doctor_id)
      router.push('/doctor/medical-records-edit')
    }
    
    // 加载数据
    onMounted(() => {
      loadPatients()
      loadDoctors()
    })
    
    return {
      patients,
      doctors,
      patientsLoading,
      doctorsLoading,
      enterPatientSystem,
      enterDoctorSystem,
      patientStore,
      doctorStore
    }
  }
}
</script>

<style scoped>
.home-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.title {
  font-size: 36px;
  color: #409EFF;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 20px;
  color: #606266;
  font-weight: normal;
}

.content {
  display: flex;
  flex-direction: column;
  gap: 30px;
  max-width: 800px;
  width: 100%;
}

.card {
  background-color: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  text-align: center;
}

.card h3 {
  margin-bottom: 30px;
  color: #303133;
}

.section {
  margin-bottom: 30px;
  padding: 20px;
  border-radius: 8px;
  background-color: #f8f9fa;
}

.section h4 {
  margin-bottom: 15px;
  color: #303133;
  font-size: 18px;
}

.buttons-container {
  min-height: 60px;
}

.buttons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

.empty-data {
  color: #909399;
  padding: 15px;
  font-style: italic;
}

.department {
  display: block;
  font-size: 12px;
  margin-top: 5px;
}

/* API测试样式 */
.api-test {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px dashed #eee;
}

.test-result {
  margin-top: 10px;
  padding: 8px;
  border-radius: 4px;
  font-size: 14px;
}

.test-result.success {
  background-color: #f0f9eb;
  color: #67c23a;
}

.test-result.error {
  background-color: #fef0f0;
  color: #f56c6c;
}

.test-result.loading {
  background-color: #f4f4f5;
  color: #909399;
}
</style> 