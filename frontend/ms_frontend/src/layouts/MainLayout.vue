<template>
  <div class="main-layout">
    <el-container>
      <!-- 头部 -->
      <el-header height="60px">
        <div class="header-container">
          <div class="logo">
            <router-link to="/">
              <h1>互联网医疗系统</h1>
            </router-link>
          </div>
          <div class="nav-menu">
            <el-menu
              mode="horizontal"
              :ellipsis="false"
              :default-active="activeIndex"
              router
              background-color="#409EFF"
              text-color="#fff"
              active-text-color="#fff"
            >
              <el-menu-item index="/">首页</el-menu-item>
              <el-menu-item index="/guide">新手引导</el-menu-item>
              <el-sub-menu index="feedback">
                <template #title>用户反馈</template>
                <el-menu-item index="/feedback">系统反馈</el-menu-item>
                <el-menu-item index="/treatment-feedback">就诊体验反馈</el-menu-item>
                <el-menu-item index="/recovery-feedback">康复情况反馈</el-menu-item>
              </el-sub-menu>
              <el-menu-item index="/timeline">行为时间轴</el-menu-item>
              <el-menu-item index="/health-assistant">健康日报助手</el-menu-item>
            </el-menu>
          </div>
          <div class="user-actions">
            <el-badge :value="unreadCount" class="notification-badge" v-if="unreadCount > 0">
              <el-button @click="goToNotifications" circle>
                <el-icon><Bell /></el-icon>
              </el-button>
            </el-badge>
            <el-button @click="goToNotifications" circle v-else>
              <el-icon><Bell /></el-icon>
            </el-button>
            
            <el-dropdown trigger="click">
              <el-avatar :size="40" src="https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png" />
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>个人中心</el-dropdown-item>
                  <el-dropdown-item>我的预约</el-dropdown-item>
                  <el-dropdown-item>退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>
      
      <!-- 内容区 -->
      <el-main>
        <div class="container">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </el-main>
      
      <!-- 页脚 -->
      <el-footer height="50px">
        <div class="footer-container">
          <p>&copy; {{ currentYear }} 互联网医疗系统 版权所有</p>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Bell } from '@element-plus/icons-vue'
import axios from 'axios'

const router = useRouter()
const route = useRoute()

// 当前激活菜单
const activeIndex = computed(() => route.path)

// 未读消息数量
const unreadCount = ref(0)

// 当前年份
const currentYear = computed(() => new Date().getFullYear())

// 获取未读消息数量
const getUnreadNotifications = async () => {
  try {
    // 模拟用户ID，实际应从登录状态获取
    const patientId = 1
    const { data } = await axios.get(`/api/notifications/${patientId}`)
    if (data.status === 'success') {
      unreadCount.value = data.data.unread_count
    }
  } catch (error) {
    console.error('获取未读消息失败:', error)
    // 模拟数据
    unreadCount.value = 3
  }
}

// 跳转到通知页面
const goToNotifications = () => {
  router.push('/notifications')
}

// 组件挂载时获取未读消息
onMounted(() => {
  getUnreadNotifications()
  
  // 定时刷新未读消息数量 (每分钟)
  setInterval(() => {
    getUnreadNotifications()
  }, 60000)
})
</script>

<style scoped>
.main-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.el-container {
  min-height: 100vh;
}

.el-header {
  background-color: #409EFF;
  color: #fff;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 20px;
}

.logo {
  display: flex;
  align-items: center;
}

.logo h1 {
  font-size: 20px;
  color: #fff;
  margin: 0;
}

.nav-menu {
  flex: 1;
  margin-left: 20px;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.notification-badge {
  margin-right: 10px;
}

.el-main {
  padding: 20px 0;
  flex: 1;
}

.el-footer {
  background-color: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #606266;
  font-size: 14px;
  border-top: 1px solid #e4e7ed;
}

.footer-container {
  width: 100%;
  max-width: 1200px;
  text-align: center;
}

@media (max-width: 768px) {
  .header-container {
    flex-direction: column;
    padding: 10px;
  }
  
  .nav-menu {
    margin-left: 0;
    margin-top: 10px;
    width: 100%;
  }
  
  .user-actions {
    margin-top: 10px;
  }
  
  .el-header {
    height: auto !important;
  }
}
</style> 