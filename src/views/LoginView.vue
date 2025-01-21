<template>
  <v-container class="d-flex justify-center align-center" style="min-height: 100vh; background: #f4f6f8;">
    <v-row
      class="login-container"
      style="width: 100%; max-width: 1400px; background: #F1F8FE; border-radius: 20px; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);"
    >
      <!-- Sección izquierda -->
      <v-col cols="12" md="6" class="left-section" style="background: #0D2B44; border-radius: 20px 0 0 20px; padding: 64px;">
        <div class="logo-container d-flex flex-column align-center justify-center" style="height: 100%;">
          <img src="/src/assets/logo_GSI.png" alt="Logo GSI" style="max-width: 380px; margin-bottom: 32px;">
          <h2 class="text-center font-weight-bold" style="color: #2a5579; font-size: 2.2rem; line-height: 1.4;">
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
.login-container {
  overflow: hidden;
}

.left-section {
  display: flex;
  align-items: center;
  justify-content: center;
}

.right-section {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.login-form {
  max-width: 550px;
  margin: 0 auto;
  width: 100%;
}

.rounded-input :deep(.v-input__control .v-input__slot) {
  border-radius: 16px !important;
}

.rounded-button {
  border-radius: 16px !important;
}

.forgot-password-link {
  color: #1976D2;
  text-decoration: none;
  font-size: 1.1rem;
  transition: color 0.3s ease;
}

.forgot-password-link:hover {
  color: #1565C0;
  text-decoration: underline;
}

@media (max-width: 960px) {
  .login-container {
    width: 95%;
    margin: 20px;
  }

  .left-section, .right-section {
    padding: 48px !important;
  }
}

@media (max-width: 600px) {
  .login-container {
    width: 100%;
    margin: 10px;
  }

  .left-section, .right-section {
    padding: 32px !important;
  }
}
</style>
