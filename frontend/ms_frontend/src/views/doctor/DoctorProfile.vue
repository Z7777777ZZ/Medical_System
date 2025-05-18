<template>
  <div class="profile-container">
    <div class="profile-header">
      <h2>医生信息</h2>
      <p>完善您的个人信息，以便为患者提供更好的医疗服务</p>
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
              </div>
            </div>

            <!-- 详细信息 -->
            <div v-show="activeTab === 'detail'" class="form-section">
              <h3>详细信息</h3>
              <div class="form-grid">
                <el-form-item label="所属医院" prop="hospital_id">
                  <el-select v-model="profileForm.hospital_id" placeholder="请选择医院">
                    <el-option
                      v-for="hospital in hospitals"
                      :key="hospital.id"
                      :label="hospital.name"
                      :value="hospital.id"
                    />
                  </el-select>
                </el-form-item>

                <el-form-item label="所属科室" prop="department_id">
                  <el-select v-model="profileForm.department_id" placeholder="请选择科室">
                    <el-option
                      v-for="department in departments"
                      :key="department.id"
                      :label="department.name"
                      :value="department.id"
                    />
                  </el-select>
                </el-form-item>

                <el-form-item label="专长" prop="specialty">
                  <el-input
                    v-model="profileForm.specialty"
                    type="textarea"
                    :rows="3"
                    placeholder="请输入您的专长领域"
                  />
                </el-form-item>

                <el-form-item label="个人简介" prop="bio">
                  <el-input
                    v-model="profileForm.bio"
                    type="textarea"
                    :rows="5"
                    placeholder="请输入您的个人简介"
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
  name: 'DoctorProfile',
  components: {
    User,
    Document
  },
  setup() {
    const profileFormRef = ref(null)
    const loading = ref(false)
    const activeTab = ref('basic')
    const hospitals = ref([])
    const departments = ref([])

    const profileForm = reactive({
      name: '',
      phone: '',
      hospital_id: '',
      department_id: '',
      specialty: '',
      bio: ''
    })

    const rules = {
      name: [
        { required: true, message: '请输入姓名', trigger: 'blur' }
      ],
      phone: [
        { required: true, message: '请输入手机号', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
      ],
      hospital_id: [
        { required: true, message: '请选择医院', trigger: 'change' }
      ],
      department_id: [
        { required: true, message: '请选择科室', trigger: 'change' }
      ],
      specialty: [
        { required: true, message: '请输入专长', trigger: 'blur' }
      ],
      bio: [
        { required: true, message: '请输入个人简介', trigger: 'blur' }
      ]
    }

    const handleSubmit = async () => {
      if (!profileFormRef.value) return
      
      try {
        await profileFormRef.value.validate()
        loading.value = true
        const doctorId = localStorage.getItem('doctor_id')
        const response = await axios.put(`/api/doctor/${doctorId}/profile`, profileForm)

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

    // 获取医院列表
    const fetchHospitals = async () => {
      try {
        const response = await axios.get('/api/hospitals')
        if (response.data.status === 'success') {
          hospitals.value = response.data.data
        }
      } catch (error) {
        ElMessage.error('获取医院列表失败')
      }
    }

    // 获取科室列表
    const fetchDepartments = async () => {
      try {
        const response = await axios.get('/api/departments')
        if (response.data.status === 'success') {
          departments.value = response.data.data
        }
      } catch (error) {
        ElMessage.error('获取科室列表失败')
      }
    }

    // 获取现有个人信息
    const fetchProfile = async () => {
      try {
        const doctorId = localStorage.getItem('doctor_id')
        const response = await axios.get(`/api/doctor/${doctorId}/profile`)
        if (response.data.status === 'success') {
          Object.assign(profileForm, response.data.data)
        }
      } catch (error) {
        ElMessage.error('获取个人信息失败')
      }
    }

    // 初始化时获取数据
    fetchHospitals()
    fetchDepartments()
    fetchProfile()

    return {
      profileForm,
      rules,
      profileFormRef,
      loading,
      activeTab,
      hospitals,
      departments,
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
