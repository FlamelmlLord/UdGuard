<template>
  <v-container
    class="d-flex justify-center align-center"
    style="min-height: 100vh; background: #f4f6f8"
  >
    <v-row
      class="login-container"
      style="
        width: 100%;
        max-width: 1400px;
        background: #f1f8fe;
        border-radius: 20px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
      "
    >
      <!-- Sección izquierda -->
      <v-col
        cols="12"
        md="6"
        class="left-section"
        style="background: #0d2b44; border-radius: 20px 0 0 20px; padding: 64px"
      >
        <div
          class="logo-container d-flex flex-column align-center justify-center"
          style="height: 100%"
        >
          <img
            :src="require('@/assets/logo_GSI.png')"
            alt="Logo GSI"
            style="max-width: 380px; margin-bottom: 32px"
          />
          <h2
            class="text-center font-weight-bold"
            style="color: #2a5579; font-size: 2.2rem; line-height: 1.4"
          >
            Maestría en Gestión y<br />Seguridad de la Información
          </h2>
        </div>
      </v-col>

      <!-- Sección derecha -->
      <v-col cols="12" md="6" class="right-section" style="padding: 64px">
        <h3
          class="text-center mb-6 font-weight-bold"
          style="color: #2a5579; font-size: 2.4rem"
        >
          Recuperar Contraseña
        </h3>

        <div class="text-center mb-8" style="color: #666">
          Ingresa tu correo electrónico y te enviaremos las instrucciones para
          recuperar tu contraseña.
        </div>

        <v-form
          ref="recoverForm"
          v-model="valid"
          lazy-validation
          class="recover-form"
        >
          <v-text-field
            v-model="email"
            label="Correo Electrónico:"
            :rules="emailRules"
            outlined
            class="mb-6 rounded-input"
            height="64"
            clearable
            style="font-size: 1.1rem"
          ></v-text-field>

          <v-btn
            :disabled="!valid"
            block
            color="primary"
            class="mb-6 rounded-button"
            height="64"
            x-large
            @click="recoverPassword"
            style="font-size: 1.2rem"
          >
            Enviar Instrucciones
          </v-btn>

          <router-link
            :to="{ name: 'Login' }"
            class="back-to-login text-center d-block"
          >
            Volver al inicio de sesión
          </router-link>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  name: 'RecoverPasswordView',
  data () {
    return {
      valid: false,
      email: '',
      emailRules: [
        (v: string) => !!v || 'El correo electrónico es requerido',
        (v: string) =>
          /.+@.+\..+/.test(v) || 'El correo electrónico debe ser válido'
      ]
    }
  }
})
</script>

  <style scoped>
.recover-form {
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

.back-to-login {
  color: #1976d2;
  text-decoration: none;
  font-size: 1.1rem;
  transition: color 0.3s ease;
}

.back-to-login:hover {
  color: #1565c0;
  text-decoration: underline;
}

@media (max-width: 960px) {
  .login-container {
    width: 95%;
    margin: 20px;
  }

  .left-section,
  .right-section {
    padding: 48px !important;
  }
}

@media (max-width: 600px) {
  .login-container {
    width: 100%;
    margin: 10px;
  }

  .left-section,
  .right-section {
    padding: 32px !important;
  }
}
</style>
