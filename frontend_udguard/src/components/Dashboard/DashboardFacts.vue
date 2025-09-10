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
          <!-- Botón Adjuntar Resultados -->
          <div class="header-actions">
            <button @click="showAttachResultsModal = true" class="attach-results-btn" title="Abrir modal para subir resultados de encuestas">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 1-8.49-8.49l9.19-9.19a4 4 0 0 1 5.66 5.66L9.64 16.2a2 2 0 0 1-2.83-2.83l8.49-8.49"/>
              </svg>
              <span>Adjuntar Resultados de Encuesta</span>
            </button>
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
                
                <!-- ⭐ AGREGAR BOTÓN EDITAR FACTOR -->
                <div class="factor-actions">
                  <button 
                    @click="editarFactor(factor)" 
                    class="icon-btn edit-btn"
                    title="Editar factor"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                      <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                    </svg>
                  </button>
                </div>
                
                <!-- MANTENER LA ESTRUCTURA ORIGINAL DEL COLOR QUE FUNCIONABA -->
                <div
                  class="factor-status"
                  :style="{ backgroundColor: getEstadoColor(factor).color || '#6b7280' }"
                  :title="`${getEstadoColor(factor).label} - Promedio: ${factor.estado?.promedio || factor.cumplimiento || 0}`"
                >
                  <span class="status-indicator">
                    {{ getEstadoColor(factor).label }}
                  </span>
                  <span v-if="factor.caracteristicas && factor.caracteristicas.length > 0" class="status-score">
                    {{ factor.estado?.promedio || parseFloat(factor.cumplimiento || 0).toFixed(1) }}
                  </span>
                </div>
              </div>
              
              <div class="factor-card-body">
                <!-- ⭐ AGREGAR LAS NUEVAS MÉTRICAS DEBAJO DEL CONTENIDO ORIGINAL -->
                <div class="factor-metrics">
                  <div class="metrics-row">
                    <span class="metric-label">Grado Cumplimiento:</span>
                    <span class="metric-value">{{ parseFloat(factor.cumplimiento || 0).toFixed(1) }}</span>
                  </div>
                  
                  <div class="metrics-row">
                    <span class="metric-label">Total Metas:</span>
                    <span class="metric-value total-metas">{{ parseFloat(factor.total_metas || 0).toFixed(1) }}</span>
                  </div>
                  
                  <div class="metrics-row">
                    <span class="metric-label">Total Puntajes:</span>
                    <span class="metric-value total-puntajes">{{ parseFloat(factor.total_puntajes || 0).toFixed(1) }}</span>
                  </div>
                  
                  <div class="metrics-row">
                    <span class="metric-label">Características:</span>
                    <span class="metric-value caracteristicas-count">{{ factor.cantidad_caracteristicas || 0 }}</span>
                  </div>
                </div>

                <!-- ⭐ MANTENER LA LISTA ORIGINAL DE CARACTERÍSTICAS -->
                <div v-if="factor.caracteristicas && factor.caracteristicas.length > 0" class="characteristics-summary">
                  <h4 class="characteristics-title">Características:</h4>
                  <ul class="factor-details">
                    <li v-for="caracteristica in factor.caracteristicas.slice(0, 3)" :key="caracteristica.nombre">
                      {{ caracteristica.nombre }}
                    </li>
                    <li v-if="factor.caracteristicas.length > 3" class="more-items">
                      +{{ factor.caracteristicas.length - 3 }} más...
                    </li>
                  </ul>
                </div>
                
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

    <!-- Modal Adjuntar Resultados -->
    <div v-if="showAttachResultsModal" class="modal-overlay" @click="closeAttachResultsModal">
      <div class="modal-content attach-results-modal" @click.stop>
        <!-- Header mejorado -->
        <div class="modal-header">
          <div class="modal-header-content">
            <div class="modal-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
              </svg>
            </div>
            <div class="modal-title-content">
              <h3 class="modal-title">Subir Resultados de Encuesta</h3>
              <p class="modal-subtitle">Cargue los archivos Excel con los resultados de las encuestas aplicadas</p>
            </div>
            <button class="modal-close-btn" @click="closeAttachResultsModal" title="Cerrar modal">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
        </div>

        <div class="modal-body">
          <!-- Información de ayuda -->
          <div class="info-section">
            <div class="info-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="16" x2="12" y2="12"/>
                <line x1="12" y1="8" x2="12.01" y2="8"/>
              </svg>
            </div>
            <div class="info-text">
              <p><strong>Instrucciones:</strong> Seleccione el tipo de encuesta y cargue el archivo Excel correspondiente. El sistema procesará automáticamente los datos.</p>
            </div>
          </div>

          <!-- Selector de tipo de resultados mejorado -->
          <div class="form-group">
            <label class="form-label">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
                <circle cx="9" cy="7" r="4"/>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
              </svg>
              Tipo de Encuesta *
            </label>
            <div class="select-wrapper">
              <select v-model="selectedResultType" class="form-select">
                <option value="estudiantes">📚 Encuesta a Estudiantes</option>
                <option value="docentes">👨‍🏫 Encuesta a Docentes</option>
                <option value="egresados">🎓 Encuesta a Egresados</option>
                <option value="empleadores">🏢 Encuesta a Empleadores</option>
                <option value="administrativos">👥 Encuesta a Personal Administrativo</option>
                <!-- ⭐ NUEVA OPCIÓN PARA DIRECTIVOS -->
                <option value="directivos">👔 Encuesta a Directivos de la Maestría</option>
              </select>
              <div class="select-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <polyline points="6,9 12,15 18,9"/>
                </svg>
              </div>
            </div>
            <div class="form-help">
              Seleccione el tipo de encuesta que corresponde al archivo que va a cargar
            </div>
          </div>

          <!-- Área de carga de archivos mejorada -->
          <div class="form-group">
            <label class="form-label">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7,10 12,15 17,10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
              Archivo Excel *
            </label>
            
            <!-- Drag & Drop Area -->
            <div 
              class="file-upload-area"
              :class="{ 'dragover': isDragOver }"
              @dragover.prevent="isDragOver = true"
              @dragleave.prevent="isDragOver = false"
              @drop.prevent="handleFileDrop"
              @click="$refs.fileInput.click()"
            >
              <input 
                type="file" 
                ref="fileInput" 
                @change="handleFileSelect" 
                accept=".xlsx,.xls,.csv" 
                class="file-input-hidden"
              />
              
              <div v-if="!selectedFile" class="file-upload-content">
                <div class="upload-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7,10 12,15 17,10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                  </svg>
                </div>
                <div class="upload-text">
                  <p class="upload-primary">Arrastre su archivo aquí o <span class="upload-link">haga clic para buscar</span></p>
                  <p class="upload-secondary">Formatos soportados: Excel (.xlsx, .xls) y CSV</p>
                </div>
              </div>
              
              <div v-else class="file-selected-content">
                <div class="file-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                    <polyline points="14,2 14,8 20,8"/>
                  </svg>
                </div>
                <div class="file-info">
                  <p class="file-name">{{ selectedFileName }}</p>
                  <p class="file-size">{{ formatFileSize(selectedFile.size) }}</p>
                </div>
                <button 
                  type="button" 
                  class="remove-file-btn" 
                  @click.stop="removeFile"
                  title="Remover archivo"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"/>
                    <line x1="6" y1="6" x2="18" y2="18"/>
                  </svg>
                </button>
              </div>
            </div>
            
            <div class="form-help">
              <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="16" x2="12" y2="12"/>
                <line x1="12" y1="8" x2="12.01" y2="8"/>
              </svg>
              Tamaño máximo: 10MB. Asegúrese de que el archivo tenga el formato correcto.
            </div>
          </div>

          <!-- Progress bar (hidden by default) -->
          <div v-if="isUploading" class="upload-progress">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
            </div>
            <p class="progress-text">Subiendo archivo... {{ uploadProgress }}%</p>
          </div>
        </div>

        <!-- Footer con botones mejorados -->
        <div class="modal-footer">
          <button 
            @click="closeAttachResultsModal" 
            class="modal-btn modal-btn-secondary"
            :disabled="isUploading"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
            Cancelar
          </button>
          
          <button 
            @click="uploadExcel" 
            class="modal-btn modal-btn-primary" 
            :disabled="!selectedFile || isUploading"
          >
            <svg v-if="!isUploading" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="7,10 12,15 17,10"/>
              <line x1="12" y1="15" x2="12" y2="3"/>
            </svg>
            <div v-else class="loading-spinner-small"></div>
            {{ isUploading ? 'Subiendo...' : 'Subir Archivo' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Modal para editar factor -->
    <div class="modal" v-if="mostrarModalEditarFactor" @click.self="cerrarModalEditarFactor">
      <div class="modal-content">
        <div class="modal-header">
          <h3>Editar Factor</h3>
          <button @click="cerrarModalEditarFactor" class="close-btn" title="Cerrar">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <!-- Campo nombre -->
          <div class="form-section">
            <label class="form-label">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 6h16M4 12h16M4 18h16"/>
              </svg>
              Nombre del Factor *
            </label>
            <input 
              v-model="factorEditando.nombre" 
              placeholder="Ej: Estudiantes" 
              class="input"
              @keypress.enter="$event.target.blur()"
              maxlength="200"
            />
            <div class="input-counter">
              {{ (factorEditando.nombre || '').length }}/200 caracteres
            </div>
          </div>
          
          <!-- Campo descripción -->
          <div class="form-section">
            <label class="form-label">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10,9 9,9 8,9"/>
              </svg>
              Descripción del Factor
            </label>
            <textarea 
              v-model="factorEditando.descripcion" 
              placeholder="Describa detalladamente este factor..." 
              class="input textarea-input"
              rows="6"
              maxlength="1000"
            ></textarea>
            <div class="input-counter">
              {{ (factorEditando.descripcion || '').length }}/1000 caracteres
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="cerrarModalEditarFactor" class="cancel-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
            Cancelar
          </button>
          <button 
            @click="guardarFactor" 
            class="save-btn primary"
            :disabled="!factorEditando.nombre?.trim()"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
              <polyline points="17,21 17,13 7,13 7,21"/>
              <polyline points="7,3 7,8 15,8"/>
            </svg>
            Guardar Cambios
          </button>
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
      error: null,
      // Modal de adjuntar resultados - variables actualizadas
      showAttachResultsModal: false,
      selectedResultType: 'estudiantes',
      selectedFile: null,
      selectedFileName: '',
      isDragOver: false,
      isUploading: false,
      uploadProgress: 0,
      
      // ⭐ VARIABLES PARA EDITAR FACTOR (mantener las existentes)
      mostrarModalEditarFactor: false,
      factorEditando: {
        id: null,
        nombre: '',
        descripcion: ''
      }
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
        console.log('Fetching factors with totals...')
        
        const response = await axios.get('/factors/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        
        console.log('Raw API response:', response.data)
        this.factores = response.data

        // ⭐ DEBUG MEJORADO PARA VERIFICAR LOS NUEVOS DATOS
        console.log('Factores con totales:', this.factores.map(f => ({
          id: f.id,
          nombre: f.nombre,
          cumplimiento: f.cumplimiento,
          total_metas: f.total_metas,
          total_puntajes: f.total_puntajes,
          cantidad_caracteristicas: f.cantidad_caracteristicas,
          total_indicadores: f.total_indicadores,
          grado_cumplimiento: f.grado_cumplimiento,
          caracteristicas_count: f.caracteristicas?.length || 0
        })));

      } catch (error) {
        console.error('Error fetching factors:', error)
        
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
      // ⭐ PRIORIZAR LOS DATOS DEL GRADO_CUMPLIMIENTO
      if (factor.grado_cumplimiento && factor.grado_cumplimiento.color) {
        return { 
          color: factor.grado_cumplimiento.color, 
          label: factor.grado_cumplimiento.descripcion 
        }
      }
      
      // Fallback al estado original si existe
      if (factor.estado && factor.estado.color) {
        return { 
          color: factor.estado.color, 
          label: factor.estado.descripcion 
        }
      }

      // Default
      return { color: '#6b7280', label: 'Sin datos' }
    },

    // ⭐ SIMPLIFICAR EL MÉTODO DE CUMPLIMIENTO PARA USAR DATOS DEL BACKEND
    getPromedioCumplimiento(factor) {
      return parseFloat(factor.cumplimiento) || 0
    },

    getEstadoColorClass(factor) {
      const estado = this.getEstadoColor(factor).label
      return {
        'status-green': estado === 'Se cumple plenamente' && this.getPromedioCumplimiento(factor) >= 4.5,
        'status-green-yellow': estado === 'Se cumple en alto grado' && this.getPromedioCumplimiento(factor) >= 4.0 && this.getPromedioCumplimiento(factor) < 4.5,
        'status-yellow': estado === 'Se cumple aceptablemente' && this.getPromedioCumplimiento(factor) >= 3.5,
        'status-orange': estado === 'Se cumple insatisfactoriamente' && this.getPromedioCumplimiento(factor) >= 3.0 && this.getPromedioCumplimiento(factor) < 3.5,
        'status-red': estado === 'No se cumple' || estado === 'Crítico',
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
    },

    // Métodos para el modal de adjuntar resultados
    closeAttachResultsModal() {
      this.showAttachResultsModal = false
      this.resetAttachResultsForm()
    },

    resetAttachResultsForm() {
      this.selectedResultType = 'estudiantes'
      this.selectedFile = null
      this.selectedFileName = ''
    },

    handleFileSelect(event) {
      const file = event.target.files[0]
      if (file) {
        this.selectedFile = file
        this.selectedFileName = file.name
      }
    },

    async uploadExcel() {
      if (!this.selectedFile) {
        this.$swal({
          title: 'Archivo requerido',
          text: 'Por favor seleccione un archivo Excel para continuar.',
          icon: 'warning',
          confirmButtonText: 'Entendido'
        });
        return;
      }

      // Validar el tipo de archivo
      const validTypes = ['.xlsx', '.xls', '.csv'];
      const fileExtension = this.selectedFile.name.toLowerCase().substring(this.selectedFile.name.lastIndexOf('.'));
      
      if (!validTypes.includes(fileExtension)) {
        this.$swal({
          title: 'Formato no válido',
          text: 'Solo se permiten archivos Excel (.xlsx, .xls) o CSV (.csv).',
          icon: 'error',
          confirmButtonText: 'Entendido'
        });
        return;
      }

      try {
        // Mostrar progreso
        this.isUploading = true;
        this.uploadProgress = 10;

        const token = localStorage.getItem('access_token');
        const encuestaInfo = this.getEncuestaInfo(this.selectedResultType);

        // Crear FormData para enviar el archivo
        const formData = new FormData();
        formData.append('file', this.selectedFile);
        formData.append('survey_type', this.selectedResultType);

        console.log('Uploading survey file:', {
          fileName: this.selectedFile.name,
          surveyType: this.selectedResultType,
          fileSize: this.selectedFile.size
        });

        // Simular progreso
        const progressInterval = setInterval(() => {
          if (this.uploadProgress < 90) {
            this.uploadProgress += Math.random() * 20;
          }
        }, 200);

        // ⭐ LLAMAR AL NUEVO ENDPOINT DEL BACKEND
        const response = await axios.post('/surveys/upload/', formData, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          },
          onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            this.uploadProgress = Math.max(this.uploadProgress, percentCompleted);
          }
        });

        clearInterval(progressInterval);
        this.uploadProgress = 100;

        console.log('Survey upload response:', response.data);

        // Mostrar resultado exitoso
        setTimeout(() => {
          this.isUploading = false;
          this.uploadProgress = 0;
          
          this.$swal({
            title: '¡Carga Exitosa!',
            html: `
              <div style="text-align: left; padding: 10px;">
                <p><strong>Archivo:</strong> ${this.selectedFile.name}</p>
                <p><strong>Tipo:</strong> ${encuestaInfo.nombre}</p>
                <p><strong>Tamaño:</strong> ${this.formatFileSize(this.selectedFile.size)}</p>
                <p><strong>Estado:</strong> ✅ Procesado correctamente</p>
                <hr style="margin: 10px 0;">
                <p><strong>Preguntas procesadas:</strong> ${response.data.questions_processed}</p>
                <p><strong>Total respuestas:</strong> ${response.data.total_responses}</p>
                <p><strong>Archivo JSON generado:</strong> ${response.data.json_file}</p>
                <hr style="margin: 10px 0;">
                <p style="color: #059669; font-weight: 600;">
                  ${encuestaInfo.mensaje}
                </p>
              </div>
            `,
            icon: 'success',
            confirmButtonText: 'Continuar'
          });
          
          this.closeAttachResultsModal();
        }, 500);

      } catch (error) {
        this.isUploading = false;
        this.uploadProgress = 0;
        
        console.error('Error uploading survey:', error);
        
        let errorMessage = 'Error al procesar el archivo.';
        
        if (error.response?.status === 401) {
          errorMessage = 'Sesión expirada. Por favor, inicia sesión nuevamente.';
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user_data');
          this.$router.push('/login');
        } else if (error.response?.status === 403) {
          errorMessage = 'No tienes permisos para subir encuestas.';
        } else if (error.response?.status === 400) {
          errorMessage = error.response.data?.error || 'Archivo inválido o datos incorrectos.';
        } else if (error.response?.status === 413) {
          errorMessage = 'El archivo es demasiado grande. Tamaño máximo: 10MB.';
        } else if (error.response?.data?.error) {
          errorMessage = error.response.data.error;
        }

        this.$swal({
          title: 'Error al procesar archivo',
          text: errorMessage,
          icon: 'error',
          confirmButtonText: 'Entendido'
        });
      }
    },

    // ⭐ NUEVO MÉTODO PARA OBTENER INFORMACIÓN DE CADA TIPO DE ENCUESTA
    getEncuestaInfo(tipo) {
      const encuestas = {
        estudiantes: {
          nombre: 'Encuesta a Estudiantes',
          mensaje: 'Los resultados de la encuesta a estudiantes han sido procesados y están disponibles para análisis.'
        },
        docentes: {
          nombre: 'Encuesta a Docentes',
          mensaje: 'Los resultados de la encuesta a docentes han sido integrados al sistema de evaluación.'
        },
        egresados: {
          nombre: 'Encuesta a Egresados',
          mensaje: 'Los datos de la encuesta a egresados han sido incorporados exitosamente.'
        },
        empleadores: {
          nombre: 'Encuesta a Empleadores',
          mensaje: 'Los resultados de la encuesta a empleadores han sido registrados en el sistema.'
        },
        administrativos: {
          nombre: 'Encuesta a Personal Administrativo',
          mensaje: 'Los datos del personal administrativo han sido procesados correctamente.'
        },
        // ⭐ NUEVA INFORMACIÓN PARA DIRECTIVOS
        directivos: {
          nombre: 'Encuesta a Directivos de la Maestría',
          mensaje: 'Los resultados de la encuesta a directivos han sido incorporados al análisis institucional. Esta información es clave para la evaluación de la gestión académica y administrativa del programa.'
        }
      };
      
      return encuestas[tipo] || {
        nombre: 'Tipo de encuesta desconocido',
        mensaje: 'Los datos han sido procesados.'
      };
    },

    // ⭐ MÉTODO PARA FORMATEAR TAMAÑO DE ARCHIVO
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes';
      
      const k = 1024;
      const sizes = ['Bytes', 'KB', 'MB', 'GB'];
      const i = Math.floor(Math.log(bytes) / Math.log(k));
      
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    // ⭐ NUEVOS MÉTODOS PARA DRAG & DROP
    handleFileDrop(event) {
      this.isDragOver = false;
      const files = event.dataTransfer.files;
      
      if (files.length > 0) {
        const file = files[0];
        
        // Validar tipo de archivo
        const validTypes = ['.xlsx', '.xls', '.csv'];
        const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
        
        if (validTypes.includes(fileExtension)) {
          this.selectedFile = file;
          this.selectedFileName = file.name;
        } else {
          this.$swal({
            title: 'Formato no válido',
            text: 'Solo se permiten archivos Excel (.xlsx, .xls) o CSV (.csv).',
            icon: 'error',
            confirmButtonText: 'Entendido'
          });
        }
      }
    },

    // ⭐ MÉTODO PARA REMOVER ARCHIVO SELECCIONADO
    removeFile() {
      this.selectedFile = null;
      this.selectedFileName = '';
      this.$refs.fileInput.value = '';
    },
    
    // Métodos para el modal de editar factor
    editarFactor(factor) {
      this.factorEditando = {
        id: factor.id,
        nombre: factor.nombre || '',
        descripcion: factor.descripcion || ''
      };
      this.mostrarModalEditarFactor = true;
      
      console.log('Editando factor:', {
        id: factor.id,
        nombre: factor.nombre,
        descripcion: factor.descripcion
      });
    },

    cerrarModalEditarFactor() {
      this.mostrarModalEditarFactor = false;
      this.factorEditando = {
        id: null,
        nombre: '',
        descripcion: ''
      };
    },

    async guardarFactor() {
      if (!this.factorEditando.nombre?.trim()) {
        this.$swal({
          title: 'Error',
          text: 'El nombre del factor es requerido.',
          icon: 'warning',
          confirmButtonText: 'Continuar'
        });
        return;
      }

      try {
        const token = localStorage.getItem('access_token');
        
        console.log('Guardando factor:', this.factorEditando);

        // ⭐ CORREGIR EL ENDPOINT - DEBE INCLUIR EL ID
        const response = await axios.patch(
          `/factors/${this.factorEditando.id}/`, // ⭐ AGREGAR EL ID AL ENDPOINT
          {
            nombre: this.factorEditando.nombre.trim(),
            descripcion: this.factorEditando.descripcion?.trim() || ''
          },
          {
            headers: {
              Authorization: `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }
        );
        
        console.log('Factor updated:', response.data);

        // ⭐ REFRESCAR DATOS DEL BACKEND DESPUÉS DE ACTUALIZAR
        await this.fetchFactores();

        this.$swal({
          title: '¡Factor Actualizado!',
          text: 'Los cambios se han guardado correctamente.',
          icon: 'success',
          confirmButtonText: 'Continuar'
        });

        this.cerrarModalEditarFactor();

      } catch (error) {
        console.error('Error updating factor:', error);
        
        let errorMessage = 'Error al guardar el factor.';
        
        if (error.response?.status === 401) {
          errorMessage = 'Sesión expirada. Por favor, inicia sesión nuevamente.';
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user_data');
          this.$router.push('/login');
        } else if (error.response?.status === 403) {
          errorMessage = 'No tienes permisos para realizar esta acción.';
        } else if (error.response?.status === 400) {
          errorMessage = 'Datos inválidos. Verifique que el nombre no esté duplicado.';
        } else if (error.response?.status === 404) {
          errorMessage = 'El factor no fue encontrado.';
        } else if (error.response?.data?.message) {
          errorMessage = error.response.data.message;
        } else if (error.response?.data?.error) {
          errorMessage = error.response.data.error;
        }

        this.$swal({
          title: 'Error',
          text: errorMessage,
          icon: 'error',
          confirmButtonText: 'Continuar'
        });
      }
    }
  },

  async mounted() {
    console.log('DashboardFacts mounted')
    
    // ⭐ VERIFICAR QUE SWEETALERT2 ESTÉ DISPONIBLE
    if (!this.$swal) {
      console.warn('SweetAlert2 not available, using browser alert as fallback')
    }
    
    if (this.checkAuthentication()) {
      console.log('User authenticated, loading data')
      await this.fetchFactores()
    }
  }
}
</script>

<style lang="css" scoped>
@import '../../styles/dashboard_facts.css';
</style>
