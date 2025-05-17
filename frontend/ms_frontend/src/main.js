import { createApp } from 'vue'
import App from './App.vue'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router/index.js'
import * as ElementPlusIconsVue from '@element-plus/icons-vue' // 添加这行导入
// import Driver from "driver.js";
// import "driver.js/dist/driver.min.css";

const app = createApp(App)

// 注册所有Element Plus图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(ElementPlus)
app.use(router)
// app.config.globalProperties.$driver = new Driver();
app.mount('#app')