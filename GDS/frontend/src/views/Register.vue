<template>
  <div class="auth-container">
    <div class="auth-box">
      <h2>Crear Cuenta</h2>
      
      <div v-if="error" class="alert alert-error">
        {{ error }}
      </div>
      
      <div v-if="success" class="alert alert-success">
        {{ success }}
      </div>
      
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>Nombre *</label>
          <input 
            v-model="formData.nombre" 
            type="text" 
            required 
            placeholder="Tu nombre"
          />
        </div>
        
        <div class="form-group">
          <label>Apellidos *</label>
          <input 
            v-model="formData.apellidos" 
            type="text" 
            required 
            placeholder="Tus apellidos"
          />
        </div>
        
        <div class="form-group">
          <label>Email *</label>
          <input 
            v-model="formData.email" 
            type="email" 
            required 
            placeholder="tu@email.com"
          />
        </div>
        
        <div class="form-group">
          <label>DNI</label>
          <input 
            v-model="formData.dni" 
            type="text" 
            placeholder="12345678A (opcional)"
          />
        </div>
        
        <div class="form-group">
          <label>Fecha de Nacimiento</label>
          <input 
            v-model="formData.fecha_nacimiento" 
            type="date" 
            :max="maxBirthDate"
          />
        </div>
        
        <div class="form-group">
          <label>Contraseña *</label>
          <input 
            v-model="formData.password" 
            type="password" 
            required 
            minlength="6"
            placeholder="Mínimo 6 caracteres"
          />
        </div>
        
        <div class="form-group">
          <label>Confirmar Contraseña *</label>
          <input 
            v-model="confirmPassword" 
            type="password" 
            required 
            placeholder="Repite tu contraseña"
          />
        </div>
        
        <button type="submit" class="btn-primary" :disabled="loading">
          {{ loading ? 'Registrando...' : 'Registrarse' }}
        </button>
      </form>
      
      <div class="form-footer">
        ¿Ya tienes cuenta? 
        <router-link to="/login">Inicia sesión aquí</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { authAPI } from '../api/auth'

export default {
  name: 'Registro',
  data() {
    return {
      formData: {
        nombre: '',
        apellidos: '',
        email: '',
        dni: '',
        fecha_nacimiento: '',
        password: ''
      },
      confirmPassword: '',
      loading: false,
      error: null,
      success: null
    }
  },
  computed: {
    maxBirthDate() {
      // Fecha máxima: hace 18 años
      const date = new Date()
      date.setFullYear(date.getFullYear() - 18)
      return date.toISOString().split('T')[0]
    }
  },
  methods: {
    async handleRegister() {
      this.error = null
      this.success = null
      
      // Validar contraseñas
      if (this.formData.password !== this.confirmPassword) {
        this.error = 'Las contraseñas no coinciden'
        return
      }
      
      if (this.formData.password.length < 6) {
        this.error = 'La contraseña debe tener al menos 6 caracteres'
        return
      }
      
      // Validar DNI solo si se ha proporcionado
      if (this.formData.dni && !/^[0-9]{8}[A-Za-z]$/.test(this.formData.dni)) {
        this.error = 'El DNI debe tener el formato 12345678A'
        return
      }
      
      this.loading = true
      
      try {
        const response = await authAPI.register(this.formData)
        console.log('[Registro] Respuesta:', response)
        this.success = 'Registro exitoso. Redirigiendo...'
        
        // Emitir evento de cambio de autenticación
        window.dispatchEvent(new Event('auth-change'))
        
        setTimeout(() => {
          // Redirigir a inicio en lugar de login, ya que el usuario ya está autenticado
          this.$router.push('/')
        }, 1500)
        
      } catch (error) {
        console.error('[Registro] Error:', error)
        this.error = error.response?.data?.message || error.message || 'Error al registrar usuario'
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
