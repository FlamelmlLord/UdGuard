<template>
  <v-container fluid class="dashboard-facts-container">
    <!-- 🎯 CONTENEDOR PRINCIPAL UNIFICADO -->
    <v-card class="dashboard-main-card" elevation="8">

      <!-- 📋 HEADER SECTION - Título y Selector (SIN BOTÓN GESTIONAR) -->
      <div class="dashboard-header">
        <v-row align="center" justify="space-between" no-gutters>
          <v-col cols="12" lg="8">
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
                
                <!-- Botón para editar descripción (mejorado con mejor posicionamiento) -->
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
          
          <!-- ⭐ BOTÓN AGREGAR INDICADOR (Mejorado con mejor diseño) -->
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
                  <div v-if="item.link_evidencia && item.link_evidencia.trim() !== ''" class="evidence-container">
                    <v-btn
                      class="evidence-btn"
                      color="info"
                      text
                      small
                      @click="openEvidence(item.link_evidencia)"
                      :title="`Abrir evidencia: ${item.link_evidencia}`"
                    >
                      <v-icon left size="16">mdi-file-eye-outline</v-icon>
                      Evidencia
                    </v-btn>
                  </div>
                  
                  <div v-else-if="item.palabra_clave && item.palabra_clave.trim() !== ''" class="evidence-container">
                    <v-btn
                      class="evidence-btn encuesta-btn"
                      color="purple"
                      text
                      small
                      @click="showEncuestaInfo(item.palabra_clave)"
                      :title="`Palabra clave: ${item.palabra_clave}`"
                    >
                      <v-icon left size="16">mdi-poll</v-icon>
                      Encuesta
                    </v-btn>
                  </div>
                  
                  <div v-else class="no-evidence">
                    <v-chip
                      class="no-evidence-chip"
                      color="grey"
                      text-color="white"
                      x-small
                      outlined
                    >
                      <v-icon left size="12">mdi-alert-circle-outline</v-icon>
                      Sin evidencia
                    </v-chip>
                  </div>
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
              <v-radio-group v-model="editingIndicator.tipoEvidencia" row hide-details @change="onEvidenceTypeChange">
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

            <!-- Campo condicional para Encuesta SIN BOTÓN DE BÚSQUEDA -->
            <v-text-field
              v-if="editingIndicator.tipoEvidencia === 'encuesta'"
              v-model="editingIndicator.palabraClave"
              label="Pregunta seleccionada de la encuesta"
              outlined
              dense
              hide-details
              class="evidence-field"
              placeholder="La pregunta se seleccionará automáticamente..."
              prepend-inner-icon="mdi-text-search"
              readonly
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

    <!-- 🔍 MODAL BÚSQUEDA DE PREGUNTAS -->
    <v-dialog v-model="showSearchModal" max-width="900px" persistent>
      <v-card class="search-modal">
        <v-card-title class="modal-header">
          <v-icon class="mr-3" size="24" color="primary">mdi-magnify</v-icon>
          <span class="modal-title">Buscar Preguntas en Encuestas</span>
          <v-spacer></v-spacer>
          <v-btn icon @click="closeSearchModal">
            <v-icon>mdi-close</v-icon>
          </v-btn>
        </v-card-title>

        <v-card-text class="search-modal-content">
          <!-- Campo de búsqueda -->
          <div class="search-section">
            <v-text-field
              v-model="searchQuery"
              label="Buscar pregunta"
              placeholder="Ingrese palabras clave para buscar en todas las encuestas..."
              outlined
              dense
              prepend-inner-icon="mdi-magnify"
              @input="performSearch"
              clearable
              autofocus
            ></v-text-field>

            <div class="search-info">
              <v-icon left size="16" color="info">mdi-information</v-icon>
              <span class="search-help-text">
                La búsqueda se realiza automáticamente en todas las encuestas 
                (Administrativos, Directivos, Docentes, Egresados, Empleadores y Estudiantes)
              </span>
            </div>
          </div>

          <!-- Resultados de búsqueda -->
          <div class="search-results">
            <div v-if="isSearching" class="search-loading">
              <v-progress-circular indeterminate color="primary"></v-progress-circular>
              <span class="ml-3">Buscando preguntas en todas las encuestas...</span>
            </div>

            <div v-else-if="searchResults.length === 0 && searchQuery" class="no-results">
              <v-icon size="48" color="grey">mdi-magnify</v-icon>
              <p>No se encontraron preguntas que coincidan con la búsqueda.</p>
              <p class="no-results-subtitle">Intente con palabras clave diferentes o más generales.</p>
            </div>

            <div v-else-if="searchResults.length > 0" class="results-list">
              <p class="results-count">
                <strong>{{ searchResults.length }}</strong> preguntas encontradas en todas las encuestas
              </p>
              
              <v-list dense>
                <v-list-item
                  v-for="(result, index) in paginatedResults"
                  :key="index"
                  @click="selectQuestion(result)"
                  :class="{ 'selected-question': selectedQuestion?.id === result.id }"
                  class="result-item"
                >
                  <v-list-item-icon>
                    <v-chip :color="getSurveyTypeColor(result.survey_type)" small outlined>
                      {{ getSurveyTypeLabel(result.survey_type) }}
                    </v-chip>
                  </v-list-item-icon>
                  
                  <v-list-item-content>
                    <v-list-item-title class="question-text">
                      {{ result.question }}
                    </v-list-item-title>
                    <v-list-item-subtitle class="response-summary">
                      Total respuestas: {{ result.total_responses }}
                    </v-list-item-subtitle>
                  </v-list-item-content>

                  <v-list-item-action>
                    <v-btn
                      icon
                      small
                      color="primary"
                      @click.stop="previewQuestion(result)"
                    >
                      <v-icon size="16">mdi-eye</v-icon>
                    </v-btn>
                  </v-list-item-action>
                </v-list-item>
              </v-list>

              <!-- Paginación -->
              <v-pagination
                v-if="totalPages > 1"
                v-model="currentPage"
                :length="totalPages"
                :total-visible="5"
                class="mt-4"
              ></v-pagination>
            </div>

            <div v-else-if="!searchQuery" class="search-instructions">
              <v-icon size="64" color="primary">mdi-text-search</v-icon>
              <h3>Buscar Pregunta de Encuesta</h3>
              <p>Escriba palabras clave relacionadas con la pregunta que está buscando.</p>
              <p class="instructions-subtitle">
                La búsqueda incluirá automáticamente todas las encuestas disponibles.
              </p>
            </div>
          </div>
        </v-card-text>

        <v-card-actions class="modal-actions">
          <v-spacer></v-spacer>
          <v-btn text @click="closeSearchModal">
            Cancelar
          </v-btn>
          <v-btn 
            color="success"
            :disabled="!selectedQuestion"
            @click="generateChart"
          >
            <v-icon left>mdi-chart-bar</v-icon>
            Seleccionar Pregunta
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
      selectedFactor: null, // ⭐ CAMBIADO DE 1 A null
      showEditIndicatorModal: false,
      showDeleteConfirmModal: false,
      showEditDescriptionModal: false,
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

      // Variables para descripción
      editingDescription: '',
      editingNombre: '',

      // Variables para búsqueda de preguntas (SIMPLIFICADAS)
      showSearchModal: false,
      searchQuery: '',
      searchResults: [],
      selectedQuestion: null,
      isSearching: false,
      
      // Paginación
      currentPage: 1,
      itemsPerPage: 10,

      factors: [],
      aspectos: [],
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
    },

    paginatedResults() {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.searchResults.slice(start, end)
    },

    totalPages() {
      return Math.ceil(this.searchResults.length / this.itemsPerPage)
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

    openEvidence (linkEvidencia) {
      if (!linkEvidencia || linkEvidencia.trim() === '') {
        this.$swal({
          title: 'Sin enlace',
          text: 'No hay enlace de evidencia disponible.',
          icon: 'warning',
          confirmButtonText: 'Continuar'
        })
        return
      }

      try {
        let url = linkEvidencia.trim()
        
        if (!url.startsWith('http://') && !url.startsWith('https://')) {
          url = 'https://' + url
        }

        // eslint-disable-next-line no-new
        new URL(url)
        window.open(url, '_blank', 'noopener,noreferrer')
        
      } catch (error) {
        this.$swal({
          title: 'URL inválida',
          text: 'El enlace de evidencia no es válido.',
          icon: 'error',
          confirmButtonText: 'Continuar'
        })
      }
    },

    showEncuestaInfo (palabraClave) {
      this.$swal({
        title: 'Evidencia de Encuesta',
        html: `
          <div style="text-align: left; padding: 10px;">
            <p><strong>Tipo:</strong> Encuesta</p>
            <p><strong>Palabra clave:</strong> "${palabraClave}"</p>
            <p><strong>Información:</strong> Esta evidencia se obtiene de las respuestas de encuestas.</p>
          </div>
        `,
        icon: 'info',
        confirmButtonText: 'Entendido'
      })
    },

    viewEvidence (index) {
      const indicadoresArray = Object.values(this.characteristic.indicadores || {})
      const item = indicadoresArray[index]
      
      if (!item) return

      if (item.link_evidencia && item.link_evidencia.trim() !== '') {
        this.openEvidence(item.link_evidencia)
      } else if (item.palabra_clave && item.palabra_clave.trim() !== '') {
        this.showEncuestaInfo(item.palabra_clave)
      } else {
        this.$swal({
          title: 'Sin evidencia',
          text: 'Este indicador no tiene evidencia configurada.',
          icon: 'info',
          confirmButtonText: 'Continuar'
        })
      }
    },

    // ⭐ MÉTODO PARA ABRIR MODAL DE AGREGAR INDICADOR
    openAddIndicatorModal() {
      this.editingIndex = -1 // Indicar que es nuevo
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

    // ⭐ MÉTODO PARA ABRIR MODAL DE EDITAR DESCRIPCIÓN
    openEditDescriptionModal() {
      this.editingNombre = this.characteristic.nombre || ''
      this.editingDescription = this.characteristic.descripcion || ''
      this.showEditDescriptionModal = true
    },

    // ⭐ MÉTODO PARA CERRAR MODAL DE EDITAR DESCRIPCIÓN
    closeEditDescriptionModal() {
      this.showEditDescriptionModal = false
      this.editingNombre = ''
      this.editingDescription = ''
    },

    // ⭐ MÉTODO PARA GUARDAR CAMBIOS DE DESCRIPCIÓN
    async saveDescriptionChanges() {
      try {
        const token = localStorage.getItem('access_token')
        
        // Validar que los campos no estén vacíos
        if (!this.editingNombre.trim() || !this.editingDescription.trim()) {
          this.$swal({
            title: 'Error',
            text: 'El nombre y la descripción son requeridos.',
            icon: 'warning',
            confirmButtonText: 'Continuar'
          })
          return
        }

        // Preparar datos para enviar al backend
        const updatedData = {
          nombre: this.editingNombre.trim(),
          descripcion: this.editingDescription.trim()
        }

        console.log('Updating characteristic:', updatedData)

        // Llamada al API para actualizar la característica
        const response = await axios.patch(
          `/characteristics/${this.characteristicsId}/`,
          updatedData,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }
        )

        console.log('Characteristic updated:', response.data)

        this.$swal({
          title: '¡Característica Actualizada!',
          text: 'Los cambios se han guardado correctamente.',
          icon: 'success',
          confirmButtonText: 'Continuar'
        })

        // Recargar los datos para mostrar los cambios
        await this.fetchCaracteristica()
        this.closeEditDescriptionModal()

      } catch (error) {
        console.error('Error updating characteristic:', error)
        
        let errorMessage = 'Error al actualizar la característica.'
        
        if (error.response?.status === 401) {
          errorMessage = 'Sesión expirada. Por favor, inicia sesión nuevamente.'
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user_data')
          this.$router.push('/login')
        } else if (error.response?.status === 403) {
          errorMessage = 'No tienes permisos para realizar esta acción.'
        } else if (error.response?.status === 404) {
          errorMessage = 'La característica no fue encontrada.'
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

    saveEvaluation() {
      // Método placeholder para guardar evaluación
      this.$swal({
        title: '¡Evaluación Guardada!',
        text: 'La evaluación se ha guardado correctamente.',
        icon: 'success',
        confirmButtonText: 'Continuar'
      })
    },

    // ⭐ NUEVO MÉTODO PARA MANEJAR CAMBIO DE TIPO DE EVIDENCIA
    onEvidenceTypeChange(newValue) {
      if (newValue === 'encuesta') {
        // Limpiar campo de link evidencia
        this.editingIndicator.link_evidencia = ''
        
        // Abrir modal de búsqueda automáticamente
        this.openSearchModal()
      } else if (newValue === 'documental') {
        // Limpiar campo de palabra clave
        this.editingIndicator.palabraClave = ''
      }
    },

    // Métodos para búsqueda de preguntas (SIMPLIFICADAS)
    openSearchModal() {
      this.showSearchModal = true
      this.searchQuery = ''
      this.selectedQuestion = null
      this.searchResults = []
      this.currentPage = 1
    },

    closeSearchModal() {
      this.showSearchModal = false
      this.searchQuery = ''
      this.searchResults = []
      this.selectedQuestion = null
      this.currentPage = 1
    },

    async performSearch() {
      if (!this.searchQuery || this.searchQuery.trim().length < 3) {
        this.searchResults = []
        return
      }

      this.isSearching = true
      this.searchResults = []

      // ⭐ AGREGAR LOGS DE DEBUG
      console.log('=== INICIANDO BÚSQUEDA DE PREGUNTAS ===')
      console.log('Query:', this.searchQuery.trim())
      console.log('Longitud del query:', this.searchQuery.trim().length)

      try {
        const token = localStorage.getItem('access_token')
        console.log('Token disponible:', token ? 'Sí' : 'No')
        
        const allSurveyTypes = ['administrativos', 'directivos', 'docentes', 'egresados', 'empleadores', 'estudiantes']
        
        const requestData = {
          query: this.searchQuery.trim(),
          survey_types: allSurveyTypes
        }
        
        console.log('Datos de la petición:', requestData)
        console.log('URL de la petición:', '/surveys/search/')
        console.log('URL completa estimada:', `${axios.defaults.baseURL}/surveys/search/`)

        const response = await axios.post('/surveys/search/', requestData, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        console.log('Respuesta exitosa:', response.data)
        this.searchResults = response.data.results || []
        this.currentPage = 1

      } catch (error) {
        console.error('=== ERROR EN BÚSQUEDA ===')
        console.error('Tipo de error:', error.constructor.name)
        console.error('Status del error:', error.response?.status)
        console.error('URL solicitada:', error.config?.url)
        console.error('Método:', error.config?.method)
        console.error('Headers enviados:', error.config?.headers)
        console.error('Datos enviados:', error.config?.data)
        console.error('Respuesta del servidor:', error.response?.data)
        console.error('Error completo:', error)

        let errorMessage = 'Error al buscar preguntas. Intente nuevamente.'
        
        if (error.response?.status === 404) {
          errorMessage = 'Endpoint de búsqueda no encontrado. Verifique la configuración del servidor.'
        } else if (error.response?.status === 403) {
          errorMessage = 'No tiene permisos para buscar preguntas.'
        } else if (error.response?.status === 401) {
          errorMessage = 'Sesión expirada. Por favor, inicie sesión nuevamente.'
        }

        this.$swal({
          title: 'Error de Búsqueda',
          text: errorMessage,
          icon: 'error',
          confirmButtonText: 'Continuar'
        })
      } finally {
        this.isSearching = false
        console.log('=== FIN DE BÚSQUEDA ===')
      }
    },

    selectQuestion(question) {
      this.selectedQuestion = question
    },

    previewQuestion(question) {
      this.$swal({
        title: 'Vista Previa de Pregunta',
        html: `
          <div style="text-align: left; padding: 10px;">
            <p><strong>Encuesta:</strong> ${this.getSurveyTypeLabel(question.survey_type)}</p>
            <p><strong>Pregunta:</strong> ${question.question}</p>
            <hr style="margin: 10px 0;">
            <p><strong>Distribución de respuestas:</strong></p>
            <ul style="text-align: left;">
              <li>No tengo información: ${question.responses['1. No tengo información o conocimiento'] || 0}</li>
              <li>Totalmente en desacuerdo: ${question.responses['2. Totalmente en desacuerdo'] || 0}</li>
              <li>En desacuerdo: ${question.responses['3. En desacuerdo'] || 0}</li>
              <li>De acuerdo: ${question.responses['4. De acuerdo'] || 0}</li>
              <li>Totalmente de acuerdo: ${question.responses['5. Totalmente de acuerdo'] || 0}</li>
            </ul>
            <p><strong>Total respuestas:</strong> ${question.total_responses}</p>
          </div>
        `,
        icon: 'info',
        confirmButtonText: 'Cerrar',
        width: '600px'
      })
    },

    getSurveyTypeLabel(type) {
      const labels = {
        administrativos: 'Administrativos',
        directivos: 'Directivos',
        docentes: 'Docentes',
        egresados: 'Egresados',
        empleadores: 'Empleadores',
        estudiantes: 'Estudiantes'
      }
      return labels[type] || type
    },

    getSurveyTypeColor(type) {
      const colors = {
        administrativos: 'purple',
        directivos: 'indigo',
        docentes: 'blue',
        egresados: 'green',
        empleadores: 'orange',
        estudiantes: 'red'
      }
      return colors[type] || 'grey'
    },

    generateChart() {
      if (!this.selectedQuestion) return

      // Actualizar el campo de palabra clave con la pregunta seleccionada
      this.editingIndicator.palabraClave = this.selectedQuestion.question
      
      this.$swal({
        title: '¡Pregunta Seleccionada!',
        text: 'La pregunta ha sido asociada al indicador.',
        icon: 'success',
        confirmButtonText: 'Continuar',
        timer: 2000,
        timerProgressBar: true
      })

      // Cerrar modal de búsqueda
      this.closeSearchModal()
    }
  },

  async mounted() {
    console.log(this.$route.params.caracteristicaId)
    this.characteristicsId = this.$route.params.caracteristicaId
    await this.fetchCaracteristica()
  }
}
</script>

<style lang="css" scoped>
@import '../../styles/dashboard_indicators.css';
</style>