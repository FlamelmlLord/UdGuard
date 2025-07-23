export const authMixin = {
  data () {
    return {
      sharedInputProps: {
        outlined: true,
        class: 'mb-6 rounded-input',
        height: 64,
        clearable: true,
        style: 'font-size: 1.1rem'
      },
      sharedButtonProps: {
        height: 64,
        'x-large': true,
        style: 'font-size: 1.2rem'
      },
      validationRules: {
        required: [v => !!v || 'Este campo es requerido.']
      }
    }
  },

  methods: {
    storeAuthData (tokens, role) {
      localStorage.setItem('access_token', tokens.access)
      localStorage.setItem('refresh_token', tokens.refresh)
      localStorage.setItem('user_role', role)
    }
  }
}
