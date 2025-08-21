<template>
  <div class="dashboard-container">
    <!-- Header Section -->
    <div class="dashboard-header">
      <h1 class="dashboard-title">
        Bienvenido, {{ userInfo.name}} a UDguard
      </h1>
      <p class="dashboard-subtitle">
        Aplicación de la Maestria en la Gestión y Seguridad de la Información
      </p>
    </div>

    <!-- Carousel Section -->
    <div class="carousel-section">
      <div class="carousel-container">
        <div class="carousel-wrapper" ref="carouselWrapper">
          <div
            v-for="(slide, index) in slides"
            :key="index"
            class="carousel-slide"
            :class="{ active: currentSlide === index }"
          >
            <img
              :src="slide.image"
              :alt="slide.title"
              class="carousel-image"
            />
            <div class="carousel-content">
              <h3 class="carousel-title">{{ slide.title }}</h3>
              <p class="carousel-description">{{ slide.description }}</p>
            </div>
          </div>
        </div>

        <!-- Navigation Arrows -->
        <button
          class="carousel-nav prev"
          @click="prevSlide"
          :disabled="slides.length <= 1"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M15 18l-6-6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>

        <button
          class="carousel-nav next"
          @click="nextSlide"
          :disabled="slides.length <= 1"
        >
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M9 18l6-6-6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>

        <!-- Dots Indicator -->
        <div class="carousel-dots">
          <button
            v-for="(slide, index) in slides"
            :key="index"
            class="carousel-dot"
            :class="{ active: currentSlide === index }"
            @click="goToSlide(index)"
          ></button>
        </div>
      </div>
    </div>

    <!-- Calendar Section -->
    <div class="calendar-section">
      <div class="calendar-header">
        <h2 class="calendar-title">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" class="calendar-icon">
            <rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke="currentColor" stroke-width="2"/>
            <line x1="16" y1="2" x2="16" y2="6" stroke="currentColor" stroke-width="2"/>
            <line x1="8" y1="2" x2="8" y2="6" stroke="currentColor" stroke-width="2"/>
            <line x1="3" y1="10" x2="21" y2="10" stroke="currentColor" stroke-width="2"/>
          </svg>
          Calendario de Actividades
        </h2>

        <!-- Admin Controls - Solo visible para administradores -->
        <div v-if="isAdmin" class="calendar-controls">
          <button
            class="btn btn-primary"
            @click="showCreateEventModal = true"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <line x1="12" y1="5" x2="12" y2="19" stroke="currentColor" stroke-width="2"/>
              <line x1="5" y1="12" x2="19" y2="12" stroke="currentColor" stroke-width="2"/>
            </svg>
            Crear Evento
          </button>

          <button
            class="btn btn-secondary"
            @click="showManageEventsModal = true"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" stroke="currentColor" stroke-width="2"/>
            </svg>
            Gestionar
          </button>
        </div>
      </div>

      <div class="calendar-container">
        <FullCalendar
          ref="fullCalendar"
          :options="calendarOptions"
          class="custom-calendar"
        />
      </div>
    </div>

    <!-- Create Event Modal -->
    <div v-if="showCreateEventModal" class="modal-overlay" @click="closeCreateEventModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Crear Nuevo Evento</h3>
          <button class="modal-close" @click="closeCreateEventModal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2"/>
              <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2"/>
            </svg>
          </button>
        </div>

        <form @submit.prevent="createEvent" class="event-form">
          <div class="form-group">
            <label for="eventTitle">Título del Evento</label>
            <input
              id="eventTitle"
              v-model="newEvent.title"
              type="text"
              required
              placeholder="Ingrese el título del evento"
            />
          </div>

          <div class="form-group">
            <label for="eventDescription">Descripción</label>
            <textarea
              id="eventDescription"
              v-model="newEvent.description"
              placeholder="Descripción del evento"
              rows="3"
            ></textarea>
          </div>

          <div class="form-group">
            <label for="eventStart">Fecha de Inicio</label>
            <input
              id="eventStart"
              v-model="newEvent.start"
              type="datetime-local"
              required
            />
          </div>

          <div class="form-group">
            <label for="eventEnd">Fecha de Fin</label>
            <input
              id="eventEnd"
              v-model="newEvent.end"
              type="datetime-local"
            />
          </div>

          <div class="form-group">
            <label for="eventType">Tipo de Evento</label>
            <select id="eventType" v-model="newEvent.type" required>
              <option value="">Seleccione un tipo</option>
              <option value="meeting">Reunión</option>
              <option value="deadline">Fecha Límite</option>
              <option value="event">Evento Especial</option>
              <option value="holiday">Feriado</option>
              <option value="exam">Examen</option>
              <option value="presentation">Presentación</option>
            </select>
          </div>

          <div class="modal-actions">
            <button type="button" class="btn btn-secondary" @click="closeCreateEventModal">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <span v-if="loading">Creando...</span>
              <span v-else>Crear Evento</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Manage Events Modal -->
    <div v-if="showManageEventsModal" class="modal-overlay" @click="closeManageEventsModal">
      <div class="modal-content modal-wide" @click.stop>
        <div class="modal-header">
          <h3>Gestionar Eventos</h3>
          <button class="modal-close" @click="closeManageEventsModal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2"/>
              <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2"/>
            </svg>
          </button>
        </div>

        <div class="events-list">
          <div v-if="events.length === 0" class="no-events">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" class="no-events-icon">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke="currentColor" stroke-width="2"/>
              <line x1="16" y1="2" x2="16" y2="6" stroke="currentColor" stroke-width="2"/>
              <line x1="8" y1="2" x2="8" y2="6" stroke="currentColor" stroke-width="2"/>
              <line x1="3" y1="10" x2="21" y2="10" stroke="currentColor" stroke-width="2"/>
              <line x1="12" y1="14" x2="12" y2="18" stroke="currentColor" stroke-width="2"/>
              <line x1="10" y1="16" x2="14" y2="16" stroke="currentColor" stroke-width="2"/>
            </svg>
            <p>No hay eventos creados aún</p>
          </div>

          <div v-else class="events-table">
            <div class="event-item" v-for="event in events" :key="event.id">
              <div class="event-info">
                <div class="event-title-row">
                  <div class="event-type-indicator" :style="{ backgroundColor: event.color }"></div>
                  <h4 class="event-title">{{ event.title }}</h4>
                  <span class="event-type-badge" :class="getTypeBadgeClass(event.extendedProps?.type)">
                    {{ getTypeLabel(event.extendedProps?.type) }}
                  </span>
                </div>
                <p class="event-description" v-if="event.extendedProps?.description">
                  {{ event.extendedProps.description }}
                </p>
                <div class="event-dates">
                  <span class="event-date">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                      <polyline points="12,6 12,12 16,14" stroke="currentColor" stroke-width="2"/>
                    </svg>
                    {{ formatEventDate(event.start) }}
                    <span v-if="event.end"> - {{ formatEventDate(event.end) }}</span>
                  </span>
                </div>
              </div>

              <div class="event-actions">
                <button
                  class="btn-icon btn-edit"
                  @click="openEditEvent(event)"
                  title="Editar evento"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" stroke-width="2"/>
                    <path d="M18.5 2.5a2.12 2.12 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="2"/>
                  </svg>
                </button>

                <button
                  class="btn-icon btn-delete"
                  @click="confirmDeleteEvent(event)"
                  title="Eliminar evento"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                    <polyline points="3,6 5,6 21,6" stroke="currentColor" stroke-width="2"/>
                    <path d="M19,6v14a2,2,0,0,1-2,2H7a2,2,0,0,1-2-2V6M8,6V4a2,2,0,0,1,2-2h4a2,2,0,0,1,2,2V6" stroke="currentColor" stroke-width="2"/>
                    <line x1="10" y1="11" x2="10" y2="17" stroke="currentColor" stroke-width="2"/>
                    <line x1="14" y1="11" x2="14" y2="17" stroke="currentColor" stroke-width="2"/>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Event Modal -->
    <div v-if="showEditEventModal" class="modal-overlay" @click="closeEditEventModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>Editar Evento</h3>
          <button class="modal-close" @click="closeEditEventModal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2"/>
              <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2"/>
            </svg>
          </button>
        </div>

        <form @submit.prevent="updateEvent" class="event-form">
          <div class="form-group">
            <label for="editEventTitle">Título del Evento</label>
            <input
              id="editEventTitle"
              v-model="editingEvent.title"
              type="text"
              required
              placeholder="Ingrese el título del evento"
            />
          </div>

          <div class="form-group">
            <label for="editEventDescription">Descripción</label>
            <textarea
              id="editEventDescription"
              v-model="editingEvent.description"
              placeholder="Descripción del evento"
              rows="3"
            ></textarea>
          </div>

          <div class="form-group">
            <label for="editEventStart">Fecha de Inicio</label>
            <input
              id="editEventStart"
              v-model="editingEvent.start"
              type="datetime-local"
              required
            />
          </div>

          <div class="form-group">
            <label for="editEventEnd">Fecha de Fin</label>
            <input
              id="editEventEnd"
              v-model="editingEvent.end"
              type="datetime-local"
            />
          </div>

          <div class="form-group">
            <label for="editEventType">Tipo de Evento</label>
            <select id="editEventType" v-model="editingEvent.type" required>
              <option value="">Seleccione un tipo</option>
              <option value="meeting">Reunión</option>
              <option value="deadline">Fecha Límite</option>
              <option value="event">Evento Especial</option>
              <option value="holiday">Feriado</option>
              <option value="exam">Examen</option>
              <option value="presentation">Presentación</option>
            </select>
          </div>

          <div class="modal-actions">
            <button type="button" class="btn btn-secondary" @click="closeEditEventModal">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <span v-if="loading">Actualizando...</span>
              <span v-else>Actualizar Evento</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Confirmation Delete Modal -->
    <div v-if="showDeleteConfirmModal" class="modal-overlay" @click="closeDeleteConfirmModal">
      <div class="modal-content modal-small" @click.stop>
        <div class="modal-header">
          <h3>Confirmar Eliminación</h3>
          <button class="modal-close" @click="closeDeleteConfirmModal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2"/>
              <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2"/>
            </svg>
          </button>
        </div>

        <div class="delete-confirm-content">
          <div class="delete-icon">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none">
              <circle cx="12" cy="12" r="10" stroke="#EF4444" stroke-width="2"/>
              <line x1="15" y1="9" x2="9" y2="15" stroke="#EF4444" stroke-width="2"/>
              <line x1="9" y1="9" x2="15" y2="15" stroke="#EF4444" stroke-width="2"/>
            </svg>
          </div>
          <h4>¿Estás seguro?</h4>
          <p>
            ¿Deseas eliminar el evento "<strong>{{ eventToDelete?.title }}</strong>"?
            <br>Esta acción no se puede deshacer.
          </p>
        </div>

        <div class="modal-actions">
          <button type="button" class="btn btn-secondary" @click="closeDeleteConfirmModal">
            Cancelar
          </button>
          <button type="button" class="btn btn-danger" @click="deleteEvent" :disabled="loading">
            <span v-if="loading">Eliminando...</span>
            <span v-else>Eliminar Evento</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Success Toast -->
    <div v-if="showSuccessToast" class="toast toast-success" :class="{ 'toast-show': showSuccessToast }">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" stroke="currentColor" stroke-width="2"/>
        <polyline points="22,4 12,14.01 9,11.01" stroke="currentColor" stroke-width="2"/>
      </svg>
      <span>{{ toastMessage }}</span>
    </div>

    <!-- Error Toast -->
    <div v-if="showErrorToast" class="toast toast-error" :class="{ 'toast-show': showErrorToast }">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
        <line x1="15" y1="9" x2="9" y2="15" stroke="currentColor" stroke-width="2"/>
        <line x1="9" y1="9" x2="15" y2="15" stroke="currentColor" stroke-width="2"/>
      </svg>
      <span>{{ toastMessage }}</span>
    </div>

    <!-- Loading Overlay -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner">
        <div class="spinner"></div>
        <p>Procesando...</p>
      </div>
    </div>
  </div>
</template>

<script>
import FullCalendar from '@fullcalendar/vue'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import esLocale from '@fullcalendar/core/locales/es'

export default {
  name: 'DashboardHome',
  components: {
    FullCalendar
  },

  data () {
    return {
      loading: false,
      currentSlide: 0,
      autoSlideInterval: null,
      showCreateEventModal: false,
      showManageEventsModal: false,
      showEditEventModal: false,
      showDeleteConfirmModal: false,
      showSuccessToast: false,
      showErrorToast: false,
      toastMessage: '',
      eventToDelete: null,

      // User info - esto debería venir del store/auth
      userInfo: {
        name: 'Admin Usuario',
        role: 'ADMIN' // CAMBIAR !!! IMPORTANTE
      },

      // Slides del carrusel
      slides: [
        {
          id: 1,
          title: 'Maestría en Gestión y Seguridad de la Información',
          description: 'Formando profesionales expertos en ciberseguridad y gestión de información.',
          image: 'https://images.unsplash.com/photo-1551434678-e076c223a692?w=800&h=400&fit=crop'
        },
        {
          id: 2,
          title: 'Últimas Noticias Académicas',
          description: 'Mantente al día con las últimas novedades de tu programa académico.',
          image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=400&fit=crop'
        },
        {
          id: 3,
          title: 'Eventos y Conferencias',
          description: 'Participa en nuestros eventos especiales y conferencias magistrales.',
          image: 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=800&h=400&fit=crop'
        }
      ],

      // Nuevo evento
      newEvent: {
        title: '',
        description: '',
        start: '',
        end: '',
        type: ''
      },

      // Evento en edición
      editingEvent: {
        id: null,
        title: '',
        description: '',
        start: '',
        end: '',
        type: ''
      },

      // Array de eventos
      events: [],

      // Opciones del calendario
      calendarOptions: {
        plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
        locale: esLocale,
        initialView: 'dayGridMonth',
        headerToolbar: {
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        buttonText: {
          today: 'Hoy',
          month: 'Mes',
          week: 'Semana',
          day: 'Día'
        },
        height: 'auto',
        events: [],
        eventClick: this.handleEventClick,
        dateClick: this.handleDateClick,
        eventColor: '#3B82F6',
        eventTextColor: '#FFFFFF',
        dayMaxEvents: 3,
        moreLinkText: 'más eventos',
        eventDisplay: 'block',
        editable: true,
        selectable: true
      }
    }
  },

  computed: {
    isAdmin () {
      return ['ADMIN', 'ADMINISTRATOR', 'SUPER_ADMIN'].includes(this.userInfo.role)
    }
  },

  mounted () {
    this.startAutoSlide()
    this.loadEvents()
  },

  beforeUnmount () {
    this.stopAutoSlide()
  },

  methods: {
    // Métodos del carrusel
    startAutoSlide () {
      this.autoSlideInterval = setInterval(() => {
        this.nextSlide()
      }, 5000)
    },

    stopAutoSlide () {
      if (this.autoSlideInterval) {
        clearInterval(this.autoSlideInterval)
      }
    },

    nextSlide () {
      if (this.slides.length === 0) return
      this.currentSlide = (this.currentSlide + 1) % this.slides.length
    },

    prevSlide () {
      if (this.slides.length === 0) return
      this.currentSlide = this.currentSlide === 0 ? this.slides.length - 1 : this.currentSlide - 1
    },

    goToSlide (index) {
      this.currentSlide = index
      this.stopAutoSlide()
      setTimeout(() => this.startAutoSlide(), 1000)
    },

    // Métodos del calendario
    async loadEvents () {
      try {
        this.loading = true
        // petición API de Django
        // const response = await this.$api.get('/api/events/')
        // this.events = response.data

        // Eventos de ejemplo
        this.events = [
          {
            id: '1',
            title: 'Reunión de Tesis',
            start: '2025-08-15T10:00:00',
            end: '2025-08-15T12:00:00',
            color: '#10B981',
            textColor: '#FFFFFF',
            extendedProps: {
              description: 'Revisión de avances del proyecto de tesis',
              type: 'meeting'
            }
          },
          {
            id: '2',
            title: 'Entrega Proyecto',
            start: '2025-08-20T23:59:00',
            color: '#EF4444',
            textColor: '#FFFFFF',
            extendedProps: {
              description: 'Fecha límite para entrega del proyecto final',
              type: 'deadline'
            }
          },
          {
            id: '3',
            title: 'Conferencia Ciberseguridad',
            start: '2025-08-25T14:00:00',
            end: '2025-08-25T18:00:00',
            color: '#8B5CF6',
            textColor: '#FFFFFF',
            extendedProps: {
              description: 'Conferencia magistral sobre tendencias en ciberseguridad',
              type: 'event'
            }
          }
        ]

        this.updateCalendarEvents()
      } catch (error) {
        console.error('Error loading events:', error)
        this.showError('Error al cargar los eventos')
      } finally {
        this.loading = false
      }
    },

    updateCalendarEvents () {
      // Actualizar eventos en el calendario
      this.calendarOptions.events = [...this.events]
      // Forzar re-render del calendario
      this.$nextTick(() => {
        if (this.$refs.fullCalendar) {
          this.$refs.fullCalendar.getApi().refetchEvents()
        }
      })
    },

    async createEvent () {
      try {
        this.loading = true

        // Validaciones
        if (!this.newEvent.title.trim()) {
          this.showError('El título del evento es obligatorio')
          return
        }

        if (this.newEvent.end && new Date(this.newEvent.start) >= new Date(this.newEvent.end)) {
          this.showError('La fecha de fin debe ser posterior a la fecha de inicio')
          return
        }

        // Crear nuevo evento
        const eventColor = this.getEventColor(this.newEvent.type)
        const newEventId = Date.now().toString()

        const newCalendarEvent = {
          id: newEventId,
          title: this.newEvent.title.trim(),
          start: this.newEvent.start,
          end: this.newEvent.end || null,
          color: eventColor,
          textColor: '#FFFFFF',
          extendedProps: {
            description: this.newEvent.description.trim(),
            type: this.newEvent.type
          }
        }

        // petición API de Django
        // const response = await this.$api.post('/api/events/', this.newEvent)
        // newCalendarEvent.id = response.data.id

        // Agregar al array local
        this.events.push(newCalendarEvent)

        // Actualizar calendario
        this.updateCalendarEvents()

        // Resetear formulario
        this.resetNewEventForm()
        this.closeCreateEventModal()
        this.showSuccess('Evento creado exitosamente')
      } catch (error) {
        console.error('Error creating event:', error)
        this.showError('Error al crear el evento')
      } finally {
        this.loading = false
      }
    },

    async updateEvent () {
      try {
        this.loading = true

        // Validaciones
        if (!this.editingEvent.title.trim()) {
          this.showError('El título del evento es obligatorio')
          return
        }

        if (this.editingEvent.end && new Date(this.editingEvent.start) >= new Date(this.editingEvent.end)) {
          this.showError('La fecha de fin debe ser posterior a la fecha de inicio')
          return
        }

        // petición API de Django
        // await this.$api.put(`/api/events/${this.editingEvent.id}/`, this.editingEvent)

        // Actualizar en el array local
        const eventIndex = this.events.findIndex(e => e.id === this.editingEvent.id)
        if (eventIndex !== -1) {
          const eventColor = this.getEventColor(this.editingEvent.type)

          this.events[eventIndex] = {
            id: this.editingEvent.id,
            title: this.editingEvent.title.trim(),
            start: this.editingEvent.start,
            end: this.editingEvent.end || null,
            color: eventColor,
            textColor: '#FFFFFF',
            extendedProps: {
              description: this.editingEvent.description.trim(),
              type: this.editingEvent.type
            }
          }
        }

        // Actualizar calendario
        this.updateCalendarEvents()
        this.closeEditEventModal()
        this.showSuccess('Evento actualizado exitosamente')
      } catch (error) {
        console.error('Error updating event:', error)
        this.showError('Error al actualizar el evento')
      } finally {
        this.loading = false
      }
    },

    async deleteEvent () {
      try {
        this.loading = true

        // petición API de Django
        // await this.$api.delete(`/api/events/${this.eventToDelete.id}/`)

        // Eliminar del array local
        this.events = this.events.filter(e => e.id !== this.eventToDelete.id)

        // Actualizar calendario
        this.updateCalendarEvents()
        this.closeDeleteConfirmModal()
        this.showSuccess('Evento eliminado exitosamente')
      } catch (error) {
        console.error('Error deleting event:', error)
        this.showError('Error al eliminar el evento')
      } finally {
        this.loading = false
      }
    },

    // Utilidades para gestión de eventos
    openEditEvent (event) {
      this.editingEvent = {
        id: event.id,
        title: event.title,
        description: event.extendedProps?.description || '',
        start: this.formatDateForInput(event.start),
        end: event.end ? this.formatDateForInput(event.end) : '',
        type: event.extendedProps?.type || ''
      }
      this.showEditEventModal = true
    },

    confirmDeleteEvent (event) {
      this.eventToDelete = event
      this.showDeleteConfirmModal = true
    },

    // Helpers para formateo
    formatDateForInput (date) {
      if (!date) return ''
      const d = new Date(date)
      const year = d.getFullYear()
      const month = String(d.getMonth() + 1).padStart(2, '0')
      const day = String(d.getDate()).padStart(2, '0')
      const hours = String(d.getHours()).padStart(2, '0')
      const minutes = String(d.getMinutes()).padStart(2, '0')
      return `${year}-${month}-${day}T${hours}:${minutes}`
    },

    formatEventDate (date) {
      if (!date) return ''
      const d = new Date(date)
      return d.toLocaleDateString('es-CO', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },

    getEventColor (type) {
      const colors = {
        meeting: '#10B981',
        deadline: '#EF4444',
        event: '#8B5CF6',
        holiday: '#F59E0B',
        exam: '#F97316',
        presentation: '#06B6D4'
      }
      return colors[type] || '#3B82F6'
    },

    getTypeLabel (type) {
      const labels = {
        meeting: 'Reunión',
        deadline: 'Fecha Límite',
        event: 'Evento',
        holiday: 'Feriado',
        exam: 'Examen',
        presentation: 'Presentación'
      }
      return labels[type] || 'Evento'
    },

    getTypeBadgeClass (type) {
      const classes = {
        meeting: 'badge-success',
        deadline: 'badge-danger',
        event: 'badge-purple',
        holiday: 'badge-warning',
        exam: 'badge-orange',
        presentation: 'badge-cyan'
      }
      return classes[type] || 'badge-primary'
    },

    // Manejo de eventos del calendario
    handleEventClick (info) {
      if (this.isAdmin) {
        this.openEditEvent(info.event)
      } else {
        // Para usuarios normales, solo mostrar detalles
        const event = info.event
        alert(`Evento: ${event.title}\nFecha: ${this.formatEventDate(event.start)}\nDescripción: ${event.extendedProps?.description || 'Sin descripción'}`)
      }
    },

    handleDateClick (info) {
      if (this.isAdmin) {
        // Pre-llenar la fecha en el formulario y abrir modal
        const selectedDate = new Date(info.date)
        selectedDate.setHours(9, 0) // Por defecto a las 9:00 AM
        this.newEvent.start = this.formatDateForInput(selectedDate)
        this.showCreateEventModal = true
      }
    },

    // Gestión de modales
    closeCreateEventModal () {
      this.showCreateEventModal = false
      this.resetNewEventForm()
    },

    closeEditEventModal () {
      this.showEditEventModal = false
      this.resetEditingEvent()
    },

    closeManageEventsModal () {
      this.showManageEventsModal = false
    },

    closeDeleteConfirmModal () {
      this.showDeleteConfirmModal = false
      this.eventToDelete = null
    },

    // Reset forms
    resetNewEventForm () {
      this.newEvent = {
        title: '',
        description: '',
        start: '',
        end: '',
        type: ''
      }
    },

    resetEditingEvent () {
      this.editingEvent = {
        id: null,
        title: '',
        description: '',
        start: '',
        end: '',
        type: ''
      }
    },

    // Sistema de notificaciones
    showSuccess (message) {
      this.toastMessage = message
      this.showSuccessToast = true
      setTimeout(() => {
        this.showSuccessToast = false
      }, 3000)
    },

    showError (message) {
      this.toastMessage = message
      this.showErrorToast = true
      setTimeout(() => {
        this.showErrorToast = false
      }, 4000)
    }
  }
}
</script>

<style lang="css"> @import '../../styles/dashboard_home.css'; </style>
