<template>
  <div class="register-container">
    <div class="register-card">
      <!-- Header -->
      <div class="register-header">
        <div class="logo-section">
          <div class="logo-circle">
            <i class="fas fa-user-graduate"></i>
          </div>
          <h2>Registro de Usuario</h2>
          <p>Universidad Distrital - Sistema de Gestión</p>
        </div>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="register-form">
        <div class="form-grid">
          <!-- Username -->
          <div class="form-group">
            <label for="username" class="form-label">
              <i class="fas fa-user"></i>
              Username
            </label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              class="form-input"
              :class="{ 'error': errors.username, 'success': validFields.username }"
              placeholder="Ingrese su nombre de usuario"
              @blur="validateUsername"
              @input="clearError('username')"
            />
            <span v-if="errors.username" class="error-text">{{ errors.username }}</span>
          </div>

          <!-- Nombre Completo -->
          <div class="form-group">
            <label for="fullName" class="form-label">
              <i class="fas fa-id-card"></i>
              Nombre Completo
            </label>
            <input
              id="fullName"
              v-model="form.fullName"
              type="text"
              class="form-input"
              :class="{ 'error': errors.fullName, 'success': validFields.fullName }"
              placeholder="Ingrese su nombre completo"
              @blur="validateFullName"
              @input="clearError('fullName')"
            />
            <span v-if="errors.fullName" class="error-text">{{ errors.fullName }}</span>
          </div>

          <!-- Email -->
          <div class="form-group full-width">
            <label for="email" class="form-label">
              <i class="fas fa-envelope"></i>
              Correo Electrónico
            </label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              class="form-input"
              :class="{ 'error': errors.email, 'success': validFields.email }"
              placeholder="ejemplo@udistrital.edu.co"
              @blur="validateEmail"
              @input="clearError('email')"
            />
            <span v-if="errors.email" class="error-text">{{ errors.email }}</span>
          </div>

          <!-- Tipo Usuario -->
          <div class="form-group">
            <label for="userType" class="form-label">
              <i class="fas fa-users"></i>
              Tipo de Usuario
            </label>
            <select
              id="userType"
              v-model="form.userType"
              class="form-select"
              :class="{ 'error': errors.userType, 'success': validFields.userType }"
              @change="validateUserType"
            >
              <option value="">Seleccione tipo</option>
              <option value="estudiante">Estudiante</option>
              <option value="docente">Docente</option>
              <option value="administrativo">Administrativo</option>
              <option value="investigador">Investigador</option>
            </select>
            <span v-if="errors.userType" class="error-text">{{ errors.userType }}</span>
          </div>

          <!-- Número de Identificación -->
          <div class="form-group">
            <label for="idNumber" class="form-label">
              <i class="fas fa-fingerprint"></i>
              N° Identificación
            </label>
            <input
              id="idNumber"
              v-model="form.idNumber"
              type="text"
              class="form-input"
              :class="{ 'error': errors.idNumber, 'success': validFields.idNumber }"
              placeholder="Número de identificación"
              @blur="validateIdNumber"
              @input="clearError('idNumber')"
            />
            <span v-if="errors.idNumber" class="error-text">{{ errors.idNumber }}</span>
          </div>

          <!-- Tipo de Estudio -->
          <div class="form-group">
            <label for="studyType" class="form-label">
              <i class="fas fa-graduation-cap"></i>
              Tipo de Estudio
            </label>
            <select
              id="studyType"
              v-model="form.studyType"
              class="form-select"
              :class="{ 'error': errors.studyType, 'success': validFields.studyType }"
              @change="validateStudyType"
            >
              <option value="">Seleccione tipo</option>
              <option value="pregrado">Pregrado</option>
              <option value="maestria">Maestría</option>
              <option value="doctorado">Doctorado</option>
              <option value="especializacion">Especialización</option>
            </select>
            <span v-if="errors.studyType" class="error-text">{{ errors.studyType }}</span>
          </div>

          <!-- Experiencia Laboral -->
          <div class="form-group full-width">
            <label for="workExperience" class="form-label">
              <i class="fas fa-briefcase"></i>
              Experiencia Laboral
            </label>
            <textarea
              id="workExperience"
              v-model="form.workExperience"
              class="form-textarea"
              :class="{ 'error': errors.workExperience, 'success': validFields.workExperience }"
              placeholder="Describa brevemente su experiencia laboral relevante..."
              rows="3"
              @blur="validateWorkExperience"
              @input="clearError('workExperience')"
            ></textarea>
            <span v-if="errors.workExperience" class="error-text">{{ errors.workExperience }}</span>
          </div>

          <!-- Contraseña -->
          <div class="form-group">
            <label for="password" class="form-label">
              <i class="fas fa-lock"></i>
              Contraseña
            </label>
            <div class="password-wrapper">
              <input
                id="password"
                v-model="form.password"
                :type="showPassword ? 'text' : 'password'"
                class="form-input"
                :class="{ 'error': errors.password, 'success': validFields.password }"
                placeholder="Ingrese su contraseña"
                @blur="validatePassword"
                @input="clearError('password')"
              />
              <button
                type="button"
                class="password-toggle"
                @click="showPassword = !showPassword"
              >
                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
            </div>
            <div v-if="form.password" class="password-strength">
              <div class="strength-bar">
                <div
                  class="strength-fill"
                  :class="passwordStrength.class"
                  :style="{ width: passwordStrength.percentage + '%' }"
                ></div>
              </div>
              <span class="strength-text">{{ passwordStrength.text }}</span>
            </div>
            <span v-if="errors.password" class="error-text">{{ errors.password }}</span>
          </div>

          <!-- Confirmar Contraseña -->
          <div class="form-group">
            <label for="confirmPassword" class="form-label">
              <i class="fas fa-lock"></i>
              Confirmar Contraseña
            </label>
            <div class="password-wrapper">
              <input
                id="confirmPassword"
                v-model="form.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                class="form-input"
                :class="{ 'error': errors.confirmPassword, 'success': validFields.confirmPassword }"
                placeholder="Confirme su contraseña"
                @blur="validateConfirmPassword"
                @input="clearError('confirmPassword')"
              />
              <button
                type="button"
                class="password-toggle"
                @click="showConfirmPassword = !showConfirmPassword"
              >
                <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
            </div>
            <span v-if="errors.confirmPassword" class="error-text">{{ errors.confirmPassword }}</span>
          </div>
        </div>

        <!-- Submit Button -->
        <div class="form-actions">
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="isLoading || !isFormValid"
            :class="{ 'loading': isLoading }"
          >
            <span v-if="isLoading" class="spinner"></span>
            <i v-else class="fas fa-user-plus"></i>
            {{ isLoading ? 'Registrando...' : 'Registrar Usuario' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RegisterUser',
  data () {
    return {
      form: {
        username: '',
        fullName: '',
        email: '',
        userType: '',
        idNumber: '',
        studyType: '',
        workExperience: '',
        password: '',
        confirmPassword: ''
      },
      errors: {},
      validFields: {},
      showPassword: false,
      showConfirmPassword: false,
      isLoading: false
    }
  },
  computed: {
    isFormValid () {
      const requiredFields = ['username', 'fullName', 'email', 'userType', 'idNumber', 'studyType', 'workExperience', 'password', 'confirmPassword']
      return requiredFields.every(field => this.validFields[field]) && Object.keys(this.errors).length === 0
    },
    passwordStrength () {
      const password = this.form.password
      if (!password) return { percentage: 0, class: '', text: '' }

      let score = 0
      let text = ''
      let className = ''

      // Longitud
      if (password.length >= 8) score += 25
      if (password.length >= 12) score += 25

      // Complejidad
      if (/[a-z]/.test(password)) score += 10
      if (/[A-Z]/.test(password)) score += 10
      if (/[0-9]/.test(password)) score += 10
      if (/[^a-zA-Z0-9]/.test(password)) score += 20

      if (score < 40) {
        text = 'Débil'
        className = 'weak'
      } else if (score < 70) {
        text = 'Media'
        className = 'medium'
      } else if (score < 90) {
        text = 'Fuerte'
        className = 'strong'
      } else {
        text = 'Muy Fuerte'
        className = 'very-strong'
      }

      return { percentage: score, class: className, text }
    }
  },
  methods: {
    validateUsername () {
      const username = this.form.username.trim()
      if (!username) {
        this.errors.username = 'El username es obligatorio'
        this.validFields.username = false
      } else if (username.length < 3) {
        this.errors.username = 'El username debe tener al menos 3 caracteres'
        this.validFields.username = false
      } else if (!/^[a-zA-Z0-9_]+$/.test(username)) {
        this.errors.username = 'Solo se permiten letras, números y guión bajo'
        this.validFields.username = false
      } else {
        this.validFields.username = true
      }
    },

    validateFullName () {
      const fullName = this.form.fullName.trim()
      if (!fullName) {
        this.errors.fullName = 'El nombre completo es obligatorio'
        this.validFields.fullName = false
      } else if (fullName.length < 2) {
        this.errors.fullName = 'El nombre debe tener al menos 2 caracteres'
        this.validFields.fullName = false
      } else if (!/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/.test(fullName)) {
        this.errors.fullName = 'Solo se permiten letras y espacios'
        this.validFields.fullName = false
      } else {
        this.validFields.fullName = true
      }
    },

    validateEmail () {
      const email = this.form.email.trim().toLowerCase()
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

      if (!email) {
        this.errors.email = 'El correo electrónico es obligatorio'
        this.validFields.email = false
      } else if (!emailRegex.test(email)) {
        this.errors.email = 'Ingrese un correo electrónico válido'
        this.validFields.email = false
      } else if (!email.includes('udistrital.edu.co') && !email.includes('correo.udistrital.edu.co')) {
        this.errors.email = 'Debe usar un correo institucional de la Universidad Distrital'
        this.validFields.email = false
      } else {
        this.validFields.email = true
      }
    },

    validateUserType () {
      if (!this.form.userType) {
        this.errors.userType = 'Debe seleccionar un tipo de usuario'
        this.validFields.userType = false
      } else {
        this.validFields.userType = true
      }
    },

    validateIdNumber () {
      const idNumber = this.form.idNumber.trim()
      if (!idNumber) {
        this.errors.idNumber = 'El número de identificación es obligatorio'
        this.validFields.idNumber = false
      } else if (!/^\d{6,12}$/.test(idNumber)) {
        this.errors.idNumber = 'Debe contener entre 6 y 12 dígitos'
        this.validFields.idNumber = false
      } else {
        this.validFields.idNumber = true
      }
    },

    validateStudyType () {
      if (!this.form.studyType) {
        this.errors.studyType = 'Debe seleccionar un tipo de estudio'
        this.validFields.studyType = false
      } else {
        this.validFields.studyType = true
      }
    },

    validateWorkExperience () {
      const experience = this.form.workExperience.trim()
      if (!experience) {
        this.errors.workExperience = 'La experiencia laboral es obligatoria'
        this.validFields.workExperience = false
      } else if (experience.length < 10) {
        this.errors.workExperience = 'Describa brevemente su experiencia (mínimo 10 caracteres)'
        this.validFields.workExperience = false
      } else {
        this.validFields.workExperience = true
      }
    },

    validatePassword () {
      const password = this.form.password
      const minLength = 8
      const hasUpper = /[A-Z]/.test(password)
      const hasLower = /[a-z]/.test(password)
      const hasNumber = /[0-9]/.test(password)
      const hasSpecial = /[^a-zA-Z0-9]/.test(password)

      if (!password) {
        this.errors.password = 'La contraseña es obligatoria'
        this.validFields.password = false
      } else if (password.length < minLength) {
        this.errors.password = `La contraseña debe tener al menos ${minLength} caracteres`
        this.validFields.password = false
      } else if (!hasUpper || !hasLower || !hasNumber || !hasSpecial) {
        this.errors.password = 'Debe incluir: mayúscula, minúscula, número y carácter especial'
        this.validFields.password = false
      } else {
        this.validFields.password = true
      }

      // Revalidar confirmación si ya fue ingresada
      if (this.form.confirmPassword) {
        this.validateConfirmPassword()
      }
    },

    validateConfirmPassword () {
      if (!this.form.confirmPassword) {
        this.errors.confirmPassword = 'Debe confirmar la contraseña'
        this.validFields.confirmPassword = false
      } else if (this.form.password !== this.form.confirmPassword) {
        this.errors.confirmPassword = 'Las contraseñas no coinciden'
        this.validFields.confirmPassword = false
      } else {
        this.validFields.confirmPassword = true
      }
    },

    clearError (field) {
      if (this.errors[field]) {
        delete this.errors[field]
      }
    },

    async handleSubmit () {
      // Validar todos los campos
      this.validateUsername()
      this.validateFullName()
      this.validateEmail()
      this.validateUserType()
      this.validateIdNumber()
      this.validateStudyType()
      this.validateWorkExperience()
      this.validatePassword()
      this.validateConfirmPassword()

      if (!this.isFormValid) {
        this.$toast.error('Por favor, corrija los errores en el formulario')
        return
      }

      this.isLoading = true

      try {
        // Aquí harías la llamada al API
        /* const userData = {
          username: this.form.username.trim(),
          full_name: this.form.fullName.trim(),
          email: this.form.email.trim().toLowerCase(),
          user_type: this.form.userType,
          id_number: this.form.idNumber.trim(),
          study_type: this.form.studyType,
          work_experience: this.form.workExperience.trim(),
          password: this.form.password
        }; */

        // Simular llamada a API (reemplazar con tu lógica)
        await new Promise(resolve => setTimeout(resolve, 2000))

        this.$toast.success('Usuario registrado exitosamente')
        this.$router.push('/login')
      } catch (error) {
        this.$toast.error('Error al registrar usuario: ' + error.message)
      } finally {
        this.isLoading = false
      }
    }
  }
}
</script>

<style scoped lang="css"> @import '../../styles/dashboard_RegisterUser.css'; </style>
