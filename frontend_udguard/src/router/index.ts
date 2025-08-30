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
        path: 'facts',
        name: 'DashboardFacts',
        component: () => import('@/components/Dashboard/DashboardFacts.vue')
      },
      {
        path: 'facts/:factorId/characteristics',
        name: 'DashboardCharacteristics',
        component: () => import('@/components/Dashboard/DashboardCharacteristics.vue'),
        props: true
      },
      {
        path: 'Cumplimiento/:caracteristicaId',
        name: 'DashboardIndicators',
        props: true,
        component: () => import('@/components/Dashboard/DashboardIndicators.vue') // 👈 Aquí se añade la nueva ruta
      },
      {
        path: 'users',
        name: 'DashboardUsers',
        component: () => import('@/components/DashboardUser/UserSettings.vue')
      },
      {
        path: 'home',
        name: 'DashboardHome',
        component: () => import('@/components/Dashboard/DashboardHome.vue')
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
