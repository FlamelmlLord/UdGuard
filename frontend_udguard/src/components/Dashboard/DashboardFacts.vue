<template>
  <div class="dashboard-facts-container">
    <div class="dashboard-header-factores">
      <div class="dashboard-header-content">
        <svg class="dashboard-header-icon" width="38" height="38" viewBox="0 0 24 24" fill="none">
          <circle cx="12" cy="12" r="10" stroke="#46AFEA" stroke-width="2"/>
          <path d="M8 12l2 2 4-4" stroke="#22c55e" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <div>
          <h2 class="dashboard-title">Gestor de Factores</h2>
          <p class="dashboard-subtitle">
            Visualiza y gestiona el estado de los factores clave del programa. Haz clic en <b>Ver</b> para profundizar en cada uno.
          </p>
        </div>
      </div>
    </div>
    <div class="dashboard-content">
      <div class="factores-container">
        <div class="factores-grid">
          <div
            v-for="factor in factores"
            :key="factor.id"
            class="factor-card"
          >
            <div class="factor-card-header">
              <h3 class="factor-title">{{ factor.nombre }}</h3>
              <div
                class="factor-status"
                :class="{
                  'status-green': getEstadoColor(factor).label === 'Alto',
                  'status-yellow': getEstadoColor(factor).label === 'Medio',
                  'status-red': getEstadoColor(factor).label === 'Bajo',
                  'status-gray': getEstadoColor(factor).label === 'Sin datos'
                }"
                :title="getEstadoColor(factor).label"
              >
                <span class="status-indicator">
                  {{ getEstadoColor(factor).label }}
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

    getEstadoColor(factor) {
      // Si no hay características, estado gris
      if (!factor.caracteristicas || factor.caracteristicas.length === 0) {
        return { color: '#6b7280', label: 'Sin datos' }
      }
      // Calcula el promedio de cumplimiento
      const promedios = factor.caracteristicas
        .map(c => Number(c.cumplimiento))
        .filter(v => !isNaN(v))
      if (promedios.length === 0) return { color: '#6b7280', label: 'Sin datos' }
      const promedio = promedios.reduce((a, b) => a + b, 0) / promedios.length
      if (promedio >= 4) return { color: '#22c55e', label: 'Alto' }// Verde
      if (promedio >= 3) return { color: '#eab308', label: 'Medio' }// Amarillo
      return { color: '#ef4444', label: 'Bajo' }// Rojo
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
