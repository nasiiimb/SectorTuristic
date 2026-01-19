<template>
  <nav class="navbar">
    <div class="container">
      <router-link to="/" class="navbar-brand">
        <i class="fas fa-hotel"></i> Principal Booking
      </router-link>
      <ul class="navbar-menu">
        <li><router-link to="/">Inicio</router-link></li>
        <li v-if="isAuthenticated">
          <router-link to="/my-reservations">Mis Reservas</router-link>
        </li>
        <li v-if="!isAuthenticated">
          <router-link to="/register">Registro</router-link>
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
export default {
  name: 'Navbar',
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('token')
    }
  },
  methods: {
    handleLogout() {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      this.$router.push('/login')
    }
  }
}
</script>
