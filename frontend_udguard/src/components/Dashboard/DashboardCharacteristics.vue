<template>
  <div class="dashboard-facts-container">
    <div class="dashboard-characteristics-container">
      <div class="dashboard-content">
        <div class="dashboard-header-factores">
          <h2 class="dashboard-title">{{ this.title }}</h2>
        </div>

        <div class="characteristics-container">
        <!-- Estado de carga -->
        <div v-if="loading" class="loading-state">
          <div class="loading-spinner"></div>
          <span style="margin-left: 16px;">Cargando características...</span>
        </div>

        <!-- Estado vacío -->
        <div v-else-if="characteristics.length === 0" class="empty-state">
          <h3>No hay características disponibles</h3>
          <p>Comienza agregando la primera característica para este factor.</p>
        </div>

        <!-- Lista de características con scroll -->
        <div v-else class="characteristics-grid">
            <div class="characteristics-list">
              <div
                v-for="characteristic in characteristics"
                :key="characteristic.id"
                class="characteristic-card"
                :class="getCharacteristicClass(characteristic)"
              >
                <!-- Icono de estado -->
                <div 
                  class="characteristic-status-icon"
                  :class="getStatusIconClass(characteristic)"
                >
                  {{ getStatusIcon(characteristic) }}
                </div>

                <!-- Contenido principal -->
                <div class="characteristic-content">
                  <div class="characteristic-card-header">
                    <div>
                      <h3 class="characteristic-title">{{ characteristic.nombre }}</h3>
                      
                      <!-- ⭐ SECCIÓN ACTUALIZADA CON TOTALES -->
                      <div class="characteristic-metrics">
                        <div class="metrics-row">
                          <span class="metric-label">Grado Cumplimiento:</span>
                          <span class="metric-value">{{ characteristic.cumplimiento || '0.0' }}</span>
                        </div>
                        
                        <div class="metrics-row">
                          <span class="metric-label">Total Metas:</span>
                          <span class="metric-value total-metas">{{ characteristic.total_metas || 0 }}</span>
                        </div>
                        
                        <div class="metrics-row">
                          <span class="metric-label">Total Puntajes:</span>
                          <span class="metric-value total-puntajes">{{ parseFloat(characteristic.total_puntajes || 0).toFixed(1) }}</span>
                        </div>
                        
                        <div class="metrics-row">
                          <span class="metric-label">Indicadores:</span>
                          <span class="metric-value indicadores-count">{{ characteristic.cantidad_indicadores || 0 }}</span>
                        </div>
                        
                        <!-- Badge de estado -->
                        <div class="status-badge-container">
                          <span 
                            class="status-badge"
                            :style="{ 
                              backgroundColor: characteristic.grado_cumplimiento?.color || '#6b7280',
                              color: 'white'
                            }"
                          >
                            {{ characteristic.grado_cumplimiento?.grado || 'N/A' }} - 
                            {{ characteristic.grado_cumplimiento?.descripcion || 'Sin evaluar' }}
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <div class="characteristic-actions">
                      <button 
                        @click="editarCaracteristica(characteristic)" 
                        class="icon-btn edit-btn"
                        title="Editar característica"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
                        </svg>
                      </button>
                      
                      <!-- ⭐ NUEVO BOTÓN ELIMINAR -->
                      <button 
                        @click="confirmarEliminarCaracteristica(characteristic)" 
                        class="icon-btn delete-btn"
                        title="Eliminar característica"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <polyline points="3,6 5,6 21,6"/>
                          <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
                          <line x1="10" y1="11" x2="10" y2="17"/>
                          <line x1="14" y1="11" x2="14" y2="17"/>
                        </svg>
                      </button>
                    </div>
                  </div>

                  <div class="characteristic-card-body">
                    {{ characteristic.descripcion }}
                  </div>
                </div>

                <!-- Botón de detalles -->
                <div class="feature-card-footer">
                  <button 
                    @click="mostrarDetalles(characteristic.id)" 
                    class="detail-button"
                    title="Ver detalles"
                  >
                    Ver
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <path d="M9 18l6-6-6-6"/>
                    </svg>
                  </button>
                </div>
              </div>
            </div>

            <!-- Botón agregar nueva característica - Fijo en la parte inferior -->
            <button class="add-characteristic-btn" @click="mostrarModal = true">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              Agregar Nueva Característica
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para agregar/editar característica simplificado -->
    <div class="modal" v-if="mostrarModal" @click.self="cerrarModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ modoEdicion ? 'Editar Característica' : 'Agregar Nueva Característica' }}</h3>
          <button @click="cerrarModal" class="close-btn" title="Cerrar">
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
              Nombre de la Característica *
            </label>
            <input 
              v-model="nuevaCaracteristica.titulo" 
              placeholder="Ej: Misión y Visión Institucional" 
              class="input"
              @keypress.enter="$event.target.blur()"
              maxlength="200"
            />
            <div class="input-counter">
              {{ nuevaCaracteristica.titulo.length }}/200 caracteres
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
              Descripción de la Característica *
            </label>
            <textarea 
              v-model="nuevaCaracteristica.descripcion" 
              placeholder="Describa detalladamente esta característica..." 
              class="input textarea-input"
              rows="6"
              maxlength="1000"
            ></textarea>
            <div class="input-counter">
              {{ (nuevaCaracteristica.descripcion || '').length }}/1000 caracteres
            </div>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="cerrarModal" class="cancel-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
            Cancelar
          </button>
          <button 
            @click="guardarCaracteristica" 
            class="save-btn primary"
            :disabled="!nuevaCaracteristica.titulo.trim() || !nuevaCaracteristica.descripcion?.trim()"
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/>
              <polyline points="17,21 17,13 7,13 7,21"/>
              <polyline points="7,3 7,8 15,8"/>
            </svg>
            {{ modoEdicion ? 'Guardar Cambios' : 'Crear Característica' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 🗑️ MODAL CONFIRMAR ELIMINACIÓN DE CARACTERÍSTICA -->
    <div class="modal" v-if="mostrarModalEliminar" @click.self="cerrarModalEliminar">
      <div class="modal-content delete-modal">
        <div class="modal-header delete-header">
          <h3>
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/>
              <line x1="15" y1="9" x2="9" y2="15"/>
              <line x1="9" y1="9" x2="15" y2="15"/>
            </svg>
            Confirmar Eliminación
          </h3>
          <button @click="cerrarModalEliminar" class="close-btn" title="Cerrar">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>
        
        <div class="modal-body">
          <div class="warning-content">
            <div class="warning-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"/>
                <line x1="12" y1="8" x2="12" y2="12"/>
                <line x1="12" y1="16" x2="12.01" y2="16"/>
              </svg>
            </div>
            
            <h4>¿Estás seguro?</h4>
            
            <p class="warning-text">
              ¿Deseas eliminar la característica 
              <strong>"{{ caracteristicaAEliminar?.nombre }}"</strong>?
            </p>
            
            <div v-if="caracteristicaAEliminar?.cantidad_indicadores > 0" class="danger-warning">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
                <line x1="12" y1="9" x2="12" y2="13"/>
                <line x1="12" y1="17" x2="12.01" y2="17"/>
              </svg>
              <span>
                Esta característica tiene <strong>{{ caracteristicaAEliminar?.cantidad_indicadores }} indicador(es)</strong> 
                que también serán eliminados permanentemente.
              </span>
            </div>
            
            <p class="warning-final">
              <strong>Esta acción no se puede deshacer.</strong>
            </p>
          </div>
        </div>
        
        <div class="modal-footer">
          <button @click="cerrarModalEliminar" class="cancel-btn">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
            Cancelar
          </button>
          <button @click="eliminarCaracteristica" class="delete-btn-confirm">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="3,6 5,6 21,6"/>
              <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
              <line x1="10" y1="11" x2="10" y2="17"/>
              <line x1="14" y1="11" x2="14" y2="17"/>
            </svg>
            Eliminar Permanentemente
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../../plugins/Axios'

export default {
  name: 'DashboardCharacteristics',
  props: {
    factorId: {
      type: [String, Number],
      required: true
    }
  },

  data () {
    return {
      characteristics: [],
      title: "",
      loading: false,
      error: null,
      nuevaCaracteristica: {
        titulo: '',
        descripcion: ''
      },
      mostrarModal: false,
      modoEdicion: false,
      indiceEdicion: null,
      
      // ⭐ NUEVAS VARIABLES PARA ELIMINACIÓN
      mostrarModalEliminar: false,
      caracteristicaAEliminar: null
    }
  },

  computed: {
    // Helper para formatear números a 1 decimal
    formatDecimal() {
      return (value) => {
        return parseFloat(value || 0).toFixed(1)
      }
    }
  },

  methods: {
    // Método para obtener la clase CSS según el estado
    getCharacteristicClass(characteristic) {
      if (!characteristic.grado_cumplimiento && !characteristic.cumplimiento) return 'gris';
      
      const cumplimiento = parseFloat(characteristic.cumplimiento) || 0;
      const descripcion = characteristic.grado_cumplimiento?.descripcion?.toLowerCase() || '';
      
      // Lógica especial para C1 con cumplimiento 3.7 (verde amarilloso)
      if (cumplimiento >= 3.5 && cumplimiento < 4.0) {
        return 'verde-amarilloso';
      }
      
      if (cumplimiento >= 4.0 || descripcion.includes('alto') || descripcion.includes('cumple')) {
        return 'verde';
      } else if ((cumplimiento >= 3.0 && cumplimiento < 3.5) || descripcion.includes('medio') || descripcion.includes('parcial')) {
        return 'amarillo';
      } else if (cumplimiento < 3.0 || descripcion.includes('bajo') || descripcion.includes('no cumple')) {
        return 'rojo';
      }
      
      return 'gris';
    },

    // Método para obtener la clase del icono de estado
    getStatusIconClass(characteristic) {
      return this.getCharacteristicClass(characteristic);
    },

    // Método para obtener el icono según el estado
    getStatusIcon(characteristic) {
      const clase = this.getCharacteristicClass(characteristic);
      
      switch (clase) {
        case 'verde':
          return '✓';
        case 'verde-amarilloso':
          return '✓';
        case 'amarillo':
          return '⚠';
        case 'rojo':
          return '✕';
        case 'gris':
        default:
          return '?';
      }
    },

    // Método para obtener características del API
    async fetchCaracteristica() {
      this.loading = true;
      this.error = null;
      
      try {
        const token = localStorage.getItem('access_token');
        console.log('Fetching characteristics for factor:', this.factorId);

        const response = await axios.get(`/factors/${this.factorId}/characteristics/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        
        console.log('Characteristics updated after operation:', response.data);
        this.characteristics = response.data;
        
        // ⭐ LOG PARA VERIFICAR DATOS DESPUÉS DE ELIMINACIÓN
        console.log('Características actuales:', this.characteristics.map(c => ({
          id: c.id,
          nombre: c.nombre,
          indicadores: c.cantidad_indicadores,
          cumplimiento: c.cumplimiento
        })));
        
      } catch (error) {
        console.error('Error fetching characteristics:', error);
        this.error = 'Error al cargar las características';
        
        if (error.response?.status === 401) {
          console.log('Token expired, clearing auth data');
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user_data');
          this.$router.push('/login');
        }
      } finally {
        this.loading = false;
      }
    },

    // Método para guardar característica
    async guardarCaracteristica() {
      if (!this.nuevaCaracteristica.titulo.trim()) {
        this.$swal({
          title: 'Error',
          text: 'El nombre de la característica es requerido.',
          icon: 'warning',
          confirmButtonText: 'Continuar'
        });
        return;
      }

      if (!this.nuevaCaracteristica.descripcion?.trim()) {
        this.$swal({
          title: 'Error',
          text: 'La descripción de la característica es requerida.',
          icon: 'warning',
          confirmButtonText: 'Continuar'
        });
        return;
      }

      try {
        const token = localStorage.getItem('access_token');
        
        if (this.modoEdicion && this.indiceEdicion !== null) {
          // ⭐ ACTUALIZAR CARACTERÍSTICA EXISTENTE
          const characteristic = this.characteristics[this.indiceEdicion];
          const response = await axios.patch(
            `/characteristics/${characteristic.id}/`,
            {
              nombre: this.nuevaCaracteristica.titulo.trim(),
              descripcion: this.nuevaCaracteristica.descripcion.trim() // ⭐ Usar descripcion directamente
            },
            {
              headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
              }
            }
          );
          
          console.log('Characteristic updated:', response.data);

          // ⭐ REFRESCAR DATOS DEL BACKEND DESPUÉS DE ACTUALIZAR
          await this.fetchCaracteristica();

          this.$swal({
            title: '¡Característica Actualizada!',
            text: 'La característica se ha actualizado correctamente.',
            icon: 'success',
            confirmButtonText: 'Continuar'
          });
          
        } else {
          // ⭐ CREAR NUEVA CARACTERÍSTICA
          const response = await axios.post(
            `/factors/${this.factorId}/characteristics/`,
            {
              nombre: this.nuevaCaracteristica.titulo.trim(),
              descripcion: this.nuevaCaracteristica.descripcion.trim() // ⭐ Usar descripcion directamente
            },
            {
              headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json'
              }
            }
          );
          
          console.log('New characteristic created:', response.data);

          // ⭐ REFRESCAR DATOS DEL BACKEND DESPUÉS DE CREAR
          await this.fetchCaracteristica();

          this.$swal({
            title: '¡Característica Creada!',
            text: 'La nueva característica se ha agregado correctamente.',
            icon: 'success',
            confirmButtonText: 'Continuar'
          });
        }

        this.cerrarModal();

      } catch (error) {
        console.error('Error saving characteristic:', error);
        
        let errorMessage = 'Error al guardar la característica.';
        
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
    },

    // Método para editar característica
    editarCaracteristica(characteristic) {
      this.nuevaCaracteristica = {
        titulo: characteristic.nombre || characteristic.titulo,
        descripcion: characteristic.descripcion || '' // ⭐ Usar descripcion directamente
      };
      this.modoEdicion = true;
      this.indiceEdicion = this.characteristics.findIndex(c => c.id === characteristic.id);
      this.mostrarModal = true;
    },

    // Método para cerrar modal
    cerrarModal() {
      this.mostrarModal = false;
      this.modoEdicion = false;
      this.indiceEdicion = null;
      this.nuevaCaracteristica = { 
        titulo: '', 
        descripcion: '' // ⭐ Cambiar detalles por descripcion
      };
    },

    // Método para mostrar detalles
    mostrarDetalles(caracteristicaId) {
      console.log('Navegando a detalles:', caracteristicaId);
      this.$router.push({
        name: 'DashboardIndicators',
        params: { 
          caracteristicaId: caracteristicaId,
          factorId: this.factorId
        }
      });
    },

    // Método para confirmar eliminación de característica
    confirmarEliminarCaracteristica(characteristic) {
      this.caracteristicaAEliminar = characteristic;
      this.mostrarModalEliminar = true;
      
      console.log('Preparando eliminación de característica:', {
        id: characteristic.id,
        nombre: characteristic.nombre,
        indicadores: characteristic.cantidad_indicadores
      });
    },

    // Método para cerrar modal de eliminación
    cerrarModalEliminar() {
      this.mostrarModalEliminar = false;
      this.caracteristicaAEliminar = null;
    },

    // Método para eliminar característica
    async eliminarCaracteristica() {
      if (!this.caracteristicaAEliminar) {
        return;
      }
      
      try {
        const token = localStorage.getItem('access_token');
        const characteristicId = this.caracteristicaAEliminar.id;
        
        console.log('Eliminando característica con ID:', characteristicId);

        // ⭐ ELIMINAR DEL BACKEND
        await axios.delete(
          `/characteristics/${characteristicId}/`,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );

        console.log('Characteristic deleted from server successfully');

        // ⭐ REFRESCAR DATOS DEL BACKEND DESPUÉS DE ELIMINAR
        await this.fetchCaracteristica();
        
        this.$swal({
          title: '¡Característica Eliminada!',
          text: `La característica "${this.caracteristicaAEliminar.nombre}" se ha eliminado correctamente.`,
          icon: 'success',
          confirmButtonText: 'Continuar'
        });

        this.cerrarModalEliminar();
        
      } catch (error) {
        console.error('Error deleting characteristic:', error);
        
        let errorMessage = 'Error al eliminar la característica.';
        
        if (error.response?.status === 401) {
          errorMessage = 'Sesión expirada. Por favor, inicia sesión nuevamente.';
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
          localStorage.removeItem('user_data');
          this.$router.push('/login');
        } else if (error.response?.status === 403) {
          errorMessage = 'No tienes permisos para realizar esta acción.';
        } else if (error.response?.status === 404) {
          errorMessage = 'La característica no fue encontrada.';
        } else if (error.response?.status === 409) {
          errorMessage = 'No se puede eliminar la característica porque tiene dependencias.';
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

  created() {
    console.log('Factor ID:', this.factorId);
  },

  async mounted() {
    this.title = this.$route.params.titulo || `Características del Factor ${this.factorId}`;
    console.log('Factor ID from route:', this.$route.params.factorId);
    await this.fetchCaracteristica();
  }
}
</script>

<style lang="css" scoped>
@import '../../styles/dashboard_characteristics.css';
</style>