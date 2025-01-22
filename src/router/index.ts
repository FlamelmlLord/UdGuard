import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import recoverPasswordView from '@/views/recoverPasswordView.vue'
import dashboardHomeView from '@/views/dashboardHomeView.vue'

Vue.use(VueRouter)

const routes: Array<RouteConfig> = [

  {
    path: '/',
    name: 'Login',
    component: LoginView
  },

  {
    path: '/dashboard',
    name: 'dashboard',
    component: dashboardHomeView
  },

  {
    path: '/recover-password',
    name: 'recover-password',
    component: recoverPasswordView
  }

]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
