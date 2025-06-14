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
            :class="getFactorClass(factor.estado)"
          >
            <div class="factor-card-header">
              <h3 class="factor-title">{{ factor.titulo }}</h3>
              <div class="factor-status">
                <span :class="['status-indicator', factor.estado]">
                  {{ factor.estadoTexto }}
                </span>
              </div>
            </div>

            <div class="factor-card-body">
              <ul class="factor-details">
                <li v-for="alerta in factor.alertas" :key="alerta">
                  {{ alerta }}
                </li>
              </ul>
            </div>

            <div class="factor-card-footer">
              <button
                class="view-button"
                @click="navigateToDashboardFeatures(factor)"
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
export default {
  name: 'DashboardFacts',
  data () {
    return {
      factores: [
        {
          id: 1,
          titulo: '#1 Misión, Proyecto Institucional y de Programa',
          estado: 'verde',
          estadoTexto: 'Cumplimiento',
          alertas: [
            'C1: Misión y Proyecto Institucional',
            'C2: Proyecto Educativo del Programa',
            'C3: Relevancia Académica y Pertinencia'
          ]
        }

      ]
    }
  },
  methods: {
    getFactorClass (estado) {
      return {
        verde: 'factor-card--verde',
        amarillo: 'factor-card--amarillo',
        rojo: 'factor-card--rojo'
      }[estado]
    },
    navigateToDashboardFeatures (factor) {
      this.$router.push({
        name: 'DashboardFeatures',
        params: { factorId: factor.id }
      })
    }
  }
}
</script>

<style lang="css"> @import '../../styles/dashboard_facts.css'; </style>
