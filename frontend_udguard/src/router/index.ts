import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import dashboardHomeView from '@/views/dashboardHomeView.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../components/auth/LoginHome.vue')
  },
  {
    path: '/recover-password',
    name: 'RecoverPassword',
    component: () => import('../components/auth/RecoverPassword.vue')
  },
  {
    path: '/dashboard',
    component: dashboardHomeView,
    children: [
      {
        path: 'docs',
        name: 'DashboardDocs',
        component: () => import('@/components/Dashboard/DashboardDocs.vue')
      },
      {
        path: 'facts',
        name: 'DashboardFacts',
        component: () => import('@/components/Dashboard/DashboardFacts.vue')
      },
      {
        path: 'features/:factorId',
        name: 'DashboardFeatures',
        component: () => import('@/components/Dashboard/DashboardFeatures.vue'),
        props: true
      }
    ]
  },
  {
    path: '*',
    redirect: '/login'
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
