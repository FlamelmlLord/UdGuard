<template>
    <v-container fluid>
      <!-- Profile Section -->
      <v-card class="mb-3">
        <v-card-title>
          <v-row align="center" justify="space-between">
            <v-col cols="12" sm="auto">
              <span class="text-h6">Mi Perfil</span>
            </v-col>
          </v-row>
        </v-card-title>
        
        <v-card-text>
          <v-row>
            <v-col cols="12" md="3" class="text-center">
              <v-avatar size="120" class="mb-3">
                <span class="text-h4">{{ getInitials(getFullName()) }}</span>
              </v-avatar>
              <h3>{{ getFullName() }}</h3>
              <p class="text-subtitle-1 text--secondary">{{ currentUser.email }}</p>
            </v-col>
            <v-col cols="12" md="9">
              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field
                    label="Fecha de registro"
                    :value="formatDate(currentUser.date_joined)"
                    readonly
                    outlined
                    dense
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    label="Último acceso"
                    :value="formatDate(currentUser.last_login)"
                    readonly
                    outlined
                    dense
                  ></v-text-field>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Users Table Section -->
      <v-card>
        <v-card-title>
          <v-row align="center" justify="space-between">
            <v-col cols="12" sm="auto">
              <span class="text-h6">Gestión de usuarios</span>
            </v-col>
            <v-col cols="12" sm="auto" class="d-flex align-center gap-3">
              <!-- Botón Registrar Usuario -->
              <v-btn
                class="register-user-btn"
                @click="openRegisterDialog"
                elevation="2"
              >
                <v-icon left>mdi-account-plus</v-icon>
                Registrar Usuario
              </v-btn>

              <!-- Campo de búsqueda -->
              <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                label="Buscar"
                single-line
                hide-details
                dense
                class="search-field"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-card-title>

        <!-- ⭐ TABLA CON PAGINACIÓN SIMPLIFICADA -->
        <v-data-table
          :headers="headers"
          :items="users"
          :search="search"
          :items-per-page="itemsPerPage"
          :loading="loading"
          :footer-props="{
            'items-per-page-text': '',
            'items-per-page-options': [],
            'show-current-page': false,
            'show-first-last-page': true,
            'disable-items-per-page': true
          }"
          class="elevation-1"
          loading-text="Cargando usuarios..."
          no-data-text="No hay usuarios disponibles"
        >
          <!-- ⭐ TEMPLATE PARA AVATARES CON IMÁGENES SEGÚN ROL -->
          <template v-slot:[`item.avatar`]="{ item }">
            <v-avatar size="40" class="role-avatar">
              <img 
                :src="getRoleImage(item.tipo_user)" 
                :alt="`Avatar ${getRoleDisplayName(item.tipo_user)}`"
                class="role-image"
              >
            </v-avatar>
          </template>

          <template v-slot:[`item.status`]="{ item }">
            <div class="status-indicator" :class="item.status === 'Activo' ? 'active' : 'inactive'">
              <v-icon 
                small 
                :color="item.status === 'Activo' ? 'success' : 'error'"
                class="mr-1"
              >
                {{ item.status === 'Activo' ? 'mdi-check-circle' : 'mdi-cancel' }}
              </v-icon>
              {{ item.status }}
            </div>
          </template>

          <template v-slot:[`item.tipo_user`]="{ item }">
            <v-chip
              :color="getRoleColor(item.tipo_user)"
              small
              class="font-weight-bold"
              label
            >
              {{ getRoleDisplayName(item.tipo_user) }}
            </v-chip>
          </template>

          <template v-slot:[`item.actions`]="{ item }">
            <div class="d-flex justify-center gap-2">
              <!-- ⭐ BOTÓN EDITAR -->
              <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    icon
                    small
                    v-bind="attrs"
                    v-on="on"
                    @click="editUser(item)"
                    class="action-btn edit-btn"
                  >
                    <v-icon small color="primary">mdi-pencil</v-icon>
                  </v-btn>
                </template>
                <span>Editar Usuario</span>
              </v-tooltip>

              <!-- ⭐ BOTÓN CAMBIAR ESTADO (ACTIVAR/DESACTIVAR) -->
              <v-tooltip bottom>
                <template v-slot:activator="{ on, attrs }">
                  <v-btn
                    icon
                    small
                    v-bind="attrs"
                    v-on="on"
                    @click="toggleUserStatus(item)"
                    class="action-btn"
                    :class="item.status === 'Activo' ? 'disable-btn' : 'enable-btn'"
                  >
                    <v-icon 
                      small 
                      :color="item.status === 'Activo' ? 'warning' : 'success'"
                    >
                      {{ item.status === 'Activo' ? 'mdi-account-off' : 'mdi-account-check' }}
                    </v-icon>
                  </v-btn>
                </template>
                <span>{{ item.status === 'Activo' ? 'Desactivar Usuario' : 'Activar Usuario' }}</span>
              </v-tooltip>
            </div>
          </template>
        </v-data-table>

        <!-- ⭐ PAGINACIÓN PERSONALIZADA (OPCIONAL) -->
        <template v-slot:footer="{ props }">
          <div class="custom-pagination">
            <v-pagination
              v-model="currentPage"
              :length="Math.ceil(props.pagination.itemsLength / itemsPerPage)"
              :total-visible="7"
              circle
              color="primary"
            ></v-pagination>
          </div>
        </template>
      </v-card>

      <!-- ⭐ MODAL DE EDICIÓN CON AVATARES POR ROL -->
      <v-dialog v-model="dialogEdit" max-width="700px" persistent>
        <v-card class="edit-user-modal">
          <!-- Header del modal -->
          <div class="edit-modal-header">
            <div class="header-content">
              <div class="header-icon">
                <v-icon size="32" color="white">mdi-account-edit</v-icon>
              </div>
              <div>
                <h2 class="modal-title">Editar Usuario</h2>
                <p class="modal-subtitle">Modifica la información del usuario seleccionado</p>
              </div>
            </div>
          </div>

          <!-- Información del usuario -->
          <v-card-text class="pa-0">
            <div class="user-info-section">
              <div class="user-avatar-section">
                <v-avatar size="80" class="user-modal-avatar">
                  <img 
                    :src="getRoleImage(editingUser.tipo_user)" 
                    :alt="`Avatar ${getRoleDisplayName(editingUser.tipo_user)}`"
                  >
                </v-avatar>
                <div>
                  <h3 class="user-display-name">{{ editingUser.name }}</h3>
                  <p class="user-username">@{{ editingUser.username }}</p>
                  <v-chip
                    :color="getRoleColor(editingUser.tipo_user)"
                    small
                    class="font-weight-bold"
                    label
                  >
                    {{ getRoleDisplayName(editingUser.tipo_user) }}
                  </v-chip>
                </div>
              </div>
            </div>

            <!-- Formulario de edición -->
            <v-form ref="editForm" v-model="editFormValid" class="pa-6">
              <div class="form-section">
                <h4 class="section-title">
                  <v-icon color="primary" class="mr-2">mdi-account-details</v-icon>
                  Credenciales
                </h4>
                
                <v-row>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="editingUser.first_name"
                      label="Nombre"
                      outlined
                      dense
                      class="editable-field"
                      :rules="[v => !!v || 'El nombre es requerido']"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="editingUser.last_name"
                      label="Apellido"
                      outlined
                      dense
                      class="editable-field"
                      :rules="[v => !!v || 'El apellido es requerido']"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field
                      v-model="editingUser.email"
                      label="Correo Electrónico"
                      outlined
                      dense
                      class="editable-field"
                      :rules="emailRules"
                    ></v-text-field>
                  </v-col>
                  
                  <!-- ⭐ NUEVA SECCIÓN DE CONTRASEÑA -->
                  <v-col cols="12">
                    <v-divider class="mb-4"></v-divider>
                    <h5 class="password-section-title">
                      <v-icon color="warning" size="18" class="mr-2">mdi-lock-reset</v-icon>
                      Cambiar Contraseña (Opcional)
                    </h5>
                    <p class="password-help-text">
                      Deje los campos vacíos si no desea cambiar la contraseña
                    </p>
                  </v-col>
                  
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="editingUser.password"
                      label="Nueva Contraseña"
                      :type="showPassword ? 'text' : 'password'"
                      outlined
                      dense
                      class="password-field"
                      :rules="passwordRules"
                      placeholder="Ingrese nueva contraseña (opcional)"
                      @input="validatePasswordMatch"
                    >
                      <template v-slot:append>
                        <v-btn
                          icon
                          small
                          @click="showPassword = !showPassword"
                          class="password-toggle-btn"
                        >
                          <v-icon size="20" :color="showPassword ? 'primary' : 'grey'">
                            {{ showPassword ? 'mdi-eye-off' : 'mdi-eye' }}
                          </v-icon>
                        </v-btn>
                      </template>
                    </v-text-field>
                  </v-col>
                  
                  <v-col cols="12" sm="6">
                    <v-text-field
                      v-model="editingUser.confirmPassword"
                      label="Confirmar Nueva Contraseña"
                      :type="showConfirmPassword ? 'text' : 'password'"
                      outlined
                      dense
                      class="password-field"
                      :rules="confirmPasswordRules"
                      placeholder="Confirme la nueva contraseña"
                      @input="validatePasswordMatch"
                    >
                      <template v-slot:append>
                        <v-btn
                          icon
                          small
                          @click="showConfirmPassword = !showConfirmPassword"
                          class="password-toggle-btn"
                        >
                          <v-icon size="20" :color="showConfirmPassword ? 'primary' : 'grey'">
                            {{ showConfirmPassword ? 'mdi-eye-off' : 'mdi-eye' }}
                          </v-icon>
                        </v-btn>
                      </template>
                    </v-text-field>
                  </v-col>
                </v-row>
              </div>

              <div class="form-section">
                <h4 class="section-title">
                  <v-icon color="grey" class="mr-2">mdi-lock</v-icon>
                  Información del Sistema (Solo Lectura)
                </h4>
                
                <v-row>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      :value="editingUser.username"
                      label="Usuario"
                      outlined
                      dense
                      readonly
                      class="readonly-field"
                    ></v-text-field>
                  </v-col>
                  <v-col cols="12" sm="6">
                    <v-text-field
                      :value="formatDate(editingUser.date_joined)"
                      label="Fecha de Registro"
                      outlined
                      dense
                      readonly
                      class="readonly-field"
                    ></v-text-field>
                  </v-col>
                </v-row>
              </div>
            </v-form>
          </v-card-text>

          <!-- Acciones del modal -->
          <div class="modal-actions">
            <v-row>
              <v-col cols="12" class="d-flex justify-end gap-3">
                <v-btn
                  @click="closeEditDialog"
                  text
                  class="cancel-btn"
                  :disabled="saving"
                >
                  Cancelar
                </v-btn>
                <v-btn
                  @click="saveUserChanges"
                  class="save-btn"
                  :loading="saving"
                  :disabled="!editFormValid"
                >
                  Guardar Cambios
                </v-btn>
              </v-col>
            </v-row>
          </div>
        </v-card>
      </v-dialog>

      <!-- Dialog para registrar usuario -->
      <v-dialog v-model="dialogRegister" max-width="1000px" persistent>
        <v-card class="register-dialog-card">
          <div class="register-dialog-header">
            <v-card-title class="white--text">
              <v-icon left color="white" size="32">mdi-account-plus</v-icon>
              <span class="text-h5 font-weight-bold">Registrar Nuevo Usuariossss</span>
            </v-card-title>
          </div>
          
          <v-card-text class="pa-0">
            <RegisterUser 
              @user-registered="handleUserRegistered" 
              @cancel="closeRegisterDialog"
            />
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-container>
  </template>

<script>
import axios from '../../plugins/Axios'
import RegisterUser from './RegisterUser.vue'

export default {
  name: 'UserSettings',
  components: {
    RegisterUser
  },

  data: () => ({
    search: '',
    loading: false,
    saving: false,
    dialogEdit: false,
    dialogRegister: false,
    editFormValid: false,
    itemsPerPage: 8,
    currentPage: 1,
    totalUsers: 0,
    currentUser: {
      date_joined: '',
      last_login: '',
      name: '',
      email: ''
    },
    editingUser: {
      id: null,
      name: '',
      username: '',
      first_name: '',
      last_name: '',
      email: '',
      tipo_user: '',
      status: '',
      date_joined: '',
      password: '', // AGREGAR CAMPO PASSWORD
      confirmPassword: '' // AGREGAR CONFIRMACIÓN
    },
    showPassword: false, // AGREGAR CONTROL VISIBILIDAD
    showConfirmPassword: false, // AGREGAR CONTROL VISIBILIDAD
    headers: [
      { text: '', value: 'avatar', sortable: false, width: '60px', align: 'center' },
      { text: 'Nombre', value: 'name', sortable: true },
      { text: 'Usuario', value: 'username', sortable: true },
      { text: 'Email', value: 'email', sortable: true },
      { text: 'Estado', value: 'status', sortable: true, align: 'center' },
      { text: 'Tipo', value: 'tipo_user', sortable: true, align: 'center' },
      { text: 'Acciones', value: 'actions', sortable: false, width: '120px', align: 'center' }
    ],
    users: [],
    emailRules: [
      v => !!v || 'El email es requerido',
      v => /.+@.+\..+/.test(v) || 'El email debe ser válido'
    ],
    // ⭐ AGREGAR REGLAS DE VALIDACIÓN PARA CONTRASEÑA
    passwordRules: [
      v => !v || v.length >= 8 || 'La contraseña debe tener al menos 8 caracteres',
      v => !v || /[A-Z]/.test(v) || 'Debe contener al menos una mayúscula',
      v => !v || /[a-z]/.test(v) || 'Debe contener al menos una minúscula',
      v => !v || /[0-9]/.test(v) || 'Debe contener al menos un número',
      v => !v || /[^a-zA-Z0-9]/.test(v) || 'Debe contener al menos un carácter especial'
    ]
  }),

  computed: {
    // ⭐ AGREGAR REGLAS DINÁMICAS PARA CONFIRMACIÓN DE CONTRASEÑA
    confirmPasswordRules() {
      return [
        v => !this.editingUser.password || !!v || 'Debe confirmar la nueva contraseña',
        v => !this.editingUser.password || v === this.editingUser.password || 'Las contraseñas no coinciden'
      ]
    }
  },

  async mounted () {
    await this.fetchCurrentUser()
    await this.fetchUsers()
  },

  methods: {
    // ⭐ CARGAR USUARIO ACTUAL
    async fetchCurrentUser () {
      try {
        console.log('Fetching current user data...')
        const response = await axios.get('auth/users/token/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        })
        console.log('Current user API response:', response.data)
        
        this.currentUser = {
          date_joined: response.data.date_joined || '',
          last_login: response.data.last_login || '',
          name: response.data.name || '',
          email: response.data.email || ''
        }
      } catch (error) {
        console.error('Error fetching current user:', error)
        if (this.$swal) {
          this.$swal({
            title: 'Error',
            text: 'No se pudieron cargar los datos del usuario',
            icon: 'error',
            confirmButtonText: 'OK'
          })
        }
      }
    },

    // ⭐ CARGAR LISTA DE USUARIOS - CON DEBUGGING MEJORADO
    async fetchUsers () {
      this.loading = true
      try {
        console.log('Fetching users from API...')
        
        const response = await axios.get('/users/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          },
          params: {
            page_size: 100
          }
        })
        
        console.log('Users API response:', response.data)
        
        let usersData = []
        let totalCount = 0
        
        if (response.data.results) {
          usersData = response.data.results
          totalCount = response.data.count || response.data.results.length
        } else if (Array.isArray(response.data)) {
          usersData = response.data
          totalCount = response.data.length
        } else {
          usersData = []
          totalCount = 0
        }

        console.log('Raw users data from backend:', usersData)

        // MAPEAR DATOS PRESERVANDO EXACTAMENTE LOS CAMPOS DEL BACKEND
        this.users = usersData.map(user => {
          console.log(`Processing user ${user.id}:`, {
            first_name: user.first_name,
            last_name: user.last_name,
            name: user.name
          })
          
          return {
            id: user.id,
            name: user.name || 'Sin nombre', // USAR LA PROPIEDAD NAME DEL BACKEND
            username: user.username,
            email: user.email,
            first_name: user.first_name || '', // MANTENER EXACTO DEL BACKEND
            last_name: user.last_name || '', // MANTENER EXACTO DEL BACKEND
            status: user.status || (user.is_active ? 'Activo' : 'Inactivo'),
            is_active: user.is_active !== undefined ? user.is_active : true,
            tipo_user: user.tipo_user || 'user',
            date_joined: user.date_joined || ''
          }
        })
        
        this.totalUsers = totalCount
        
        console.log(`Users loaded successfully: ${this.users.length} users`)
        console.log('Final mapped users:', this.users)
        
      } catch (error) {
        console.error('Error fetching users:', error)
        
        if (this.$swal) {
          this.$swal({
            title: 'Error',
            text: 'No se pudieron cargar los usuarios',
            icon: 'error',
            confirmButtonText: 'OK'
          })
        }
      } finally {
        this.loading = false
      }
    },

    // NUEVO MÉTODO: CAMBIAR ESTADO DEL USUARIO
    async toggleUserStatus (user) {
      try {
        const action = user.status === 'Activo' ? 'desactivar' : 'activar'
        const actionPast = user.status === 'Activo' ? 'desactivado' : 'activado'
        
        const confirmed = await this.$swal({
          title: `¿${action.charAt(0).toUpperCase() + action.slice(1)} usuario?`,
          text: `¿Estás seguro de que deseas ${action} a "${user.name}"?`,
          icon: user.status === 'Activo' ? 'warning' : 'question',
          showCancelButton: true,
          confirmButtonText: `Sí, ${action}`,
          cancelButtonText: 'Cancelar',
          confirmButtonColor: user.status === 'Activo' ? '#f56565' : '#48bb78',
          cancelButtonColor: '#3085d6'
        })

        if (confirmed.isConfirmed) {
          console.log(`Toggling user status:`, user.id, `from ${user.status}`)
          
          // ⭐ ACTUALIZAR LA URL PARA USAR LA NUEVA RUTA
          const response = await axios.delete(`/users/manage/${user.id}/`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`
            }
          })

          console.log('User status toggled successfully:', response.data)

          // ACTUALIZAR LISTA LOCAL
          const userIndex = this.users.findIndex(u => u.id === user.id)
          if (userIndex !== -1) {
            this.users[userIndex].is_active = response.data.user.is_active
            this.users[userIndex].status = response.data.user.status
          }

          this.$swal({
            title: '¡Estado cambiado!',
            text: `El usuario "${user.name}" ha sido ${actionPast} correctamente`,
            icon: 'success',
            confirmButtonText: 'OK'
          })
        }
      } catch (error) {
        console.error('Error toggling user status:', error)
        
        let errorMessage = 'No se pudo cambiar el estado del usuario'
        
        if (error.response?.status === 403) {
          errorMessage = 'No tienes permisos para cambiar el estado de usuarios'
        } else if (error.response?.status === 404) {
          errorMessage = 'Usuario no encontrado'
        }
        
        this.$swal({
          title: 'Error',
          text: errorMessage,
          icon: 'error',
          confirmButtonText: 'OK'
        })
      }
    },

    // ⭐ MÉTODOS DE UTILIDAD
    formatDate (dateString) {
      if (!dateString) return 'No disponible'
      const date = new Date(dateString)
      const options = {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
      }
      return date.toLocaleDateString('es-CO', options)
    },

    getFullName () {
      const fullName = `${this.currentUser.name}`.trim()
      return fullName || this.currentUser.username || 'Usuario'
    },

    getInitials (name) {
      if (!name) return '??'
      const words = name.trim().split(' ')
      if (words.length >= 2) {
        return (words[0][0] + words[1][0]).toUpperCase()
      }
      return name.substring(0, 2).toUpperCase()
    },

    // ⭐ MÉTODO PARA OBTENER IMAGEN SEGÚN ROL
    getRoleImage (userType) {
      const images = {
        admin: require('@/assets/Adm.png'),
        user: require('@/assets/Colaborador.png')
      }
      return images[userType] || images.user // Fallback a colaborador
    },

    // SOLO 2 TIPOS DE USUARIO: ADMINISTRADOR Y COLABORADOR
    getRoleColor (userType) {
      const colors = {
        admin: 'primary',
        user: 'orange'
      }
      return colors[userType] || 'grey'
    },

    getRoleDisplayName (userType) {
      const names = {
        admin: 'Administrador',
        user: 'Colaborador'
      }
      return names[userType] || 'Colaborador'
    },

    // ABRIR MODAL DE EDICIÓN - CORREGIDO PARA USAR DATOS ORIGINALES
    editUser (user) {
      console.log('Opening edit modal for user:', user)
      console.log('User first_name from backend:', user.first_name)
      console.log('User last_name from backend:', user.last_name)
      
      this.editingUser = {
        id: user.id,
        name: user.name,
        username: user.username,
        first_name: user.first_name || '',
        last_name: user.last_name || '',
        email: user.email,
        tipo_user: user.tipo_user,
        status: user.status,
        date_joined: user.date_joined,
        password: '', // INICIALIZAR VACÍO
        confirmPassword: '' // INICIALIZAR VACÍO
      }
      
      // RESETEAR VISIBILIDAD DE CONTRASEÑAS
      this.showPassword = false
      this.showConfirmPassword = false
      
      console.log('Editing user data:', this.editingUser)
      this.dialogEdit = true
    },

    // GUARDAR CAMBIOS AL BACKEND - VERSIÓN MEJORADA
    // GUARDAR CAMBIOS - CON ACTUALIZACIÓN FORZADA DE LA TABLA
    async saveUserChanges () {
      if (!this.$refs.editForm.validate()) return

      this.saving = true
      try {
        console.log('Saving user changes:', this.editingUser)
        
        const updateData = {
          first_name: this.editingUser.first_name.trim(),
          last_name: this.editingUser.last_name.trim(),
          email: this.editingUser.email.trim()
        }
        
        // ⭐ INCLUIR CONTRASEÑA SOLO SI SE PROPORCIONÓ
        if (this.editingUser.password && this.editingUser.password.trim()) {
          if (this.editingUser.password !== this.editingUser.confirmPassword) {
            this.$swal({
              title: 'Error de Validación',
              text: 'Las contraseñas no coinciden',
              icon: 'error',
              confirmButtonText: 'OK'
            })
            return
          }
          updateData.password = this.editingUser.password.trim()
        }
        
        console.log('Sending update data:', { ...updateData, password: updateData.password ? '[HIDDEN]' : undefined })
        
        const response = await axios.patch(`/users/manage/${this.editingUser.id}/`, updateData, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        })

        console.log('User updated successfully:', response.data)

        // ⭐ ACTUALIZAR LISTA LOCAL
        const userIndex = this.users.findIndex(u => u.id === this.editingUser.id)
        if (userIndex !== -1) {
          const updatedUserData = response.data
          
          this.users[userIndex] = {
            ...this.users[userIndex],
            first_name: updatedUserData.first_name || this.editingUser.first_name,
            last_name: updatedUserData.last_name || this.editingUser.last_name,
            name: updatedUserData.name || `${this.editingUser.first_name} ${this.editingUser.last_name}`.trim(),
            email: updatedUserData.email || this.editingUser.email
          }
          
          this.$forceUpdate()
          this.$set(this.users, userIndex, this.users[userIndex])
        }

        this.closeEditDialog()
        
        // ⭐ MENSAJE ESPECÍFICO SI SE CAMBIÓ LA CONTRASEÑA
        const successMessage = updateData.password 
          ? 'Usuario actualizado correctamente. La contraseña ha sido cambiada.'
          : 'Usuario actualizado correctamente'
        
        this.$swal({
          title: '¡Éxito!',
          text: successMessage,
          icon: 'success',
          confirmButtonText: 'OK'
        })

      } catch (error) {
        console.error('Error updating user:', error)
        console.error('Error response data:', error.response?.data)
        
        let errorMessage = 'No se pudo actualizar el usuario'
        
        if (error.response?.status === 400) {
          errorMessage = 'Datos inválidos. Verifique la información ingresada.'
          
          // ⭐ MANEJO ESPECÍFICO DE ERRORES DE CONTRASEÑA
          if (error.response.data && error.response.data.password) {
            const passwordErrors = Array.isArray(error.response.data.password) 
              ? error.response.data.password.join(', ')
              : error.response.data.password
            errorMessage = `Error en la contraseña: ${passwordErrors}`
          }
          
          if (error.response.data) {
            console.error('Validation errors:', error.response.data)
          }
        } else if (error.response?.status === 401) {
          errorMessage = 'Sesión expirada. Por favor, inicia sesión nuevamente.'
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          this.$router.push('/login')
        } else if (error.response?.status === 403) {
          errorMessage = 'No tienes permisos para editar usuarios.'
        } else if (error.response?.status === 404) {
          errorMessage = 'Usuario no encontrado.'
        }
        
        this.$swal({
          title: 'Error',
          text: errorMessage,
          icon: 'error',
          confirmButtonText: 'OK'
        })
      } finally {
        this.saving = false
      }
    },

    // CERRAR MODAL - LIMPIAR CAMPOS DE CONTRASEÑA
    closeEditDialog () {
      this.dialogEdit = false
      this.editingUser = {
        id: null,
        name: '',
        username: '',
        first_name: '',
        last_name: '',
        email: '',
        tipo_user: '',
        status: '',
        date_joined: '',
        password: '', // LIMPIAR
        confirmPassword: '' // LIMPIAR
      }
      
      // ⭐ RESETEAR VISIBILIDAD
      this.showPassword = false
      this.showConfirmPassword = false
    },

    // ⭐ MÉTODOS PARA REGISTRO
    openRegisterDialog () {
      this.dialogRegister = true
    },

    closeRegisterDialog () {
      this.dialogRegister = false
    },

    async handleUserRegistered (userData) {
      try {
        console.log('User registered successfully:', userData)
        this.closeRegisterDialog()

        this.$swal({
          title: '¡Éxito!',
          text: 'Usuario registrado correctamente',
          icon: 'success',
          confirmButtonText: 'OK'
        })

        // ⭐ RECARGAR LA LISTA DE USUARIOS
        await this.fetchUsers()
      } catch (error) {
        console.error('Error handling user registration:', error)
        this.$swal({
          title: 'Error',
          text: 'Hubo un problema al registrar el usuario',
          icon: 'error',
          confirmButtonText: 'OK'
        })
      }
    }
  }
}
</script>

<style scoped lang="css"> @import '../../styles/dashboard_usersettings.css'; </style>
