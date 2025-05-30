<template>
  <div class="register-container">
    <div class="register-box">
      <div class="left-section">
        <div class="welcome-text">
          <h2>医生注册</h2>
          <p>欢迎加入我们的医疗团队，请填写以下信息完成注册</p>
        </div>
        <el-button 
          type="primary" 
          class="login-button"
          @click="goToLogin"
        >
          已有账号？立即登录
        </el-button>
      </div>

      <div class="right-section">
        <el-form 
          :model="registerForm" 
          :rules="rules" 
          ref="registerFormRef"
          label-position="top"
          class="register-form"
        >
          <el-form-item label="手机号" prop="phone">
            <el-input
              v-model="registerForm.phone"
              placeholder="请输入手机号"
              class="custom-input"
            >
              <template #prefix>
                <el-icon><Phone /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="姓名" prop="name">
            <el-input
              v-model="registerForm.name"
              placeholder="请输入姓名"
              class="custom-input"
            >
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="医院" prop="hospital_id">
            <el-select
              v-model="registerForm.hospital_id"
              placeholder="请选择医院"
              class="custom-input"
            >
              <el-option
                v-for="hospital in hospitals"
                :key="hospital.id"
                :label="hospital.name"
                :value="hospital.id"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="科室" prop="department_id">
            <el-select
              v-model="registerForm.department_id"
              placeholder="请选择科室"
              class="custom-input"
            >
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
              v-model="registerForm.specialty"
              placeholder="请输入专长领域"
              class="custom-input"
            >
              <template #prefix>
                <el-icon><Star /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="密码" prop="password">
            <el-input
              v-model="registerForm.password"
              type="password"
              placeholder="请输入密码"
              class="custom-input"
              show-password
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item label="确认密码" prop="confirmPassword">
            <el-input
              v-model="registerForm.confirmPassword"
              type="password"
              placeholder="请再次输入密码"
              class="custom-input"
              show-password
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </el-form-item>

          <el-form-item>
            <el-button 
              type="primary" 
              @click="handleRegister" 
              :loading="loading" 
              class="register-button"
            >
              注册
            </el-button>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  User, 
  Lock, 
  Phone,
  Star
} from '@element-plus/icons-vue'
import axios from 'axios'

export default {
  name: 'DoctorRegister',
  components: {
    User,
    Lock,
    Phone,
    Star
  },
  setup() {
    const router = useRouter()
    const registerFormRef = ref(null)
    const loading = ref(false)
    //const hospitals = ref([])
    const hospitals=[
      { id: 1, name: '医院A' },
      { id: 2, name: '医院B' },
      { id: 3, name: '医院C' }
    ]
    //const departments = ref([])
    const departments=[
      { id: 1, name: '内科' },
      { id: 2, name: '外科' },
      { id: 3, name: '儿科' }
    ]

    const registerForm = reactive({
      phone: '',
      name: '',
      hospital_id: '',
      department_id: '',
      specialty: '',
      password: '',
      confirmPassword: ''
    })

    const validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else if (value.length < 6) {
        callback(new Error('密码长度不能小于6位'))
      } else {
        if (registerForm.confirmPassword !== '') {
          registerFormRef.value?.validateField('confirmPassword')
        }
        callback()
      }
    }

    const validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== registerForm.password) {
        callback(new Error('两次输入密码不一致'))
      } else {
        callback()
      }
    }

    const rules = {
      phone: [
        { required: true, message: '请输入手机号', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
      ],
      name: [
        { required: true, message: '请输入姓名', trigger: 'blur' },
        { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
      ],
      hospital_id: [
        { required: true, message: '请选择医院', trigger: 'change' }
      ],
      department_id: [
        { required: true, message: '请选择科室', trigger: 'change' }
      ],
      specialty: [
        { required: true, message: '请输入专长', trigger: 'blur' },
        { max: 100, message: '长度不能超过100个字符', trigger: 'blur' }
      ],
      password: [
        { required: true, validator: validatePass, trigger: 'blur' }
      ],
      confirmPassword: [
        { required: true, validator: validatePass2, trigger: 'blur' }
      ]
    }

    // const fetchHospitals = async () => {
    //   try {
    //     const response = await axios.get('/api/hospitals')
    //     hospitals.value = response.data.data
    //   } catch (error) {
    //     ElMessage.error('获取医院列表失败')
    //   }
    // }

    // const fetchDepartments = async (hospitalId) => {
    //   try {
    //     const response = await axios.get(`/api/departments?hospital_id=${hospitalId}`)
    //     departments.value = response.data.data
    //     registerForm.department_id = ''
    //   } catch (error) {
    //     ElMessage.error('获取科室列表失败')
    //   }
    // }

    // const handleHospitalChange = (hospitalId) => {
    //   if (hospitalId) {
    //     fetchDepartments(hospitalId)
    //   } else {
    //     departments.value = []
    //     registerForm.department_id = ''
    //   }
    // }

    const handleRegister = async () => {
      if (!registerFormRef.value) return
      
      try {
        await registerFormRef.value.validate()
        loading.value = true
        
        const { confirmPassword, ...registerData } = registerForm
        //console.log(registerData)
        const response = await axios.post('/api/user-service/doctor/register', registerData)

        if (response.data.status === 'success') {
          ElMessage.success('注册成功')
          router.push('/login?type=doctor')
        } else {
          ElMessage.error(response.data.message || '注册失败')
        }
      } catch (error) {
        ElMessage.error(error.response?.data?.message || '注册失败，请稍后重试')
      } finally {
        loading.value = false
      }
    }

    const goToLogin = () => {
      router.push('/login?type=doctor')
    }

    // 初始化时获取医院列表
    //fetchHospitals()

    return {
      registerForm,
      rules,
      registerFormRef,
      loading,
      hospitals,
      departments,
      handleRegister,
      goToLogin,
      //handleHospitalChange
    }
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  background: white;
  margin: 0;
}

.register-box {
  display: flex;
  width: 1000px;
  max-width: 100%;
  background: white;
  border-radius: 20px;
  overflow: visible;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1;
}

.left-section {
  flex: 0.4;
  background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
  padding: 60px 40px;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.welcome-text {
  margin-bottom: 50px;
  position: relative;
  z-index: 1;
}

.welcome-text h2 {
  font-size: 32px;
  margin-bottom: 20px;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.welcome-text p {
  font-size: 16px;
  opacity: 0.9;
  line-height: 1.6;
}

.login-button {
  width: 200px;
  height: 50px;
  font-size: 16px;
  background: white;
  color: #4b6cb7;
  border: none;
  border-radius: 25px;
  transition: all 0.3s ease;
  position: relative;
  z-index: 1;
  font-weight: 500;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
  background: rgba(255, 255, 255, 0.95);
}

.right-section {
  flex: 0.6;
  padding: 60px 40px;
  background: white;
  position: relative;
  overflow: visible;
}

.register-form {
  max-width: 400px;
  margin: 0 auto;
  overflow: visible;
}

.custom-input {
  margin-bottom: 20px;
}

.custom-input :deep(.el-input__wrapper) {
  background-color: #f8f9fa;
  border-radius: 10px;
  box-shadow: none;
  padding: 0 15px;
  border: 1px solid #e9ecef;
  transition: all 0.3s ease;
}

.custom-input :deep(.el-input__wrapper:hover) {
  border-color: #4b6cb7;
  background-color: #fff;
}

.custom-input :deep(.el-input__wrapper.is-focus) {
  background-color: #fff;
  box-shadow: 0 0 0 2px rgba(75, 108, 183, 0.2);
  border-color: #4b6cb7;
}

.register-button {
  width: 100%;
  height: 50px;
  font-size: 16px;
  border-radius: 25px;
  background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
  border: none;
  transition: all 0.3s ease;
  font-weight: 500;
}

.register-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(75, 108, 183, 0.3);
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #333;
}

:deep(.el-icon) {
  color: #4b6cb7;
  font-size: 18px;
}
</style>
