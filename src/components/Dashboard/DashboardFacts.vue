<template>
    <div class="factores-container">
      <h2 class="section-title">Factores</h2>
      <div class="factores-grid">
        <div
          v-for="factor in factores"
          :key="factor.id"
          class="factor-card"
          :class="getFactorClass(factor.estado)"
          @mouseover="hover = factor.id"
          @mouseleave="hover = null"
        >
          <h3 class="factor-title">{{ factor.titulo }}</h3>
          <div class="factor-status">
            <span :class="['status-indicator', factor.estado]">
              {{ factor.estadoTexto }}
            </span>
          </div>
          <ul class="factor-details">
            <li v-for="alerta in factor.alertas" :key="alerta">
              {{ alerta }}
            </li>
          </ul>
          <button class="view-button" @click="verDetalles(factor.id)">Ver</button>
        </div>
      </div>
    </div>
  </template>

<script>
export default {
  name: 'FactoresView',
  data () {
    return {
      factores: [
        {
          id: 1,
          titulo: '#1 Misión, Proyecto Institucional y de Programa',
          estado: 'verde',
          estadoTexto: 'Cumplimiento',
          alertas: [
            'C1: Misión y Proyecto Institucional',
            'C2: Proyecto Educativo del Programa',
            'C3: Relevancia Académica y Pertinencia'
          ]
        },
        {
          id: 2,
          titulo: '#2 Estudiantes',
          estado: 'amarillo',
          estadoTexto: 'En Proceso',
          alertas: ['Número de Característica']
        },
        {
          id: 3,
          titulo: '#3 Profesores',
          estado: 'verde',
          estadoTexto: 'Cumplimiento',
          alertas: ['Número de Característica']
        },
        {
          id: 4,
          titulo: '#4 Procesos Académicos',
          estado: 'rojo',
          estadoTexto: 'Pendiente',
          alertas: ['Número de Característica']
        }
      ],
      hover: null
    }
  },
  methods: {
    getFactorClass (estado) {
      return {
        verde: 'factor-card--verde',
        amarillo: 'factor-card--amarillo',
        rojo: 'factor-card--rojo'
      }[estado]
    },
    verDetalles (id) {
      alert(`Ver detalles del factor ${id}`)
    }
  }
}
</script>

  <style scoped>
  .factores-container {
    padding: 2rem;
  }

  .section-title {
    text-align: center;
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    color: var(--primary-color);
  }

  .factores-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
  }

  .factor-card {
    background-color: white;
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
  }

  .factor-card:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }

  .factor-card--verde {
    border-left: 5px solid #4caf50;
  }

  .factor-card--amarillo {
    border-left: 5px solid #ffeb3b;
  }

  .factor-card--rojo {
    border-left: 5px solid #f44336;
  }

  .factor-title {
    font-size: 1.2rem;
    margin-bottom: 1rem;
    color: var(--primary-color);
  }

  .factor-status {
    margin-bottom: 1rem;
  }

  .status-indicator {
    font-weight: bold;
    padding: 0.3rem 0.5rem;
    border-radius: 4px;
    display: inline-block;
  }

  .status-indicator.verde {
    background-color: #e8f5e9;
    color: #4caf50;
  }

  .status-indicator.amarillo {
    background-color: #fffde7;
    color: #ffeb3b;
  }

  .status-indicator.rojo {
    background-color: #ffebee;
    color: #f44336;
  }

  .factor-details {
    list-style: none;
    padding: 0;
    margin: 0 0 1rem 0;
  }

  .factor-details li {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 0.3rem;
  }

  .view-button {
    background-color: var(--primary-color);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }

  .view-button:hover {
    background-color: var(--primary-color-dark);
  }
  </style>
