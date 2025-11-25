<template>
  <div class="dashboard">
    <div class="page-header">
      <h1>Dashboard</h1>
      <p>Resumen de tu Channel Manager</p>
    </div>
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
        </div>
        <div class="stat-info">
          <h3>{{ stats.hoteles }}</h3>
          <p>Hoteles</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 4v16"></path><path d="M2 8h18a2 2 0 0 1 2 2v10"></path><path d="M2 17h20"></path><path d="M6 8v9"></path></svg>
        </div>
        <div class="stat-info">
          <h3>{{ stats.habitaciones }}</h3>
          <p>Tipos Habitacion</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
        </div>
        <div class="stat-info">
          <h3>{{ stats.disponibilidad }}</h3>
          <p>Registros Disp.</p>
        </div>
      </div>
    </div>
    <div class="cards-row">
      <div class="card">
        <div class="card-header">
          <h3>Mis Hoteles</h3>
          <router-link to="/hoteles" class="btn btn-sm">Ver todos</router-link>
        </div>
        <div class="card-body">
          <div v-if="loading" class="loading">Cargando...</div>
          <div v-else-if="hoteles.length === 0" class="empty">No hay hoteles</div>
          <ul v-else class="hotel-list">
            <li v-for="hotel in hoteles.slice(0, 5)" :key="hotel.id">
              <span class="hotel-name">{{ hotel.nombre }}</span>
              <span class="hotel-city">{{ hotel.ciudad }}</span>
            </li>
          </ul>
        </div>
      </div>
      <div class="card">
        <div class="card-header">
          <h3>Accesos Rapidos</h3>
        </div>
        <div class="card-body">
          <div class="quick-links">
            <router-link to="/hoteles" class="quick-link">
              <span class="link-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
              </span>
              <span>Gestionar Hoteles</span>
            </router-link>
            <router-link to="/habitaciones" class="quick-link">
              <span class="link-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 4v16"></path><path d="M2 8h18a2 2 0 0 1 2 2v10"></path><path d="M2 17h20"></path><path d="M6 8v9"></path></svg>
              </span>
              <span>Tipos de Habitacion</span>
            </router-link>
            <router-link to="/disponibilidad" class="quick-link">
              <span class="link-icon">
                <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
              </span>
              <span>Disponibilidad</span>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { hotelesApi, habitacionesApi, disponibilidadApi } from '../api'
const loading = ref(true)
const hoteles = ref([])
const stats = ref({ hoteles: 0, habitaciones: 0, disponibilidad: 0 })
const cargarDatos = async () => {
  try {
    const [hotelesRes, habRes, dispRes] = await Promise.all([
      hotelesApi.listar(),
      habitacionesApi.listar(),
      disponibilidadApi.listar({})
    ])
    hoteles.value = hotelesRes.data
    stats.value = { hoteles: hotelesRes.data.length, habitaciones: habRes.data.length, disponibilidad: dispRes.data.length }
  } catch (e) {
    // Error silencioso - mostrar UI fallback
  } finally {
    loading.value = false
  }
}
onMounted(cargarDatos)
</script>
<style scoped>
.dashboard { padding: 20px; }
.page-header { margin-bottom: 30px; }
.page-header h1 { color: var(--primary-color); margin-bottom: 5px; }
.page-header p { color: #666; margin: 0; }
.stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 30px; }
.stat-card { background: white; border-radius: 12px; padding: 20px; display: flex; align-items: center; gap: 15px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); }
.stat-icon { color: var(--primary-color); background: #e8f4f3; padding: 12px; border-radius: 10px; display: flex; align-items: center; justify-content: center; }
.stat-info h3 { margin: 0; font-size: 28px; color: var(--primary-color); }
.stat-info p { margin: 5px 0 0; color: #666; }
.cards-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
.card { background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); overflow: hidden; }
.card-header { padding: 15px 20px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
.card-header h3 { margin: 0; color: var(--primary-color); }
.card-body { padding: 20px; }
.btn { padding: 8px 16px; background: var(--primary-color); color: white; border: none; border-radius: 6px; text-decoration: none; font-size: 14px; }
.btn-sm { padding: 6px 12px; font-size: 12px; }
.loading, .empty { text-align: center; padding: 20px; color: #666; }
.hotel-list { list-style: none; padding: 0; margin: 0; }
.hotel-list li { display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid #eee; }
.hotel-list li:last-child { border-bottom: none; }
.hotel-name { font-weight: 500; }
.hotel-city { color: #666; font-size: 14px; }
.quick-links { display: flex; flex-direction: column; gap: 10px; }
.quick-link { display: flex; align-items: center; gap: 12px; padding: 12px; background: #f8f9fa; border-radius: 8px; text-decoration: none; color: #333; transition: all 0.2s; }
.quick-link:hover { background: var(--primary-color); color: white; }
.quick-link:hover .link-icon { color: white; }
.link-icon { color: var(--primary-color); display: flex; align-items: center; }
</style>
