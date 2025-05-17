import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  // Patient Routes
  {
    path: '/patient',
    name: 'PatientLayout',
    component: () => import('../views/patient/Layout.vue'),
    children: [
      {
        path: '',
        name: 'PatientHome',
        component: () => import('../views/Home.vue')
      },
      {
        path: 'home',
        name: 'PatientHomeRedirect',
        component: () => import('../views/Home.vue')
      },
      {
        path: 'medical-records',
        name: 'MedicalRecords',
        component: () => import('../views/patient/MedicalRecords.vue')
      },
      {
        path: 'appointment',
        name: 'Appointment',
        component: () => import('../views/patient/Appointment.vue')
      },
      {
        path: 'payment',
        name: 'Payment',
        component: () => import('../views/patient/Payment.vue')
      },
      {
        path: 'payment-history',
        name: 'PaymentHistory',
        component: () => import('../views/patient/PaymentHistory.vue')
      },
      {
        path: 'appointments',
        name: 'Appointments',
        component: () => import('../views/patient/Appointments.vue')
      },
      {
        path: 'records',
        name: 'PatientRecords',
        component: () => import('../views/patient/MedicalRecords.vue')
      }
    ]
  },
  // Doctor Routes
  {
    path: '/doctor',
    name: 'DoctorLayout',
    component: () => import('../views/doctor/Layout.vue'),
    children: [
      {
        path: 'medical-records-edit',
        name: 'MedicalRecordsEdit',
        component: () => import('../views/doctor/MedicalRecordsEdit.vue')
      }
    ]
  },
  // Catch all route for 404
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})


export default router 