<template>
    <v-container class="auth-container">
      <v-row class="auth-row">
        <!-- Left Section Component -->
        <auth-left-section
          :logo-src="require('@/assets/logo_UD.png')"
          title="Maestría en Gestión y"
          subtitle="Seguridad de la Información"
        />

        <!-- Right Section -->
        <v-col cols="12" md="6" class="auth-right-section">
          <h3 class="auth-title">Iniciar Sesión</h3>

          <v-form ref="loginForm" v-model="valid" lazy-validation>
            <v-text-field
              v-model="formData.username"
              label="Username:"
              :rules="validationRules.required"
              v-bind="sharedInputProps"
            />

            <v-text-field
              v-model="formData.password"
              :type="showPassword ? 'text' : 'password'"
              label="Password:"
              :rules="validationRules.required"
              v-bind="sharedInputProps"
            >
              <template #append>
                <v-icon @click="togglePasswordVisibility" class="password-toggle">
                  {{ showPassword ? 'mdi-eye-off' : 'mdi-eye' }}
                </v-icon>
              </template>
            </v-text-field>

            <v-btn
              :disabled="!valid"
              block
              color="primary"
              class="auth-submit-btn"
              @click="handleLogin"
              v-bind="sharedButtonProps"
            >
              Iniciar Sesión
            </v-btn>

            <router-link to="/recover-password" class="forgot-password-link">
              Olvidé mi contraseña
            </router-link>
          </v-form>
        </v-col>
      </v-row>
    </v-container>
  </template>

<script>
import AuthLeftSection from './AuthLeftSection.vue'
import { authMixin } from '../../mixins/AuthMixin'
import { handleApiError } from '../../utils/ErrorHandler'

export default {
  name: 'LoginHome',

  components: {
    AuthLeftSection
  },

  mixins: [authMixin],

  data () {
    return {
      formData: {
        username: '',
        password: ''
      },
      showPassword: false,
      valid: false
    }
  },

  methods: {
    async handleLogin () {
      if (!this.$refs.loginForm.validate()) return

      try {
        const response = await this.axios.post('http://localhost:8000/api/auth/login/', this.formData)

        if (response.data.status === 'success') {
          this.handleLoginSuccess(response.data.data)
        }
      } catch (error) {
        handleApiError(error)
      }
    },

    handleLoginSuccess (data) {
      // Store tokens
      this.storeAuthData(data.tokens, data.role)

      // Show success message and redirect
      this.$swal({
        title: '¡Éxito!',
        text: 'Has iniciado sesión correctamente.',
        icon: 'success',
        confirmButtonText: 'Continuar'
      }).then(() => {
        const route = data.role === 'ADMIN' ? '/dashboard/admin' : '/dashboard'
        this.$router.push(route)
      })
    },

    togglePasswordVisibility () {
      this.showPassword = !this.showPassword
    }
  }
}
</script>
