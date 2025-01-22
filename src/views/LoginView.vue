<template>
  <v-container class="d-flex justify-center align-center" style="min-height: 100vh; background: #f4f6f8;">
    <v-row
      class="login-container"
      style="width: 100%; max-width: 1400px; background: #F1F8FE; border-radius: 20px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);"
    >
      <!-- Sección izquierda -->
      <v-col cols="12" md="6" class="left-section" style="background: #0D2B44; border-radius: 20px 0 0 20px; padding: 64px;">
        <div class="logo-container d-flex flex-column align-center justify-center" style="height: 100%;">
          <img :src="require('@/assets/logo_UD.png')" alt="Logo Universidad Distrital" style="max-width: 380px; margin-bottom: 32px;">
          <h2 class="text-center font-weight-bold" style="color: #ffffff; font-size: 2.2rem; line-height: 1.4;">
            Maestría en Gestión y<br />Seguridad de la Información
          </h2>
        </div>
      </v-col>

      <!-- Sección derecha -->
      <v-col cols="12" md="6" class="right-section" style="padding: 64px;">
        <h3 class="text-center mb-10 font-weight-bold" style="color: #2a5579; font-size: 2.4rem;">Iniciar Sesión</h3>

        <v-form ref="loginForm" v-model="valid" lazy-validation class="login-form">
          <v-text-field
            v-model="username"
            label="Username:"
            :rules="[rules.required]"
            outlined
            class="mb-6 rounded-input"
            height="64"
            clearable
            style="font-size: 1.1rem;"
          ></v-text-field>

          <v-text-field
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            label="Password:"
            :rules="[rules.required]"
            outlined
            height="64"
            class="mb-8 rounded-input"
            clearable
            style="font-size: 1.1rem;"
          >
            <template v-slot:append>
              <v-icon @click="togglePasswordVisibility" style="cursor: pointer; font-size: 24px;">
                {{ showPassword ? 'mdi-eye-off' : 'mdi-eye' }}
              </v-icon>
            </template>
          </v-text-field>

          <v-btn
            :disabled="!valid"
            block
            color="primary"
            class="mb-6 rounded-button"
            height="64"
            x-large
            @click="login"
            style="font-size: 1.2rem;"
          >
            Iniciar Sesión
          </v-btn>

          <router-link
            to="/recover-password"
            class="forgot-password-link text-center d-block"
          >
            Olvidé mi contraseña
          </router-link>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import Swal from 'sweetalert2'

export default {
  data () {
    return {
      username: '',
      password: '',
      showPassword: false,
      valid: false,
      rules: {
        required: (value) => !!value || 'Este campo es requerido.'
      }
    }
  },
  methods: {
    login () {
      if (this.$refs.loginForm.validate()) {
        Swal.fire({
          title: '¡Éxito!',
          text: 'Has iniciado sesión correctamente.',
          icon: 'success',
          confirmButtonText: 'Continuar'
        }).then(() => {
          this.$router.push('/dashboard')
        })
      }
    },
    togglePasswordVisibility () {
      this.showPassword = !this.showPassword
    }
  }
}
</script>

<style scoped>
/* Misma configuración de estilos que tu código original */
</style>
