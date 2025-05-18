import { createRouter, createWebHistory } from 'vue-router'

// 布局
import MainLayout from '@/layouts/MainLayout.vue'

// 页面
const HomePage = () => import('@/views/HomePage.vue')
const UserGuide = () => import('@/views/UserGuide.vue')
const FeedbackSystem = () => import('@/views/FeedbackSystem.vue')
const TreatmentFeedback = () => import('@/views/TreatmentFeedback.vue')
const RecoveryFeedback = () => import('@/views/RecoveryFeedback.vue')
const NotificationCenter = () => import('@/views/NotificationCenter.vue')
const UserTimeline = () => import('@/views/UserTimeline.vue')
const HealthAssistant = () => import('@/views/HealthAssistant.vue')

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      {
        path: '',
        name: 'Home',
        component: HomePage,
        meta: { title: '首页' }
      },
      {
        path: 'guide',
        name: 'UserGuide',
        component: UserGuide,
        meta: { title: '新手引导' }
      },
      {
        path: 'feedback',
        name: 'Feedback',
        component: FeedbackSystem,
        meta: { title: '系统反馈' }
      },
      {
        path: 'treatment-feedback',
        name: 'TreatmentFeedback',
        component: TreatmentFeedback,
        meta: { title: '就诊体验反馈' }
      },
      {
        path: 'recovery-feedback',
        name: 'RecoveryFeedback',
        component: RecoveryFeedback,
        meta: { title: '康复情况反馈' }
      },
      {
        path: 'notifications',
        name: 'Notifications',
        component: NotificationCenter,
        meta: { title: '消息中心' }
      },
      {
        path: 'timeline',
        name: 'Timeline',
        component: UserTimeline,
        meta: { title: '行为时间轴' }
      },
      {
        path: 'health-assistant',
        name: 'HealthAssistant',
        component: HealthAssistant,
        meta: { title: '健康日报助手' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由前置守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 互联网医疗系统` : '互联网医疗系统'
  
  // 这里可以添加登录验证等逻辑
  
  next()
})

export default router 