<template>
  <div class="dashboard-characteristics-container">
    <div class="dashboard-content">
      <div class="dashboard-title-container">
        <h2 class="dashboard-title">{{this.title}}</h2>
      </div>

      <div class="characteristics-container">
        <div class="characteristics-grid">
          <div
            v-for="characteristic in characteristics"
            :key="characteristic.id"
            class="characteristic-card"
          >
            <div class="characteristic-card-header">
              <h3 class="characteristic-title">{{ characteristic.nombre }}</h3>
              <div class="characteristic-actions">
                <button @click="editarCaracteristica(characteristic)" class="icon-btn">
                  ✏️
                </button>
              </div>
                <div class="characteristic-status">
                  <span :style="{ fontWeight: 'bold' }">Grado Cumplimiento: {{ characteristic.cumplimiento }}</span><br>
                <span :style="{ backgroundColor: characteristic.grado_cumplimiento.color }">
                  {{ characteristic.grado_cumplimiento.descripcion }}
                </span>
              </div> 
            </div>

            <div class="characteristic-card-body">
              {{characteristic.descripcion}}
            </div>

            <div class="feature-card-footer">
              <button @click="mostrarDetalles(characteristic.id)" class="detail-button">
                Detalles
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M9 18l6-6-6-6"/>
                </svg>
              </button>
            </div>
          </div>

          <button class="icon-add" @click="mostrarModal = true">+</button>
        </div>
      </div>
    </div>

    <!-- Modal para agregar/editar característica -->
    <div class="modal" v-if="mostrarModal">
      <div class="modal-content">
        <h3>{{ modoEdicion ? 'Editar Característica' : 'Agregar Característica' }}</h3>
        <input v-model="nuevaCaracteristica.titulo" placeholder="Título de la característica" class="input" />
        <textarea v-model="nuevoDetalle" placeholder="Agregar detalle" class="input"></textarea>
        <button @click="agregarDetalle" class="add-btn">Agregar Detalle</button>
        <ul class="feature-details">
          <li v-for="(detalle, index) in nuevaCaracteristica.detalles" :key="index">{{ detalle }}</li>
        </ul>
        <div class="modal-footer">
          <button @click="guardarCaracteristica" class="add-btn primary">{{ modoEdicion ? 'Guardar Cambios' : 'Agregar' }}</button>
          <button @click="cerrarModal" class="add-btn">Cancelar</button>
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
      title:"",
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
    getFeatureClass (estado) {
      return {
        verde: 'feature-card--verde',
        amarillo: 'feature-card--amarillo',
        rojo: 'feature-card--rojo'
      }[estado]
    },
    agregarDetalle () {
      if (this.nuevoDetalle.trim() !== '') {
        this.nuevaCaracteristica.detalles.push(this.nuevoDetalle.trim())
        this.nuevoDetalle = ''
      }
    },
    async fetchCaracteristica () {
      
      this.loading = true
      this.error = null
      
      try {
        const token = localStorage.getItem('access_token')
        console.log('Making API request with token')

        const response = await axios.get(`/factors/${this.factorId}/characteristics/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })
        
        console.log('API response received Characteristics:', response.data)
        this.characteristics = response.data
        // Procesar datos...
        
      } catch (error) {
        console.error('Error fetching factors:', error)
        
        // Si es error 401, el token expiró
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
    guardarCaracteristica () {
      if (!this.nuevaCaracteristica.titulo || this.nuevaCaracteristica.detalles.length === 0) return

      if (this.modoEdicion && this.indiceEdicion !== null) {
        this.characteristics[this.indiceEdicion].titulo = this.nuevaCaracteristica.titulo
        this.characteristics[this.indiceEdicion].detalles = [...this.nuevaCaracteristica.detalles]
      } else {
        this.characteristics.push({
          id: Date.now(),
          titulo: this.nuevaCaracteristica.titulo,
          estado: 'verde',
          estadoTexto: 'Cumplimiento',
          detalles: [...this.nuevaCaracteristica.detalles]
        })
      }

      this.cerrarModal()
    },
    editarCaracteristica (feature) {
      this.nuevaCaracteristica = {
        titulo: feature.titulo,
        detalles: [...feature.detalles]
      }
      this.modoEdicion = true
      this.indiceEdicion = this.characteristics.findIndex(f => f.id === feature.id)
      this.mostrarModal = true
    },
    cerrarModal () {
      this.mostrarModal = false
      this.modoEdicion = false
      this.indiceEdicion = null
      this.nuevaCaracteristica = { titulo: '', detalles: [] }
      this.nuevoDetalle = ''
    },
    mostrarDetalles (caracteristicaId) {
      console.log( caracteristicaId)
            this.$router.push({
        name: 'DashboardIndicators',
        params: { caracteristicaId: caracteristicaId }
      })
    }
  },
  created () {
    console.log('Factor ID:', this.factorId)
  },
  async mounted() {

    this.title = this.$route.params.titulo
    console.log(this.$route.params.factorId)
    this.fetchCaracteristica()
  }
}
</script>

<style scoped lang="css"> @import '../../styles/dashboard_characteristics.css'; </style>
