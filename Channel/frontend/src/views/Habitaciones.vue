<template>
  <div class="habitaciones-view">
    <div class="page-header">
      <div>
        <h1>Tipos de Habitacion</h1>
        <p>Gestiona los tipos de habitaciones de tus hoteles</p>
      </div>
      <button class="btn btn-primary" @click="openModal()">+ Nuevo Tipo</button>
    </div>
    <div v-if="loading" class="loading">Cargando...</div>
    <div v-else-if="habitaciones.length === 0" class="empty-state">
      <div class="empty-icon">B</div>
      <h3>No hay tipos de habitacion</h3>
      <p>Primero debes tener hoteles creados</p>
    </div>
    <div v-else class="rooms-grid">
      <div v-for="hab in habitaciones" :key="hab.id" class="room-card">
        <div class="room-header">
          <span class="room-code">{{ hab.codigo }}</span>
          <span class="room-hotel">Hotel ID: {{ hab.hotel_id }}</span>
        </div>
        <h3>{{ hab.nombre }}</h3>
        <p class="room-desc" v-if="hab.descripcion">{{ hab.descripcion }}</p>
        <div class="room-specs">
          <div class="spec" v-if="hab.capacidad_min || hab.capacidad_max">
            <span>Capacidad: {{ hab.capacidad_min || 1 }}-{{ hab.capacidad_max || 2 }} pers.</span>
          </div>
          <div class="spec" v-if="hab.camas"><span>Camas: {{ hab.camas }}</span></div>
          <div class="spec" v-if="hab.superficie"><span>{{ hab.superficie }} m2</span></div>
        </div>
        <div class="room-services" v-if="hab.servicios"><small>{{ hab.servicios }}</small></div>
        <div class="room-actions">
          <button class="btn btn-sm btn-secondary" @click="openModal(hab)">Editar</button>
          <button class="btn btn-sm btn-danger" @click="eliminar(hab.id)">Eliminar</button>
        </div>
      </div>
    </div>
    <div class="modal-overlay" v-if="showModal" @click.self="closeModal">
      <div class="modal modal-lg">
        <div class="modal-header">
          <h3>{{ editing ? 'Editar Tipo' : 'Nuevo Tipo de Habitacion' }}</h3>
          <button class="btn-close" @click="closeModal">X</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardar">
            <div class="form-section">
              <h4>Informacion Basica</h4>
              <div class="form-group">
                <label>Hotel *</label>
                <select v-model.number="form.hotel_id" class="form-control" required>
                  <option value="">Selecciona un hotel</option>
                  <option v-for="h in hoteles" :key="h.id" :value="h.id">{{ h.nombre }}</option>
                </select>
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label>Codigo *</label>
                  <input type="text" v-model="form.codigo" class="form-control" placeholder="DBL01" required />
                </div>
                <div class="form-group">
                  <label>Nombre *</label>
                  <input type="text" v-model="form.nombre" class="form-control" placeholder="Doble Estandar" required />
                </div>
              </div>
              <div class="form-group">
                <label>Descripcion</label>
                <textarea v-model="form.descripcion" class="form-control" rows="2"></textarea>
              </div>
            </div>
            <div class="form-section">
              <h4>Capacidad y Dimensiones</h4>
              <div class="form-row">
                <div class="form-group">
                  <label>Capacidad Minima *</label>
                  <input type="number" v-model.number="form.capacidad_min" class="form-control" min="1" required />
                </div>
                <div class="form-group">
                  <label>Capacidad Maxima *</label>
                  <input type="number" v-model.number="form.capacidad_max" class="form-control" min="1" required />
                </div>
                <div class="form-group">
                  <label>Camas</label>
                  <input type="text" v-model="form.camas" class="form-control" placeholder="1 doble o 2 individuales" />
                </div>
              </div>
              <div class="form-group">
                <label>Superficie (m2)</label>
                <input type="number" v-model.number="form.superficie" class="form-control" min="10" step="0.5" />
              </div>
            </div>
            <div class="form-section">
              <h4>Servicios</h4>
              <div class="form-group">
                <label>Servicios Incluidos</label>
                <textarea v-model="form.servicios" class="form-control" rows="2" placeholder="WiFi, TV, Aire acondicionado, Minibar..."></textarea>
              </div>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-secondary" @click="closeModal">Cancelar</button>
              <button type="submit" class="btn btn-primary">{{ editing ? 'Guardar' : 'Crear' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { habitacionesApi, hotelesApi } from '../api'
const habitaciones = ref([])
const hoteles = ref([])
const loading = ref(true)
const showModal = ref(false)
const editing = ref(null)
const defaultForm = { hotel_id: '', codigo: '', nombre: '', descripcion: '', capacidad_min: 1, capacidad_max: 2, camas: '', superficie: null, servicios: '' }
const form = ref({ ...defaultForm })
const cargarDatos = async () => {
  loading.value = true
  try {
    const [habR, hotR] = await Promise.all([habitacionesApi.listar(), hotelesApi.listar()])
    habitaciones.value = habR.data
    hoteles.value = hotR.data
  } catch (e) { /* Error silencioso */ }
  finally { loading.value = false }
}
const openModal = (hab = null) => {
  if (hab) { editing.value = hab; form.value = { ...hab } }
  else { editing.value = null; form.value = { ...defaultForm } }
  showModal.value = true
}
const closeModal = () => { showModal.value = false; editing.value = null; form.value = { ...defaultForm } }
const guardar = async () => {
  try {
    if (editing.value) { await habitacionesApi.actualizar(editing.value.id, form.value) }
    else { await habitacionesApi.crear(form.value) }
    closeModal(); await cargarDatos()
  } catch (e) { alert(e.response?.data?.detail || 'Error') }
}
const eliminar = async (id) => {
  if (confirm('Eliminar tipo de habitacion?')) {
    try { await habitacionesApi.eliminar(id); await cargarDatos() }
    catch (e) { alert(e.response?.data?.detail || 'Error') }
  }
}
onMounted(cargarDatos)
</script>
<style scoped>
.habitaciones-view { padding: 20px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h1 { color: var(--primary-color); margin-bottom: 5px; }
.page-header p { color: #666; margin: 0; }
.rooms-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
.room-card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.room-header { display: flex; justify-content: space-between; margin-bottom: 10px; }
.room-code { background: var(--primary-color); color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
.room-hotel { color: #888; font-size: 12px; }
.room-card h3 { margin: 0 0 10px 0; }
.room-desc { color: #666; font-size: 14px; margin-bottom: 15px; }
.room-specs { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 15px; }
.spec { background: #f8f9fa; padding: 6px 12px; border-radius: 20px; font-size: 13px; }
.spec.price { background: #e8f5e9; color: #2e7d32; font-weight: 500; }
.room-services { background: #fff3e0; padding: 10px; border-radius: 8px; margin-bottom: 15px; }
.room-services small { color: #e65100; }
.room-actions { display: flex; gap: 10px; }
.empty-state { text-align: center; padding: 60px; background: white; border-radius: 12px; }
.empty-icon { font-size: 64px; margin-bottom: 20px; color: var(--primary-color); }
.loading { text-align: center; padding: 40px; }
.btn { padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; }
.btn-sm { padding: 6px 12px; font-size: 12px; }
.btn-primary { background: var(--primary-color); color: white; }
.btn-secondary { background: #6c757d; color: white; }
.btn-danger { background: #dc3545; color: white; }
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: white; border-radius: 12px; width: 100%; max-width: 500px; max-height: 90vh; overflow-y: auto; }
.modal-lg { max-width: 650px; }
.modal-header { padding: 20px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; }
.modal-header h3 { margin: 0; color: var(--primary-color); }
.btn-close { background: none; border: none; font-size: 24px; cursor: pointer; }
.modal-body { padding: 20px; }
.form-section { margin-bottom: 20px; padding-bottom: 15px; border-bottom: 1px solid #eee; }
.form-section h4 { margin: 0 0 15px 0; color: var(--primary-color); font-size: 14px; }
.form-row { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 15px; }
.form-group { margin-bottom: 15px; }
.form-group label { display: block; margin-bottom: 5px; font-weight: 500; font-size: 14px; }
.form-control { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
textarea.form-control { resize: vertical; }
.form-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }
</style>
