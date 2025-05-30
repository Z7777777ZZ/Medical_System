<template>
  <div class="doctor-layout">
    <el-container>
      <el-aside width="250px">
        <div class="logo-container">
          <h2>门诊医生系统</h2>
        </div>
        <el-menu
          router
          default-active="/doctor/dashboard"
          class="el-menu-vertical"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF">
          <el-menu-item index="/doctor/dashboard">
            <el-icon><el-icon-odometer /></el-icon>
            <span>工作台</span>
          </el-menu-item>
          <el-menu-item index="/doctor/queue">
            <el-icon><el-icon-user /></el-icon>
            <span>患者队列</span>
          </el-menu-item>
          <el-menu-item index="/doctor/prescription">
            <el-icon><el-icon-document /></el-icon>
            <span>处方管理</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-container>
        <el-header height="60px">
          <div class="header-right">
            <el-dropdown>
              <span class="el-dropdown-link">
                医生姓名<el-icon class="el-icon--right"><el-icon-arrow-down /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>个人信息</el-dropdown-item>
                  <el-dropdown-item>修改密码</el-dropdown-item>
                  <el-dropdown-item divided>退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useQueueStore } from '../stores/queueStore'

export default {
  name: 'DoctorLayout',
  setup() {
    const queueStore = useQueueStore()
    
    onMounted(() => {
      // 初始化数据
      queueStore.initData()
    })
    
    return {
      queueStore
    }
  }
}
</script>

<style scoped>
.doctor-layout {
  height: 100vh;
}

.logo-container {
  height: 60px;
  background-color: #263445;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.el-header {
  background-color: #fff;
  color: #333;
  line-height: 60px;
  border-bottom: 1px solid #e6e6e6;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-right {
  display: flex;
  align-items: center;
}

.el-menu-vertical {
  height: calc(100vh - 60px);
  border-right: none;
}

.el-aside {
  background-color: #304156;
  color: #fff;
}

.el-main {
  background-color: #f0f2f5;
  padding: 20px;
}

.el-dropdown-link {
  cursor: pointer;
  display: flex;
  align-items: center;
  font-size: 14px;
  color: #333;
}
</style>

<style>
/* 为了解决Element Plus图标不显示的问题 */
.el-icon {
  vertical-align: middle;
}
</style>