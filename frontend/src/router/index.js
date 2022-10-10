import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import UserView from '../views/UserView.vue'
import MessageView from '../views/MessageView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: LoginView
    },
    {
      path: '/users',
      name: 'user',
      component: UserView,
    },
    {
      path: '/im',
      name: 'im',
      component: MessageView,
    }
    // {
    //   path: '/about',
    //   name: 'about',
    //   // route level code-splitting
    //   // this generates a separate chunk (About.[hash].js) for this route
    //   // which is lazy-loaded when the route is visited.
    //   component: () => import('../views/AboutView.vue')
    // }
  ]
})

export default router
