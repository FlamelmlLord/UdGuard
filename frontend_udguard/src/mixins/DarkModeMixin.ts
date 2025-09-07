// mixins/DarkModeMixin.ts
import { Component, Vue } from 'vue-property-decorator'

@Component
export default class DarkModeMixin extends Vue {
  // Computed property para acceder al estado del dark mode
  get isDarkMode (): boolean {
    return this.$store.getters.isDarkMode
  }

  // Computed property para las clases CSS dinámicas
  get themeClasses (): Record<string, boolean> {
    return {
      'dark-mode': this.isDarkMode,
      'light-mode': !this.isDarkMode
    }
  }

  // Method para aplicar dark mode a elementos específicos
  applyDarkModeToElement (element: HTMLElement): void {
    if (this.isDarkMode) {
      element.classList.add('dark-mode')
    } else {
      element.classList.remove('dark-mode')
    }
  }

  // Lifecycle hook para asegurar dark mode en mounted
  mounted (): void {
    this.ensureDarkModeConsistency()
    this.listenToDarkModeChanges()
  }

  // Method para forzar consistencia de dark mode
  ensureDarkModeConsistency (): void {
    this.$nextTick(() => {
      const isDark = this.$store.state.darkMode
      document.documentElement.classList.toggle('dark-mode', isDark)
      document.body.classList.toggle('dark-mode', isDark)
      
      // Aplicar a elementos específicos del componente si es necesario
      const componentEl = this.$el as HTMLElement
      if (componentEl) {
        componentEl.classList.toggle('dark-mode', isDark)
      }
    })
  }

  // Listener para cambios de dark mode
  listenToDarkModeChanges (): void {
    this.$eventBus.$on('dark-mode-changed', (isDark: boolean) => {
      this.$nextTick(() => {
        this.ensureDarkModeConsistency()
        this.onDarkModeChanged(isDark)
      })
    })
  }

  // Hook que pueden sobreescribir los componentes hijos
  onDarkModeChanged (isDark: boolean): void {
    // Override en componentes específicos si necesitan lógica adicional
  }

  // Cleanup en destroy
  beforeDestroy (): void {
    this.$eventBus.$off('dark-mode-changed')
  }
}