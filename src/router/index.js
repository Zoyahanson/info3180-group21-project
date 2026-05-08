import { createRouter, createWebHistory } from 'vue-router'

import LoginView        from '../views/LoginView.vue'
import RegisterView     from '../views/RegisterView.vue'
import DashboardView    from '../views/DashboardView.vue'
import MatchesView      from '../views/MatchesView.vue'
import ConversationsView from '../views/ConversationsView.vue'
import MessagesView     from '../views/MessagesView.vue'
import ProfileView      from '../views/ProfileView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),

  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/matches',
      name: 'matches',
      component: MatchesView
    },
    {
      path: '/messages',
      name: 'conversations',
      component: ConversationsView
    },
    {
      path: '/messages/:matchId',
      name: 'messages',
      component: MessagesView
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView
    }
  ]
})

export default router
