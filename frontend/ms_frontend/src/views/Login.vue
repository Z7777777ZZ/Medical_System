<template>
  <div class="login-container">
    <div class="login-box">
      <h2 class="title">医疗系统门诊部</h2>
      <el-form ref="formRef" :model="loginForm" :rules="loginRules" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="用户类型" prop="userType">
          <el-radio-group v-model="loginForm.userType">
            <el-radio label="doctor">医生</el-radio>
            <el-radio label="patient">患者</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleLogin" :loading="loading">登录</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

export default {
  name: 'LoginPage',
  setup() {
    const router = useRouter()
    const loading = ref(false)
    const formRef = ref(null)
    
    const loginForm = reactive({
      username: '',
      password: '',
      userType: 'doctor'
    })
    
    const loginRules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' }
      ],
      userType: [
        { required: true, message: '请选择用户类型', trigger: 'change' }
      ]
    }
    
    const handleLogin = async () => {
      if (!formRef.value) return
      
      await formRef.value.validate((valid) => {
        if (!valid) return
        
        loading.value = true
        
        // 模拟登录
        setTimeout(() => {
          loading.value = false
          
          if (loginForm.userType === 'doctor') {
            router.push('/doctor/queue')
            ElMessage.success('医生登录成功')
          } else {
            router.push('/patient/queue')
            ElMessage.success('患者登录成功')
          }
        }, 1000)
      })
    }
    
    return {
      loading,
      loginForm,
      loginRules,
      formRef,
      handleLogin
    }
  }
}
</script>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  width: 400px;
  padding: 40px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  margin-bottom: 30px;
  color: #409EFF;
  font-weight: 600;
}
</style>