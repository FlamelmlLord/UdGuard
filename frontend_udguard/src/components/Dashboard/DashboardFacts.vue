<template>
  <div class="dashboard-facts-wrapper">
    <div class="dashboard-facts-container">
      <!-- Header mejorado y centrado -->
      <div class="dashboard-header-factores">
        <div class="dashboard-header-content">
          <div class="header-text-content">
            <h1 class="dashboard-title">Gestor de Factores</h1>
            <p class="dashboard-subtitle">
              Visualiza y gestiona el estado de los factores clave del programa. Haz clic en <strong>Ver</strong> para profundizar en cada uno.
            </p>
          </div>
        </div>
      </div>

      <!-- Contenido principal -->
      <div class="dashboard-content">
        <div class="factores-container">
          <div v-if="loading" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Cargando factores...</p>
          </div>
          
          <div v-else-if="error" class="error-state">
            <div class="error-icon">⚠️</div>
            <p>{{ error }}</p>
            <button @click="fetchFactores" class="retry-button">Reintentar</button>
          </div>

          <div v-else class="factores-grid">
            <div
              v-for="factor in factores"
              :key="factor.id"
              class="factor-card"
            >
              <div class="factor-card-header">
                <h3 class="factor-title">{{ factor.nombre }}</h3>
                <div
                  class="factor-status"
                  :class="getEstadoColorClass(factor)"
                  :title="`${getEstadoColor(factor).label} - Promedio: ${getPromedioCumplimiento(factor).toFixed(1)}`"
                >
                  <span class="status-indicator">
                    {{ getEstadoColor(factor).label }}
                  </span>
                  <span v-if="factor.caracteristicas && factor.caracteristicas.length > 0" class="status-score">
                    {{ getPromedioCumplimiento(factor).toFixed(1) }}
                  </span>
                </div>
              </div>
              
              <div class="factor-card-body">
                <ul class="factor-details" v-if="factor.caracteristicas && factor.caracteristicas.length > 0">
                  <li v-for="caracteristica in factor.caracteristicas" :key="caracteristica.nombre">
                    {{ caracteristica.nombre }}
                  </li>
                </ul>
                <div v-else class="no-data-message">
                  <span class="no-data-icon">📊</span>
                  <p>No hay datos disponibles</p>
                </div>
              </div>
              
              <div class="factor-card-footer">
                <button
                  class="view-button"
                  @click="navigateToDashboardCharacteristics(factor)"
                >
                  <span>Ver detalles</span>
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
  </div>
</template>

<script>
import axios from '../../plugins/Axios'

export default {
  name: 'DashboardFacts',
  
  data() {
    return {
      factores: [],
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
        
      } catch (error) {
        console.error('Error fetching factors:', error)
        
        // Si es error 401, el token expiró
        if (error.response?.status === 401) {
          console.log('Token expired, clearing auth data')
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user_data')
          this.$router.push('/login')
        } else {
          this.error = 'Error al cargar los factores. Por favor, intenta nuevamente.'
        }
      } finally {
        this.loading = false
      }
    },

    getEstadoColor(factor) {
      // Si no hay características, estado gris
      if (!factor.caracteristicas || factor.caracteristicas.length === 0) {
        return { color: '#6b7280', label: 'Sin datos' }
      }
      
      // Calcula el promedio de cumplimiento usando la nueva función
      const promedio = this.getPromedioCumplimiento(factor)
      
      if (promedio === 0) return { color: '#6b7280', label: 'Sin datos' }
      
      // Escala más precisa basada en tu ejemplo (3.9 = verde tirando a amarillo)
      if (promedio >= 4.5) return { color: '#22c55e', label: 'Alto' }// Verde puro
      if (promedio >= 4.0) return { color: '#84cc16', label: 'Alto' }// Verde-amarillo
      if (promedio >= 3.5) return { color: '#eab308', label: 'Medio' }// Amarillo
      if (promedio >= 3.0) return { color: '#f97316', label: 'Medio' }// Naranja
      if (promedio >= 2.5) return { color: '#ef4444', label: 'Bajo' } // Rojo
      return { color: '#dc2626', label: 'Crítico' }// Rojo intenso
    },

    getPromedioCumplimiento(factor) {
      // Si no hay características, retorna 0
      if (!factor.caracteristicas || factor.caracteristicas.length === 0) {
        return 0
      }
      
      // Calcula el promedio de cumplimiento
      const cumplimientos = factor.caracteristicas
        .map(c => Number(c.cumplimiento))
        .filter(v => !isNaN(v) && v > 0) // Solo valores válidos y positivos
        
      if (cumplimientos.length === 0) return 0
      
      // Fórmula: suma de cumplimientos / cantidad de características
      const promedio = cumplimientos.reduce((suma, valor) => suma + valor, 0) / cumplimientos.length
      
      console.log(`Factor: ${factor.nombre}, Cumplimientos: [${cumplimientos.join(', ')}], Promedio: ${promedio.toFixed(2)}`)
      
      return promedio
    },

    getEstadoColorClass(factor) {
      const estado = this.getEstadoColor(factor).label
      return {
        'status-green': estado === 'Alto' && this.getPromedioCumplimiento(factor) >= 4.5,
        'status-green-yellow': estado === 'Alto' && this.getPromedioCumplimiento(factor) >= 4.0 && this.getPromedioCumplimiento(factor) < 4.5,
        'status-yellow': estado === 'Medio' && this.getPromedioCumplimiento(factor) >= 3.5,
        'status-orange': estado === 'Medio' && this.getPromedioCumplimiento(factor) >= 3.0 && this.getPromedioCumplimiento(factor) < 3.5,
        'status-red': estado === 'Bajo' || estado === 'Crítico',
        'status-gray': estado === 'Sin datos'
      }
    },

    navigateToDashboardCharacteristics(factor) {
      this.$router.push({
        name: 'DashboardCharacteristics',
        params: { 
          factorId: factor.id, 
          titulo: factor.nombre 
        }
      })
    }
  },

  async mounted() {
    console.log('DashboardFacts mounted')
    
    if (this.checkAuthentication()) {
      console.log('User authenticated, loading data')
      await this.fetchFactores()
    }
  }
}
</script>

<style lang="css"> @import '../../styles/dashboard_facts.css'; </style>
