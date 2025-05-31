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
    path: '/',
    redirect: '/home'
  },
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
    path: '/patient/dashboard',
    name: 'PatientDashboard',
    component: () => import('../views/patient/DashboardView.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: 'profile',
        name: 'PatientProfile',
        component: () => import('../views/patient/PatientProfile.vue')
      }
    ]
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
  },
  // 用户体验模块路由
  {
    path: '/ue',
    name: 'UserExperience',
    component: () => import('../views/ue/HomePage.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/ue/guide',
    name: 'UserGuide',
    component: () => import('../views/ue/UserGuide.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/ue/feedback',
    name: 'FeedbackSystem',
    component: () => import('../views/ue/FeedbackSystem.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/ue/treatment-feedback',
    name: 'TreatmentFeedback',
    component: () => import('../views/ue/TreatmentFeedback.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/ue/recovery-feedback',
    name: 'RecoveryFeedback',
    component: () => import('../views/ue/RecoveryFeedback.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/ue/notifications',
    name: 'NotificationCenter',
    component: () => import('../views/ue/NotificationCenter.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/ue/timeline',
    name: 'UserTimeline',
    component: () => import('../views/ue/UserTimeline.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/ue/health-assistant',
    name: 'HealthAssistant',
    component: () => import('../views/ue/HealthAssistant.vue'),
    meta: { requiresAuth: true }
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