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
          <!-- ⭐ NOMBRES (FIRST_NAME) -->
          <div class="form-group">
            <label for="firstName" class="form-label">
              <i class="fas fa-id-card"></i>
              Nombres *
            </label>
            <input
              id="firstName"
              v-model="form.firstName"
              type="text"
              class="form-input"
              :class="{ 'error': errors.firstName, 'success': validFields.firstName }"
              placeholder="Ingrese sus nombres"
              @blur="validateFirstName"
              @input="handleNameChange"
            />
            <span v-if="errors.firstName" class="error-text">{{ errors.firstName }}</span>
          </div>

          <!-- ⭐ APELLIDOS (LAST_NAME) -->
          <div class="form-group">
            <label for="lastName" class="form-label">
              <i class="fas fa-id-card"></i>
              Apellidos *
            </label>
            <input
              id="lastName"
              v-model="form.lastName"
              type="text"
              class="form-input"
              :class="{ 'error': errors.lastName, 'success': validFields.lastName }"
              placeholder="Ingrese sus apellidos"
              @blur="validateLastName"
              @input="handleNameChange"
            />
            <span v-if="errors.lastName" class="error-text">{{ errors.lastName }}</span>
          </div>

          <!-- ⭐ USERNAME (GENERADO AUTOMÁTICAMENTE) -->
          <div class="form-group">
            <label for="username" class="form-label">
              <i class="fas fa-user"></i>
              Nombre de Usuario
            </label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              class="form-input"
              :class="{ 'error': errors.username, 'success': validFields.username }"
              placeholder="Se genera automáticamente"
              readonly
              style="background-color: #f8f9fa; color: #6c757d;"
            />
            <small class="form-help-text">
              <i class="fas fa-info-circle"></i>
              Se genera automáticamente: primer carácter de cada nombre + primer apellido + primer carácter del segundo apellido
            </small>
            <span v-if="errors.username" class="error-text">{{ errors.username }}</span>
          </div>

          <!-- ⭐ EMAIL (PREDILENGENCIADO) -->
          <div class="form-group">
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
              placeholder="Se genera automáticamente"
              readonly
              style="background-color: #f8f9fa; color: #6c757d;"
            />
            <small class="form-help-text">
              <i class="fas fa-info-circle"></i>
              Se genera automáticamente basado en el nombre de usuario
            </small>
            <span v-if="errors.email" class="error-text">{{ errors.email }}</span>
          </div>

          <!-- ⭐ TIPO USUARIO - CORREGIDO -->
          <div class="form-group">
            <label for="userType" class="form-label">
              <i class="fas fa-users"></i>
              Tipo de Usuario *
            </label>
            <select
              id="userType"
              v-model="form.userType"
              class="form-select"
              :class="{ 'error': errors.userType, 'success': validFields.userType }"
              @change="validateUserType"
              @input="clearError('userType')"
            >
              <option value="">Seleccione tipo de usuario</option>
              <option value="admin">Administrador</option>
              <option value="user">Colaborador</option>
            </select>
            <span v-if="errors.userType" class="error-text">{{ errors.userType }}</span>
          </div>

          <!-- Número de Identificación -->
          <div class="form-group">
            <label for="idNumber" class="form-label">
              <i class="fas fa-fingerprint"></i>
              N° Identificación *
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
              Tipo de Estudio *
            </label>
            <select
              id="studyType"
              v-model="form.studyType"
              class="form-select"
              :class="{ 'error': errors.studyType, 'success': validFields.studyType }"
              @change="validateStudyType"
              @input="clearError('studyType')"
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
              Experiencia Laboral *
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
              Contraseña *
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
              Confirmar Contraseña *
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

        <!-- ⭐ BOTÓN CON DEBUG -->
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
          
          <!-- ⭐ BOTÓN CANCELAR -->
          <button
            type="button"
            class="btn btn-secondary"
            @click="cancelRegistration"
            :disabled="isLoading"
          >
            <i class="fas fa-times"></i>
            Cancelar
          </button>
        </div>

        <!-- ⭐ DEBUG INFO (TEMPORAL) -->
        <div v-if="$dev" class="debug-info" style="margin-top: 20px; padding: 10px; background: #f8f9fa; border-radius: 4px; font-size: 12px;">
          <strong>DEBUG INFO:</strong><br>
          <strong>Form Valid:</strong> {{ isFormValid }}<br>
          <strong>Valid Fields:</strong> {{ Object.keys(validFields).length }}/10<br>
          <strong>Errors:</strong> {{ Object.keys(errors).length }}<br>
          <strong>User Type:</strong> "{{ form.userType }}" (Valid: {{ validFields.userType }})<br>
          <strong>Study Type:</strong> "{{ form.studyType }}" (Valid: {{ validFields.studyType }})
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from '../../plugins/Axios'

export default {
  name: 'RegisterUser',
  
  data () {
    return {
      form: {
        firstName: '',
        lastName: '',
        username: '',
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
      isLoading: false,
      userTypes: [
        { text: 'Administrador', value: 'admin' },
        { text: 'Colaborador', value: 'user' }
      ]
    }
  },

  // ⭐ AGREGAR WATCHERS PARA VALIDACIÓN AUTOMÁTICA
  watch: {
    'form.firstName'() {
      if (this.form.firstName.trim()) {
        this.validateFirstName()
      }
    },
    
    'form.lastName'() {
      if (this.form.lastName.trim()) {
        this.validateLastName()
      }
    },
    
    'form.username'() {
      if (this.form.username.trim()) {
        this.validateUsername()
      }
    },
    
    'form.email'() {
      if (this.form.email.trim()) {
        this.validateEmail()
      }
    },
    
    'form.userType'() {
      if (this.form.userType) {
        this.validateUserType()
      }
    },
    
    'form.idNumber'() {
      if (this.form.idNumber.trim()) {
        this.validateIdNumber()
      }
    },
    
    'form.studyType'() {
      if (this.form.studyType) {
        this.validateStudyType()
      }
    },
    
    'form.workExperience'() {
      if (this.form.workExperience.trim()) {
        this.validateWorkExperience()
      }
    },
    
    'form.password'() {
      if (this.form.password) {
        this.validatePassword()
      }
    },
    
    'form.confirmPassword'() {
      if (this.form.confirmPassword) {
        this.validateConfirmPassword()
      }
    }
  },
  
  computed: {
    isFormValid () {
      const requiredFields = ['firstName', 'lastName', 'username', 'email', 'userType', 'idNumber', 'studyType', 'workExperience', 'password', 'confirmPassword']
      
      // ⭐ DEBUG DETALLADO
      console.log('=== VALIDACIÓN DEL FORMULARIO ===')
      console.log('Campos requeridos:', requiredFields)
      
      const validationResults = {}
      requiredFields.forEach(field => {
        const hasValue = this.form[field] && this.form[field].toString().trim() !== ''
        const isValid = this.validFields[field] === true
        validationResults[field] = { hasValue, isValid, value: this.form[field] }
        console.log(`${field}: valor="${this.form[field]}" | tiene_valor=${hasValue} | es_válido=${isValid}`)
      })
      
      const allFieldsValid = requiredFields.every(field => this.validFields[field] === true)
      const noErrors = Object.keys(this.errors).length === 0
      
      console.log('Campos válidos:', this.validFields)
      console.log('Errores:', this.errors)
      console.log(`Todos los campos válidos: ${allFieldsValid}`)
      console.log(`Sin errores: ${noErrors}`)
      console.log(`Formulario válido final: ${allFieldsValid && noErrors}`)
      console.log('================================')
      
      return allFieldsValid && noErrors
    },
    
    passwordStrength () {
      const password = this.form.password
      if (!password) return { percentage: 0, class: '', text: '' }

      let score = 0
      let text = ''
      let className = ''

      if (password.length >= 8) score += 25
      if (password.length >= 12) score += 25
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
    // ⭐ GENERAR USERNAME Y EMAIL AUTOMÁTICAMENTE
    generateUsernameAndEmail() {
      const firstName = this.form.firstName.trim()
      const lastName = this.form.lastName.trim()
      
      if (!firstName || !lastName) {
        this.form.username = ''
        this.form.email = ''
        return
      }
      
      try {
        const cleanFirstName = this.cleanName(firstName)
        const cleanLastName = this.cleanName(lastName)
        
        const nombres = cleanFirstName.split(' ').filter(n => n.length > 0)
        const apellidos = cleanLastName.split(' ').filter(a => a.length > 0)
        
        if (nombres.length === 0 || apellidos.length === 0) {
          this.form.username = ''
          this.form.email = ''
          return
        }
        
        let username = ''
        
        nombres.forEach(nombre => {
          if (nombre.length > 0) {
            username += nombre.charAt(0).toLowerCase()
          }
        })
        
        if (apellidos.length > 0) {
          username += apellidos[0].toLowerCase()
        }
        
        if (apellidos.length > 1) {
          username += apellidos[1].charAt(0).toLowerCase()
        }
        
        this.form.username = username
        this.form.email = `${username}@udistrital.edu.co`
        
        console.log('Generated username:', username)
        console.log('Generated email:', this.form.email)
        
      } catch (error) {
        console.error('Error generating username:', error)
        this.form.username = ''
        this.form.email = ''
      }
    },
    
    cleanName(name) {
      return name
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .replace(/[^a-zA-Z\s]/g, '')
        .replace(/\s+/g, ' ')
        .trim()
    },
    
    // ⭐ MANEJADOR MEJORADO PARA CAMBIOS EN NOMBRES
    handleNameChange() {
      this.clearError('firstName')
      this.clearError('lastName')
      this.clearError('username')
      this.clearError('email')
      
      this.generateUsernameAndEmail()
      
      // ⭐ VALIDAR INMEDIATAMENTE DESPUÉS DE GENERAR
      this.$nextTick(() => {
        if (this.form.firstName.trim()) this.validateFirstName()
        if (this.form.lastName.trim()) this.validateLastName()
        if (this.form.username.trim()) this.validateUsername()
        if (this.form.email.trim()) this.validateEmail()
      })
    },
    
    // ⭐ VALIDACIONES CON LOGGING MEJORADO
    validateFirstName () {
      const firstName = this.form.firstName.trim()
      console.log('Validando firstName:', firstName)
      
      if (!firstName) {
        this.errors.firstName = 'Los nombres son obligatorios'
        this.validFields.firstName = false
      } else if (firstName.length < 2) {
        this.errors.firstName = 'Los nombres deben tener al menos 2 caracteres'
        this.validFields.firstName = false
      } else if (!/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/.test(firstName)) {
        this.errors.firstName = 'Solo se permiten letras y espacios'
        this.validFields.firstName = false
      } else {
        this.validFields.firstName = true
        delete this.errors.firstName
      }
      
      console.log('firstName válido:', this.validFields.firstName)
    },

    validateLastName () {
      const lastName = this.form.lastName.trim()
      console.log('Validando lastName:', lastName)
      
      if (!lastName) {
        this.errors.lastName = 'Los apellidos son obligatorios'
        this.validFields.lastName = false
      } else if (lastName.length < 2) {
        this.errors.lastName = 'Los apellidos deben tener al menos 2 caracteres'
        this.validFields.lastName = false
      } else if (!/^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/.test(lastName)) {
        this.errors.lastName = 'Solo se permiten letras y espacios'
        this.validFields.lastName = false
      } else {
        this.validFields.lastName = true
        delete this.errors.lastName
      }
      
      console.log('lastName válido:', this.validFields.lastName)
    },

    validateUsername () {
      const username = this.form.username.trim()
      console.log('Validando username:', username)
      
      if (!username) {
        this.errors.username = 'El nombre de usuario es obligatorio'
        this.validFields.username = false
      } else if (username.length < 3) {
        this.errors.username = 'El nombre de usuario debe tener al menos 3 caracteres'
        this.validFields.username = false
      } else if (!/^[a-zA-Z0-9_]+$/.test(username)) {
        this.errors.username = 'Solo se permiten letras, números y guión bajo'
        this.validFields.username = false
      } else {
        this.validFields.username = true
        delete this.errors.username
      }
      
      console.log('username válido:', this.validFields.username)
    },

    validateEmail () {
      const email = this.form.email.trim().toLowerCase()
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      console.log('Validando email:', email)

      if (!email) {
        this.errors.email = 'El correo electrónico es obligatorio'
        this.validFields.email = false
      } else if (!emailRegex.test(email)) {
        this.errors.email = 'Ingrese un correo electrónico válido'
        this.validFields.email = false
      } else if (!email.includes('udistrital.edu.co')) {
        this.errors.email = 'Debe usar un correo institucional de la Universidad Distrital'
        this.validFields.email = false
      } else {
        this.validFields.email = true
        delete this.errors.email
      }
      
      console.log('email válido:', this.validFields.email)
    },

    validateUserType () {
      console.log('Validando userType:', this.form.userType)
      
      if (!this.form.userType) {
        this.errors.userType = 'Debe seleccionar un tipo de usuario'
        this.validFields.userType = false
      } else {
        this.validFields.userType = true
        delete this.errors.userType
      }
      
      console.log('userType válido:', this.validFields.userType)
    },

    validateIdNumber () {
      const idNumber = this.form.idNumber.trim()
      console.log('Validando idNumber:', idNumber)
      
      if (!idNumber) {
        this.errors.idNumber = 'El número de identificación es obligatorio'
        this.validFields.idNumber = false
      } else if (!/^\d{6,12}$/.test(idNumber)) {
        this.errors.idNumber = 'Debe contener entre 6 y 12 dígitos'
        this.validFields.idNumber = false
      } else {
        this.validFields.idNumber = true
        delete this.errors.idNumber
      }
      
      console.log('idNumber válido:', this.validFields.idNumber)
    },

    validateStudyType () {
      console.log('Validando studyType:', this.form.studyType)
      
      if (!this.form.studyType) {
        this.errors.studyType = 'Debe seleccionar un tipo de estudio'
        this.validFields.studyType = false
      } else {
        this.validFields.studyType = true
        delete this.errors.studyType
      }
      
      console.log('studyType válido:', this.validFields.studyType)
    },

    validateWorkExperience () {
      const experience = this.form.workExperience.trim()
      console.log('Validando workExperience:', experience)
      
      if (!experience) {
        this.errors.workExperience = 'La experiencia laboral es obligatoria'
        this.validFields.workExperience = false
      } else if (experience.length < 10) {
        this.errors.workExperience = 'Describa brevemente su experiencia (mínimo 10 caracteres)'
        this.validFields.workExperience = false
      } else {
        this.validFields.workExperience = true
        delete this.errors.workExperience
      }
      
      console.log('workExperience válido:', this.validFields.workExperience)
    },

    validatePassword () {
      const password = this.form.password
      const minLength = 8
      const hasUpper = /[A-Z]/.test(password)
      const hasLower = /[a-z]/.test(password)
      const hasNumber = /[0-9]/.test(password)
      const hasSpecial = /[^a-zA-Z0-9]/.test(password)
      
      console.log('Validando password:', password ? '[OCULTA]' : 'vacía')

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
        delete this.errors.password
      }

      console.log('password válido:', this.validFields.password)

      if (this.form.confirmPassword) {
        this.validateConfirmPassword()
      }
    },

    validateConfirmPassword () {
      console.log('Validando confirmPassword')
      
      if (!this.form.confirmPassword) {
        this.errors.confirmPassword = 'Debe confirmar la contraseña'
        this.validFields.confirmPassword = false
      } else if (this.form.password !== this.form.confirmPassword) {
        this.errors.confirmPassword = 'Las contraseñas no coinciden'
        this.validFields.confirmPassword = false
      } else {
        this.validFields.confirmPassword = true
        delete this.errors.confirmPassword
      }
      
      console.log('confirmPassword válido:', this.validFields.confirmPassword)
    },

    clearError (field) {
      if (this.errors[field]) {
        delete this.errors[field]
      }
    },

    // ⭐ MÉTODO PRINCIPAL DE ENVÍO DEL FORMULARIO AL BACKEND
    async handleSubmit () {
      console.log('🚀 Iniciando registro de usuario...')
      
      this.validateFirstName()
      this.validateLastName()
      this.validateUsername()
      this.validateEmail()
      this.validateUserType()
      this.validateIdNumber()
      this.validateStudyType()
      this.validateWorkExperience()
      this.validatePassword()
      this.validateConfirmPassword()

      if (!this.isFormValid) {
        console.error('❌ Formulario inválido:', this.errors)
        
        this.$swal({
          title: 'Formulario Incompleto',
          text: 'Por favor, corrija los errores en el formulario antes de continuar',
          icon: 'warning',
          confirmButtonText: 'Entendido',
          confirmButtonColor: '#ed8936'
        })
        return
      }

      const token = localStorage.getItem('access_token')
      if (!token) {
        console.error('❌ No hay token de autenticación')
        
        this.$swal({
          title: 'Sesión Expirada',
          text: 'Por favor, inicia sesión nuevamente',
          icon: 'error',
          confirmButtonText: 'OK'
        }).then(() => {
          this.$router.push('/login')
        })
        return
      }

      this.isLoading = true

      try {
        const userData = {
          username: this.form.username.trim(),
          first_name: this.form.firstName.trim(),
          last_name: this.form.lastName.trim(),
          email: this.form.email.trim().toLowerCase(),
          tipo_user: this.form.userType,
          documento: this.form.idNumber.trim(),
          tipo_estudio: this.form.studyType,
          experiencia_laboral: this.form.workExperience.trim(),
          password: this.form.password
        }

        console.log('📤 Enviando datos al backend:', {
          ...userData,
          password: '[HIDDEN]'
        })

        const response = await axios.post('/register/', userData, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })

        console.log('Usuario registrado exitosamente:', response.data)

        this.$emit('user-registered', {
          ...userData,
          id: response.data.id || Date.now(),
          status: 'Activo',
          is_active: true,
          name: `${userData.first_name} ${userData.last_name}`.trim()
        })

        this.$swal({
          title: '¡Usuario Registrado!',
          html: `
            <div style="text-align: left; margin: 20px 0;">
              <p><strong>Nombre:</strong> ${this.form.firstName} ${this.form.lastName}</p>
              <p><strong>Usuario:</strong> ${this.form.username}</p>
              <p><strong>Email:</strong> ${this.form.email}</p>
              <p><strong>Tipo:</strong> ${this.userTypes.find(t => t.value === this.form.userType)?.text}</p>
            </div>
            <div style="background: #f0f9ff; padding: 10px; border-radius: 6px; margin-top: 15px;">
              <p style="margin: 0; color: #0369a1; font-size: 14px;">
                <strong>📧 Credenciales generadas automáticamente</strong><br>
                El usuario ya puede acceder al sistema con estas credenciales.
              </p>
            </div>
          `,
          icon: 'success',
          confirmButtonText: 'Continuar',
          confirmButtonColor: '#46AFEA'
        })

        this.resetForm()

      } catch (error) {
        console.error('Error registrando usuario:', error)
        
        let errorTitle = 'Error al Registrar Usuario'
        let errorMessage = 'Ocurrió un error inesperado al registrar el usuario'
        
        if (error.response) {
          const status = error.response.status
          const data = error.response.data
          
          switch (status) {
            case 400:
              errorTitle = 'Datos Inválidos'
              if (typeof data === 'object' && data !== null) {
                const firstField = Object.keys(data)[0]
                const firstError = data[firstField]
                
                if (Array.isArray(firstError)) {
                  errorMessage = firstError[0]
                } else if (typeof firstError === 'string') {
                  errorMessage = firstError
                } else {
                  errorMessage = `Error en campo "${firstField}"`
                }
                
                if (data.username) {
                  errorMessage = `Nombre de usuario: ${Array.isArray(data.username) ? data.username[0] : data.username}`
                } else if (data.email) {
                  errorMessage = `Email: ${Array.isArray(data.email) ? data.email[0] : data.email}`
                } else if (data.documento) {
                  errorMessage = `Número de identificación: ${Array.isArray(data.documento) ? data.documento[0] : data.documento}`
                }
              } else if (typeof data === 'string') {
                errorMessage = data
              }
              break
              
            case 401:
              errorTitle = 'Sin Autorización'
              errorMessage = 'No tienes permisos para registrar usuarios'
              break
              
            case 403:
              errorTitle = 'Acceso Denegado'
              errorMessage = 'No tienes los permisos necesarios para esta acción'
              break
              
            case 409:
              errorTitle = 'Usuario Duplicado'
              errorMessage = 'Ya existe un usuario con ese nombre de usuario o email'
              break
              
            case 500:
              errorTitle = 'Error del Servidor'
              errorMessage = 'Error interno del servidor. Intenta nuevamente'
              break
              
            default:
              errorMessage = data?.message || data?.detail || `Error HTTP ${status}`
          }
        } else if (error.request) {
          errorTitle = 'Error de Conexión'
          errorMessage = 'No se pudo conectar con el servidor. Verifica tu conexión a internet'
        }
        
        this.$swal({
          title: errorTitle,
          text: errorMessage,
          icon: 'error',
          confirmButtonText: 'Entendido',
          confirmButtonColor: '#f56565'
        })
      } finally {
        this.isLoading = false
      }
    },

    // ⭐ MÉTODO PARA CANCELAR Y CERRAR EL FORMULARIO
    cancelRegistration() {
      console.log('🚫 Cancelando registro de usuario')
      
      // ⭐ VERIFICAR SI HAY DATOS SIN GUARDAR
      const hasData = Object.values(this.form).some(value => 
        typeof value === 'string' ? value.trim() : value
      )
      
      if (hasData) {
        this.$swal({
          title: '¿Cancelar Registro?',
          text: 'Se perderán todos los datos ingresados. ¿Estás seguro?',
          icon: 'warning',
          showCancelButton: true,
          confirmButtonText: 'Sí, cancelar',
          cancelButtonText: 'Continuar editando',
          confirmButtonColor: '#f56565',
          cancelButtonColor: '#6c757d'
        }).then((result) => {
          if (result.isConfirmed) {
            this.resetForm()
            this.$emit('cancel')
          }
        })
      } else {
        this.resetForm()
        this.$emit('cancel')
      }
    },

    // MÉTODO PARA LIMPIAR EL FORMULARIO
    resetForm() {
      console.log('🧹 Limpiando formulario')
      
      this.form = {
        firstName: '',
        lastName: '',
        username: '',
        email: '',
        userType: '',
        idNumber: '',
        studyType: '',
        workExperience: '',
        password: '',
        confirmPassword: ''
      }
      this.errors = {}
      this.validFields = {}
      this.showPassword = false
      this.showConfirmPassword = false
    }
  }
}
</script>

<style scoped lang="css"> @import '../../styles/dashboard_RegisterUser.css'; </style>
