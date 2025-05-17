import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import axios from 'axios'

// Set base URL for axios
axios.defaults.baseURL = 'http://localhost:5000'

// Add request logging for debugging
axios.interceptors.request.use(config => {
  console.log('Making request to:', config.url)
  return config
})

const app = createApp(App)

// Use plugins
app.use(createPinia())
app.use(router)
app.use(ElementPlus)

// Mount app
app.mount('#app')
