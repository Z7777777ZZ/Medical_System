import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './assets/styles/global.css'
import axios from 'axios'

// 配置axios默认URL
axios.defaults.baseURL = 'http://localhost:5000/api'

const app = createApp(App)
// 全局配置
app.config.globalProperties.$axios = axios

// 使用插件
app.use(createPinia())



app.use(ElementPlus)
app.use(router)
app.mount('#app')
