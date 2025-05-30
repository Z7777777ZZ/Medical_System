import { createRouter, createWebHistory } from 'vue-router'

// 医生端页面
import DoctorDashboard from '../views/doctor/Dashboard.vue'
import DoctorQueue from '../views/doctor/Queue.vue'
import DoctorPrescription from '../views/doctor/Prescription.vue'

// 患者端页面
import component from 'element-plus/es/components/tree-select/src/tree-select-option.mjs'
// 路由配置

const routes = [
  {
    path: '/home',
    name: 'home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/LoginView.vue')
  },
  {
    path: '/doctor',
    name: 'DoctorLayout',
    component: () => import('../layouts/DoctorLayout.vue'),
    children: [
      {
        path: '',
        redirect: { name: 'DoctorQueue' }
      },
      {
        path: 'dashboard',
        name: 'DoctorDashboard',
        component: DoctorDashboard
      },
      {
        path: 'queue',
        name: 'DoctorQueue',
        component: DoctorQueue
      },
      {
        path: 'prescription',
        name: 'DoctorPrescription',
        component: DoctorPrescription
      }
    ]
  },

  {
    path:'/doctor/register',
    name:'DoctorRegister',
    component: () => import('../views/auth/DoctorRegister.vue')
  },
  {
    path:'/patient/register',
    name:'PatientRegister',
    component: () => import('../views/auth/PatientRegister.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
// // 路由守卫
// router.beforeEach((to, from, next) => {
//   const token = localStorage.getItem('token')
  
//   if (to.meta.requiresAuth && !token) {
//     // 需要登录但未登录，重定向到登录页
//     next('/login')
//   } else {
//     next()
//   }
// })