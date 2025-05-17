<template>
  <div class="page-container">
    <div class="page-header">
      <h2>病例编辑</h2>
    </div>
    
    <div class="medical-records-container" v-loading="loading">
      <!-- Patient list -->
      <div class="patient-list">
        <el-table
          :data="patients"
          style="width: 100%"
          stripe
          border
          highlight-current-row
        >
          <el-table-column prop="name" label="姓名" min-width="100" />
          <el-table-column prop="gender" label="性别" width="80">
            <template #default="scope">
              {{ formatGender(scope.row.gender) }}
            </template>
          </el-table-column>
          <el-table-column prop="date_of_birth" label="出生日期" width="120" />
          <el-table-column label="身高/体重" width="120">
            <template #default="scope">
              {{ scope.row.height || '---' }} cm / {{ scope.row.weight || '---' }} kg
            </template>
          </el-table-column>
          <el-table-column label="操作" width="100" fixed="right">
            <template #default="scope">
              <el-button 
                type="primary" 
                size="small" 
                @click="openEditDialog(scope.row)"
              >
                编辑
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>
    
    <!-- 编辑病历对话框 -->
    <el-dialog
      v-model="dialogVisible"
      title="病历编辑"
      width="70%"
      destroy-on-close
    >
      <div v-if="selectedPatient" class="record-edit-form">
        <el-form 
          ref="recordFormRef"
          :model="recordForm" 
          label-width="100px"
          label-position="top"
        >
          <!-- 患者基本信息 -->
          <el-descriptions title="患者信息" :column="3" border>
            <el-descriptions-item label="姓名">{{ selectedPatient.name }}</el-descriptions-item>
            <el-descriptions-item label="性别">{{ formatGender(selectedPatient.gender) }}</el-descriptions-item>
            <el-descriptions-item label="出生日期">{{ selectedPatient.date_of_birth }}</el-descriptions-item>
            <el-descriptions-item label="身高">{{ selectedPatient.height || '---' }} cm</el-descriptions-item>
            <el-descriptions-item label="体重">{{ selectedPatient.weight || '---' }} kg</el-descriptions-item>
          </el-descriptions>
          
          <el-divider content-position="left">病历信息</el-divider>
          
          <!-- 病历内容 -->
          <el-form-item label="主诉">
            <el-input 
              v-model="recordForm.discription" 
              type="textarea" 
              :rows="3" 
              placeholder="请输入患者主诉"
            />
          </el-form-item>
          
          <el-form-item label="诊断结果">
            <el-input 
              v-model="recordForm.diagnosis" 
              type="textarea" 
              :rows="3" 
              placeholder="请输入诊断结果"
            />
          </el-form-item>
          
          <el-form-item label="治疗方案">
            <el-input 
              v-model="recordForm.treatment" 
              type="textarea" 
              :rows="3" 
              placeholder="请输入治疗方案"
            />
          </el-form-item>
          
          <el-divider content-position="left">用药信息</el-divider>
          
          <!-- 药品列表 -->
          <div class="medicine-list">
            <div v-for="(med, index) in recordForm.medicines" :key="index" class="medicine-item">
              <el-row :gutter="20" style="margin-bottom: 10px;">
                <el-col :span="8">
                  <el-select 
                    v-model="med.medicine_id" 
                    placeholder="选择药品" 
                    filterable
                    style="width: 100%"
                  >
                    <el-option
                      v-for="item in medicineOptions"
                      :key="item.medicine_id"
                      :label="`${item.name} (¥${item.price})`"
                      :value="item.medicine_id"
                    />
                  </el-select>
                </el-col>
                <el-col :span="12">
                  <el-input 
                    v-model="med.instructions" 
                    placeholder="用药说明（如：一日三次，饭后服用）"
                  />
                </el-col>
                <el-col :span="4">
                  <el-button type="danger" plain @click="removeMedicine(index)">
                    <el-icon><Delete /></el-icon> 删除
                  </el-button>
                </el-col>
              </el-row>
            </div>
            
            <el-button type="primary" @click="addMedicine" style="margin-top: 10px;">
              <el-icon><Plus /></el-icon> 添加药品
            </el-button>
          </div>
        </el-form>
      </div>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="saveRecord" :loading="saving">保存</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { Delete, Plus } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

export default {
  name: 'MedicalRecordsEdit',
  components: {
    Delete,
    Plus
  },
  setup() {
    // 状态数据
    const loading = ref(false)
    const saving = ref(false)
    const dialogVisible = ref(false)
    const patients = ref([])
    const selectedPatient = ref(null)
    const medicineOptions = ref([])
    
    // 表单数据
    const recordFormRef = ref(null)
    const recordForm = reactive({
      record_id: null,
      patient_id: null,
      doctor_id: null,
      appointment_id: null,
      discription: '',
      diagnosis: '',
      treatment: '',
      medicines: []
    })
    
    // 格式化性别显示
    const formatGender = (gender) => {
      return gender === 'male' ? '男' : gender === 'female' ? '女' : '未知'
    }
    
    // 获取医生ID
    const getDoctorId = () => {
      return localStorage.getItem('doctorId') || 1
    }
    
    // 获取患者列表
    const fetchPatients = async () => {
      loading.value = true
      try {
        const doctorId = getDoctorId()
        const response = await axios.get(`/api/patient/doctor/patients`, {
          params: { doctor_id: doctorId }
        })
        
        if (response.data && response.data.status === 'success') {
          patients.value = response.data.data || []
          console.log('获取患者列表成功', patients.value)
        } else {
          ElMessage.warning('获取患者列表失败')
          patients.value = []
        }
      } catch (error) {
        console.error('获取患者列表出错', error)
        ElMessage.error('无法获取患者列表，请稍后重试')
        patients.value = []
      } finally {
        loading.value = false
      }
    }
    
    // 获取药品列表
    const fetchMedicines = async () => {
      try {
        const response = await axios.get('/api/patient/medicines')
        
        if (response.data && response.data.status === 'success') {
          medicineOptions.value = response.data.data || []
          console.log('获取药品列表成功', medicineOptions.value)
        } else {
          ElMessage.warning('获取药品列表失败')
          medicineOptions.value = []
        }
      } catch (error) {
        console.error('获取药品列表出错', error)
        ElMessage.error('无法获取药品列表，请稍后重试')
        medicineOptions.value = []
      }
    }
    
    // 打开编辑对话框
    const openEditDialog = (patient) => {
      selectedPatient.value = patient
      
      // 重置表单
      recordForm.record_id = patient.record_id || null
      recordForm.patient_id = patient.patient_id
      recordForm.doctor_id = getDoctorId()
      recordForm.appointment_id = patient.appointment_id || null
      recordForm.discription = ''
      recordForm.diagnosis = ''
      recordForm.treatment = ''
      // 始终初始化为一个空的药品项
      recordForm.medicines = [{
        medicine_id: '',
        instructions: ''
      }]
      
      // 如果有病历记录，获取详情
      if (patient.record_id) {
        fetchRecordDetails(patient.record_id)
      } else {
        // 如果是新病历，不需要额外操作，已经初始化好了
        console.log('创建新病历')
      }
      
      dialogVisible.value = true
    }
    
    // 获取病历详情
    const fetchRecordDetails = async (recordId) => {
      loading.value = true
      try {
        // 添加patient_id参数，这是获取病历详情的必要参数
        const patientId = selectedPatient.value.patient_id;
        const response = await axios.get(`/api/patient/records/${recordId}`, {
          params: { patient_id: patientId }
        });
        
        if (response.data && response.data.status === 'success') {
          const recordData = response.data.data
          
          // 填充表单
          recordForm.discription = recordData.discription || ''
          recordForm.diagnosis = recordData.diagnosis || ''
          recordForm.treatment = recordData.treatment || ''
          
          console.log('获取病历详情成功', recordData)
        } else {
          ElMessage.warning('获取病历详情失败')
        }
      } catch (error) {
        console.error('获取病历详情出错', error)
        ElMessage.error('无法获取病历详情，请稍后重试')
      } finally {
        loading.value = false
      }
    }
    
    // 添加药品
    const addMedicine = () => {
      recordForm.medicines.push({
        medicine_id: '',
        instructions: ''
      })
    }
    
    // 删除药品
    const removeMedicine = (index) => {
      recordForm.medicines.splice(index, 1)
    }
    
    // 保存病历
    const saveRecord = async () => {
      // 表单验证
      if (!recordForm.discription.trim()) {
        ElMessage.warning('主诉不能为空')
        return
      }
      
      if (!recordForm.diagnosis.trim()) {
        ElMessage.warning('诊断结果不能为空')
        return
      }
      
      if (!recordForm.treatment.trim()) {
        ElMessage.warning('治疗方案不能为空')
        return
      }
      
      // 确保至少有一种药品
      if (recordForm.medicines.length === 0) {
        ElMessage.warning('请至少添加一种药品')
        return
      }
      
      // 验证药品数据
      let validMedicines = true;
      recordForm.medicines.forEach((med, index) => {
        if (!med.medicine_id) {
          ElMessage.warning(`请选择第${index + 1}项药品`)
          validMedicines = false;
        } else if (!med.instructions.trim()) {
          ElMessage.warning(`请为第${index + 1}项药品填写用药说明`)
          validMedicines = false;
        }
      });
      
      if (!validMedicines) return;
      
      saving.value = true
      try {
        console.log('提交的数据:', recordForm);
        
        // 发送保存请求
        const response = await axios.put('/api/patient/records/update', recordForm)
        
        if (response.data && response.data.status === 'success') {
          ElMessage.success('病历保存成功')
          dialogVisible.value = false
          
          // 更新record_id（如果是新创建的记录）
          if (!recordForm.record_id && response.data.data && response.data.data.record_id) {
            const updatedPatient = {...selectedPatient.value};
            updatedPatient.record_id = response.data.data.record_id;
            
            // 更新本地患者数据
            const index = patients.value.findIndex(p => p.patient_id === updatedPatient.patient_id);
            if (index !== -1) {
              patients.value[index] = updatedPatient;
            }
          }
          
          // 刷新患者列表
          fetchPatients()
        } else {
          ElMessage.error(response.data?.message || '保存失败')
        }
      } catch (error) {
        console.error('保存病历出错', error.response?.data || error)
        ElMessage.error(`保存病历失败: ${error.response?.data?.message || '请稍后重试'}`)
      } finally {
        saving.value = false
      }
    }
    
    // 初始化
    onMounted(() => {
      fetchPatients()
      fetchMedicines()
    })
    
    return {
      loading,
      saving,
      dialogVisible,
      patients,
      selectedPatient,
      medicineOptions,
      recordForm,
      recordFormRef,
      formatGender,
      openEditDialog,
      addMedicine,
      removeMedicine,
      saveRecord
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
}

.medical-records-container {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
}

.medicine-item {
  margin-bottom: 15px;
  padding: 10px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  background-color: #f8f8f8;
}

.medicine-list {
  margin-bottom: 20px;
}
</style> 