import { createRouter, createWebHistory } from 'vue-router'
// import BookVue from '@/components/Book.vue'
// import CardVue from '@/components/Card.vue'
// import BorrowVue from '@/components/Borrow.vue'
import AIDiagnosisView from '@/views/AIDiagnosisView.vue'
import DoctorSearchView from '@/views/DoctorSearchView.vue'

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/ai-diagnosis'
    },
    {
      path: '/ai-diagnosis',
      component: AIDiagnosisView
    },
    {
      path: '/doctor-search',
      component: DoctorSearchView
    },
    // {
    //   path: '/borrow',
    //   component: BorrowVue
    // }
  ]
})

export default router
