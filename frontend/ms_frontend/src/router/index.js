import { createRouter, createWebHistory } from 'vue-router'
import UserExperience from '../views/UserExperience.vue'
// import GuideTour from '../views/GuideTour.vue'
// import FeedbackSystem from '../views/FeedbackSystem.vue'
// import MessagePush from '../views/MessagePush.vue'
// import UserTimeline from '../views/UserTimeline.vue'
// import HealthDaily from '../views/HealthDaily.vue'

const routes = [
  {
    path: '/',
    component: UserExperience,
    // children: [
    //   {
    //     path: 'guide',
    //     component: GuideTour
    //   },
    //   {
    //     path: 'feedback',
    //     component: FeedbackSystem
    //   },
    //   {
    //     path: 'messages',
    //     component: MessagePush
    //   },
    //   {
    //     path: 'timeline',
    //     component: UserTimeline
    //   },
    //   {
    //     path: 'health',
    //     component: HealthDaily
    //   }
    // ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router