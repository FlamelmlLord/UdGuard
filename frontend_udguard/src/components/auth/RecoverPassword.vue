<template>
    <v-container class="auth-container">
      <v-row class="auth-row">
        <!-- Left Section Component -->
        <auth-left-section
          :logo-src="require('@/assets/logo_GSI.png')"
          title="Maestría en Gestión y"
          subtitle="Seguridad de la Información"
        />

        <!-- Right Section -->
        <v-col cols="12" md="6" class="auth-right-section">
          <h3 class="auth-title">Recuperar Contraseña</h3>

          <div class="auth-description">
            Ingresa tu correo electrónico y te enviaremos las instrucciones para
            recuperar tu contraseña.
          </div>

          <v-form ref="recoverForm" v-model="valid" lazy-validation>
            <v-text-field
              v-model="email"
              label="Correo Electrónico:"
              :rules="emailRules"
              v-bind="sharedInputProps"
            />

            <v-btn
              :disabled="!valid"
              block
              color="primary"
              class="auth-submit-btn"
              @click="handleRecoverPassword"
              v-bind="sharedButtonProps"
            >
              Enviar Instrucciones
            </v-btn>

            <router-link :to="{ name: 'Login' }" class="back-to-login">
              Volver al inicio de sesión
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
  name: 'RecoverPassword',

  components: {
    AuthLeftSection
  },

  mixins: [authMixin],

  data () {
    return {
      email: '',
      valid: false,
      emailRules: [
        v => !!v || 'El correo electrónico es requerido',
        v => /.+@.+\..+/.test(v) || 'El correo electrónico debe ser válido'
      ]
    }
  },

  methods: {
    async handleRecoverPassword () {
      if (!this.$refs.recoverForm.validate()) return

      try {
        await this.axios.post('http://localhost:8000/api/auth/recover-password/', {
          email: this.email
        })

        this.$swal({
          title: '¡Enviado!',
          text: 'Se han enviado las instrucciones a tu correo electrónico.',
          icon: 'success',
          confirmButtonText: 'OK'
        })
      } catch (error) {
        handleApiError(error)
      }
    }
  }
}
</script>
