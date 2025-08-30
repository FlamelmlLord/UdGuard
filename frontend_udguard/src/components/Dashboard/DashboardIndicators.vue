<template>
  <v-container fluid class="dashboard-container">
    <!-- 🎯 CONTENEDOR PRINCIPAL UNIFICADO -->
    <v-card class="dashboard-main-card" elevation="8">

      <!-- 📋 HEADER SECTION - Título, Selector y Botón Gestionar -->
      <div class="dashboard-header">
        <v-row align="center" justify="space-between" no-gutters>
          <v-col cols="12" lg="6">
            <div class="header-title-section">
              <h2 class="dashboard-main-title">
                <v-icon class="title-icon mr-3" size="28" color="primary">mdi-chart-box-outline</v-icon>
                {{characteristic.nombre}}
              </h2>
            </div>
          </v-col>

          <v-col cols="12" lg="4">
            <div class="factor-selector-wrapper">
              <v-select
                v-model="selectedFactor"
                :items="factors"
                item-text="nombre"
                item-value="id"
                label="Seleccionar Caracteristica"
                @change="navigateToCharacteristic(selectedFactor)"
                outlined
                dense
                class="factor-select"
                prepend-inner-icon="mdi-filter-outline"
              >
                <template v-slot:prepend-item>
                  <div class="px-3 py-2">
                    <v-subheader class="text-primary font-weight-bold">FACTORES DISPONIBLES</v-subheader>
                  </div>
                  <v-divider></v-divider>
                </template>
              </v-select>
            </div>
          </v-col>

          <v-col cols="12" lg="2" v-if="isAdmin">
            <div class="manage-button-wrapper">
              <v-btn
                @click="toggleManageModal"
                class="manage-btn"
                color="primary"
                elevation="4"
                large
              >
                <v-icon left size="20">mdi-cog-outline</v-icon>
                Gestionar
              </v-btn>
            </div>
          </v-col>
        </v-row>
      </div>

      <v-divider class="header-divider"></v-divider>

      <!-- 📊 ANALYTICS SECTION - Gráfico y Descripción -->
      <div class="analytics-section">
        <v-row no-gutters>
          <!-- Chart Container -->
          <v-col cols="12" md="5">
            <div class="chart-container">
              <div class="chart-wrapper">
                <canvas id="complianceChart"></canvas>
              </div>
              <div class="chart-info">

<!--                 <div class="compliance-score">4.6</div> -->
                <!-- Removemos compliance-percentage ya que estará en el centro del gráfico -->
              </div>
            </div>
          </v-col>

          <!-- Center Section - Grado Cumplimiento -->
          <v-col cols="12" md="2">
            <div class="grado-section">
              <div class="grado-header">
                <v-icon class="grado-icon" color="info" size="24">mdi-information-outline</v-icon>
                <h3 class="grado-title">Grado Cumplimiento</h3>
              </div>
              <div class="grado-value">
                <h2 
                  class="grado-cumplimiento" 
                  :style="{ color: characteristic.color_grado || '#2c3e50' }" 
                >
                  {{ characteristic.cumplimiento || '0.0' }}
                </h2>
                <span class="grado-scale">/5.0</span>
              </div>
            </div>
          </v-col>

          <!-- Description Container -->
          <v-col cols="12" md="5">
            <div class="description-container">
              <div class="description-header">
                <v-icon class="description-icon mr-2" color="primary">mdi-text-box-outline</v-icon>
                <h3 class="description-title">Descripción</h3>
              </div>
              <div class="description-content">
                <p class="description-text">
                  {{ characteristic.descripcion || 'Descripción no disponible' }}
                </p>
              </div>
              <div class="description-footer">
                <v-chip class="status-chip" color="success" text-color="white" small>
                  <v-icon left size="16">mdi-shield-check</v-icon>
                  Evaluación Completa
                </v-chip>
                <v-chip class="status-chip ml-2" color="info" text-color="white" small>
                  <v-icon left size="16">mdi-calendar-clock</v-icon>
                  Última actualización: {{ lastUpdate }}
                </v-chip>
              </div>
            </div>
          </v-col>
        </v-row>
      </div>

      <v-divider class="section-divider"></v-divider>

      <!-- 📋 EVALUATION SECTION - Aspectos a Evaluar -->
      <div class="evaluation-section">
        <div class="section-header">
          <v-icon class="section-icon mr-3" size="24" color="primary">mdi-clipboard-list-outline</v-icon>
          <h3 class="section-title">Indicadores</h3>
          <v-spacer></v-spacer>
          <v-chip class="aspect-count-chip" color="primary" outlined small>
            {{ Object.keys(characteristic.indicadores).length }} Aspectos
          </v-chip>
        </div>

        <div class="evaluation-table-wrapper">
          <v-simple-table class="evaluation-table" dense>
            <thead>
              <tr class="table-header">
                <th class="text-left aspect-header">
                  <v-icon class="mr-2" size="18">mdi-format-list-bulleted</v-icon>
                  ASPECTOS A EVALUAR
                </th>
                <th class="text-left evidence-header">
                  <v-icon class="mr-2" size="18">mdi-file-document-outline</v-icon>
                  EVIDENCIA
                </th>
                <th class="text-left rating-header">
                  <v-icon class="mr-2" size="18">mdi-star-outline</v-icon>
                  CALIFICACIÓN
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(item, index) in characteristic.indicadores"
                :key="index"
                class="table-row"
                :class="{ 'row-even': index % 2 === 0 }"
              >
                <td class="aspect-cell">
                  <div class="aspect-content">
                    <div class="aspect-number">{{ index + 1 }}.</div>
                    <div class="aspect-description">{{ item.nombre }}</div>
                  </div>
                </td>
                <td class="evidence-cell">
                  <v-btn
                    class="evidence-btn"
                    color="info"
                    text
                    small
                    @click="viewEvidence(index)"
                  >
                    <v-icon left size="16">mdi-file-eye-outline</v-icon>
                    Evidencia {{ item.link_evidencia }}
                  </v-btn>
                </td>
                <td class="rating-cell">
                  <div class="rating-input-wrapper">
                    <v-text-field
                      v-model="item.calificacion"
                      type="number"
                      class="rating-input"
                      hide-details
                      outlined
                      dense
                      min="0"
                      max="5"
                      step="0.1"
                      suffix="/5.0"
                      placeholder="0.0"
                    >
                      <template v-slot:prepend-inner>
                        <v-icon size="16" color="warning">mdi-star</v-icon>
                      </template>
                    </v-text-field>
                  </div>
                </td>
              </tr>
            </tbody>
          </v-simple-table>
        </div>

        <!-- Summary Footer -->
        <div class="evaluation-summary">
          <v-row align="center" justify="space-between">
            <v-col cols="auto">
              <div class="summary-stats">
                <v-chip class="stat-chip" color="success" outlined small>
                  <v-icon left size="16">mdi-check-circle</v-icon>
                  Completados: {{ completedAspects }}/{{ aspectos.length }}
                </v-chip>
                <v-chip class="stat-chip ml-2" color="info" outlined small>
                  <v-icon left size="16">mdi-calculator</v-icon>
                  Promedio: {{ averageRating }}
                </v-chip>
              </div>
            </v-col>
            <v-col cols="auto">
              <v-btn
                class="save-btn"
                color="primary"
                elevation="2"
                @click="saveEvaluation"
              >
                <v-icon left>mdi-content-save</v-icon>
                Guardar Evaluación
              </v-btn>
            </v-col>
          </v-row>
        </div>
      </div>
    </v-card>

    <!-- 🛠️ MODAL DE GESTIÓN (Solo para Administradores) -->
    <v-dialog v-model="showManageModal" max-width="900px" persistent>
      <v-card class="manage-modal">
        <v-card-title class="modal-header">
          <v-icon class="mr-3" size="28" color="primary">mdi-cog</v-icon>
          <span class="modal-title">Gestión del Factor</span>
          <v-spacer></v-spacer>
          <v-btn icon @click="toggleManageModal">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="modal-content">
          <v-tabs v-model="activeTab" class="modal-tabs">
            <v-tab class="tab-item">
              <v-icon left>mdi-text-box-outline</v-icon>
              Descripción
            </v-tab>
            <v-tab class="tab-item">
              <v-icon left>mdi-format-list-bulleted</v-icon>
              Aspectos
            </v-tab>
          </v-tabs>

          <v-tabs-items v-model="activeTab" class="modal-tabs-content">
            <!-- Tab 1: Descripción -->
            <v-tab-item>
              <div class="tab-content">
                <h3 class="tab-subtitle">Editar Descripción de la Característica</h3>
                <v-textarea
                  v-model="editableDescription"
                  label="Descripción del Factor"
                  outlined
                  rows="6"
                  counter
                  class="description-textarea"
                ></v-textarea>
              </div>
            </v-tab-item>

            <!-- Tab 2: Aspectos -->
            <v-tab-item>
              <div class="tab-content">
                <div class="aspects-header">
                  <h3 class="tab-subtitle">Gestionar Aspectos a Evaluar</h3>
                  <v-btn
                    class="add-aspect-btn"
                    color="success"
                    @click="addNewAspect"
                    small
                  >
                    <v-icon left size="18">mdi-plus</v-icon>
                    Agregar Aspecto
                  </v-btn>
                </div>

                <div class="aspects-list">
                  <v-card
                    v-for="(aspect, index) in editableAspects"
                    :key="index"
                    class="aspect-card mb-3"
                    outlined
                  >
                    <v-card-text class="aspect-card-content">
                      <v-row align="center">
                        <v-col cols="1">
                          <v-icon class="aspect-drag-handle" color="grey">mdi-drag-vertical</v-icon>
                        </v-col>
                        <v-col cols="9">
                          <v-textarea
                            v-model="aspect.descripcion"
                            :label="`Aspecto ${index + 1}`"
                            outlined
                            rows="2"
                            dense
                          ></v-textarea>
                        </v-col>
                        <v-col cols="2" class="text-center">
                          <v-btn
                            icon
                            color="error"
                            @click="removeAspect(index)"
                          >
                            <v-icon>mdi-delete</v-icon>
                          </v-btn>
                        </v-col>
                      </v-row>
                    </v-card-text>
                  </v-card>
                </div>
              </div>
            </v-tab-item>
          </v-tabs-items>
        </v-card-text>

        <v-card-actions class="modal-actions">
          <v-spacer></v-spacer>
          <v-btn
            class="cancel-btn"
            text
            @click="toggleManageModal"
          >
            Cancelar
          </v-btn>
          <v-btn
            class="save-changes-btn"
            color="primary"
            elevation="2"
            @click="saveChanges"
          >
            <v-icon left>mdi-content-save</v-icon>
            Guardar Cambios
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from '../../plugins/Axios'
import Chart from 'chart.js/auto'

export default {
  name: 'DashboardGraphs',
  data () {
    return {
      selectedFactor: 1,
      showManageModal: false,
      activeTab: 0,
      characteristicsId: 0,
      characteristic: {},
      isAdmin: true, // Cambiar según el rol del usuario
      lastUpdate: '15 de Agosto, 2025',

      factors: [

      ],

      aspectos: [],
      editableDescription: '',
      editableAspects: [],
      complianceChart: null
    }
  },

  computed: {
    completedAspects () {
      return this.aspectos.filter(aspect => aspect.calificacion && parseFloat(aspect.calificacion) > 0).length
    },

    averageRating () {
      const ratings = this.aspectos.filter(aspect => aspect.calificacion && parseFloat(aspect.calificacion) > 0)
      if (ratings.length === 0) return '0.0'
      const sum = ratings.reduce((acc, aspect) => acc + parseFloat(aspect.calificacion), 0)
      return (sum / ratings.length).toFixed(1)
    }
  },

  beforeDestroy () {
    if (this.complianceChart) {
      this.complianceChart.destroy()
    }
  },

  methods: {
    renderChart (percentage, color) {
      const ctx = document.getElementById('complianceChart')
      console.log(color)
      
      // Destruir chart anterior si existe
      if (this.complianceChart) {
        this.complianceChart.destroy()
      }

      // Usar el percentage que viene como parámetro, no un valor fijo
      const numericPercentage = parseFloat(percentage) || 0
      const remaining = 100 - numericPercentage

      this.complianceChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Cumplimiento', 'Restante'],
          datasets: [
            {
              data: [numericPercentage, remaining],
              backgroundColor: [color, '#E8F5E8'],
              borderColor: [color, '#E8F5E8'],
              borderWidth: 0,
              cutout: '75%'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
            tooltip: { enabled: false }
          }
        },
        plugins: [{
          id: 'centerText',
          beforeDraw: function(chart) {
            const ctx = chart.ctx
            const centerX = (chart.chartArea.left + chart.chartArea.right) / 2
            const centerY = (chart.chartArea.top + chart.chartArea.bottom) / 2
            
            ctx.restore()
            
            // Configurar el texto principal - usar el percentage dinámico
            const fontSize = Math.min(chart.width, chart.height) / 6
            ctx.font = `bold ${fontSize}px Arial`
            ctx.textAlign = 'center'
            ctx.textBaseline = 'middle'
            ctx.fillStyle = '#2c3e50'

            // Mostrar el porcentaje dinámico con el símbolo %
            const percentageText = `${Math.round(numericPercentage)}%`
            ctx.fillText(percentageText, centerX, centerY)
            
            ctx.save()
          }
        }]
      })
    },
    navigateToCharacteristic(caracteristicaId) {
      this.$router.replace({
        name: 'DashboardIndicators',
        params: { caracteristicaId }
      }).catch(err => { console.log(err) });
    },
      async characteristicsByFactor(factor) {
        const token = localStorage.getItem('access_token')
        const response = await axios.get(`/factors/${factor}/characteristics/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        console.log('API response received Characteristics by factor:', response.data)
        this.factors = response.data
      },
      async fetchCaracteristica () {
      console.log(this.characteristicsId)
      this.loading = true
      this.error = null
      
      try {
        const token = localStorage.getItem('access_token')
        console.log('Making API request with token')

        const response = await axios.get(`/characteristics/${this.characteristicsId}/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        console.log('API response received Characteristics:', response.data)
        this.characteristic = response.data

        await this.characteristicsByFactor(response.data.factors)

        // Esperar a que Vue termine de actualizar el DOM
        await this.$nextTick()
        
        // Ahora renderizar el gráfico
        this.renderChart(`${this.characteristic.porcentaje}`, `${this.characteristic.grado_cumplimiento.color}`)

      } catch (error) {
        console.error('Error fetching factors:', error)
        
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

    toggleManageModal () {
      this.showManageModal = !this.showManageModal
      if (this.showManageModal) {
        this.editableDescription = this.currentFactorDescription
        this.editableAspects = JSON.parse(JSON.stringify(this.aspectos))
      }
    },

    addNewAspect () {
      this.editableAspects.push({
        descripcion: '',
        calificacion: ''
      })
    },

    removeAspect (index) {
      this.editableAspects.splice(index, 1)
    },

    saveChanges () {
      this.currentFactorDescription = this.editableDescription
      this.aspectos = JSON.parse(JSON.stringify(this.editableAspects))
      this.showManageModal = false

      this.$swal({
        title: '¡Éxito!',
        text: 'Los cambios se han guardado correctamente.',
        icon: 'success',
        confirmButtonText: 'Continuar'
      })
    },

    viewEvidence (index) {
      console.log('Ver evidencia del aspecto:', index)
    },

    saveEvaluation () {
      this.$swal({
        title: '¡Evaluación Guardada!',
        text: 'La evaluación se ha guardado exitosamente.',
        icon: 'success',
        confirmButtonText: 'Continuar'
      })
    }
  },
    async mounted() {
      console.log(this.$route.params.caracteristicaId)
      this.characteristicsId = this.$route.params.caracteristicaId
    await this.fetchCaracteristica()
      
  }
}
</script>
<style scoped lang="css"> @import '../../styles/dashboard_indicators.css'; </style>