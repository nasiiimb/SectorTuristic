<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2>Iniciar Sesión</h2>
      
      <div v-if="error" class="alert alert-error">
        {{ error }}
      </div>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Email</label>
          <input 
            v-model="email" 
            type="email" 
            required 
            placeholder="tu@email.com"
          />
        </div>
        
        <div class="form-group">
          <label>Contraseña</label>
          <input 
            v-model="password" 
            type="password" 
            required 
            placeholder="Tu contraseña"
          />
        </div>
        
        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? 'Iniciando...' : 'Iniciar Sesión' }}
        </button>
      </form>
      
      <div class="form-footer">
        ¿No tienes cuenta? 
        <router-link to="/registro">Regístrate aquí</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { authAPI } from '../api/auth'

export default {
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      loading: false,
      error: null
    }
  },
  methods: {
    async handleLogin() {
      this.error = null
      
      if (!this.email || !this.password) {
        this.error = 'Por favor, completa todos los campos'
        return
      }
      
      this.loading = true
      
      try {
        await authAPI.login(this.email, this.password)
        
        // Emitir evento de cambio de autenticación
        window.dispatchEvent(new Event('auth-change'))
        
        // Redirigir a la página anterior o a inicio
        const redirect = this.$route.query.redirect || '/'
        this.$router.push(redirect)
        
      } catch (error) {
        console.error('Error en login:', error)
        this.error = error.response?.data?.error || 'Credenciales incorrectas'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
