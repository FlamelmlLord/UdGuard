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
                      <div class="characteristic-status">
                        <span>Grado Cumplimiento: {{ characteristic.cumplimiento }}</span><br>
                        <span :style="{ backgroundColor: characteristic.grado_cumplimiento?.color || '#6b7280' }">
                          {{ characteristic.grado_cumplimiento?.descripcion || 'Sin evaluar' }}
                        </span>
                      </div>
                    </div>
                    
                    <div class="characteristic-actions">
                      <button 
                        @click="editarCaracteristica(characteristic)" 
                        class="icon-btn"
                        title="Editar característica"
                      >
                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                          <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
                          <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
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

    <!-- Modal para agregar/editar característica -->
    <div class="modal" v-if="mostrarModal" @click.self="cerrarModal">
      <div class="modal-content">
        <h3>{{ modoEdicion ? 'Editar Característica' : 'Agregar Característica' }}</h3>
        
        <input 
          v-model="nuevaCaracteristica.titulo" 
          placeholder="Título de la característica" 
          class="input"
          @keypress.enter="$event.target.blur()"
        />
        
        <textarea 
          v-model="nuevoDetalle" 
          placeholder="Agregar detalle descriptivo" 
          class="input textarea-input"
          @keypress.ctrl.enter="agregarDetalle"
        ></textarea>
        
        <button @click="agregarDetalle" class="add-detail-btn">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          Agregar Detalle
        </button>
        
        <ul class="feature-details" v-if="nuevaCaracteristica.detalles.length > 0">
          <li v-for="(detalle, index) in nuevaCaracteristica.detalles" :key="index">
            <span class="detail-text">{{ detalle }}</span>
            <button 
              @click="eliminarDetalle(index)"
              class="delete-detail-btn"
              title="Eliminar detalle"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"/>
                <line x1="6" y1="6" x2="18" y2="18"/>
              </svg>
            </button>
          </li>
        </ul>
        
        <div class="modal-footer">
          <button @click="guardarCaracteristica" class="add-btn primary">
            {{ modoEdicion ? '💾 Guardar Cambios' : '➕ Agregar' }}
          </button>
          <button @click="cerrarModal" class="add-btn">
            ✕ Cancelar
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
        detalles: []
      },
      nuevoDetalle: '',
      mostrarModal: false,
      modoEdicion: false,
      indiceEdicion: null
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

    // Método para agregar detalle
    agregarDetalle() {
      if (this.nuevoDetalle.trim() !== '') {
        this.nuevaCaracteristica.detalles.push(this.nuevoDetalle.trim());
        this.nuevoDetalle = '';
      }
    },

    // Método para eliminar detalle
    eliminarDetalle(index) {
      this.nuevaCaracteristica.detalles.splice(index, 1);
    },

    // Método para obtener características del API
    async fetchCaracteristica() {
      this.loading = true;
      this.error = null;
      
      try {
        const token = localStorage.getItem('access_token');
        console.log('Making API request with token');

        const response = await axios.get(`/factors/${this.factorId}/characteristics/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        
        console.log('API response received Characteristics:', response.data);
        this.characteristics = response.data;
        
      } catch (error) {
        console.error('Error fetching characteristics:', error);
        this.error = 'Error al cargar las características';
        
        // Si es error 401, el token expiró
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
      if (!this.nuevaCaracteristica.titulo || this.nuevaCaracteristica.detalles.length === 0) {
        alert('Por favor completa todos los campos requeridos');
        return;
      }

      try {
        const token = localStorage.getItem('access_token');
        
        if (this.modoEdicion && this.indiceEdicion !== null) {
          // Actualizar característica existente
          const characteristic = this.characteristics[this.indiceEdicion];
          const response = await axios.put(
            `/factors/${this.factorId}/characteristics/${characteristic.id}/`,
            {
              nombre: this.nuevaCaracteristica.titulo,
              descripcion: this.nuevaCaracteristica.detalles.join('. ')
            },
            {
              headers: {
                Authorization: `Bearer ${token}`
              }
            }
          );
          
          this.characteristics[this.indiceEdicion] = response.data;
        } else {
          // Crear nueva característica
          const response = await axios.post(
            `/factors/${this.factorId}/characteristics/`,
            {
              nombre: this.nuevaCaracteristica.titulo,
              descripcion: this.nuevaCaracteristica.detalles.join('. ')
            },
            {
              headers: {
                Authorization: `Bearer ${token}`
              }
            }
          );
          
          this.characteristics.push(response.data);
        }

        this.cerrarModal();
      } catch (error) {
        console.error('Error saving characteristic:', error);
        alert('Error al guardar la característica');
      }
    },

    // Método para editar característica
    editarCaracteristica(characteristic) {
      this.nuevaCaracteristica = {
        titulo: characteristic.nombre || characteristic.titulo,
        detalles: characteristic.descripcion ? [characteristic.descripcion] : []
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
      this.nuevaCaracteristica = { titulo: '', detalles: [] };
      this.nuevoDetalle = '';
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

<style scoped lang="css"> 
@import '../../styles/dashboard_characteristics.css'; 
</style>