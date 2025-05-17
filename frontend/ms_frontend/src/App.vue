<template>
  <div class="app-container">
    <el-config-provider>
      <router-view />
    </el-config-provider>
  </div>
</template>

<script>
import { useAuthStore } from './store/auth'
import axios from 'axios'

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore()
    
    // Check if token exists on app load
    if (authStore.token) {
      // Set axios auth header if token exists
      const token = authStore.token
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`
    }
    
    return {
      authStore
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB',
    'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f7fa;
}

.app-container {
  min-height: 100vh;
}

.page-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}
</style>
