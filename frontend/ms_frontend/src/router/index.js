import component from 'element-plus/es/components/tree-select/src/tree-select-option.mjs'
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
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
    path: '/doctor/dashboard',
    name: 'DoctorDashboard',
    component: () => import('../views/doctor/DashboardView.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: 'profile',
        name: 'DoctorProfile',
        component: () => import('../views/doctor/DoctorProfile.vue')
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

export default router 