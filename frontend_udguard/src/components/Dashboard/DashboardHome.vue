<template>
  <div class="dashboard-container">
    <!-- Header Section - Compacto -->
    <div class="dashboard-header dashboard-home-header">
      <div class="header-content dashboard-home-header-content">
        <h1 class="dashboard-title dashboard-home-title">
          Bienvenido a UdGuard, Sistema de gestion de indicadores
        </h1>
        <p class="dashboard-subtitle dashboard-home-subtitle">
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
        <!-- Panel de Próximos Eventos - REEMPLAZA EL CARRUSEL -->
        <div class="upcoming-events-panel">
          <div class="panel-header-small">
            <h3 class="panel-title-small">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" class="panel-icon-small">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke="currentColor" stroke-width="2"/>
                <line x1="16" y1="2" x2="16" y2="6" stroke="currentColor" stroke-width="2"/>
                <line x1="8" y1="2" x2="8" y2="6" stroke="currentColor" stroke-width="2"/>
                <line x1="3" y1="10" x2="21" y2="10" stroke="currentColor" stroke-width="2"/>
              </svg>
              Próximos Eventos
            </h3>
            <span class="events-badge">{{ upcomingEvents.length }}</span>
          </div>

          <div class="events-preview-container">
            <!-- Estado vacío -->
            <div v-if="upcomingEvents.length === 0" class="empty-events-state">
              <svg width="36" height="36" viewBox="0 0 24 24" fill="none" class="empty-icon">
                <rect x="3" y="4" width="18" height="18" rx="2" ry="2" stroke="currentColor" stroke-width="2"/>
                <line x1="16" y1="2" x2="16" y2="6" stroke="currentColor" stroke-width="2"/>
                <line x1="8" y1="2" x2="8" y2="6" stroke="currentColor" stroke-width="2"/>
                <line x1="3" y1="10" x2="21" y2="10" stroke="currentColor" stroke-width="2"/>
                <line x1="12" y1="14" x2="12" y2="18" stroke="currentColor" stroke-width="2"/>
                <line x1="10" y1="16" x2="14" y2="16" stroke="currentColor" stroke-width="2"/>
              </svg>
              <p>No hay eventos próximos</p>
              <button v-if="isAdmin" class="btn btn-sm btn-primary" @click="showCreateEventModal = true">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                  <line x1="12" y1="5" x2="12" y2="19" stroke="currentColor" stroke-width="2"/>
                  <line x1="5" y1="12" x2="19" y2="12" stroke="currentColor" stroke-width="2"/>
                </svg>
                Crear Evento
              </button>
            </div>

            <!-- Lista de eventos -->
            <div v-else class="events-preview-list">
              <div 
                v-for="event in upcomingEvents" 
                :key="event.id" 
                class="event-preview-item"
                @click="viewEventDetails(event)"
              >
                <div class="event-preview-indicator" :style="{ backgroundColor: event.color }"></div>
                <div class="event-preview-content">
                  <div class="event-preview-header">
                    <h4 class="event-preview-title">{{ event.title }}</h4>
                    <span class="event-preview-badge" :class="getTypeBadgeClass(event.extendedProps?.type)">
                      {{ getTypeLabel(event.extendedProps?.type) }}
                    </span>
                  </div>
                  <div class="event-preview-info">
                    <div class="event-preview-date">
                      <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                        <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
                        <polyline points="12,6 12,12 16,14" stroke="currentColor" stroke-width="2"/>
                      </svg>
                      <span>{{ formatEventDateShort(event.start) }}</span>
                    </div>
                    <div v-if="isToday(event.start)" class="today-indicator">
                      <span>HOY</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Ver todos los eventos -->
            <div v-if="upcomingEvents.length > 0" class="events-preview-footer">
              <button class="btn btn-text btn-sm" @click="showManageEventsModal = true">
                Ver todos los eventos
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none">
                  <polyline points="9 18 15 12 9 6" stroke="currentColor" stroke-width="2"/>
                </svg>
              </button>
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
              v-model="newEvent.titulo"
              type="text"
              required
              maxlength="100"
            />
          </div>

          <div class="form-group">
            <label for="eventDescription">Descripción</label>
            <textarea
              id="eventDescription"
              v-model="newEvent.descripcion"
              rows="3"
              maxlength="500"
            ></textarea>
          </div>

          <div class="form-row">
            <div class="form-group">
              <label for="eventStart">Fecha de Inicio</label>
              <input
                id="eventStart"
                v-model="newEvent.fecha_inicio"
                type="datetime-local"
                required
              />
            </div>

            <div class="form-group">
              <label for="eventEnd">Fecha de Fin (Opcional)</label>
              <input
                id="eventEnd"
                v-model="newEvent.fecha_fin"
                type="datetime-local"
              />
            </div>
          </div>

          <div class="form-group">
            <label for="eventType">Tipo de Evento</label>
            <select id="eventType" v-model="newEvent.tipo_evento" required>
              <option value="">Selecciona un tipo</option>
              <option value="meeting">Reunión</option>
              <option value="deadline">Fecha Límite</option>
              <option value="event">Evento</option>
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
                v-model="newEvent.titulo"
                type="text"
                required
                maxlength="100"
              />
            </div>

            <div class="form-group">
              <label for="eventDescription">Descripción</label>
              <textarea
                id="eventDescription"
                v-model="newEvent.descripcion"
                rows="3"
                maxlength="500"
              ></textarea>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label for="eventStart">Fecha de Inicio</label>
                <input
                  id="eventStart"
                  v-model="newEvent.fecha_inicio"
                  type="datetime-local"
                  required
                />
              </div>

              <div class="form-group">
                <label for="eventEnd">Fecha de Fin (Opcional)</label>
                <input
                  id="eventEnd"
                  v-model="newEvent.fecha_fin"
                  type="datetime-local"
                />
              </div>
            </div>

            <div class="form-group">
              <label for="eventType">Tipo de Evento</label>
              <select id="eventType" v-model="newEvent.tipo_evento" required>
                <option value="">Selecciona un tipo</option>
                <option value="meeting">Reunión</option>
                <option value="deadline">Fecha Límite</option>
                <option value="event">Evento</option>
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
                v-model="editingEvent.titulo"
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
                v-model="editingEvent.descripcion"
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
                  v-model="editingEvent.fecha_inicio"
                  type="datetime-local"
                  required
                />
              </div>

              <div class="form-group">
                <label for="editEventEnd">Fecha de Fin (Opcional)</label>
                <input
                  id="editEventEnd"
                  v-model="editingEvent.fecha_fin"
                  type="datetime-local"
                />
              </div>
            </div>

            <div class="form-group">
              <label for="editEventType">Tipo de Evento</label>
              <select id="editEventType" v-model="editingEvent.tipo_evento" required>
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
                  <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" stroke="currentColor" stroke-width="2"/>
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
                  <path d="M12 1v6m0 6v6m11-7h-6m-6 0H1" stroke="currentColor" stroke-width="2"/>
                </svg>
                <div>
                  <strong>Duración:</strong>
                  <p>{{ calculateEventDuration(selectedEvent) }}</p>
                </div>
              </div>
            </div>

            <!-- ⭐ BOTONES DE ACCIÓN - VERIFICAR QUE ESTÁN CONECTADOS CORRECTAMENTE -->
            <div class="modal-actions" v-if="isAdmin">
              <button type="button" class="btn btn-secondary" @click="openEditEventFromDetails(selectedEvent)">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" stroke-width="2"/>
                  <path d="M18.5 2.5a2.12 2.12 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="2"/>
                </svg>
                Editar Evento
              </button>
              <button type="button" class="btn btn-danger" @click="confirmDeleteEventFromDetails(selectedEvent)">
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
  </div>
</template>

<script>
import FullCalendar from '@fullcalendar/vue'
import dayGridPlugin from '@fullcalendar/daygrid'
import timeGridPlugin from '@fullcalendar/timegrid'
import interactionPlugin from '@fullcalendar/interaction'
import esLocale from '@fullcalendar/core/locales/es'
import axios from '../../plugins/Axios'

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

      // ⭐ DATOS DE USUARIO DESDE EL BACKEND
      userInfo: {
        name: 'Usuario',
        role: 'user'
      },

      // ⭐ ESTADÍSTICAS DEL DASHBOARD
      dashboardStats: {
        total_events: 0,
        today_events: 0,
        upcoming_events: 0,
        events_by_type: {}
      },

      // Slides del carrusel
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
        titulo: '',
        descripcion: '',
        fecha_inicio: '',
        fecha_fin: '',
        tipo_evento: ''
      },

      // Evento en edición
      editingEvent: {
        id: null,
        titulo: '',
        descripcion: '',
        fecha_inicio: '',
        fecha_fin: '',
        tipo_evento: ''
      },

      // Array de eventos del backend
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
      return this.userInfo.role === 'admin'
    },

    upcomingEvents () {
      const now = new Date()
      const futureEvents = this.events
        .filter(event => new Date(event.start) > now)
        .sort((a, b) => new Date(a.start) - new Date(b.start))
      return futureEvents.slice(0, 5) // Mostrar solo los próximos 5
    },

    filteredEvents () {
      let filtered = [...this.events]

      if (this.eventsFilter.trim()) {
        const searchTerm = this.eventsFilter.toLowerCase().trim()
        filtered = filtered.filter(event =>
          event.title.toLowerCase().includes(searchTerm) ||
          (event.extendedProps?.description || '').toLowerCase().includes(searchTerm)
        )
      }

      if (this.eventsTypeFilter) {
        filtered = filtered.filter(event =>
          event.extendedProps?.type === this.eventsTypeFilter
        )
      }

      return filtered.sort((a, b) => new Date(a.start) - new Date(b.start))
    },

    isFormValid () {
      return this.newEvent.titulo.trim() && 
             this.newEvent.fecha_inicio && 
             this.newEvent.tipo_evento &&
             (!this.newEvent.fecha_fin || new Date(this.newEvent.fecha_inicio) < new Date(this.newEvent.fecha_fin))
    },

    isEditFormValid () {
      return this.editingEvent.titulo.trim() && 
             this.editingEvent.fecha_inicio && 
             this.editingEvent.tipo_evento &&
             (!this.editingEvent.fecha_fin || new Date(this.editingEvent.fecha_inicio) < new Date(this.editingEvent.fecha_fin))
    }
  },

  async mounted () {
    this.startAutoSlide()
    await this.loadUserInfo()
    await this.loadDashboardStats()
    await this.loadEvents()
    this.initializeCalendarSize()
  },

  beforeUnmount () {
    this.stopAutoSlide()
  },

  methods: {
    // ⭐ NUEVOS MÉTODOS PARA CONECTAR CON EL BACKEND
    
    async loadUserInfo() {
      try {
        const token = localStorage.getItem('access_token')
        if (!token) {
          this.$router.push('/login')
          return
        }

        const response = await axios.get('/auth/users/token/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })

        this.userInfo = {
          name: response.data.name || response.data.username || 'Usuario',
          role: response.data.tipo_user || 'user'
        }

        console.log('User info loaded:', this.userInfo)
      } catch (error) {
        console.error('Error loading user info:', error)
        if (error.response?.status === 401) {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          this.$router.push('/login')
        }
      }
    },

    async loadDashboardStats() {
      try {
        const token = localStorage.getItem('access_token')
        if (!token) return

        const response = await axios.get('/events/stats/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })

        this.dashboardStats = response.data
        console.log('Dashboard stats loaded:', this.dashboardStats)
      } catch (error) {
        console.error('Error loading dashboard stats:', error)
      }
    },

    async loadEvents () {
      try {
        this.loading = true
        const token = localStorage.getItem('access_token')
        
        if (!token) {
          this.$router.push('/login')
          return
        }

        console.log('Loading events from backend...')
        
        const response = await axios.get('/events/50/', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })

        console.log('Events API response:', response.data)

        // Transformar eventos del backend al formato del calendario
        const backendEvents = response.data.results || response.data
        this.events = backendEvents.map(event => this.transformEventFromAPI(event))

        console.log('Events transformed for calendar:', this.events.length)
        this.updateCalendarEvents()
        
      } catch (error) {
        console.error('Error loading events:', error)
        
        if (error.response?.status === 401) {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          this.$router.push('/login')
        } else {
          this.showError('Error al cargar los eventos. Por favor, recarga la página.')
        }
      } finally {
        this.loading = false
      }
    },

    transformEventFromAPI (apiEvent) {
      return {
        id: apiEvent.id.toString(),
        title: apiEvent.titulo,
        start: apiEvent.fecha_inicio,
        end: apiEvent.fecha_fin,
        color: this.getEventColor(apiEvent.tipo_evento),
        textColor: '#FFFFFF',
        extendedProps: {
          description: apiEvent.descripcion,
          type: apiEvent.tipo_evento,
          created_by: apiEvent.creado_por,
          created_at: apiEvent.fecha_creacion
        }
      }
    },

    async createEvent () {
      try {
        this.loading = true

        // Validaciones mejoradas
        if (!this.newEvent.titulo.trim()) {
          this.showError('El título del evento es obligatorio')
          return
        }

        if (this.newEvent.titulo.length > 100) {
          this.showError('El título no puede exceder 100 caracteres')
          return
        }

        if (this.newEvent.descripcion.length > 500) {
          this.showError('La descripción no puede exceder 500 caracteres')
          return
        }

        if (this.newEvent.fecha_fin && new Date(this.newEvent.fecha_inicio) >= new Date(this.newEvent.fecha_fin)) {
          this.showError('La fecha de fin debe ser posterior a la fecha de inicio')
          return
        }

        if (new Date(this.newEvent.fecha_inicio) < new Date()) {
          this.showError('No puedes crear eventos en fechas pasadas')
          return
        }

        const token = localStorage.getItem('access_token')
        console.log('Creating event:', this.newEvent)

        const response = await axios.post('/events/', {
          titulo: this.newEvent.titulo.trim(),
          descripcion: this.newEvent.descripcion.trim(),
          fecha_inicio: this.newEvent.fecha_inicio,
          fecha_fin: this.newEvent.fecha_fin || null,
          tipo_evento: this.newEvent.tipo_evento
        }, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        console.log('Event created successfully:', response.data)

        // Recargar eventos y estadísticas
        await this.loadEvents()
        await this.loadDashboardStats()
        
        this.resetNewEventForm()
        this.closeCreateEventModal()
        this.showSuccess('Evento creado exitosamente')
        
      } catch (error) {
        console.error('Error creating event:', error)
        
        let errorMessage = 'Error al crear el evento.'
        
        if (error.response?.status === 403) {
          errorMessage = 'No tienes permisos para crear eventos.'
        } else if (error.response?.status === 400) {
          const details = error.response.data.details
          if (details) {
            const firstError = Object.values(details)[0]
            errorMessage = Array.isArray(firstError) ? firstError[0] : firstError
          } else {
            errorMessage = error.response.data.error || 'Datos inválidos.'
          }
        } else if (error.response?.status === 401) {
          errorMessage = 'Sesión expirada. Por favor, inicia sesión nuevamente.'
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          this.$router.push('/login')
        }
        
        this.showError(errorMessage)
      } finally {
        this.loading = false
      }
    },

    async updateEvent () {
      try {
        this.loading = true

        // Validaciones
        if (!this.editingEvent.titulo.trim()) {
          this.showError('El título del evento es obligatorio')
          return
        }

        if (this.editingEvent.titulo.length > 100) {
          this.showError('El título no puede exceder 100 caracteres')
          return
        }

        if (this.editingEvent.descripcion.length > 500) {
          this.showError('La descripción no puede exceder 500 caracteres')
          return
        }

        if (this.editingEvent.fecha_fin && new Date(this.editingEvent.fecha_inicio) >= new Date(this.editingEvent.fecha_fin)) {
          this.showError('La fecha de fin debe ser posterior a la fecha de inicio')
          return
        }

        const token = localStorage.getItem('access_token')
        console.log('Updating event:', this.editingEvent)

        const response = await axios.put(`/events/${this.editingEvent.id}/`, {
          titulo: this.editingEvent.titulo.trim(),
          descripcion: this.editingEvent.descripcion.trim(),
          fecha_inicio: this.editingEvent.fecha_inicio,
          fecha_fin: this.editingEvent.fecha_fin || null,
          tipo_evento: this.editingEvent.tipo_evento
        }, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        console.log('Event updated successfully:', response.data)

        // Recargar eventos y estadísticas
        await this.loadEvents()
        await this.loadDashboardStats()
        
        this.closeEditEventModal()
        this.showSuccess('Evento actualizado exitosamente')
        
      } catch (error) {
        console.error('Error updating event:', error)
        this.handleEventError(error, 'actualizar')
      } finally {
        this.loading = false
      }
    },

    async deleteEvent () {
      try {
        this.loading = true
        const token = localStorage.getItem('access_token')

        console.log('Deleting event:', this.eventToDelete.id)

        await axios.delete(`/events/${this.eventToDelete.id}/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        })

        console.log('Event deleted successfully')

        // Recargar eventos y estadísticas
        await this.loadEvents()
        await this.loadDashboardStats()
        
        this.closeDeleteConfirmModal()
        this.showSuccess('Evento eliminado exitosamente')
        
      } catch (error) {
        console.error('Error deleting event:', error)
        this.handleEventError(error, 'eliminar')
      } finally {
        this.loading = false
      }
    },

    handleEventError(error, action) {
      let errorMessage = `Error al ${action} el evento.`
      
      if (error.response?.status === 403) {
        errorMessage = `No tienes permisos para ${action} eventos.`
      } else if (error.response?.status === 404) {
        errorMessage = 'El evento no fue encontrado.'
      } else if (error.response?.status === 400) {
        const details = error.response.data.details
        if (details) {
          const firstError = Object.values(details)[0]
          errorMessage = Array.isArray(firstError) ? firstError[0] : firstError
        } else {
          errorMessage = error.response.data.error || 'Datos inválidos.'
        }
      } else if (error.response?.status === 401) {
        errorMessage = 'Sesión expirada. Por favor, inicia sesión nuevamente.'
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        this.$router.push('/login')
      }
      
      this.showError(errorMessage)
    },

    // Actualizar métodos existentes para usar nombres de campos correctos
    openEditEvent (event) {
      console.log(event)
      this.editingEvent = {
        id: event.id,
        titulo: event.title,
        descripcion: event.extendedProps?.description || '',
        fecha_inicio: this.formatDateForInput(event.start),
        fecha_fin: event.end ? this.formatDateForInput(event.end) : '',
        tipo_evento: event.extendedProps?.type || ''
      }
      this.showEditEventModal = true
    },

    handleDateClick (info) {
      if (this.isAdmin) {
        const selectedDate = new Date(info.date)
        selectedDate.setHours(9, 0)
        this.newEvent.fecha_inicio = this.formatDateForInput(selectedDate)
        this.showCreateEventModal = true
      }
    },

    resetNewEventForm () {
      this.newEvent = {
        titulo: '',
        descripcion: '',
        fecha_inicio: '',
        fecha_fin: '',
        tipo_evento: ''
      }
    },

    resetEditingEvent () {
      this.editingEvent = {
        id: null,
        titulo: '',
        descripcion: '',
        fecha_inicio: '',
        fecha_fin: '',
        tipo_evento: ''
      }
    },

    // Mantener métodos existentes del carrusel...
    startAutoSlide () {
      this.autoSlideInterval = setInterval(() => {
        this.nextSlide()
      }, 6000)
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

    // Mantener métodos de utilidad existentes...
    initializeCalendarSize () {
      this.$nextTick(() => {
        if (this.$refs.fullCalendar) {
          this.$refs.fullCalendar.getApi().updateSize()
        }
      })
    },

    updateCalendarEvents () {
      this.calendarOptions.events = [...this.events]
      this.$nextTick(() => {
        if (this.$refs.fullCalendar) {
          this.$refs.fullCalendar.getApi().refetchEvents()
        }
      })
    },

    viewEventDetails (event) {
      this.selectedEvent = event
      this.showEventDetailsModal = true
    },

    openEditEventFromDetails (event) {
      console.log(event)
      this.closeEventDetailsModal()
      this.openEditEvent(event)
    },

    confirmDeleteEventFromDetails (Event) {
      this.closeEventDetailsModal()
      this.confirmDeleteEvent(Event)
    },

    closeEventDetailsModal () {
      this.showEventDetailsModal = false
      this.selectedEvent = null
    },

    confirmDeleteEvent (event) {
      this.eventToDelete = event
      this.showDeleteConfirmModal = true
    },

    handleEventClick (info) {
      this.viewEventDetails(info.event)
    },

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

    formatEventDateShort (date) {
      if (!date) return ''
      const d = new Date(date)
      const now = new Date()
      const isToday = d.toDateString() === now.toDateString()
      const isTomorrow = d.toDateString() === new Date(now.getTime() + 24 * 60 * 60 * 1000).toDateString()
      
      if (isToday) {
        return d.toLocaleTimeString('es-CO', {
          hour: '2-digit',
          minute: '2-digit'
        })
      } else if (isTomorrow) {
        return 'Mañana ' + d.toLocaleTimeString('es-CO', {
          hour: '2-digit',
          minute: '2-digit'
        })
      } else {
        return d.toLocaleDateString('es-CO', {
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        })
      }
    },

    isToday (date) {
      if (!date) return false
      const d = new Date(date)
      const today = new Date()
      return d.toDateString() === today.toDateString()
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
    }
  }
}
</script>

<style lang="css" scoped>
@import '../../styles/dashboard_home.css';
</style>