<template>
  <nav class="navbar">
    <div class="container">
      <router-link to="/" class="navbar-brand"><i class="fas fa-hotel"></i> Principal Booking</router-link>
      <ul class="navbar-menu">
        <li><router-link to="/">Inicio</router-link></li>
        <li v-if="isAuthenticated">
          <router-link to="/mis-reservas">Mis Reservas</router-link>
        </li>
        <li v-if="!isAuthenticated">
          <router-link to="/registro">Registro</router-link>
        </li>
        <li v-if="!isAuthenticated">
          <router-link to="/login">Iniciar Sesión</router-link>
        </li>
        <li v-if="isAuthenticated">
          <a @click="handleLogout" style="cursor: pointer;">Cerrar Sesión</a>
        </li>
      </ul>
    </div>
  </nav>
</template>

<script>
import { authAPI } from '../api/auth'

export default {
  name: 'Navbar',
  data() {
    return {
      isAuthenticated: false
    }
  },
  mounted() {
    this.checkAuth()
    // Escuchar cambios en el almacenamiento (para sincronizar entre pestañas)
    window.addEventListener('storage', this.checkAuth)
    // Escuchar evento personalizado para cambios de autenticación
    window.addEventListener('auth-change', this.checkAuth)
  },
  beforeUnmount() {
    window.removeEventListener('storage', this.checkAuth)
    window.removeEventListener('auth-change', this.checkAuth)
  },
  watch: {
    $route() {
      this.checkAuth()
    }
  },
  methods: {
    checkAuth() {
      this.isAuthenticated = authAPI.isAuthenticated()
    },
    handleLogout() {
      authAPI.logout()
      this.checkAuth()
      // Emitir evento de cambio de autenticación
      window.dispatchEvent(new Event('auth-change'))
      this.$router.push('/login')
    }
  }
}
</script>
