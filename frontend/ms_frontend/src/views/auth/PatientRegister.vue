<template>
  <div class="register-container">
    <div class="register-box">
      <div class="left-section">
        <div class="welcome-text">
          <h2>患者注册</h2>
          <p>欢迎使用我们的医疗服务，请填写以下信息完成注册</p>
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

          <el-form-item label="邮箱" prop="email">
            <el-input
              v-model="registerForm.email"
              placeholder="请输入邮箱"
              class="custom-input"
            >
              <template #prefix>
                <el-icon><Message /></el-icon>
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
  Message
} from '@element-plus/icons-vue'
import axios from 'axios'

export default {
  name: 'PatientRegister',
  components: {
    User,
    Lock,
    Phone,
    Message
  },
  setup() {
    const router = useRouter()
    const registerFormRef = ref(null)
    const loading = ref(false)

    const registerForm = reactive({
      phone: '',
      email: '',
      name: '',
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
      email: [
        { required: true, message: '请输入邮箱', trigger: 'blur' },
        { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
      ],
      name: [
        { required: true, message: '请输入姓名', trigger: 'blur' },
        { min: 2, max: 50, message: '长度在 2 到 50 个字符', trigger: 'blur' }
      ],
      password: [
        { required: true, validator: validatePass, trigger: 'blur' }
      ],
      confirmPassword: [
        { required: true, validator: validatePass2, trigger: 'blur' }
      ]
    }

    const handleRegister = async () => {
      if (!registerFormRef.value) return
      
      try {
        await registerFormRef.value.validate()
        loading.value = true
        
        const { confirmPassword, ...registerData } = registerForm
        
        const response = await axios.post('/api/user-service/patient/register', registerData)

        if (response.data.status === 'success') {
          ElMessage.success('注册成功')
          router.push('/login?type=patient')
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
      router.push('/login?type=patient')
    }

    return {
      registerForm,
      rules,
      registerFormRef,
      loading,
      handleRegister,
      goToLogin
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
  padding-top: 20px;
  margin-top:20px;
}

.register-box {
  display: flex;
  width: 1000px;
  max-width: 100%;
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
