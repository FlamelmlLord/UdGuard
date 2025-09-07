<template>
  <div class="dashboard-container">
    <!-- Header Section - Compacto -->
    <div class="dashboard-header">
      <div class="header-content">
        <h1 class="dashboard-title">
          Bienvenido a UdGuard, Sistema de gestion de indicadores
        </h1>
        <p class="dashboard-subtitle">
          Panel de Control - Maestría en Gestión y Seguridad de la Información
        </p>
      </div>
    </div>

    <!-- Main Content Grid -->
    <div class="main-grid">
      <!-- Left Panel: Calendar (Principal) -->
      <div class="calendar-panel">
        <div class="panel-header">
          <h2 class="panel-title">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" class="panel-icon">
              <rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke="currentColor" stroke-width="2"/>
              <line x1="16" y1="2" x2="16" y2="6" stroke="currentColor" stroke-width="2"/>
              <line x1="8" y1="2" x2="8" y2="6" stroke="currentColor" stroke-width="2"/>
              <line x1="3" y1="10" x2="21" y2="10" stroke="currentColor" stroke-width="2"/>
            </svg>
            Calendario de Actividades
          </h2>

          <!-- Admin Controls -->
          <div v-if="isAdmin" class="panel-controls">
            <button class="btn btn-primary" @click="showCreateEventModal = true">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <line x1="12" y1="5" x2="12" y2="19" stroke="currentColor" stroke-width="2"/>
                <line x1="5" y1="12" x2="19" y2="12" stroke="currentColor" stroke-width="2"/>
              </svg>
              Crear Evento
            </button>

            <button class="btn btn-secondary" @click="showManageEventsModal = true">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
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

      <!-- Right Panel: Info Cards -->
      <div class="info-panel">
        <!-- Event Counters Modernizados -->
        <div class="event-counters">
          <div class="event-counter-card">
            <div class="event-counter-number">{{ upcomingEventsCount }}</div>
            <div class="event-counter-label">Próximos Eventos</div>
          </div>
          <div class="event-counter-card">
            <div class="event-counter-number">{{ todayEventsCount }}</div>
            <div class="event-counter-label">Eventos Hoy</div>
          </div>
        </div>

        <!-- Noticias (Carrusel Moderno) -->
        <div class="info-carousel-modern">
          <div class="carousel-title-row">
            <h3 class="carousel-title">Noticias</h3>
          </div>
          <div class="carousel-slide-modern">
            <img
              v-if="slides[currentSlide].image"
              :src="slides[currentSlide].image"
              alt="Imagen noticia"
              class="slide-image-modern"
            />
            <!-- Flechas overlay -->
            <button class="carousel-arrow-modern left" @click="prevSlide" aria-label="Anterior">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                <polyline points="15 18 9 12 15 6" stroke="white" stroke-width="2" fill="none"/>
              </svg>
            </button>
            <button class="carousel-arrow-modern right" @click="nextSlide" aria-label="Siguiente">
              <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                <polyline points="9 6 15 12 9 18" stroke="white" stroke-width="2" fill="none"/>
              </svg>
            </button>
            <!-- Overlay de texto -->
            <div class="slide-overlay-modern">
              <h4 class="slide-title-modern">{{ slides[currentSlide].title }}</h4>
              <p class="slide-description-modern">{{ slides[currentSlide].description }}</p>
              <button class="btn-link-modern">Leer más</button>
            </div>
          </div>
          <div class="carousel-indicators-modern">
            <button
              v-for="(slide, index) in slides"
              :key="index"
              class="indicator-dot-modern"
              :class="{ active: currentSlide === index }"
              @click="goToSlide(index)"
            ></button>
          </div>
        </div>
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
              maxlength="100"
            />
          </div>

          <div class="form-group">
            <label for="eventDescription">Descripción</label>
            <textarea
              id="eventDescription"
              v-model="newEvent.description"
              placeholder="Descripción del evento (opcional)"
              rows="3"
              maxlength="500"
            ></textarea>
          </div>

          <div class="form-row">
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
              <label for="eventEnd">Fecha de Fin (Opcional)</label>
              <input
                id="eventEnd"
                v-model="newEvent.end"
                type="datetime-local"
              />
            </div>
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
              <option value="workshop">Taller</option>
              <option value="conference">Conferencia</option>
            </select>
          </div>

          <div class="modal-actions">
            <button type="button" class="btn btn-secondary" @click="closeCreateEventModal">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary" :disabled="loading || !isFormValid">
              <span v-if="loading">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" class="loading-icon">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                  <path d="M12 6v6l4 2" stroke="currentColor" stroke-width="2"/>
                </svg>
                Creando...
              </span>
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
          <div class="modal-header-actions">
            <span class="events-count">{{ events.length }} evento{{ events.length !== 1 ? 's' : '' }}</span>
            <button class="modal-close" @click="closeManageEventsModal">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2"/>
                <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2"/>
              </svg>
            </button>
          </div>
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
            <button class="btn btn-primary" @click="showCreateEventModal = true; closeManageEventsModal()">
              Crear mi primer evento
            </button>
          </div>

          <div v-else class="events-table">
            <div class="events-filter">
              <input
                v-model="eventsFilter"
                type="text"
                placeholder="Buscar eventos..."
                class="filter-input"
              />
              <select v-model="eventsTypeFilter" class="filter-select">
                <option value="">Todos los tipos</option>
                <option value="meeting">Reuniones</option>
                <option value="deadline">Fechas Límite</option>
                <option value="event">Eventos Especiales</option>
                <option value="holiday">Feriados</option>
                <option value="exam">Exámenes</option>
                <option value="presentation">Presentaciones</option>
                <option value="workshop">Talleres</option>
                <option value="conference">Conferencias</option>
              </select>
            </div>

            <div class="event-item" v-for="event in filteredEvents" :key="event.id">
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
              maxlength="100"
            />
          </div>

          <div class="form-group">
            <label for="eventDescription">Descripción</label>
            <textarea
              id="eventDescription"
              v-model="newEvent.description"
              placeholder="Descripción del evento (opcional)"
              rows="3"
              maxlength="500"
            ></textarea>
          </div>

          <div class="form-row">
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
              <label for="eventEnd">Fecha de Fin (Opcional)</label>
              <input
                id="eventEnd"
                v-model="newEvent.end"
                type="datetime-local"
              />
            </div>
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
              <option value="workshop">Taller</option>
              <option value="conference">Conferencia</option>
            </select>
          </div>

          <div class="modal-actions">
            <button type="button" class="btn btn-secondary" @click="closeCreateEventModal">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary" :disabled="loading || !isFormValid">
              <span v-if="loading">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" class="loading-icon">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                  <path d="M12 6v6l4 2" stroke="currentColor" stroke-width="2"/>
                </svg>
                Creando...
              </span>
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
          <div class="modal-header-actions">
            <span class="events-count">{{ events.length }} evento{{ events.length !== 1 ? 's' : '' }}</span>
            <button class="modal-close" @click="closeManageEventsModal">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2"/>
                <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2"/>
              </svg>
            </button>
          </div>
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
            <button class="btn btn-primary" @click="showCreateEventModal = true; closeManageEventsModal()">
              Crear mi primer evento
            </button>
          </div>

          <div v-else class="events-table">
            <div class="events-filter">
              <input
                v-model="eventsFilter"
                type="text"
                placeholder="Buscar eventos..."
                class="filter-input"
              />
              <select v-model="eventsTypeFilter" class="filter-select">
                <option value="">Todos los tipos</option>
                <option value="meeting">Reuniones</option>
                <option value="deadline">Fechas Límite</option>
                <option value="event">Eventos Especiales</option>
                <option value="holiday">Feriados</option>
                <option value="exam">Exámenes</option>
                <option value="presentation">Presentaciones</option>
                <option value="workshop">Talleres</option>
                <option value="conference">Conferencias</option>
              </select>
            </div>

            <div class="event-item" v-for="event in filteredEvents" :key="event.id">
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
              maxlength="100"
            />
          </div>

          <div class="form-group">
            <label for="editEventDescription">Descripción</label>
            <textarea
              id="editEventDescription"
              v-model="editingEvent.description"
              placeholder="Descripción del evento (opcional)"
              rows="3"
              maxlength="500"
            ></textarea>
          </div>

          <div class="form-row">
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
              <label for="editEventEnd">Fecha de Fin (Opcional)</label>
              <input
                id="editEventEnd"
                v-model="editingEvent.end"
                type="datetime-local"
              />
            </div>
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
              <option value="workshop">Taller</option>
              <option value="conference">Conferencia</option>
            </select>
          </div>

          <div class="modal-actions">
            <button type="button" class="btn btn-secondary" @click="closeEditEventModal">
              Cancelar
            </button>
            <button type="submit" class="btn btn-primary" :disabled="loading || !isEditFormValid">
              <span v-if="loading">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" class="loading-icon">
                  <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                  <path d="M12 6v6l4 2" stroke="currentColor" stroke-width="2"/>
                </svg>
                Actualizando...
              </span>
              <span v-else>Actualizar Evento</span>
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Event Details Modal -->
    <div v-if="showEventDetailsModal" class="modal-overlay" @click="closeEventDetailsModal">
      <div class="modal-content modal-small" @click.stop>
        <div class="modal-header">
          <h3>Detalles del Evento</h3>
          <button class="modal-close" @click="closeEventDetailsModal">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <line x1="18" y1="6" x2="6" y2="18" stroke="currentColor" stroke-width="2"/>
              <line x1="6" y1="6" x2="18" y2="18" stroke="currentColor" stroke-width="2"/>
            </svg>
          </button>
        </div>

        <div class="event-details-content" v-if="selectedEvent">
          <div class="event-detail-header">
            <div class="event-detail-indicator" :style="{ backgroundColor: selectedEvent.color }"></div>
            <div>
              <h4 class="event-detail-title">{{ selectedEvent.title }}</h4>
              <span class="event-detail-badge" :class="getTypeBadgeClass(selectedEvent.extendedProps?.type)">
                {{ getTypeLabel(selectedEvent.extendedProps?.type) }}
              </span>
            </div>
          </div>

          <div class="event-detail-info">
            <div class="detail-row" v-if="selectedEvent.extendedProps?.description">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" stroke-width="2"/>
                <polyline points="14,2 14,8 20,8" stroke="currentColor" stroke-width="2"/>
                <line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" stroke-width="2"/>
                <line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" stroke-width="2"/>
                <polyline points="10,9 9,9 8,9" stroke="currentColor" stroke-width="2"/>
              </svg>
              <div>
                <strong>Descripción:</strong>
                <p>{{ selectedEvent.extendedProps.description }}</p>
              </div>
            </div>

            <div class="detail-row">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <polyline points="12,6 12,12 16,14" stroke="currentColor" stroke-width="2"/>
              </svg>
              <div>
                <strong>Fecha de Inicio:</strong>
                <p>{{ formatEventDate(selectedEvent.start) }}</p>
              </div>
            </div>

            <div class="detail-row" v-if="selectedEvent.end">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <polyline points="12,6 12,12 16,14" stroke="currentColor" stroke-width="2"/>
              </svg>
              <div>
                <strong>Fecha de Fin:</strong>
                <p>{{ formatEventDate(selectedEvent.end) }}</p>
              </div>
            </div>

            <div class="detail-row">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1 1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" stroke="currentColor" stroke-width="2"/>
              </svg>
              <div>
                <strong>Duración:</strong>
                <p>{{ calculateEventDuration(selectedEvent) }}</p>
              </div>
            </div>
          </div>

          <div class="modal-actions" v-if="isAdmin">
            <button type="button" class="btn btn-secondary" @click="openEditEventFromDetails">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" stroke-width="2"/>
                <path d="M18.5 2.5a2.12 2.12 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="2"/>
              </svg>
              Editar Evento
            </button>
            <button type="button" class="btn btn-danger" @click="confirmDeleteEventFromDetails">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                <polyline points="3,6 5,6 21,6" stroke="currentColor" stroke-width="2"/>
                <path d="M19,6v14a2,2,0,0,1-2,2H7a2,2,0,0,1-2-2V6M8,6V4a2,2,0,0,1,2-2h4a2,2,0,0,1,2,2V6" stroke="currentColor" stroke-width="2"/>
              </svg>
              Eliminar Evento
            </button>
          </div>
        </div>
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
            <span v-if="loading">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" class="loading-icon">
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                <path d="M12 6v6l4 2" stroke="currentColor" stroke-width="2"/>
              </svg>
              Eliminando...
            </span>
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
      showEventDetailsModal: false,
      showSuccessToast: false,
      showErrorToast: false,
      toastMessage: '',
      eventToDelete: null,
      selectedEvent: null,
      eventsFilter: '',
      eventsTypeFilter: '',

      // User info - esto debería venir del store/auth
      userInfo: {
        name: 'Admin Usuario',
        role: 'ADMIN' // CAMBIAR según tu sistema de autenticación
      },

      // Slides del carrusel - más compactos y relevantes
      slides: [
        {
          id: 1,
          title: 'Maestría en GSI',
          description: 'Formando expertos en ciberseguridad y gestión de información para el futuro digital.',
          image: 'https://images.unsplash.com/photo-1551434678-e076c223a692?w=400&h=200&fit=crop'
        },
        {
          id: 2,
          title: 'Noticias Académicas',
          description: 'Mantente actualizado con las últimas novedades y eventos del programa.',
          image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=200&fit=crop'
        },
        {
          id: 3,
          title: 'Eventos Especiales',
          description: 'Participa en conferencias magistrales y actividades académicas destacadas.',
          image: 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=400&h=200&fit=crop'
        },
        {
          id: 4,
          title: 'Recursos Digitales',
          description: 'Accede a la biblioteca digital y herramientas especializadas del programa.',
          image: 'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=200&fit=crop'
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

      // Opciones del calendario - optimizadas
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
        selectable: true,
        selectMirror: true,
        dayMaxEventRows: 3,
        weekends: true,
        nowIndicator: true,
        businessHours: {
          daysOfWeek: [1, 2, 3, 4, 5],
          startTime: '08:00',
          endTime: '18:00'
        }
      }
    }
  },

  computed: {
    isAdmin () {
      return ['ADMIN', 'ADMINISTRATOR', 'SUPER_ADMIN'].includes(this.userInfo.role)
    },

    upcomingEvents () {
      const now = new Date()
      const futureEvents = this.events
        .filter(event => new Date(event.start) > now)
        .sort((a, b) => new Date(a.start) - new Date(b.start))
      return futureEvents
    },

    upcomingEventsCount () {
      return this.upcomingEvents.length
    },

    todayEventsCount () {
      const today = new Date()
      const todayStart = new Date(today.getFullYear(), today.getMonth(), today.getDate())
      const todayEnd = new Date(todayStart.getTime() + 24 * 60 * 60 * 1000)
      
      return this.events.filter(event => {
        const eventDate = new Date(event.start)
        return eventDate >= todayStart && eventDate < todayEnd
      }).length
    },

    filteredEvents () {
      let filtered = [...this.events]

      // Filtrar por texto
      if (this.eventsFilter.trim()) {
        const searchTerm = this.eventsFilter.toLowerCase().trim()
        filtered = filtered.filter(event =>
          event.title.toLowerCase().includes(searchTerm) ||
          (event.extendedProps?.description || '').toLowerCase().includes(searchTerm)
        )
      }

      // Filtrar por tipo
      if (this.eventsTypeFilter) {
        filtered = filtered.filter(event =>
          event.extendedProps?.type === this.eventsTypeFilter
        )
      }

      // Ordenar por fecha de inicio
      return filtered.sort((a, b) => new Date(a.start) - new Date(b.start))
    },

    isFormValid () {
      return this.newEvent.title.trim() && 
             this.newEvent.start && 
             this.newEvent.type &&
             (!this.newEvent.end || new Date(this.newEvent.start) < new Date(this.newEvent.end))
    },

    isEditFormValid () {
      return this.editingEvent.title.trim() && 
             this.editingEvent.start && 
             this.editingEvent.type &&
             (!this.editingEvent.end || new Date(this.editingEvent.start) < new Date(this.editingEvent.end))
    }
  },

  mounted () {
    this.startAutoSlide()
    this.loadEvents()
    this.initializeCalendarSize()
  },

  beforeUnmount () {
    this.stopAutoSlide()
  },

  methods: {
    // Inicialización
    initializeCalendarSize () {
      this.$nextTick(() => {
        if (this.$refs.fullCalendar) {
          this.$refs.fullCalendar.getApi().updateSize()
        }
      })
    },

    // Métodos del carrusel - optimizados
    startAutoSlide () {
      this.autoSlideInterval = setInterval(() => {
        this.nextSlide()
      }, 6000) // Más lento para mejor UX
    },

    stopAutoSlide () {
      if (this.autoSlideInterval) {
        clearInterval(this.autoSlideInterval)
        this.autoSlideInterval = null
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
      setTimeout(() => this.startAutoSlide(), 3000)
    },

    // Métodos de navegación para Quick Actions
    navigateToDocuments () {
      // TODO: Implementar navegación
      this.$router.push('/documents')
      // O emitir evento: this.$emit('navigate', 'documents')
    },

    navigateToTraining () {
      // TODO: Implementar navegación
      this.$router.push('/training')
    },

    navigateToResources () {
      // TODO: Implementar navegación
      this.$router.push('/resources')
    },

    navigateToVirtualClassroom () {
      // TODO: Implementar navegación
      window.open('https://aula-virtual.udistrital.edu.co', '_blank')
    },

    navigateToLibrary () {
      // TODO: Implementar navegación
      window.open('https://biblioteca.udistrital.edu.co', '_blank')
    },

    navigateToTeachers () {
      // TODO: Implementar navegación
      this.$router.push('/teachers')
    },

    navigateToSupport () {
      // TODO: Implementar navegación
      this.$router.push('/support')
    },

    // Métodos del calendario
    async loadEvents () {
      try {
        this.loading = true
        
        // TODO: Conectar con API de Django
        // const response = await this.$api.get('/api/events/')
        // this.events = response.data.map(event => this.transformEventFromAPI(event))

        // Eventos de ejemplo mejorados para demostración
        this.events = [
          {
            id: '1',
            title: 'Reunión de Tesis - Director Académico',
            start: '2025-09-05T10:00:00',
            end: '2025-09-05T12:00:00',
            color: '#10B981',
            textColor: '#FFFFFF',
            extendedProps: {
              description: 'Revisión de avances del proyecto de tesis con el director académico. Presentación de capítulos 1 y 2.',
              type: 'meeting'
            }
          },
          {
            id: '2',
            title: 'Entrega Proyecto Final - Ciberseguridad',
            start: '2025-09-15T23:59:00',
            color: '#EF4444',
            textColor: '#FFFFFF',
            extendedProps: {
              description: 'Fecha límite para entrega del proyecto final de la materia Ciberseguridad Avanzada',
              type: 'deadline'
            }
          },
          {
            id: '3',
            title: 'Conferencia Internacional Ciberseguridad 2025',
            start: '2025-09-20T14:00:00',
            end: '2025-09-20T18:00:00',
            color: '#8B5CF6',
            textColor: '#FFFFFF',
            extendedProps: {
              description: 'Conferencia magistral sobre tendencias emergentes en ciberseguridad y inteligencia artificial',
              type: 'conference'
            }
          },
          {
            id: '4',
            title: 'Examen Parcial - Gestión de Riesgos',
            start: '2025-09-10T08:00:00',
            end: '2025-09-10T10:00:00',
            color: '#F97316',
            textColor: '#FFFFFF',
            extendedProps: {
              description: 'Evaluación parcial de la materia Gestión de Riesgos en Seguridad de la Información',
              type: 'exam'
            }
          },
          {
            id: '5',
            title: 'Taller de Herramientas OSINT',
            start: '2025-09-12T15:00:00',
            end: '2025-09-12T17:00:00',
            color: '#06B6D4',
            textColor: '#FFFFFF',
            extendedProps: {
              description: 'Taller práctico sobre herramientas de inteligencia de fuentes abiertas (OSINT)',
              type: 'workshop'
            }
          },
          {
            id: '6',
            title: 'Presentación Proyectos de Grado',
            start: '2025-09-25T09:00:00',
            end: '2025-09-25T17:00:00',
            color: '#8B5CF6',
            textColor: '#FFFFFF',
            extendedProps: {
              description: 'Jornada de presentaciones de proyectos de grado - Cohorte 2024',
              type: 'presentation'
            }
          }
        ]

        this.updateCalendarEvents()
      } catch (error) {
        console.error('Error loading events:', error)
        this.showError('Error al cargar los eventos. Por favor, recarga la página.')
      } finally {
        this.loading = false
      }
    },

    // Transformar evento de API a formato del calendario
    transformEventFromAPI (apiEvent) {
      return {
        id: apiEvent.id.toString(),
        title: apiEvent.title,
        start: apiEvent.start_datetime,
        end: apiEvent.end_datetime,
        color: this.getEventColor(apiEvent.event_type),
        textColor: '#FFFFFF',
        extendedProps: {
          description: apiEvent.description,
          type: apiEvent.event_type,
          created_by: apiEvent.created_by,
          created_at: apiEvent.created_at
        }
      }
    },

    updateCalendarEvents () {
      this.calendarOptions.events = [...this.events]
      this.$nextTick(() => {
        if (this.$refs.fullCalendar) {
          this.$refs.fullCalendar.getApi().refetchEvents()
        }
      })
    },

    async createEvent () {
      try {
        this.loading = true

        // Validaciones mejoradas
        if (!this.newEvent.title.trim()) {
          this.showError('El título del evento es obligatorio')
          return
        }

        if (this.newEvent.title.length > 100) {
          this.showError('El título no puede exceder 100 caracteres')
          return
        }

        if (this.newEvent.description.length > 500) {
          this.showError('La descripción no puede exceder 500 caracteres')
          return
        }

        if (this.newEvent.end && new Date(this.newEvent.start) >= new Date(this.newEvent.end)) {
          this.showError('La fecha de fin debe ser posterior a la fecha de inicio')
          return
        }

        // Verificar que la fecha no sea en el pasado
        if (new Date(this.newEvent.start) < new Date()) {
          this.showError('No puedes crear eventos en fechas pasadas')
          return
        }

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
            type: this.newEvent.type,
            created_by: this.userInfo.name,
            created_at: new Date().toISOString()
          }
        }

        // TODO: Enviar a API de Django
        // const response = await this.$api.post('/api/events/', {
        //   title: this.newEvent.title.trim(),
        //   description: this.newEvent.description.trim(),
        //   start_datetime: this.newEvent.start,
        //   end_datetime: this.newEvent.end,
        //   event_type: this.newEvent.type
        // })
        // newCalendarEvent.id = response.data.id.toString()

        this.events.push(newCalendarEvent)
        this.updateCalendarEvents()
        this.resetNewEventForm()
        this.closeCreateEventModal()
        this.showSuccess('Evento creado exitosamente')
      } catch (error) {
        console.error('Error creating event:', error)
        this.showError('Error al crear el evento. Inténtalo nuevamente.')
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

        if (this.editingEvent.title.length > 100) {
          this.showError('El título no puede exceder 100 caracteres')
          return
        }

        if (this.editingEvent.description.length > 500) {
          this.showError('La descripción no puede exceder 500 caracteres')
          return
        }

        if (this.editingEvent.end && new Date(this.editingEvent.start) >= new Date(this.editingEvent.end)) {
          this.showError('La fecha de fin debe ser posterior a la fecha de inicio')
          return
        }

        // TODO: Enviar a API de Django
        // await this.$api.put(`/api/events/${this.editingEvent.id}/`, {
        //   title: this.editingEvent.title.trim(),
        //   description: this.editingEvent.description.trim(),
        //   start_datetime: this.editingEvent.start,
        //   end_datetime: this.editingEvent.end,
        //   event_type: this.editingEvent.type
        // })

        const eventIndex = this.events.findIndex(e => e.id === this.editingEvent.id)
        if (eventIndex !== -1) {
          const eventColor = this.getEventColor(this.editingEvent.type)

          this.events[eventIndex] = {
            ...this.events[eventIndex],
            title: this.editingEvent.title.trim(),
            start: this.editingEvent.start,
            end: this.editingEvent.end || null,
            color: eventColor,
            extendedProps: {
              ...this.events[eventIndex].extendedProps,
              description: this.editingEvent.description.trim(),
              type: this.editingEvent.type,
              updated_at: new Date().toISOString()
            }
          }
        }

        this.updateCalendarEvents()
        this.closeEditEventModal()
        this.showSuccess('Evento actualizado exitosamente')
      } catch (error) {
        console.error('Error updating event:', error)
        this.showError('Error al actualizar el evento. Inténtalo nuevamente.')
      } finally {
        this.loading = false
      }
    },

    async deleteEvent () {
      try {
        this.loading = true

        // TODO: Enviar a API de Django
        // await this.$api.delete(`/api/events/${this.eventToDelete.id}/`)

        this.events = this.events.filter(e => e.id !== this.eventToDelete.id)
        this.updateCalendarEvents()
        this.closeDeleteConfirmModal()
        this.showSuccess('Evento eliminado exitosamente')
      } catch (error) {
        console.error('Error deleting event:', error)
        this.showError('Error al eliminar el evento. Inténtalo nuevamente.')
      } finally {
        this.loading = false
      }
    },

    // Nuevos métodos para gestión mejorada de eventos
    viewEventDetails (event) {
      this.selectedEvent = event
      this.showEventDetailsModal = true
    },

    openEditEventFromDetails () {
      this.closeEventDetailsModal()
      this.openEditEvent(this.selectedEvent)
    },

    confirmDeleteEventFromDetails () {
      this.closeEventDetailsModal()
      this.confirmDeleteEvent(this.selectedEvent)
    },

    closeEventDetailsModal () {
      this.showEventDetailsModal = false
      this.selectedEvent = null
    },

    calculateEventDuration (event) {
      if (!event.end) return 'Sin hora de fin definida'
      
      const start = new Date(event.start)
      const end = new Date(event.end)
      const diffMs = end - start
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
      const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))
      
      if (diffHours === 0) {
        return `${diffMinutes} minuto${diffMinutes !== 1 ? 's' : ''}`
      } else if (diffMinutes === 0) {
        return `${diffHours} hora${diffHours !== 1 ? 's' : ''}`
      } else {
        return `${diffHours} hora${diffHours !== 1 ? 's' : ''} y ${diffMinutes} minuto${diffMinutes !== 1 ? 's' : ''}`
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

    // Helpers para formateo mejorados
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

    formatShortDate (date) {
      if (!date) return ''
      const d = new Date(date)
      const today = new Date()
      const tomorrow = new Date(today)
      tomorrow.setDate(tomorrow.getDate() + 1)
      
      if (d.toDateString() === today.toDateString()) {
        return `Hoy, ${d.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' })}`
      } else if (d.toDateString() === tomorrow.toDateString()) {
        return `Mañana, ${d.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' })}`
      } else {
        return d.toLocaleDateString('es-CO', {
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        })
      }
    },

    getEventColor (type) {
      const colors = {
        meeting: '#10B981',
        deadline: '#EF4444',
        event: '#8B5CF6',
        holiday: '#F59E0B',
        exam: '#F97316',
        presentation: '#06B6D4',
        workshop: '#06B6D4',
        conference: '#8B5CF6'
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
        presentation: 'Presentación',
        workshop: 'Taller',
        conference: 'Conferencia'
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
        presentation: 'badge-cyan',
        workshop: 'badge-cyan',
        conference: 'badge-purple'
      }
      return classes[type] || 'badge-primary'
    },

    // Manejo de eventos del calendario
    handleEventClick (info) {
      this.viewEventDetails(info.event)
    },

    handleDateClick (info) {
      if (this.isAdmin) {
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
      this.eventsFilter = ''
      this.eventsTypeFilter = ''
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

    // Sistema de notificaciones mejorado
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
      }, 5000)
    },

    // Método para manejar errores de red
    handleNetworkError (error) {
      if (error.response) {
        // Error del servidor
        const status = error.response.status
        if (status === 401) {
          this.showError('Sesión expirada. Por favor, inicia sesión nuevamente.')
          // TODO: Redirigir al login
          // this.$router.push('/login')
        } else if (status === 403) {
          this.showError('No tienes permisos para realizar esta acción.')
        } else if (status === 500) {
          this.showError('Error interno del servidor. Contacta al administrador.')
        } else {
          this.showError('Error del servidor. Inténtalo más tarde.')
        }
      } else if (error.request) {
        // Error de red
        this.showError('Error de conexión. Verifica tu conexión a internet.')
      } else {
        // Error desconocido
        this.showError('Ha ocurrido un error inesperado.')
      }
    },

    // Método para refrescar datos
    async refreshData () {
      await this.loadEvents()
    },

    // Método para exportar eventos (funcionalidad adicional)
    exportEvents () {
      try {
        const eventsToExport = this.events.map(event => ({
          titulo: event.title,
          descripcion: event.extendedProps?.description || '',
          inicio: this.formatEventDate(event.start),
          fin: event.end ? this.formatEventDate(event.end) : '',
          tipo: this.getTypeLabel(event.extendedProps?.type)
        }))

        const csvContent = this.convertToCSV(eventsToExport)
        this.downloadCSV(csvContent, 'eventos_udguard.csv')
        this.showSuccess('Eventos exportados exitosamente')
      } catch (error) {
        console.error('Error exporting events:', error)
        this.showError('Error al exportar los eventos')
      }
    },

    convertToCSV (data) {
      if (data.length === 0) return ''
      
      const headers = Object.keys(data[0])
      const csvRows = [
        headers.join(','),
        ...data.map(row => 
          headers.map(header => {
            const value = row[header] || ''
            return `"${value.toString().replace(/"/g, '""')}"`
          }).join(',')
        )
      ]
      
      return csvRows.join('\n')
    },

    downloadCSV (csvContent, filename) {
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      const url = URL.createObjectURL(blob)
      link.setAttribute('href', url)
      link.setAttribute('download', filename)
      link.style.visibility = 'hidden'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },

    // Método para buscar eventos por fecha
    searchEventsByDate (date) {
      const targetDate = new Date(date)
      const dayStart = new Date(targetDate.getFullYear(), targetDate.getMonth(), targetDate.getDate())
      const dayEnd = new Date(dayStart.getTime() + 24 * 60 * 60 * 1000)
      
      return this.events.filter(event => {
        const eventDate = new Date(event.start)
        return eventDate >= dayStart && eventDate < dayEnd
      })
    }
  }
}
</script>

<style lang="css" scoped>
@import '../../styles/dashboard_home.css';
</style>