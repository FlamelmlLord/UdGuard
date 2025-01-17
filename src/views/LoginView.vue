<template>
    <v-container class="d-flex justify-center align-center" style="min-height: 100vh; background: #f4f6f8;">
      <v-row class="login-container" style="width: 80%; max-width: 900px; background: #F1F8FE; border-radius: 16px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
        <v-col cols="12" md="6" class="left-section" style="background: #0D2B44; border-radius: 16px 0 0 16px; padding: 32px;">
          <div class="logo-container d-flex flex-column align-center justify-center" style="height: 100%;">
            <img src="/src/assets/logo_GSI.png" alt="Logo GSI" style="max-width: 200px; margin-bottom: 16px;">
            <h3 class="text-center font-weight-bold" style="color: #2a5579;">Maestría en Gestión y<br />Seguridad de la Información</h3>
          </div>
        </v-col>

        <v-col cols="12" md="6" class="right-section" style="padding: 48px;">
          <h4 class="text-center mb-6 font-weight-bold" style="color: #2a5579;">Iniciar Sesión</h4>

          <v-form ref="loginForm" v-model="valid" lazy-validation>
            <v-text-field
              v-model="username"
              label="Username:"
              :rules="[rules.required]"
              outlined
              dense
              clearable
            ></v-text-field>

            <v-text-field
              v-model="password"
              label="Password:"
              type="password"
              :rules="[rules.required]"
              outlined
              dense
              clearable
            ></v-text-field>

            <v-btn :disabled="!valid" block color="primary" class="mt-4" @click="login">
              Login
            </v-btn>

            <v-btn text block class="mt-2" color="primary" @click="forgotPassword">
              Olvidé mi contraseña
            </v-btn>
          </v-form>
        </v-col>
      </v-row>
    </v-container>
  </template>

<script>
export default {
  data () {
    return {
      username: '',
      password: '',
      valid: false,
      rules: {
        required: value => !!value || 'Este campo es requerido.'
      }
    }
  },
  methods: {
    login () {
      if (this.$refs.loginForm.validate()) {
        alert('Login exitoso (simulación de frontend).')
      }
    },
    forgotPassword () {
      alert('Función de recuperación de contraseña (simulación de frontend).')
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
  </style>
