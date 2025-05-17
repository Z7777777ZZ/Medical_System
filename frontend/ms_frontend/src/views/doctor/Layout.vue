<template>
  <div class="layout-container">
    <el-container>
      <el-header>
        <div class="header-content">
          <div class="logo">
            <h2>医疗系统 - 医生端</h2>
          </div>
          <el-menu
            mode="horizontal"
            :router="true"
            :default-active="activeMenu"
            class="nav-menu"
          >
            <el-menu-item index="/doctor/medical-records-edit">
              <el-icon><Edit /></el-icon>
              <span>病例编辑</span>
            </el-menu-item>
          </el-menu>
          <div class="user-actions">
            <el-dropdown>
              <span class="user-dropdown">
                <el-avatar :size="32" :src="userAvatar">{{ userInitials }}</el-avatar>
                <span class="username">{{ username }}</span>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </div>
      </el-header>
      
      <el-main>
        <router-view />
      </el-main>
      
      <el-footer>
        <div class="footer-content">
          &copy; {{ currentYear }} 医疗系统 - 患者就诊流程管理子系统
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'
import { useDoctorStore } from '../../store/doctor'
import { Edit } from '@element-plus/icons-vue'
import { ElMessageBox } from 'element-plus'

export default {
  name: 'DoctorLayout',
  components: {
    Edit
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    const doctorStore = useDoctorStore()
    
    // Get active menu item
    const activeMenu = computed(() => route.path)
    
    // User information
    const username = computed(() => authStore.currentUser?.name || '医生')
    const userAvatar = computed(() => authStore.currentUser?.avatar || '')
    const userInitials = computed(() => {
      const name = username.value
      return name ? name.charAt(0).toUpperCase() : 'D'
    })
    
    // Current year for footer
    const currentYear = new Date().getFullYear()
    
    // Logout function
    const logout = () => {
      ElMessageBox.confirm(
        '确定要退出登录吗？',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(() => {
        authStore.logout()
        doctorStore.resetState()
        router.push('/')
      }).catch(() => {})
    }
    
    return {
      activeMenu,
      username,
      userAvatar,
      userInitials,
      currentYear,
      logout
    }
  }
}
</script>

<style scoped>
.layout-container {
  min-height: 100vh;
}

.el-header {
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: relative;
  padding: 0;
  height: auto !important;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
  padding: 0 20px;
}

.logo {
  flex-shrink: 0;
}

.logo h2 {
  margin: 0;
  color: #409EFF;
}

.nav-menu {
  margin-left: 40px;
  flex-grow: 1;
  border-bottom: none;
}

.user-actions {
  margin-left: 20px;
}

.user-dropdown {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.username {
  margin-left: 8px;
  font-size: 14px;
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 120px);
}

.el-footer {
  background-color: #fff;
  padding: 20px;
  text-align: center;
  color: #909399;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}
</style> 