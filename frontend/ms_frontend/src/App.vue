<template>
  <div class="app-container">
    <router-view></router-view>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const router = useRouter()
    
    onMounted(() => {
      if (router.currentRoute.value.path === '/') {
        router.push('/home')
      }
    })
  }
}
</script>

<style>
#app {
  font-family: 'Inter', 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
  width: 100%;
  margin: 0;
  padding: 0;
}

.app-container {
  min-height: 100vh;
  width: 100%;
  margin: 0;
  padding: 0;
  overflow-x: hidden; /* 只隐藏横向滚动条 */
  overflow-y: auto;   /* 允许纵向滚动 */
}
</style>


