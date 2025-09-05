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
                
                <!-- Nuevo botón para editar descripción -->
                <v-btn 
                  v-if="isAdmin"
                  class="edit-description-btn ml-2" 
                  color="primary" 
                  small 
                  outlined
                  @click="openEditDescriptionModal"
                >
                  <v-icon left size="16">mdi-pencil</v-icon>
                  Editar Característica
                </v-btn>
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
          
          <!-- ⭐ NUEVO BOTÓN AGREGAR INDICADOR -->
          <v-btn 
            v-if="isAdmin"
            class="add-indicator-btn ml-3" 
            color="success" 
            small 
            outlined
            @click="openAddIndicatorModal"
          >
            <v-icon left size="16">mdi-plus</v-icon>
            Agregar Indicador
          </v-btn>
          
          <v-spacer></v-spacer>
          <v-chip class="aspect-count-chip" color="primary" outlined small>
            {{ Object.keys(characteristic.indicadores || {}).length }} Aspectos
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
                <th class="text-center evidence-header">
                  <v-icon class="mr-2" size="18">mdi-file-document-outline</v-icon>
                  EVIDENCIA
                </th>
                <th class="text-center rating-header">
                  <v-icon class="mr-2" size="18">mdi-star-outline</v-icon>
                  CALIFICACIÓN
                </th>
                <th class="text-center actions-header">
                  <v-icon class="mr-2" size="18">mdi-cog</v-icon>
                  ACCIONES
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
                <td class="actions-cell">
                  <div class="indicator-actions-vertical">
                    <!-- Botón Editar -->
                    <v-tooltip left>
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn 
                          icon 
                          small 
                          class="action-btn edit-btn"
                          v-bind="attrs"
                          v-on="on"
                          @click="editIndicator(index)"
                        >
                          <v-icon size="16" color="primary">mdi-pencil</v-icon>
                        </v-btn>
                      </template>
                      <span>Editar</span>
                    </v-tooltip>
                    
                    <!-- Botón Eliminar -->
                    <v-tooltip left>
                      <template v-slot:activator="{ on, attrs }">
                        <v-btn 
                          icon 
                          small 
                          class="action-btn delete-btn"
                          v-bind="attrs"
                          v-on="on"
                          @click="confirmDeleteIndicator(index)"
                        >
                          <v-icon size="16" color="error">mdi-delete</v-icon>
                        </v-btn>
                      </template>
                      <span>Eliminar</span>
                    </v-tooltip>
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

    <!-- 📝 MODAL EDITAR INDICADOR -->
    <v-dialog v-model="showEditIndicatorModal" max-width="600px" persistent>
      <v-card class="edit-indicator-modal">
        <!-- Actualizar el título del modal de editar indicador -->
        <v-card-title class="modal-header">
          <v-icon class="mr-3" size="24" color="primary">mdi-pencil</v-icon>
          <span class="modal-title">
            {{ editingIndex === -1 ? 'AGREGAR NUEVO INDICADOR' : `EDICIÓN ASPECTO A EVALUAR #${editingIndex + 1}` }}
          </span>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeEditIndicatorModal">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="edit-modal-content">
          <!-- DEFINICIÓN -->
          <div class="form-section">
            <h3 class="section-title">DEFINICIÓN</h3>
            <v-textarea
              v-model="editingIndicator.nombre"
              outlined
              rows="3"
              hide-details
              class="definition-textarea"
              placeholder="Descripción del aspecto a evaluar..."
            ></v-textarea>
          </div>

          <!-- TIPO EVIDENCIA -->
          <div class="form-section">
            <h3 class="section-title">TIPO EVIDENCIA</h3>
            <div class="evidence-type-group">
              <v-radio-group v-model="editingIndicator.tipoEvidencia" row hide-details>
                <v-radio label="Documental" value="documental" color="primary"></v-radio>
                <v-radio label="Encuesta" value="encuesta" color="primary"></v-radio>
              </v-radio-group>
            </div>

            <!-- Campo condicional para Documental -->
            <v-text-field
              v-if="editingIndicator.tipoEvidencia === 'documental'"
              v-model="editingIndicator.link_evidencia"
              label="Ingrese el link en donde almacenan la evidencia para este indicador"
              outlined
              dense
              hide-details
              class="evidence-field"
              placeholder="https://ejemplo.com/evidencia"
              prepend-inner-icon="mdi-link"
            ></v-text-field>

            <!-- Campo condicional para Encuesta -->
            <v-text-field
              v-if="editingIndicator.tipoEvidencia === 'encuesta'"
              v-model="editingIndicator.palabraClave"
              label="Ingrese el texto o palabra clave que pertenezca a la pregunta que satisfaga este aspecto a evaluar"
              outlined
              dense
              hide-details
              class="evidence-field"
              placeholder="Palabra clave o pregunta relacionada"
              prepend-inner-icon="mdi-text-search"
            ></v-text-field>
          </div>

          <!-- INGRESO DE DATOS -->
          <div class="form-section">
            <h3 class="section-title">INGRESO DE DATOS</h3>
            <v-row>
              <v-col cols="6">
                <v-text-field
                  v-model.number="editingIndicator.ponderacion"
                  label="Ponderación"
                  type="number"
                  outlined
                  dense
                  hide-details
                  min="0"
                  max="100"
                  suffix=""
                  class="data-input"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field
                  v-model.number="editingIndicator.calificacion"
                  label="Calificación"
                  type="number"
                  outlined
                  dense
                  hide-details
                  min="0"
                  max="5"
                  step="0.1"
                  suffix=""
                  class="data-input"
                  @input="calculateResults"
                ></v-text-field>
              </v-col>
            </v-row>
          </div>

          <!-- ALCANCE OBTENIDO -->
          <div class="form-section">
            <h3 class="section-title">ALCANCE OBTENIDO</h3>
            <v-row>
              <v-col cols="4">
                <div class="result-field">
                  <label class="result-label">Meta</label>
                  <div class="result-value">{{ calculatedMeta }}</div>
                </div>
              </v-col>
              <v-col cols="4">
                <div class="result-field">
                  <label class="result-label">Puntaje</label>
                  <div class="result-value">{{ calculatedPuntaje }}</div>
                </div>
              </v-col>
              <v-col cols="4">
                <div class="result-field">
                  <label class="result-label">Grado Cumplimiento %</label>
                  <div class="result-value">{{ calculatedPorcentaje }}</div>
                </div>
              </v-col>
            </v-row>
          </div>
        </v-card-text>

        <v-card-actions class="modal-actions">
          <v-spacer></v-spacer>
          <v-btn class="cancel-btn" text @click="closeEditIndicatorModal">
            Cancelar
          </v-btn>
          <v-btn 
            class="save-changes-btn" 
            color="primary" 
            @click="saveIndicatorChanges"
            :disabled="!editingIndicator.nombre.trim()"
          >
            <v-icon left>{{ editingIndex === -1 ? 'mdi-plus' : 'mdi-content-save' }}</v-icon>
            {{ editingIndex === -1 ? 'Crear Indicador' : 'Guardar Cambios' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 📝 MODAL EDITAR DESCRIPCIÓN -->
    <v-dialog v-model="showEditDescriptionModal" max-width="700px" persistent>
      <v-card class="edit-description-modal">
        <v-card-title class="modal-header">
          <v-icon class="mr-3" size="24" color="primary">mdi-text-box-edit</v-icon>
          <span class="modal-title">Editar Característica</span>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeEditDescriptionModal">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="edit-description-content">
          <!-- NOMBRE DE LA CARACTERÍSTICA -->
          <div class="form-section">
            <h3 class="section-title">NOMBRE DE LA CARACTERÍSTICA</h3>
            <v-text-field
              v-model="editingNombre"
              label="Nombre"
              outlined
              dense
              counter="200"
              placeholder="Ingrese el nombre de la característica..."
              class="name-input"
              :rules="[v => !!v || 'El nombre es requerido']"
              prepend-inner-icon="mdi-format-title"
            ></v-text-field>
          </div>

          <!-- DESCRIPCIÓN DE LA CARACTERÍSTICA -->
          <div class="form-section">
            <h3 class="section-title">DESCRIPCIÓN DE LA CARACTERÍSTICA</h3>
            <v-textarea
              v-model="editingDescription"
              label="Descripción"
              outlined
              rows="6"
              counter="1000"
              placeholder="Ingrese la descripción de la característica..."
              class="description-textarea"
              :rules="[v => !!v || 'La descripción es requerida']"
              prepend-inner-icon="mdi-text"
            ></v-textarea>
            
            <div class="description-info">
              <v-icon left size="16" color="info">mdi-information</v-icon>
              <span class="info-text">
                Proporcione un nombre claro y una descripción detallada de esta característica para facilitar la evaluación.
              </span>
            </div>
          </div>
        </v-card-text>

        <v-card-actions class="modal-actions">
          <v-spacer></v-spacer>
          <v-btn class="cancel-btn" text @click="closeEditDescriptionModal">
            Cancelar
          </v-btn>
          <v-btn 
            class="save-changes-btn" 
            color="primary" 
            @click="saveDescriptionChanges"
            :disabled="!editingDescription || !editingNombre || 
                       editingDescription.trim() === '' || editingNombre.trim() === ''"
          >
            <v-icon left>mdi-content-save</v-icon>
            Guardar Cambios
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 🗑️ MODAL CONFIRMAR ELIMINACIÓN -->
    <v-dialog v-model="showDeleteConfirmModal" max-width="400px" persistent>
      <v-card class="delete-confirm-modal">
        <v-card-title class="modal-header error">
          <v-icon class="mr-3" size="24" color="white">mdi-alert</v-icon>
          <span class="modal-title">Confirmar Eliminación</span>
        </v-card-title>

        <v-card-text class="delete-modal-content">
          <div class="warning-content">
            <v-icon size="48" color="error" class="warning-icon">mdi-alert-circle</v-icon>
            <h3>¿Estás seguro?</h3>
            <p>
              ¿Deseas eliminar este indicador?<br>
              <strong>Esta acción no se puede deshacer.</strong>
            </p>
          </div>
        </v-card-text>

        <v-card-actions class="modal-actions">
          <v-spacer></v-spacer>
          <v-btn text @click="closeDeleteConfirmModal">
            Cancelar
          </v-btn>
          <v-btn color="error" @click="deleteIndicator">
            <v-icon left>mdi-delete</v-icon>
            Eliminar
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
      showEditIndicatorModal: false,
      showDeleteConfirmModal: false,
      showEditDescriptionModal: false, // ⭐ NUEVA VARIABLE
      activeTab: 0,
      characteristicsId: 0,
      characteristic: {},
      isAdmin: true,
      lastUpdate: '15 de Agosto, 2025',


      // Estados para CRUD de indicadores
      editingIndicator: {
        nombre: '',
        calificacion: 0,
        ponderacion: 0,
        meta: 0,
        link_evidencia: '',
        palabraClave: '',
        tipoEvidencia: 'documental'
      },
      editingIndex: -1,
      indicatorToDelete: -1,

      // ⭐ NUEVA VARIABLE PARA DESCRIPCIÓN
      editingDescription: '',
      editingNombre: '',

      factors: [],
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
    },

    calculatedPuntaje() {
      const ponderacion = this.editingIndicator.ponderacion || 0
      const calificacion = this.editingIndicator.calificacion || 0
      return Math.round(ponderacion * calificacion) || '00'
    },
    calculatedMeta () {
      return this.editingIndicator.ponderacion * 5
    },

    calculatedPorcentaje() {
      const puntaje = this.calculatedPuntaje
      const meta = this.calculatedMeta
      return meta > 0 ? Math.round((puntaje / meta) * 100) || '00' : '00'
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
        this.editableDescription = this.characteristic.descripcion || ''
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
      this.characteristic.descripcion = this.editableDescription
      this.aspectos = JSON.parse(JSON.stringify(this.editableAspects))
      this.showManageModal = false

      this.$swal({
        title: '¡Éxito!',
        text: 'Los cambios se han guardado correctamente.',
        icon: 'success',
        confirmButtonText: 'Continuar'
      })
    },

    // Métodos para CRUD de indicadores
    editIndicator(index) {
      const indicadoresArray = Object.values(this.characteristic.indicadores || {})
      if (indicadoresArray[index]) {
        this.editingIndex = index
        const indicador = indicadoresArray[index]

        this.editingIndicator = {
          nombre: indicador.nombre || '',
          calificacion: indicador.calificacion || 0,
          ponderacion: indicador.ponderacion || 0,
          meta: indicador.ponderacion * 5 || 0,
          link_evidencia: indicador.link_evidencia || '',
          palabraClave: indicador.palabra_clave || '', // ⭐ Corregido el nombre del campo
          tipoEvidencia: indicador.link_evidencia ? 'documental' : 'encuesta'
        }
        this.showEditIndicatorModal = true
      }
    },

    closeEditIndicatorModal() {
      this.showEditIndicatorModal = false
      this.editingIndex = -1
      this.editingIndicator = {
        nombre: '',
        calificacion: 0,
        ponderacion: 0,
        meta: 0,
        link_evidencia: '',
        palabraClave: '',
        tipoEvidencia: 'documental'
      }
    },

    calculateResults() {
      // Este método se llama automáticamente cuando cambia la calificación
      // Los computed properties se actualizan automáticamente
    },

async saveIndicatorChanges() {
  try {
    const token = localStorage.getItem('access_token')
    
    // Validar que el nombre no esté vacío
    if (!this.editingIndicator.nombre.trim()) {
      this.$swal({
        title: 'Error',
        text: 'El nombre del indicador es requerido.',
        icon: 'warning',
        confirmButtonText: 'Continuar'
      })
      return
    }
    
    // ⭐ CALCULAR LA META EN TIEMPO REAL
    const metaCalculada = this.calculatedMeta

    // ⭐ PREPARAR DATOS PARA ENVIAR AL BACKEND
    const indicatorData = {
      nombre: this.editingIndicator.nombre.trim(),
      calificacion: this.editingIndicator.calificacion,
      ponderacion: this.editingIndicator.ponderacion,
      meta: metaCalculada,
      link_evidencia: this.editingIndicator.tipoEvidencia === 'documental' ? this.editingIndicator.link_evidencia : '',
      palabra_clave: this.editingIndicator.tipoEvidencia === 'encuesta' ? this.editingIndicator.palabraClave : '',
      tipo_evidencia: this.editingIndicator.tipoEvidencia
    }

    if (this.editingIndex === -1) {
      // ⭐ CREAR NUEVO INDICADOR
      console.log('Creating new indicator:', indicatorData)
      
      const response = await axios.post(
        `/characteristics/${this.characteristicsId}/indicators/`,
        indicatorData,
        {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        }
      )
      
      console.log('New indicator created:', response.data)

      this.$swal({
        title: '¡Indicador Creado!',
        text: 'El nuevo indicador se ha agregado correctamente.',
        icon: 'success',
        confirmButtonText: 'Continuar'
      })
      
    } else {
      // ⭐ ACTUALIZAR INDICADOR EXISTENTE
      const indicadorKey = Object.keys(this.characteristic.indicadores)[this.editingIndex]
      
      if (indicadorKey) {
        console.log('Updating existing indicator:', indicatorData)
        
        const response = await axios.patch(
          `/indicators/${this.characteristic.indicadores[indicadorKey].id}/`,
          indicatorData,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }
        )
        
        console.log('Indicator updated on server:', response.data)

        this.$swal({
          title: '¡Indicador Actualizado!',
          text: 'Los cambios se han guardado correctamente.',
          icon: 'success',
          confirmButtonText: 'Continuar'
        })
      }
    }

    // ⭐ REFRESCAR DATOS DEL BACKEND DESPUÉS DE CREAR/ACTUALIZAR
    await this.fetchCaracteristica()
    this.closeEditIndicatorModal()

  } catch (error) {
    console.error('Error saving indicator:', error)
    
    let errorMessage = 'Hubo un problema al guardar el indicador.'
    
    if (error.response?.status === 401) {
      errorMessage = 'Sesión expirada. Por favor, inicia sesión nuevamente.'
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user_data')
      this.$router.push('/login')
    } else if (error.response?.status === 403) {
      errorMessage = 'No tienes permisos para realizar esta acción.'
    } else if (error.response?.status === 400) {
      errorMessage = 'Datos inválidos. Verifique que toda la información sea correcta.'
    } else if (error.response?.data?.message) {
      errorMessage = error.response.data.message
    } else if (error.response?.data?.error) {
      errorMessage = error.response.data.error
    }

    this.$swal({
      title: 'Error',
      text: errorMessage,
      icon: 'error',
      confirmButtonText: 'Continuar'
    })
  }
},




  confirmDeleteIndicator(index) {
  this.indicatorToDelete = index
  this.showDeleteConfirmModal = true
},

    closeDeleteConfirmModal() {
      this.showDeleteConfirmModal = false
      this.indicatorToDelete = -1
    },

    async deleteIndicator() {
      if (this.indicatorToDelete >= 0) {
        try {
          const indicadorKey = Object.keys(this.characteristic.indicadores)[this.indicatorToDelete]
          
          if (indicadorKey) {
            const token = localStorage.getItem('access_token')
            const indicadorId = this.characteristic.indicadores[indicadorKey].id

            console.log('Deleting indicator with ID:', indicadorId)

            // ⭐ ELIMINAR DEL BACKEND CON EL ENDPOINT CORRECTO
            await axios.delete(
              `/indicators/${indicadorId}/`,
              {
                headers: {
                  Authorization: `Bearer ${token}`
                }
              }
            )

            console.log('Indicator deleted from server successfully')

            // ⭐ REFRESCAR DATOS DEL BACKEND DESPUÉS DE ELIMINAR
            await this.fetchCaracteristica()
            
            this.$swal({
              title: '¡Indicador Eliminado!',
              text: 'El indicador se ha eliminado correctamente.',
              icon: 'success',
              confirmButtonText: 'Continuar'
            })
          }
        } catch (error) {
          console.error('Error deleting indicator:', error)
          this.$swal({
            title: 'Error',
            text: 'Error al eliminar el indicador.',
            icon: 'error',
            confirmButtonText: 'Continuar'
          })
        }
      }
      this.closeDeleteConfirmModal()
    },

    viewEvidence (index) {
      console.log('Ver evidencia del aspecto:', index)
    },

    async saveEvaluation() {
      // ⭐ REFRESCAR DATOS DEL BACKEND
      await this.fetchCaracteristica()
      
      this.$swal({
        title: '¡Evaluación Guardada!',
        text: 'La evaluación se ha guardado exitosamente.',
        icon: 'success',
        confirmButtonText: 'Continuar'
      })
    },

    // ⭐ MÉTODOS PARA EDITAR DESCRIPCIÓN
    openEditDescriptionModal() {
      this.editingDescription = this.characteristic.descripcion || ''
      this.editingNombre = this.characteristic.nombre || ''
      this.showEditDescriptionModal = true
    },

    closeEditDescriptionModal() {
      this.showEditDescriptionModal = false
      this.editingDescription = ''
      this.editingNombre = ''
    },

    async saveDescriptionChanges() {
      try {
        const token = localStorage.getItem('access_token')
        
        // Validar que hay contenido en ambos campos
        if (!this.editingNombre || this.editingNombre.trim() === '') {
          this.$swal({
            title: 'Error',
            text: 'El nombre no puede estar vacío.',
            icon: 'warning',
            confirmButtonText: 'Continuar'
          })
          return
        }

        if (!this.editingDescription || this.editingDescription.trim() === '') {
          this.$swal({
            title: 'Error',
            text: 'La descripción no puede estar vacía.',
            icon: 'warning',
            confirmButtonText: 'Continuar'
          })
          return
        }

        // ⭐ PREPARAR DATOS CON NOMBRE Y DESCRIPCIÓN
        const updateData = {
          nombre: this.editingNombre.trim(),
          descripcion: this.editingDescription.trim()
        }

        console.log('Updating characteristic:', updateData)

        // Enviar al backend
        const response = await axios.patch(
          `/characteristics/${this.characteristicsId}/`,
          updateData,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }
        )
        
        console.log('Characteristic updated on server:', response.data)

        // ⭐ REFRESCAR DATOS DEL BACKEND DESPUÉS DE GUARDAR
        await this.fetchCaracteristica()

        this.$swal({
          title: '¡Característica Actualizada!',
          text: 'El nombre y la descripción se han actualizado correctamente.',
          icon: 'success',
          confirmButtonText: 'Continuar'
        })

        this.closeEditDescriptionModal()

      } catch (error) {
        console.error('Error updating characteristic:', error)
        
        let errorMessage = 'Hubo un problema al actualizar la característica.'
        
        if (error.response?.status === 401) {
          errorMessage = 'Sesión expirada. Por favor, inicia sesión nuevamente.'
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user_data')
          this.$router.push('/login')
        } else if (error.response?.status === 403) {
          errorMessage = 'No tienes permisos para realizar esta acción.'
        } else if (error.response?.status === 400) {
          errorMessage = 'Datos inválidos. Verifique que el nombre no esté duplicado.'
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message
        } else if (error.response?.data?.error) {
          errorMessage = error.response.data.error
        }

        this.$swal({
          title: 'Error',
          text: errorMessage,
          icon: 'error',
          confirmButtonText: 'Continuar'
        })
      }
    },

    // ⭐ MÉTODO PARA ABRIR MODAL DE AGREGAR INDICADOR
    openAddIndicatorModal() {
      this.editingIndex = -1 // -1 indica que es un nuevo indicador
      this.editingIndicator = {
        nombre: '',
        calificacion: 0,
        ponderacion: 0,
        meta: 0,
        link_evidencia: '',
        palabraClave: '',
        tipoEvidencia: 'documental'
      }
      this.showEditIndicatorModal = true
    },
  },

  async mounted() {
    console.log(this.$route.params.caracteristicaId)
    this.characteristicsId = this.$route.params.caracteristicaId
    await this.fetchCaracteristica()
  }
}
</script>
<style scoped lang="css"> @import '../../styles/dashboard_indicators.css'; </style>