<template>
  <div class="dashboard-facts-container">
    <div class="dashboard-content">
      <div class="dashboard-title-container">
        <h2 class="dashboard-title">Gestor de Factores</h2>
      </div>

      <div class="factores-container">
        <div class="factores-grid">
          <div
            v-for="factor in factores"
            :key="factor.id"
            class="factor-card"
            :class="getFactorClass(factor.estado.color)"
          >
            <div class="factor-card-header" >
              <h3 class="factor-title">{{ factor.nombre }}</h3>
              <div class="factor-status" :style="{ backgroundColor: factor.estado.color }">
                <span :class="['status-indicator']">
                  {{ factor.estado.descripcion }}
                </span>
              </div>
            </div>

            <div class="factor-card-body">
              <ul class="factor-details">
                <li v-for="alerta in factor.caracteristicas" :key="alerta.nombre">
                  {{ alerta.nombre }}
                </li>
              </ul>
            </div>

            <div class="factor-card-footer">
              <button
                class="view-button"
                @click="navigateToDashboardCharacteristics(factor)"
              >
                Ver
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 18l6-6-6-6"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../../plugins/Axios'

export default {
  name: 'DashboardFacts',
  
  data() {
    return {
      factores: [

      ],
      loading: false,
      error: null
    }
  },

  methods: {
    checkAuthentication() {
      const token = localStorage.getItem('access_token')
      console.log('Token in DashboardFacts:', token ? 'Present' : 'Missing')
      
      if (!token) {
        console.log('No token found, redirecting to login')
        this.$router.push('/login')
        return false
      }
      return true
    },

    async fetchFactores() {
      if (!this.checkAuthentication()) return
      
      this.loading = true
      this.error = null
      
      try {
        const token = localStorage.getItem('access_token')
        console.log('Making API request with token')
        
        const response = await axios.get('/factors/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        
        console.log('API response received Factors:', response.data)
        this.factores = response.data
        // Procesar datos...
        
      } catch (error) {
        console.error('Error fetching factors:', error)
        
        // Si es error 401, el token expiró
        if (error.response?.status === 401) {
          console.log('Token expired, clearing auth data')
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user_data')
          this.$router.push('/login')
        }
      } finally {
        this.loading = false
      }
    },

    getFactorClass (estado) {
      return {
        verde: 'factor-card--verde',
        amarillo: 'factor-card--amarillo',
        rojo: 'factor-card--rojo'
      }[estado]
    },

    navigateToDashboardCharacteristics (factor) {
      this.$router.push({
        name: 'DashboardCharacteristics',
        params: { factorId: factor.id, titulo:factor.nombre }
      })
    }
  },

  // Verificar autenticación al montar el componente
  async mounted() {

    console.log('DashboardFacts mounted')
    
    if (this.checkAuthentication()) {
      console.log('User authenticated, loading data')
      await this.fetchFactores() // Descomenta cuando quieras usar la API
    }
  }
}
</script>

<style lang="css"> @import '../../styles/dashboard_facts.css'; </style>
