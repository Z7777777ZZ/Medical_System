<template>
  <div class="login-container">
    <div class="login-box">
      <!-- 左侧注册提示 -->
      <div class="left-section">
        <div class="welcome-text">
          <h2>欢迎使用</h2>
          <p>如果您还没有账号，请点击下方按钮进行注册</p>
        </div>
        <el-button 
          type="primary" 
          class="register-button"
          @click="goToRegister"
        >
          立即注册
        </el-button>
      </div>

      <!-- 右侧登录表单 -->
      <div class="right-section">
        <div class="login-form">
          <h2>{{ isDoctor ? '医生登录' : '患者登录' }}</h2>
          <el-form :model="loginForm" :rules="rules" ref="loginFormRef">
            <el-form-item prop="phone">
              <el-input
                v-model="loginForm.phone"
                placeholder="请输入手机号"
                class="custom-input"
              >
                <template #prefix>
                  <el-icon><User /></el-icon>
                </template>
              </el-input>
            </el-form-item>
            
            <el-form-item prop="password">
              <el-input
                v-model="loginForm.password"
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

            <div class="form-options">
              <el-checkbox v-model="rememberMe">记住我</el-checkbox>
              <a href="#" class="forgot-password">忘记密码？</a>
            </div>

            <el-form-item>
              <el-button 
                type="primary" 
                @click="handleLogin" 
                :loading="loading" 
                class="login-button"
              >
                登录
              </el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import axios from 'axios'

export default {
  name: 'LoginView',
  components: {
    User,
    Lock
  },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const loginFormRef = ref(null)
    const loading = ref(false)
    const rememberMe = ref(false)
    
    const isDoctor = computed(() => {
      return route.query.type === 'doctor'
    })
    
    const loginForm = reactive({
      phone: '',
      password: ''
    })

    const rules = {
      phone: [
        { required: true, message: '请输入手机号', trigger: 'blur' },
        { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码长度不能小于6位', trigger: 'blur' }
      ]
    }

    const handleLogin = async () => {
      if (!loginFormRef.value) return
      
      try {
        await loginFormRef.value.validate()
        loading.value = true
        // 确保使用正确的 API 路径
        const loginEndpoint = isDoctor.value ? '/api/user-service/doctor/login' : '/api/user-service/patient/login'
        console.log('Login endpoint:', loginEndpoint)
        
        const response = await axios.post(loginEndpoint, {
          phone: loginForm.phone,
          password: loginForm.password,
          //type: isDoctor.value ? 'doctor' : 'patient'
        }, {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          }
          // 移除 withCredentials: true，因为它可能导致预检请求失败
        })

        if (response.data.status === 'success') {
          //localStorage.setItem('user', JSON.stringify(response.data.data))
          localStorage.setItem(isDoctor.value?'doctor_id':'patient_id', isDoctor.value?response.data.data.doctor_id:response.data.data.patient_id)
          localStorage.setItem('token', response.data.data.token)
          
          if (response.data.data.patient_id) {
            router.push('/patient/dashboard')
          } else if (response.data.data.doctor_id) {
            router.push('/doctor/dashboard')
          }
          
          ElMessage.success('登录成功')
        } else {
          ElMessage.error(response.data.message || '登录失败')
        }
      } catch (error) {
        ElMessage.error(error.response?.data?.message || '登录失败，请稍后重试')
      } finally {
        loading.value = false
      }
    }

    const goToRegister = () => {
      router.push({
        path: isDoctor.value?'/doctor/register':'/patient/register',
        //query: { type: isDoctor.value ? 'doctor' : 'patient' }
      })
    }

    return {
      loginForm,
      rules,
      loginFormRef,
      loading,
      rememberMe,
      isDoctor,
      handleLogin,
      goToRegister
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  width: 100vw;
  position: fixed;
  top: 0;
  left: 0;
  /*background: linear-gradient(135deg, #b0b2b9 0%, #182848 100%);*/
  background: white;
  background-size: 400% 400%;
  animation: gradient 15s ease infinite;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

@keyframes gradient {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.login-box {
  display: flex;
  width: 900px;
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  position: relative;
  z-index: 1;
}

.login-box::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
  pointer-events: none;
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

.left-section::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
  transform: rotate(30deg);
  pointer-events: none;
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

.register-button {
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

.register-button:hover {
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

.login-form {
  max-width: 320px;
  margin: 0 auto;
}

.login-form h2 {
  text-align: center;
  color: #333;
  margin-bottom: 40px;
  font-size: 28px;
  font-weight: 600;
}

.custom-input {
  height: 50px;
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

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.forgot-password {
  color: #4b6cb7;
  text-decoration: none;
  font-size: 14px;
  transition: all 0.3s ease;
}

.forgot-password:hover {
  color: #182848;
  text-decoration: underline;
}

.login-button {
  width: 100%;
  height: 50px;
  font-size: 16px;
  border-radius: 25px;
  background: linear-gradient(135deg, #4b6cb7 0%, #182848 100%);
  border: none;
  transition: all 0.3s ease;
  font-weight: 500;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(75, 108, 183, 0.3);
}

:deep(.el-checkbox__label) {
  color: #666;
  font-size: 14px;
}

:deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: #4b6cb7;
  border-color: #4b6cb7;
}

:deep(.el-checkbox__input.is-checked + .el-checkbox__label) {
  color: #4b6cb7;
}

:deep(.el-icon) {
  color: #4b6cb7;
  font-size: 18px;
}
</style>
