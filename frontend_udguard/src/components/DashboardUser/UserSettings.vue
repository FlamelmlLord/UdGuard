<template>
    <v-container fluid>
      <!-- Profile Section -->
      <v-card class="mb-6">
        <v-card-text>
          <v-row align="center">
            <v-col cols="12" sm="3" class="text-center">
              <v-avatar size="150">
              <!--   <v-img
                  src="@/assets/default-avatar.png"
                  alt="User Profile"
                ></v-img> -->
              </v-avatar>
            </v-col>
            <v-col cols="12" sm="9">
              <v-row>
                <v-col cols="12" sm="6">
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-subtitle class="text-caption grey--text">
                        Fecha de registro
                      </v-list-item-subtitle>
                      <v-list-item-title>{{ formatDate(currentUser.date_joined) }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-subtitle class="text-caption grey--text">
                        Nombre
                      </v-list-item-subtitle>
                      <v-list-item-title>{{ getFullName() }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-subtitle class="text-caption grey--text">
                        Último acceso
                      </v-list-item-subtitle>
                      <v-list-item-title>{{ formatDate(currentUser.last_login) }} </v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-subtitle class="text-caption grey--text">
                        E-mail
                      </v-list-item-subtitle>
                      <v-list-item-title>{{ currentUser.email }}</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
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
            <v-col cols="auto">
            <span class="text-h6">Gestion de usuarios</span>
            </v-col>
            <v-col cols="auto">
              <v-text-field
                v-model="search"
                append-icon="mdi-magnify"
                label="Search"
                single-line
                hide-details
                dense
              ></v-text-field>
            </v-col>
          </v-row>
        </v-card-title>

        <v-data-table
          :headers="headers"
          :items="users"
          :search="search"
          :items-per-page="5"
          class="elevation-1"
        >
          <template v-slot:[`item.avatar`]="{ item }">
            <v-avatar size="40">
              <v-img :src="item.avatar"></v-img>
            </v-avatar>
          </template>

          <template v-slot:[`item.status`]="{ item }">
            <span :class="{ 'red--text': item.status === 'Not Logged in' }">
              {{ item.status }}
            </span>
          </template>

          <template v-slot:[`item.roles`]="{ item }">
            <v-chip
              v-for="role in item.roles"
              :key="role"
              :color="getRoleColor(role)"
              small
              class="mr-1"
              label
            >
              {{ role }}
            </v-chip>
          </template>

          <template v-slot:[`item.actions`]="{ item }">
            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  icon
                  small
                  v-bind="attrs"
                  v-on="on"
                  @click="modifyRoles(item)"
                  class="mr-2"
                >
                  <v-icon small>mdi-cog</v-icon>
                </v-btn>
              </template>
              <span>Editar Usuario</span>
            </v-tooltip>

            <v-tooltip bottom>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  icon
                  small
                  v-bind="attrs"
                  v-on="on"
                  @click="removeUser(item)"
                >
                  <v-icon small>mdi-delete</v-icon>
                </v-btn>
              </template>
              <span>Eliminar Usuario</span>
            </v-tooltip>
          </template>
        </v-data-table>
      </v-card>

      <!-- Dialog para modificar roles -->
      <v-dialog v-model="dialogRoles" max-width="500px">
        <v-card>
          <v-card-title>
            <span class="text-h5">Editar Usuario</span>
            <v-spacer></v-spacer>
            <v-btn icon @click="closeDialog">
              <v-icon>mdi-close</v-icon>
            </v-btn>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <c-col cols="12">
                  <!--no editable-->
                </c-col>
              </v-row>
            </v-container>
          </v-card-text>
        </v-card>

      </v-dialog>
    </v-container>
  </template>

<script>
import axios from '../../plugins/Axios'
export default {
  name: 'UserSettings',

  data: () => ({
    search: '',
    dialogRoles: false,
    selectedRoles: [],
    editedItem: null,
    loading: false, // Agregar estado de carga
    currentUser: {
      date_joined: '',
      last_login: '',
      first_name: '',
      last_name: '',
      email: ''
    },
    headers: [
      { text: '', value: 'avatar', sortable: false, width: '50px' },
      { text: 'Name', value: 'name' },
      { text: 'Username', value: 'username' }, // Agregar username
      { text: 'Email', value: 'email' }, // Agregar email
      { text: 'Status', value: 'status' },
      { text: 'User Role', value: 'tipo_user' },
      { text: 'Actions', value: 'actions', sortable: false, width: '100px' }
    ],
    users: [],
    availableRoles: ['Administrador', 'Consultor']
  }),

  methods: {
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
        console.log('Current user data:', this.currentUser)
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
    async fetchUsers () {
      this.loading = true
      try {
        console.log('Fetching users from API...')
        const response = await axios.get('/users/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        })
        console.log('Users API response:', response.data)
        if (Array.isArray(response.data)) {
          this.users = response.data.map(user => ({
            id: user.id,
            name: `${user.first_name || ''} ${user.last_name || ''}`.trim() || user.username,
            username: user.username,
            email: user.email,
            status: user.is_active ? 'Active' : 'Inactive',
            roles: this.mapUserRoles(user.tipo_user)
          }))
        } else {
          this.users = response.data.results || response.data.users || []
        }
        console.log('Users fetched successfully:', this.users)
      } catch (error) {
        console.error('Error fetching users:', error)
        if (this.$swal) {
          this.$swal({
            title: 'Error',
            text: 'No se pudieron cargar los usuarios',
            icon: 'error',
            confirmButtonText: 'OK'
          })
        } else {
          alert('Error al cargar usuarios')
        }
      } finally {
        this.loading = false
      }
    },
    mapUserRoles (userType) {
      // Mapear tipos de usuario del backend a roles del frontend
      const roleMapping = {
        ADMIN: ['Administrador'],
        AUXILIAR: ['Colaborador']
      }
      console.log('Mapping user type:', userType, 'to roles:', roleMapping[userType])
      return roleMapping[userType] || ['Colaborador']
    },
    getRoleColor (role) {
      const colors = {
        Administrador: 'primary darken-1',
        Auxiliar: 'orange darken-1'
      }
      return colors[role] || 'grey'
    },
    modifyRoles (item) {
      this.editedItem = item
      this.selectedRoles = [...item.roles]
      this.dialogRoles = true
    },
    closeDialog () {
      this.dialogRoles = false
      this.editedItem = null
      this.selectedRoles = []
    },
    saveRoles () {
      if (this.editedItem) {
        this.editedItem.roles = [...this.selectedRoles]
      }
      this.closeDialog()
    },
    async removeUser (item) {
      try {
        const confirmed = await this.$swal({
          title: '¿Estás seguro?',
          text: `¿Deseas deshabilitar el usuario "${item.name}"?`,
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: 'Sí, deshabilitar',
          cancelButtonText: 'Cancelar',
          confirmButtonColor: '#d33',
          cancelButtonColor: '#3085d6'
        })
        if (confirmed.isConfirmed) {
          console.log('Disabling user:', item.id)
          // Realizar la petición para desactivar el usuario
          const response = await axios.patch(`/users/${item.id}/`, {
            is_active: false // Desactivar el usuario
          }, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`
            }
          })
          console.log('User disabled response:', response.data)
          // Mostrar mensaje de éxito
          await this.$swal({
            title: 'Usuario deshabilitado',
            text: `El usuario "${item.name}" ha sido deshabilitado correctamente`,
            icon: 'success',
            confirmButtonText: 'OK'
          })
          // Refrescar la tabla con los nuevos datos
          const userIndex = this.users.findIndex(u => u.id === item.id)
          if (userIndex !== -1) {
            this.users[userIndex].status = 'Inactive'
          }
          console.log('estado actualizado individualmente')
        }
      } catch (error) {
        console.error('Error disabling user:', error)
        // Mostrar mensaje de error
        this.$swal({
          title: 'Error',
          text: 'No se pudo deshabilitar el usuario. Inténtalo de nuevo.',
          icon: 'error',
          confirmButtonText: 'OK'
        })
      }
    }
  },
  async mounted () {
    // Simulación de datos de usuarios
    await this.fetchCurrentUser()
    console.log('Fetching user data...')
    await axios.get('/users/40', { headers: { Authorization: `Bearer ${localStorage.getItem('access_token')}` } })
      .then(response => {
        console.log('Users fetched successfully:', response.data)
        this.users = response.data.results || response.data.users || []
      })
      .catch(error => {
        console.error('Error fetching users:', error)
      })
  }
}
</script>

  <style scoped lang="css"> @import '../../styles/dashboard_usersettings.css'; </style>
