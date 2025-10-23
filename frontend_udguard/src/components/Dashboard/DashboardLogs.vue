<!-- filepath: c:\Users\Flame Lord\Documents\Documentos U\Monografía\UD_Guard\frontend_udguard\src\components\Dashboard\DashboardLogs.vue -->
<template>
  <div class="dashboard-logs-wrapper">
    <div class="dashboard-logs-container">
      <!-- Header con título y filtros -->
      <div class="dashboard-header-logs dashboard-logs-specific-header">
        <div class="dashboard-header-content dashboard-logs-header-content">
          <div class="header-text-content dashboard-logs-text-content">
            <h1 class="dashboard-title dashboard-logs-title">Sistema de Logs</h1>
            <p class="dashboard-subtitle dashboard-logs-subtitle">
              Visualiza y monitorea el historial de actividades del sistema. 
              <strong>Rastrea acciones</strong>, usuarios y fechas de eventos importantes.
            </p>
          </div>
        </div>
      </div>

      <!-- Sección de filtros -->
      <div class="filters-section">
        <div class="filter-container">
          <div class="search-filter">
            <div class="search-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="11" cy="11" r="8"/>
                <path d="M21 21l-4.35-4.35"/>
              </svg>
            </div>
            <input 
              v-model="searchFilter" 
              type="text" 
              placeholder="Buscar por acción, usuario o fecha..."
              class="search-input"
              @input="handleSearch"
            />
            <button 
              v-if="searchFilter" 
              @click="clearSearch" 
              class="clear-search-btn"
              title="Limpiar búsqueda"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </div>
          
          <!-- Stats del filtro -->
          <div class="filter-stats">
            <span class="results-count">
              {{ logs.length }} de {{ totalItems }} registros
            </span>
          </div>
        </div>
      </div>

      <!-- Contenido principal -->
      <div class="dashboard-content">
        <div class="logs-container">
          <!-- Estado de carga -->
          <div v-if="loading" class="loading-state">
            <div class="loading-spinner"></div>
            <p>Cargando logs del sistema...</p>
          </div>
          
          <!-- Estado de error -->
          <div v-else-if="error" class="error-state">
            <div class="error-icon">⚠️</div>
            <p>{{ error }}</p>
            <button @click="fetchLogs" class="retry-button">Reintentar</button>
          </div>

          <!-- Estado vacío -->
          <div v-else-if="logs.length === 0" class="empty-state">
            <div class="empty-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14,2 14,8 20,8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
                <polyline points="10,9 9,9 8,9"/>
              </svg>
            </div>
            <h3>No hay logs registrados</h3>
            <p>Aún no se han registrado actividades en el sistema.</p>
          </div>

          <!-- Tabla de logs -->
          <div v-else class="logs-table-wrapper" style="width: 100%;">
            <div class="table-controls">
              <div class="table-info">
                <span class="table-results">
                  Mostrando {{ startIndex + 1 }}-{{ endIndex }} de {{ totalItems }} registros
                </span>
              </div>
              <div class="table-actions">
                <button 
                  @click="refreshLogs" 
                  class="refresh-btn"
                  title="Actualizar datos"
                  :disabled="loading"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="23 4 23 10 17 10"/>
                    <polyline points="1 20 1 14 7 14"/>
                    <path d="M20.49 9A9 9 0 0 0 5.64 5.64L1 10m22 4l-4.64 4.36A9 9 0 0 1 3.51 15"/>
                  </svg>
                  Actualizar
                </button>
              </div>
            </div>

            <div class="logs-table-container">
              <table class="logs-table">
                <thead class="table-header">
                  <tr>
                    <th 
                      class="sortable-header" 
                      @click="sortBy('accion')"
                      :class="{ 'sorted-asc': sortField === 'accion' && sortDirection === 'asc', 'sorted-desc': sortField === 'accion' && sortDirection === 'desc' }"
                    >
                      <div class="header-content">
                        <span>Acción</span>
                        <div class="sort-icon">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="6,9 12,15 18,9"/>
                          </svg>
                        </div>
                      </div>
                    </th>
                    <th 
                      class="sortable-header" 
                      @click="sortBy('usuario')"
                      :class="{ 'sorted-asc': sortField === 'usuario' && sortDirection === 'asc', 'sorted-desc': sortField === 'usuario' && sortDirection === 'desc' }"
                    >
                      <div class="header-content">
                        <span>Usuario</span>
                        <div class="sort-icon">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="6,9 12,15 18,9"/>
                          </svg>
                        </div>
                      </div>
                    </th>
                    <th 
                      class="sortable-header" 
                      @click="sortBy('fecha')"
                      :class="{ 'sorted-asc': sortField === 'fecha' && sortDirection === 'asc', 'sorted-desc': sortField === 'fecha' && sortDirection === 'desc' }"
                    >
                      <div class="header-content">
                        <span>Fecha</span>
                        <div class="sort-icon">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <polyline points="6,9 12,15 18,9"/>
                          </svg>
                        </div>
                      </div>
                    </th>
                  </tr>
                </thead>
                <tbody class="table-body">
                  <tr 
                    v-for="(log, index) in paginatedLogs" 
                    :key="log.id"
                    class="table-row"
                    :class="{ 'row-even': index % 2 === 0 }"
                  >
                    <td class="action-cell">
                      <div class="action-content">
                        <div class="action-icon" :class="getActionIconClass(log.accion)">
                          {{ getActionIcon(log.accion) }}
                        </div>
                        <div class="action-details">
                          <span class="action-text">{{ log.accion }}</span>
                          <span class="action-category">{{ getActionCategory(log.accion) }}</span>
                        </div>
                      </div>
                    </td>
                    <td class="user-cell">
                      <div class="user-content">
                        <div class="user-avatar">
                          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                            <circle cx="12" cy="7" r="4"/>
                          </svg>
                        </div>
                        <div class="user-details">
                          <span class="user-name">{{ getUserDisplayName(log.usuario) }}</span>
                          <span class="user-role">{{ getUserRole(log.usuario) }}</span>
                        </div>
                      </div>
                    </td>
                    <td class="date-cell">
                      <div class="date-content">
                        <div class="date-icon">
                          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <rect x="3" y="4" width="18" height="18" rx="2" ry="2"/>
                            <line x1="16" y1="2" x2="16" y2="6"/>
                            <line x1="8" y1="2" x2="8" y2="6"/>
                            <line x1="3" y1="10" x2="21" y2="10"/>
                          </svg>
                        </div>
                        <div class="date-details">
                          <span class="date-text">{{ formatDate(log.fecha) }}</span>
                          <span class="time-text">{{ formatTime(log.fecha) }}</span>
                        </div>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Paginación -->
            <div class="pagination-container">
              <div class="pagination-info">
                <span>Registros por página:</span>
                <select v-model="itemsPerPage" @change="handlePageSizeChange" class="page-size-select">
                  <option value="25">25</option>
                  <option value="50">50</option>
                  <option value="100">100</option>
                </select>
              </div>
              
              <div class="pagination-controls">
                <button 
                  @click="goToPage(1)" 
                  :disabled="currentPage === 1"
                  class="pagination-btn"
                  title="Primera página"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="11,17 6,12 11,7"/>
                    <polyline points="18,17 13,12 18,7"/>
                  </svg>
                </button>
                
                <button 
                  @click="goToPage(currentPage - 1)" 
                  :disabled="currentPage === 1"
                  class="pagination-btn"
                  title="Página anterior"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="15,18 9,12 15,6"/>
                  </svg>
                </button>
                
                <div class="page-numbers">
                  <button
                    v-for="page in visiblePages"
                    :key="page"
                    @click="goToPage(page)"
                    :class="{ 'active': page === currentPage }"
                    class="page-number-btn"
                  >
                    {{ page }}
                  </button>
                </div>
                
                <button 
                  @click="goToPage(currentPage + 1)" 
                  :disabled="currentPage === totalPages"
                  class="pagination-btn"
                  title="Página siguiente"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9,18 15,12 9,6"/>
                  </svg>
                </button>
                
                <button 
                  @click="goToPage(totalPages)" 
                  :disabled="currentPage === totalPages"
                  class="pagination-btn"
                  title="Última página"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="13,17 18,12 13,7"/>
                    <polyline points="6,17 11,12 6,7"/>
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
  name: 'DashboardLogs',
  
  data() {
    return {
      logs: [],
      loading: false,
      error: null,
      
      // Filtros y búsqueda
      searchFilter: '',
      searchTimeout: null,
      
      // Ordenamiento
      sortField: 'fecha',
      sortDirection: 'desc',
      
      // Paginación
      currentPage: 1,
      itemsPerPage: 25,
      totalItems: 0,
      
      // ⭐ ELIMINAR sampleLogs YA QUE USAREMOS DATOS REALES
    }
  },

  computed: {
    // ⭐ SIMPLIFICAR COMPUTED PROPERTIES PARA USAR DATOS DEL BACKEND
    filteredLogs() {
      // Los filtros ahora se manejan en el backend
      return this.logs
    },

    sortedLogs() {
      // El ordenamiento ahora se maneja en el backend
      return this.logs
    },

    paginatedLogs() {
      // La paginación ahora se maneja en el backend
      return this.logs
    },

    totalPages() {
      return Math.ceil(this.totalItems / this.itemsPerPage)
    },

    startIndex() {
      return (this.currentPage - 1) * this.itemsPerPage
    },

    endIndex() {
      return Math.min(this.startIndex + this.logs.length, this.totalItems)
    },

    visiblePages() {
      const total = this.totalPages
      const current = this.currentPage
      const delta = 2
      
      const range = []
      const rangeWithDots = []
      
      for (let i = Math.max(2, current - delta);
           i <= Math.min(total - 1, current + delta);
           i++) {
        range.push(i)
      }
      
      if (current - delta > 2) {
        rangeWithDots.push(1, '...')
      } else {
        rangeWithDots.push(1)
      }
      
      rangeWithDots.push(...range)
      
      if (current + delta < total - 1) {
        rangeWithDots.push('...', total)
      } else if (total > 1) {
        rangeWithDots.push(total)
      }
      
      return rangeWithDots.filter((item, index, array) => array.indexOf(item) === index)
    }
  },

  methods: {
    // ⭐ MÉTODO PRINCIPAL PARA CARGAR LOGS DEL BACKEND
    async fetchLogs() {
      this.loading = true
      this.error = null
      
      try {
        const token = localStorage.getItem('access_token')
        
        if (!token) {
          this.error = 'No se encontró token de autenticación'
          this.$router.push('/login')
          return
        }

        // ⭐ CONSTRUIR PARÁMETROS DE LA PETICIÓN
        const params = new URLSearchParams({
          search: this.searchFilter.trim(),
          sort_field: this.sortField,
          sort_direction: this.sortDirection,
          page: this.currentPage.toString(),
          page_size: this.itemsPerPage.toString()
        })

        console.log('Fetching logs with params:', params.toString())

        const response = await axios.get(`/logs/${this.itemsPerPage}/?${params.toString()}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })

        console.log('Logs API response:', response.data)

        // ⭐ MANEJAR RESPUESTA PAGINADA
        if (response.data.results) {
          this.logs = response.data.results
          this.totalItems = response.data.count || response.data.results.length
        } else {
          this.logs = response.data
          this.totalItems = response.data.length
        }

        console.log(`Logs cargados: ${this.logs.length} de ${this.totalItems} total`)
        
      } catch (error) {
        console.error('Error fetching logs:', error)
        
        if (error.response?.status === 401) {
          this.error = 'Sesión expirada. Por favor, inicia sesión nuevamente.'
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user_data')
          this.$router.push('/login')
        } else if (error.response?.status === 403) {
          this.error = 'No tienes permisos para ver los logs del sistema.'
        } else if (error.response?.status === 404) {
          this.error = 'Endpoint de logs no encontrado.'
        } else {
          this.error = 'Error al cargar los logs. Por favor, intenta nuevamente.'
        }
      } finally {
        this.loading = false
      }
    },

    // Método para refrescar logs
    async refreshLogs() {
      this.currentPage = 1
      await this.fetchLogs()
    },

    // ⭐ MÉTODOS DE BÚSQUEDA ACTUALIZADOS
    handleSearch() {
      // Debounce para evitar búsquedas muy frecuentes
      if (this.searchTimeout) {
        clearTimeout(this.searchTimeout)
      }
      
      this.searchTimeout = setTimeout(async () => {
        this.currentPage = 1 // Resetear a primera página al buscar
        await this.fetchLogs()
      }, 500)
    },

    async clearSearch() {
      this.searchFilter = ''
      this.currentPage = 1
      await this.fetchLogs()
    },

    // ⭐ MÉTODOS DE ORDENAMIENTO ACTUALIZADOS
    async sortBy(field) {
      if (this.sortField === field) {
        this.sortDirection = this.sortDirection === 'asc' ? 'desc' : 'asc'
      } else {
        this.sortField = field
        this.sortDirection = 'asc'
      }
      this.currentPage = 1
      await this.fetchLogs()
    },

    // ⭐ MÉTODOS DE PAGINACIÓN ACTUALIZADOS
    async goToPage(page) {
      if (page >= 1 && page <= this.totalPages && page !== this.currentPage) {
        this.currentPage = page
        await this.fetchLogs()
      }
    },

    async handlePageSizeChange() {
      this.currentPage = 1
      await this.fetchLogs()
    },

    // ⭐ MÉTODOS DE FORMATEO MEJORADOS
    formatDate(date) {
      if (!date) return 'N/A'
      
      try {
        const dateObj = new Date(date)
        return dateObj.toLocaleDateString('es-CO', {
          year: 'numeric',
          month: '2-digit',
          day: '2-digit'
        })
      } catch (error) {
        return 'Fecha inválida'
      }
    },

    formatTime(date) {
      if (!date) return 'N/A'
      
      try {
        const dateObj = new Date(date)
        return dateObj.toLocaleTimeString('es-CO', {
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        })
      } catch (error) {
        return 'Hora inválida'
      }
    },

    // ⭐ MÉTODOS PARA OBTENER ICONOS Y ESTILOS SEGÚN LA ACCIÓN - ACTUALIZADO
    getActionIcon(action) {
      if (!action) return '📋'
      
      const actionMap = {
        // ⭐ OPERACIONES CRUD BÁSICAS
        CREAR: '➕',
        CREATE: '➕',
        ACTUALIZAR: '✏️',
        UPDATE: '✏️',
        ELIMINAR: '🗑️',
        DELETE: '🗑️',
        
        // ⭐ OPERACIONES DE USUARIOS
        LOGIN: '🔑',
        LOGOUT: '🚪',
        INHABILITAR: '⛔',
        DISABLE: '⛔',
        HABILITAR: '✅',
        ENABLE: '✅',
        
        // ⭐ OPERACIONES DE ARCHIVOS Y CONTENIDO
        SUBIR: '📤',
        UPLOAD: '📤',
        DESCARGAR: '📥',
        DOWNLOAD: '📥',

        // ⭐ OPERACIONES DE GRÁFICOS Y REPORTES
        GENERAR: '📊',
        GENERATE: '📊',
        GENERATE_CHART: '📊',
        EXPORTAR: '📋',
        EXPORT: '📋',

        // ⭐ OPERACIONES ESPECÍFICAS POR ENTIDAD
        FACTOR: '🎯',
        FACTORS: '🎯',
        CARACTERÍSTICAS: '📌',
        CARACTERÍSTICA: '📌',
        INDICADOR: '📈',
        INDICADORES: '📈',
        EVENTOS: '📅',
        EVENTO: '📅',
        CUSTOMUSER: '👤',
        USUARIO: '👤',

        // ⭐ OPERACIONES DE ENCUESTAS
        ENCUESTA: '📋',
        SURVEY: '📋',
        GRÁFICA: '📊',
        CHART: '📊',

        // ⭐ OPERACIONES DEL SISTEMA
        SISTEMA: '⚙️',
        SYSTEM: '⚙️',
        ERROR: '❌',
        SUCCESS: '✅',
        WARNING: '⚠️'
      }
      
      // ⭐ LÓGICA MEJORADA PARA DETECTAR LA ACCIÓN
      const upperAction = action.toUpperCase()
      
      // Buscar coincidencia exacta primero
      for (const [key, icon] of Object.entries(actionMap)) {
        if (upperAction.includes(key)) {
          return icon
        }
      }
      
      // Si no encuentra coincidencia, usar icono por defecto
      return '📋'
    },

    getActionIconClass(action) {
      if (!action) return { 'action-other': true }
      
      const upperAction = action.toUpperCase()
      
      return {
        // ⭐ CLASES PARA OPERACIONES CRUD
        'action-create': upperAction.includes('CREAR') || upperAction.includes('CREATE'),
        'action-update': upperAction.includes('ACTUALIZAR') || upperAction.includes('UPDATE'),
        'action-delete': upperAction.includes('ELIMINAR') || upperAction.includes('DELETE'),
        
        // ⭐ CLASES PARA OPERACIONES DE USUARIOS
        'action-login': upperAction.includes('LOGIN'),
        'action-logout': upperAction.includes('LOGOUT'),
        'action-disable': upperAction.includes('INHABILITAR') || upperAction.includes('DISABLE'),
        'action-enable': upperAction.includes('HABILITAR') || upperAction.includes('ENABLE'),
        
        // ⭐ CLASES PARA OPERACIONES DE ARCHIVOS
        'action-upload': upperAction.includes('SUBIR') || upperAction.includes('UPLOAD') || upperAction.includes('ENCUESTA'),
        'action-download': upperAction.includes('DESCARGAR') || upperAction.includes('DOWNLOAD'),
        
        // ⭐ CLASES PARA OPERACIONES DE GRÁFICOS
        'action-chart': upperAction.includes('GENERAR') || upperAction.includes('GENERATE') || upperAction.includes('GRÁFICA') || upperAction.includes('CHART'),
        'action-export': upperAction.includes('EXPORTAR') || upperAction.includes('EXPORT'),
        
        // ⭐ CLASES PARA ENTIDADES ESPECÍFICAS
        'action-factor': upperAction.includes('FACTOR'),
        'action-characteristic': upperAction.includes('CHARACTERISTICS') || upperAction.includes('CARACTERÍSTICA'),
        'action-indicator': upperAction.includes('INDICATOR') || upperAction.includes('INDICADOR'),
        'action-event': upperAction.includes('EVENTS') || upperAction.includes('EVENTO'),
        'action-user': upperAction.includes('CUSTOMUSER') || upperAction.includes('USUARIO'),
        
        // ⭐ CLASES PARA ESTADOS DEL SISTEMA
        'action-error': upperAction.includes('ERROR'),
        'action-success': upperAction.includes('SUCCESS') || upperAction.includes('EXITOSO'),
        'action-warning': upperAction.includes('WARNING') || upperAction.includes('ADVERTENCIA'),
        
        // ⭐ CLASE POR DEFECTO
        'action-other': true
      }
    },

    getActionCategory(action) {
      if (!action) return 'Sistema'
      
      const upperAction = action.toUpperCase()
      
      // ⭐ CATEGORÍAS ESPECÍFICAS SEGÚN EL TIPO DE OPERACIÓN
      if (upperAction.includes('FACTOR')) return 'Gestión de Factores'
      if (upperAction.includes('CHARACTERISTICS') || upperAction.includes('CARACTERÍSTICA')) return 'Gestión de Características'
      if (upperAction.includes('INDICATOR') || upperAction.includes('INDICADOR')) return 'Gestión de Indicadores'
      if (upperAction.includes('EVENTS') || upperAction.includes('EVENTO')) return 'Gestión de Eventos'
      if (upperAction.includes('CUSTOMUSER') || upperAction.includes('USUARIO')) return 'Gestión de Usuarios'
      if (upperAction.includes('LOGIN') || upperAction.includes('LOGOUT')) return 'Autenticación'
      if (upperAction.includes('ENCUESTA') || upperAction.includes('SURVEY')) return 'Gestión de Encuestas'
      if (upperAction.includes('GRÁFICA') || upperAction.includes('CHART') || upperAction.includes('GENERAR')) return 'Generación de Reportes'
      if (upperAction.includes('SUBIR') || upperAction.includes('UPLOAD')) return 'Carga de Archivos'
      if (upperAction.includes('DESCARGAR') || upperAction.includes('DOWNLOAD')) return 'Descarga de Archivos'
      if (upperAction.includes('EXPORTAR') || upperAction.includes('EXPORT')) return 'Exportación'
      
      return 'Sistema'
    },

    // ⭐ MÉTODO ACTUALIZADO PARA OBTENER ROL DEL USUARIO
    getUserRole(user) {
      if (!user) return 'Desconocido'
      
      const roleMap = {
        admin: 'Administrador',
        consultor: 'Consultor',
        user: 'Usuario',
        auxiliar: 'Auxiliar'
      }
      
      return roleMap[user.tipo_user] || user.tipo_user || 'Usuario'
    },

    // ⭐ MÉTODO PARA OBTENER NOMBRE COMPLETO DEL USUARIO
    getUserDisplayName(user) {
      if (!user) return 'Usuario Desconocido'
      
      // Usar la propiedad 'name' del serializer que combina first_name y last_name
      if (user.name && user.name.trim()) {
        return user.name
      }
      
      // Fallback al username si no hay nombre completo
      return user.username || 'Usuario Desconocido'
    }
  },

  async mounted() {
    console.log('DashboardLogs mounted - Connecting to backend')
    await this.fetchLogs()
  }
}
</script>

<style lang="css" scoped>
@import '../../styles/dashboard_logs.css';
</style>