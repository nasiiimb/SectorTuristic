<template>
  <!-- Login view (sin navbar) -->
  <div v-if="isLoginRoute">
    <router-view />
  </div>

  <!-- App con navbar horizontal -->
  <div v-else class="app-container">
    <!-- Navbar horizontal -->
    <header class="navbar">
      <div class="navbar-brand">
        <h1>Channel Manager</h1>
      </div>
      <nav class="navbar-nav">
        <router-link to="/" class="nav-item" active-class="active" exact>
          Dashboard
        </router-link>
        <router-link to="/hoteles" class="nav-item" active-class="active">
          Hoteles
        </router-link>
        <router-link to="/habitaciones" class="nav-item" active-class="active">
          Habitaciones
        </router-link>
        <router-link to="/disponibilidad" class="nav-item" active-class="active">
          Disponibilidad
        </router-link>
      </nav>
      <div class="navbar-right">
        <div class="user-section" v-if="user">
          <div class="user-avatar">{{ (user.nombre || user.email).charAt(0).toUpperCase() }}</div>
          <span class="user-name">{{ user.nombre || user.email }}</span>
          <button class="btn-logout" @click="logout">Salir</button>
        </div>
        <div :class="['api-status', apiStatus]">
          <span class="status-dot"></span>
          <span>{{ apiStatusText }}</span>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { healthCheck, authApi } from './api'

const route = useRoute()
const router = useRouter()

const apiStatus = ref('connecting')
const apiStatusText = ref('Conectando...')
const user = ref(null)

const isLoginRoute = computed(() => route.path === '/login')

const loadUser = () => {
  const userData = localStorage.getItem('user')
  if (userData) {
    user.value = JSON.parse(userData)
  }
}

const logout = async () => {
  try {
    await authApi.logout()
  } catch (e) {
    // Ignorar errores de logout
  }
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  user.value = null
  router.push('/login')
}

const checkApiStatus = async () => {
  try {
    await healthCheck()
    apiStatus.value = 'connected'
    apiStatusText.value = 'API Conectada'
  } catch (error) {
    apiStatus.value = 'error'
    apiStatusText.value = 'API Desconectada'
  }
}

onMounted(() => {
  loadUser()
  checkApiStatus()
  setInterval(checkApiStatus, 30000)
})
</script>

<style>
/* Reset y variables */
:root {
  --primary-color: #2B7A78;
  --primary-dark: #14443F;
  --primary-hover: #3D9970;
  --success-color: #22c55e;
  --danger-color: #ef4444;
  --warning-color: #f59e0b;
  --info-color: #06b6d4;
  --bg-dark: #1e293b;
  --bg-darker: #14443F;
  --bg-light: #f8fafc;
  --bg-white: #ffffff;
  --text-primary: #1e293b;
  --text-secondary: #64748b;
  --text-light: #94a3b8;
  --text-white: #ffffff;
  --border-color: #e2e8f0;
  --navbar-height: 60px;
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', system-ui, sans-serif;
  background-color: var(--bg-light);
  color: var(--text-primary);
}

.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* Navbar horizontal */
.navbar {
  height: var(--navbar-height);
  background: var(--bg-darker);
  color: var(--text-white);
  display: flex;
  align-items: center;
  padding: 0 24px;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.navbar-brand h1 {
  font-size: 18px;
  font-weight: 600;
  margin-right: 40px;
}

.navbar-nav {
  display: flex;
  gap: 8px;
  flex: 1;
}

.nav-item {
  padding: 10px 18px;
  color: var(--text-light);
  text-decoration: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--text-white);
}

.nav-item.active {
  background: var(--primary-color);
  color: var(--text-white);
}

.navbar-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.user-section {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--primary-hover);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 600;
  color: white;
}

.user-name {
  font-size: 13px;
  color: var(--text-white);
  max-width: 120px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.btn-logout {
  padding: 6px 12px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: var(--text-light);
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  font-weight: 500;
  transition: all 0.2s ease;
}

.btn-logout:hover {
  background: rgba(239, 68, 68, 0.2);
  color: #f87171;
  border-color: rgba(239, 68, 68, 0.4);
}

.api-status {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-light);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--warning-color);
}

.api-status.connected .status-dot {
  background: var(--success-color);
}

.api-status.error .status-dot {
  background: var(--danger-color);
}

/* Main content */
.main-content {
  flex: 1;
  margin-top: var(--navbar-height);
  padding: 32px;
}

/* Cards */
.card {
  background: var(--bg-white);
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: 1px solid var(--border-color);
  margin-bottom: 24px;
}

.card-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  font-size: 18px;
  font-weight: 600;
}

.card-body {
  padding: 24px;
}

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: 500;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: var(--primary-color);
  color: var(--text-white);
}

.btn-primary:hover {
  background: var(--primary-hover);
}

.btn-danger {
  background: var(--danger-color);
  color: var(--text-white);
}

.btn-sm {
  padding: 6px 12px;
  font-size: 12px;
}

/* Forms */
.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 6px;
  font-size: 14px;
  font-weight: 500;
}

.form-control {
  width: 100%;
  padding: 10px 14px;
  font-size: 14px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  transition: border-color 0.2s;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-color);
}

.form-row {
  display: flex;
  gap: 16px;
}

.form-row .form-group {
  flex: 1;
}

/* Tables */
.table {
  width: 100%;
  border-collapse: collapse;
}

.table th,
.table td {
  padding: 12px 16px;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.table th {
  font-weight: 600;
  font-size: 13px;
  color: var(--text-secondary);
  text-transform: uppercase;
  background: var(--bg-light);
}

.table tbody tr:hover {
  background: var(--bg-light);
}

/* Badges */
.badge {
  display: inline-block;
  padding: 4px 10px;
  font-size: 12px;
  font-weight: 500;
  border-radius: 20px;
}

.badge-success {
  background: rgba(34, 197, 94, 0.1);
  color: var(--success-color);
}

.badge-danger {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger-color);
}

.badge-warning {
  background: rgba(245, 158, 11, 0.1);
  color: var(--warning-color);
}

/* Stats */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.stat-card {
  background: var(--bg-white);
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  border: 1px solid var(--border-color);
}

.stat-icon {
  font-size: 32px;
}

.stat-info h3 {
  font-size: 28px;
  font-weight: 700;
}

.stat-info p {
  color: var(--text-secondary);
  font-size: 14px;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: var(--bg-white);
  border-radius: 12px;
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow: auto;
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  font-size: 18px;
  font-weight: 600;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: var(--text-secondary);
}

.modal-body {
  padding: 24px;
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
