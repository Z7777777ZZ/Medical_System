<template>
  <div class="profile-container">
    <div class="profile-header">
      <h2>个人信息</h2>
      <p>完善您的个人信息，以便我们提供更好的医疗服务</p>
    </div>

    <div class="profile-content">
      <div class="profile-layout">
        <!-- 左侧导航 -->
        <div class="profile-nav">
          <div 
            class="nav-item" 
            :class="{ active: activeTab === 'basic' }"
            @click="activeTab = 'basic'"
          >
            <el-icon><User /></el-icon>
            <span>基础信息</span>
          </div>
          <div 
            class="nav-item" 
            :class="{ active: activeTab === 'detail' }"
            @click="activeTab = 'detail'"
          >
            <el-icon><Document /></el-icon>
            <span>详细信息</span>
          </div>
        </div>

        <!-- 右侧内容 -->
        <div class="profile-main">
          <el-form 
            :model="profileForm" 
            :rules="rules" 
            ref="profileFormRef"
            label-position="right"
            label-width="120px"
            class="profile-form"
          >
            <!-- 基础信息 -->
            <div v-show="activeTab === 'basic'" class="form-section">
              <h3>基础信息</h3>
              <div class="form-grid">
                <el-form-item label="姓名" prop="name">
                  <el-input v-model="profileForm.name" placeholder="请输入姓名" />
                </el-form-item>

                <el-form-item label="手机号" prop="phone">
                  <el-input v-model="profileForm.phone" placeholder="请输入手机号" />
                </el-form-item>

                <el-form-item label="邮箱" prop="email">
                  <el-input v-model="profileForm.email" placeholder="请输入邮箱" />
                </el-form-item>
              </div>
            </div>

            <!-- 详细信息 -->
            <div v-show="activeTab === 'detail'" class="form-section">
              <h3>详细信息</h3>
              <div class="form-grid">
                <el-form-item label="性别" prop="gender">
                  <el-select v-model="profileForm.gender" placeholder="请选择性别">
                    <el-option label="男" value="male" />
                    <el-option label="女" value="female" />
                    <el-option label="其他" value="other" />
                  </el-select>
                </el-form-item>

                <el-form-item label="出生日期" prop="date_of_birth">
                  <el-date-picker
                    v-model="profileForm.date_of_birth"
                    type="date"
                    placeholder="请选择出生日期"
                    value-format="YYYY-MM-DD"
                  />
                </el-form-item>

                <el-form-item label="血型" prop="blood_type">
                  <el-select v-model="profileForm.blood_type" placeholder="请选择血型">
                    <el-option label="A+" value="A+" />
                    <el-option label="A-" value="A-" />
                    <el-option label="B+" value="B+" />
                    <el-option label="B-" value="B-" />
                    <el-option label="AB+" value="AB+" />
                    <el-option label="AB-" value="AB-" />
                    <el-option label="O+" value="O+" />
                    <el-option label="O-" value="O-" />
                  </el-select>
                </el-form-item>

                <el-form-item label="身高(cm)" prop="height">
                  <el-input-number 
                    v-model="profileForm.height" 
                    :min="0" 
                    :max="300" 
                    :precision="2"
                    controls-position="right"
                  />
                </el-form-item>

                <el-form-item label="体重(kg)" prop="weight">
                  <el-input-number 
                    v-model="profileForm.weight" 
                    :min="0" 
                    :max="500" 
                    :precision="2"
                    controls-position="right"
                  />
                </el-form-item>

                <el-form-item label="紧急联系人" prop="emergency_contact">
                  <el-input v-model="profileForm.emergency_contact" placeholder="请输入紧急联系人姓名" />
                </el-form-item>

                <el-form-item label="紧急电话" prop="emergency_phone">
                  <el-input v-model="profileForm.emergency_phone" placeholder="请输入紧急联系人电话" />
                </el-form-item>

                <el-form-item label="医保卡号" prop="medical_insurance_id">
                  <el-input v-model="profileForm.medical_insurance_id" placeholder="请输入医保卡号" />
                </el-form-item>

                <el-form-item label="过敏史" prop="allergies">
                  <el-input
                    v-model="profileForm.allergies"
                    type="textarea"
                    :rows="3"
                    placeholder="请输入过敏史，如无请填写'无'"
                  />
                </el-form-item>

                <el-form-item label="慢性病史" prop="chronic_conditions">
                  <el-input
                    v-model="profileForm.chronic_conditions"
                    type="textarea"
                    :rows="3"
                    placeholder="请输入慢性病史，如无请填写'无'"
                  />
                </el-form-item>

                <el-form-item label="当前用药" prop="medications">
                  <el-input
                    v-model="profileForm.medications"
                    type="textarea"
                    :rows="3"
                    placeholder="请输入当前用药情况，如无请填写'无'"
                  />
                </el-form-item>
              </div>
            </div>

            <div class="form-actions">
              <el-button type="primary" @click="handleSubmit" :loading="loading">保存修改</el-button>
              <el-button @click="handleReset">重置</el-button>
            </div>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { User, Document } from '@element-plus/icons-vue'
import axios from 'axios'

export default {
  name: 'PatientProfile',
  components: {
    User,
    Document
  },
  setup() {
    const profileFormRef = ref(null)
    const loading = ref(false)
    const activeTab = ref('basic')

    const profileForm = reactive({
      name: '',
      phone: '',
      email: '',
      gender: '',
      date_of_birth: '',
      blood_type: '',
      height: null,
      weight: null,
      emergency_contact: '',
      emergency_phone: '',
      medical_insurance_id: '',
      allergies: '',
      chronic_conditions: '',
      medications: ''
    })

    const rules = {
      name: [
        { required: true, message: '请输入姓名', trigger: 'blur' }
      ],
      phone: [
        { required: true, message: '请输入手机号', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
      ],
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      gender: [
        { required: true, message: '请选择性别', trigger: 'change' }
      ],
      date_of_birth: [
        { required: true, message: '请选择出生日期', trigger: 'change' }
      ],
      blood_type: [
        { required: true, message: '请选择血型', trigger: 'change' }
      ],
      height: [
        { required: true, message: '请输入身高', trigger: 'blur' }
      ],
      weight: [
        { required: true, message: '请输入体重', trigger: 'blur' }
      ],
      emergency_contact: [
        { required: true, message: '请输入紧急联系人姓名', trigger: 'blur' }
      ],
      emergency_phone: [
        { required: true, message: '请输入紧急联系人电话', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
      ],
      medical_insurance_id: [
        { required: true, message: '请输入医保卡号', trigger: 'blur' }
      ],
      allergies: [
        { required: true, message: '请输入过敏史', trigger: 'blur' }
      ],
      chronic_conditions: [
        { required: true, message: '请输入慢性病史', trigger: 'blur' }
      ],
      medications: [
        { required: true, message: '请输入当前用药情况', trigger: 'blur' }
      ]
    }

    const handleSubmit = async () => {
      if (!profileFormRef.value) return
      
      try {
        await profileFormRef.value.validate()
        loading.value = true
        const patientId = localStorage.getItem('patient_id')
        console.log('profileForm', profileForm)
        const{name, phone, email, ...details} = profileForm
        const inputData = {
          phone,
          email,
          name,
          details
        }
        console.log('inputData', inputData)
        const response = await axios.put(`/api/user-service/patient/${patientId}/profile`, inputData)

        if (response.data.status === 'success') {
          ElMessage.success('保存成功')
        } else {
          ElMessage.error(response.data.message || '保存失败')
        }
      } catch (error) {
        ElMessage.error(error.response?.data?.message || '保存失败，请稍后重试')
      } finally {
        loading.value = false
      }
    }

    const handleReset = () => {
      if (profileFormRef.value) {
        profileFormRef.value.resetFields()
      }
    }

    // 获取现有个人信息
    const fetchProfile = async () => {
      try {
        // console.log('patient_id', localStorage.getItem('patient_id'))
        const patientId = localStorage.getItem('patient_id')
        console.log('patientId', patientId)
        const response = await axios.get(`/api/user-service/patient/${patientId}/profile`)
        // const response={
        //   data:{
        //     status: "success",
        //     message: "获取成功",
        //     data: {
        //       patient_id: 1,
        //       phone: "13800138000",
        //       email: "user@example.com",
        //       name: "张三",
        //       patient_details: {
        //           gender: "男",  
        //           date_of_birth: "1990-01-01",
        //           blood_type: "A+",
        //           height: 175,
        //           weight: 70,  
        //           emergency_contact: "李四",
        //           emergency_phone: "13900139000",
        //           medical_insurance_id: "1234567890",

        //           allergies: "string",  
        //           chronic_conditions: "string",
        //           medications: "string"
        //       }
        //     }
        //   }
        // }
        //console.log('response', response)
        //console.log('response.status', response.status=== 'success')
        if (response.data.status === 'success') {
          //Object.assign(profileForm, response.data.data)
          //console.log('response.data.data', response.data.data)
          const { name, phone, email, details } = response.data.data
          Object.assign(profileForm, {
            name,
            phone,
            email,
            ...details // 解构 gender, date_of_birth 等字段
          })
        }
      } catch (error) {
        ElMessage.error('获取个人信息失败')
      }
    }

    // 初始化时获取个人信息
    fetchProfile()

    return {
      profileForm,
      rules,
      profileFormRef,
      loading,
      activeTab,
      handleSubmit,
      handleReset
    }
  }
}
</script>

<style scoped>
.profile-container {
  width: 70%;
  margin: 0 auto;
}

.profile-header {
  margin-bottom: 40px;
}

.profile-header h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 10px;

}

.profile-header p {
  color: #666;
  font-size: 14px;
}

.profile-content {
  background: white;
  border-radius: 8px;
  border: 2px solid #eee;
  border-bottom: none;
}

.profile-layout {
  display: flex;
  min-height: 600px;
}

.profile-nav {
  width: 200px;
  padding: 20px 0;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  cursor: pointer;
  color: #666;
  transition: all 0.3s;
}

.nav-item:hover {
  background-color: #f5f7fa;
  color: #409eff;
}

.nav-item.active {
  background-color: #ecf5ff;
  color: #409eff;
  border-right: 2px solid #409eff;
}

.nav-item .el-icon {
  margin-right: 10px;
  font-size: 18px;
}

.profile-main {
  flex: 1;
  padding: 20px 40px;
  display: flex;
  justify-content: center;
  border-bottom: none;
}

.profile-form {
  width: 100%;
  max-width: 600px;
}

.form-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-section {
  margin-bottom: 30px;
  width: 100%;
}

.form-section h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 40px;
}

:deep(.el-form-item) {
  margin-bottom: 0;
}

:deep(.el-input),
:deep(.el-select),
:deep(.el-date-picker),
:deep(.el-input-number),
:deep(.el-textarea) {
  width: 100%;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-input__wrapper),
:deep(.el-textarea__inner) {
  border-radius: 4px;
}

:deep(.el-button) {
  min-width: 120px;
}
</style>