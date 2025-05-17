import { createApp } from 'vue'
import App from './App.vue'

import './assets/aidg-css/main.css'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import router from './router'

// 不能先挂载#app
// const app = createApp(App).mount('#app')
const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.use(router)
app.use(ElementPlus)

app.mount('#app')