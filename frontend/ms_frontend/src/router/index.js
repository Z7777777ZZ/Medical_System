import { createRouter, createWebHistory } from 'vue-router'

// 医生端页面
import DoctorDashboard from '../views/doctor/Dashboard.vue'
import DoctorQueue from '../views/doctor/Queue.vue'
import DoctorPrescription from '../views/doctor/Prescription.vue'

// 患者端页面
import PatientDashboard from '../views/patient/Dashboard.vue'
import PatientQueue from '../views/patient/Queue.vue'
import PatientPrescription from '../views/patient/Prescription.vue'

// 路由配置
const routes = [
  {
    path: '/',
    redirect: '/doctor/queue'  // 直接进入医生队列页面
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
    path: '/patient',
    name: 'PatientLayout',
    component: () => import('../layouts/PatientLayout.vue'),
    children: [
      {
        path: '',
        redirect: { name: 'PatientDashboard' }
      },
      {
        path: 'dashboard',
        name: 'PatientDashboard',
        component: PatientDashboard
      },
      {
        path: 'queue',
        name: 'PatientQueue',
        component: PatientQueue
      },
      {
        path: 'prescription',
        name: 'PatientPrescription',
        component: PatientPrescription
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router