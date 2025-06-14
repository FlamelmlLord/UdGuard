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
                      <v-list-item-title>24 noviembre 2022</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-subtitle class="text-caption grey--text">
                        País, ciudad
                      </v-list-item-subtitle>
                      <v-list-item-title>Colombia, Andres</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-subtitle class="text-caption grey--text">
                        Fecha de nacimiento
                      </v-list-item-subtitle>
                      <v-list-item-title>08/04/1993</v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item>
                    <v-list-item-content>
                      <v-list-item-subtitle class="text-caption grey--text">
                        E-mail
                      </v-list-item-subtitle>
                      <v-list-item-title>user@email.com</v-list-item-title>
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
          :items-per-page="10"
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
export default {
  name: 'UserSettings',

  data: () => ({
    search: '',
    dialogRoles: false,
    selectedRoles: [],
    editedItem: null,
    headers: [
      { text: '', value: 'avatar', sortable: false, width: '50px' },
      { text: 'Name', value: 'name' },
      { text: 'Status', value: 'status' },
      { text: 'User Role', value: 'roles' },
      { text: 'Actions', value: 'actions', sortable: false, width: '100px' }
    ],
    users: [
      {
        avatar: 'https://via.placeholder.com/40',
        name: 'Andres Guevara',
        status: 'Not Logged in',
        roles: ['Administrador', 'Auxiliar']
      },
      {
        avatar: 'https://via.placeholder.com/40',
        name: 'Carlos Guerrero',
        status: 'Active',
        roles: ['Administrador', 'Auxiliar']
      },
      {
        avatar: 'https://via.placeholder.com/40',
        name: 'David Bincoman ',
        status: 'Active',
        roles: ['Docente']
      },
      {
        avatar: 'https://via.placeholder.com/40',
        name: 'Miguel Arial',
        status: 'Active',
        roles: ['Estudiante']
      }
    ],
    availableRoles: ['Administrador', 'Docente', 'Estudiante', 'Auxiliar']
  }),

  methods: {
    getRoleColor (role) {
      const colors = {
        Administrador: 'primary darken-1'
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
  }
}
</script>

   <style scoped lang="css"> @import '../../styles/dashboard_usersettings.css'; </style>
