<template>
  <div class="home">
    <!-- 顶部导航栏 -->
    <div class="header">
      <div class="header-content">
        <div class="logo">
          <h1>医院管理系统</h1>
        </div>
        <div class="nav-links">
          <el-button type="text" @click="goToDashboard">患者入口</el-button>
          <el-button type="text" @click="goToLogin('doctor')">医生入口</el-button>
        </div>
      </div>
    </div>

    <!-- 主要内容区 -->
    <div class="main-content">
      <div class="banner">
        <h2>大医精诚 尚美至善</h2>
        <p>专业医疗团队，为您提供优质医疗服务</p>
      </div>

      <div class="entrance-cards">
        <el-card class="entrance-card" @click="goToDashboard">
          <div class="card-content">
            <el-icon class="card-icon"><User /></el-icon>
            <h3>患者入口</h3>
            <p>预约挂号、查看报告、在线咨询</p>
          </div>
        </el-card>

        <el-card class="entrance-card" @click="goToLogin('doctor')">
          <div class="card-content">
            <el-icon class="card-icon"><FirstAidKit /></el-icon>
            <h3>医生入口</h3>
            <p>患者管理、诊断记录、排班管理</p>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 页脚 -->
    <div class="footer">
      <div class="footer-content">
        <p>医院地址：XX市XX区XX路XX号</p>
        <p>联系电话：123-456-7890</p>
        <p>© 2024 医院管理系统 版权所有</p>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { User, FirstAidKit } from '@element-plus/icons-vue'

export default {
  name: 'HomeView',
  components: {
    User,
    FirstAidKit
  },
  setup() {
    const router = useRouter()

    const goToLogin = (type) => {
      router.push({path:'/login',query: { type }})
    }
    const goToDashboard = () => {
      router.push({path:'/patient/dashboard'})
    }
    return {
      goToLogin,
      goToDashboard
    }
  }
}
</script>

<style scoped>
.home {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 10px 0;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.logo h1 {
  margin: 0;
  color: #409EFF;
  font-size: 24px;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.main-content {
  flex: 1;
  padding: 40px 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.banner {
  text-align: center;
  margin-bottom: 60px;
}

.banner h2 {
  font-size: 32px;
  color: #333;
  margin-bottom: 20px;
}

.banner p {
  font-size: 18px;
  color: #666;
}

.entrance-cards {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-top: 40px;
}

.entrance-card {
  width: 300px;
  cursor: pointer;
  transition: transform 0.3s;
}

.entrance-card:hover {
  transform: translateY(-5px);
}

.card-content {
  text-align: center;
  padding: 30px;
}

.card-icon {
  font-size: 48px;
  color: #409EFF;
  margin-bottom: 20px;
}

.card-content h3 {
  font-size: 24px;
  color: #333;
  margin-bottom: 10px;
}

.card-content p {
  color: #666;
  font-size: 16px;
}

.footer {
  background-color: #f5f7fa;
  padding: 20px 0;
  margin-top: auto;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
  color: #666;
}

.footer-content p {
  margin: 5px 0;
}
</style>
