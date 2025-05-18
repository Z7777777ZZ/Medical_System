import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import VueTimeago from 'vue3-timeago'
import zhCN from 'date-fns/locale/zh-CN'
import axios from 'axios'
import { ElMessage } from 'element-plus'

import './assets/styles/main.scss'

// 配置axios的全局错误处理
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.code === 'ECONNABORTED' || error.message.includes('Network Error') || error.message.includes('timeout')) {
      console.warn('API请求超时或网络错误:', error.config.url)
      ElMessage.error('网络连接错误，请稍后再试')
    }
    return Promise.reject(error)
  }
)

const app = createApp(App)

// 全局错误处理
app.config.errorHandler = (err, vm, info) => {
  console.error('Vue错误:', err)
  console.info('组件:', vm)
  console.info('错误信息:', info)
}

app.use(router)
app.use(createPinia())
app.use(ElementPlus, {
  locale: zhCn,
  size: 'default'
})
app.use(VueTimeago, {
  name: 'TimeAgo',
  locale: 'zh-CN',
  locales: {
    'zh-CN': zhCN
  }
})

app.mount('#app')
