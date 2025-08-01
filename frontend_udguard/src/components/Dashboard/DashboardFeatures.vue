<template>
  <div class="dashboard-features-container">
    <div class="dashboard-content">
      <div class="dashboard-title-container">
        <h2 class="dashboard-title">#1 Misión, Proyecto Institucional y de Programa</h2>
      </div>

      <div class="features-container">
        <div class="features-grid">
          <div
            v-for="feature in features"
            :key="feature.id"
            class="feature-card"
            :class="getFeatureClass(feature.estado)"
          >
            <div class="feature-card-header">
              <h3 class="feature-title">{{ feature.titulo }}</h3>
              <div class="feature-actions">
                <button @click="editarCaracteristica(feature)" class="icon-btn">
                  ✏️
                </button>
              </div>
              <div class="feature-status">
                <span :class="['status-indicator', feature.estado]">
                  {{ feature.estadoTexto }}
                </span>
              </div>
            </div>

            <div class="feature-card-body">
              <ul class="feature-details">
                <li v-for="detalle in feature.detalles" :key="detalle">
                  {{ detalle }}
                </li>
              </ul>
            </div>

            <div class="feature-card-footer">
              <button class="detail-button">
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
export default {
  name: 'DashboardFeatures',
  props: {
    factorId: {
      type: [String, Number],
      required: true
    }
  },
  data () {
    return {
      features: [
        {
          id: 1,
          titulo: 'C1: Misión y Proyecto Institucional',
          estado: 'verde',
          estadoTexto: 'Cumplimiento',
          detalles: [
            'Coherencia con la misión institucional',
            'Alineación con objetivos del programa',
            'Documentación actualizada y clara'
          ]
        },
        {
          id: 2,
          titulo: 'C2: Proyecto Educativo del Programa',
          estado: 'verde',
          estadoTexto: 'Cumplimiento',
          detalles: [
            'Definición clara de objetivos',
            'Plan de estudios coherente',
            'Metodologías de enseñanza innovadoras'
          ]
        },
        {
          id: 3,
          titulo: 'C3: Relevancia Académica y Pertinencia',
          estado: 'verde',
          estadoTexto: 'Cumplimiento',
          detalles: [
            'Impacto del programa en el contexto',
            'Líneas de investigación relevantes',
            'Articulación con necesidades sociales'
          ]
        }
      ],
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
    guardarCaracteristica () {
      if (!this.nuevaCaracteristica.titulo || this.nuevaCaracteristica.detalles.length === 0) return

      if (this.modoEdicion && this.indiceEdicion !== null) {
        this.features[this.indiceEdicion].titulo = this.nuevaCaracteristica.titulo
        this.features[this.indiceEdicion].detalles = [...this.nuevaCaracteristica.detalles]
      } else {
        this.features.push({
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
      this.indiceEdicion = this.features.findIndex(f => f.id === feature.id)
      this.mostrarModal = true
    },
    cerrarModal () {
      this.mostrarModal = false
      this.modoEdicion = false
      this.indiceEdicion = null
      this.nuevaCaracteristica = { titulo: '', detalles: [] }
      this.nuevoDetalle = ''
    }
  },
  created () {
    console.log('Factor ID:', this.factorId)
  }
}
</script>

<style scoped lang="css"> @import '../../styles/dashboard_features.css'; </style>
