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
              <span>Editar Roles</span>
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
            <span class="text-h5">Editar Roles de usuario</span>
          </v-card-title>

          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-checkbox
                    v-for="role in availableRoles"
                    :key="role"
                    v-model="selectedRoles"
                    :label="role"
                    :value="role"
                  ></v-checkbox>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="closeDialog">Cancelar</v-btn>
            <v-btn color="blue darken-1" text @click="saveRoles">Guardar</v-btn>
          </v-card-actions>
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
      { text: 'User Role', value: 'roles' },
      { text: 'Actions', value: 'actions', sortable: false, width: '100px' }
    ],
    users: [],
    availableRoles: ['Administrador', 'Auxiliar']
  }),

  methods: {

    async fetchCurrentUser () {
      try {
        console.log('Fetching current user data...')
        const response = await axios.get('/auth/user/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        })
        console.log('Current user API response:', response.data)
        this.currentUser = {
          date_joined: response.data.date_joined || '',
          last_login: response.data.last_login || '',
          first_name: response.data.first_name || '',
          last_name: response.data.last_name || '',
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
      const firstName = this.currentUser.first_name || ''
      const lastName = this.currentUser.last_name || ''
      const fullName = `${firstName} ${lastName}`.trim()
      return fullName || this.currentUser.username || 'Usuario'
    },
    async fetchUsers () {
      this.loading = true
      try {
        console.log('Fetching users from API...')
        // Hacer la petición correctamente
        const response = await axios.get('/users/', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`
          }
        })
        console.log('Users API response:', response.data)
        // Mapear los datos si es necesario
        if (Array.isArray(response.data)) {
          this.users = response.data.map(user => ({
            id: user.id,
            name: `${user.first_name || ''} ${user.last_name || ''}`.trim() || user.username,
            username: user.username,
            email: user.email,
            // avatar: user.avatar || require('@/assets/default-avatar.png'),
            status: user.is_active ? 'Active' : 'Inactive',
            roles: this.mapUserRoles(user.tipo_user || user.role) // Mapear roles
          }))
        } else {
          // Si la respuesta tiene estructura diferente
          this.users = response.data.results || response.data.users || []
        }
        console.log('Processed users:', this.users)
      } catch (error) {
        console.error('Error fetching users:', error)
        // Mostrar mensaje de error
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
        AUXILIAR: ['Auxiliar']
      }
      return roleMapping[userType] || ['Auxiliar']
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
    removeUser (item) {
      const index = this.users.indexOf(item)
      if (confirm('¿Estás seguro de eliminar este usuario?')) {
        this.users.splice(index, 1)
      }
    }
  },
  async mounted () {
    // Simulación de datos de usuarios
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
