<template>
  <v-container fluid>
    <v-row>
      <!-- Título y selector de factores -->
      <v-col cols="12">
        <v-card class="pa-4 mb-4">
          <v-row align="center" justify="space-between">
            <v-col cols="12" md="8">
              <h2 class="font-weight-bold mb-0">C.1 PROYECTO EDUCATIVO DEL PROGRAMA</h2>
            </v-col>
            <v-col cols="12" md="4">
              <v-select
                v-model="selectedFactor"
                :items="factors"
                item-text="nombre"
                item-value="id"
                label="Seleccionar Factor"
                dense
                outlined
              ></v-select>
            </v-col>
          </v-row>
        </v-card>
      </v-col>

      <!-- Gráfico y texto descriptivo -->
      <v-col cols="12" md="4">
        <v-card class="pa-4 text-center">
          <canvas id="complianceChart" style="max-height: 350px;"></canvas>
          <div class="mt-3">
            <h3 class="font-weight-bold">CUMPLIMIENTO</h3>
            <h2 class="green--text font-weight-bold">4.6</h2>
          </div>
        </v-card>
      </v-col>

      <v-col cols="12" md="8">
        <v-card class="pa-4">
          <p>
            La MGSI cuenta con un Proyecto Educativo acorde a los parámetros y estamentos de la UDFJC en cuanto a sus diferentes disciplinas
            definiendo sus objetivos de una forma específica y puntual para el buen desarrollo, cabe mencionar que la MGSI cuenta con una
            Buena transmisión de identidad tanto del programa como de la Universidad.
          </p>
        </v-card>
      </v-col>

      <!-- Tabla de aspectos -->
      <v-col cols="12">
        <v-simple-table dense class="elevation-1">
          <thead>
            <tr>
              <th class="text-left">ASPECTOS A EVALUAR</th>
              <th class="text-left">EVIDENCIA</th>
              <th class="text-left">CALIFICACIÓN</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in aspectos" :key="index">
              <td>{{ item.descripcion }}</td>
              <td><a href="#">Evidencia 1</a></td>
              <td>
                <v-text-field
                  v-model="item.calificacion"
                  type="number"
                  class="mt-0"
                  hide-details
                  solo
                  flat
                  dense
                ></v-text-field>
              </td>
            </tr>
          </tbody>
        </v-simple-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Chart from 'chart.js/auto'

export default {
  name: 'DashboardGraphs',
  data () {
    return {
      selectedFactor: 1,
      factors: [
        { id: 1, nombre: 'C.1 Proyecto Educativo del Programa' },
        { id: 2, nombre: 'C.2 Otro Factor' }
      ],
      aspectos: [
        { descripcion: 'Articulación del Proyecto Educativo del Programa con el Proyecto Educativo Institucional...', calificacion: '' },
        { descripcion: 'Impacto de las políticas y estrategias de planeación y evaluación curricular...', calificacion: '' },
        { descripcion: 'Articulación de las tres funciones sustantivas en el proyecto educativo del programa', calificacion: '' },
        { descripcion: 'Evidencia de la evolución del Proyecto Educativo del Programa...', calificacion: '' },
        { descripcion: 'Impactos de la evolución del Proyecto Educativo del Programa...', calificacion: '' }
      ],
      complianceChart: null
    }
  },
  mounted () {
    this.renderChart()
  },
  beforeDestroy () {
    if (this.complianceChart) {
      this.complianceChart.destroy()
    }
  },
  methods: {
    renderChart () {
      const ctx = document.getElementById('complianceChart')
      this.complianceChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Cumplimiento', 'Restante'],
          datasets: [
            {
              data: [88, 12],
              backgroundColor: ['#4CAF50', '#E0E0E0'],
              borderWidth: 1
            }
          ]
        },
        options: {
          cutout: '75%',
          plugins: {
            legend: {
              display: false
            }
          }
        }
      })
    }
  }
}
</script>

<style scoped lang="css"> @import '../../styles/dashboard_cum.css'; </style>
