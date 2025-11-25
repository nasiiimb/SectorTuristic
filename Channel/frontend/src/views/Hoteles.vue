<template>
  <div class="hoteles-view">
    <div class="page-header">
      <div>
        <h1>Hoteles</h1>
        <p>Gestiona tus establecimientos hoteleros</p>
      </div>
      <button class="btn btn-primary" @click="openModal()">+ Nuevo Hotel</button>
    </div>
    <div v-if="loading" class="loading">Cargando...</div>
    <div v-else-if="hoteles.length === 0" class="empty-state">
      <div class="empty-icon">H</div>
      <h3>No hay hoteles</h3>
      <p>Crea tu primer hotel para empezar</p>
    </div>
    <div v-else class="hotels-grid">
      <div v-for="hotel in hoteles" :key="hotel.id" class="hotel-card">
        <div class="hotel-header">
          <div class="hotel-stars"><span v-for="n in (hotel.estrellas || 3)" :key="n">*</span></div>
        </div>
        <h3>{{ hotel.nombre }}</h3>
        <div class="hotel-info">
          <p v-if="hotel.direccion">Dir: {{ hotel.direccion }}</p>
          <p v-if="hotel.ciudad">Ciudad: {{ hotel.ciudad }}<span v-if="hotel.pais">, {{ hotel.pais }}</span></p>
          <p v-if="hotel.telefono">Tel: {{ hotel.telefono }}</p>
          <p v-if="hotel.email">Email: {{ hotel.email }}</p>
        </div>
        <div class="hotel-actions">
          <button class="btn btn-sm btn-secondary" @click="openModal(hotel)">Editar</button>
          <button class="btn btn-sm btn-danger" @click="eliminar(hotel.id)">Eliminar</button>
        </div>
      </div>
    </div>
    <div class="modal-overlay" v-if="showModal" @click.self="closeModal">
      <div class="modal modal-lg">
        <div class="modal-header">
          <h3>{{ editingHotel ? 'Editar Hotel' : 'Nuevo Hotel' }}</h3>
          <button class="btn-close" @click="closeModal">X</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardar">
            <div class="form-section">
              <h4>Informacion Basica</h4>
              <div class="form-row">
                <div class="form-group">
                  <label>Nombre del Hotel *</label>
                  <input type="text" v-model="form.nombre" class="form-control" placeholder="Hotel Ejemplo" required />
                </div>
                <div class="form-group">
                  <label>Categoria *</label>
                  <select v-model.number="form.estrellas" class="form-control" required>
                    <option :value="1">1 Estrella</option>
                    <option :value="2">2 Estrellas</option>
                    <option :value="3">3 Estrellas</option>
                    <option :value="4">4 Estrellas</option>
                    <option :value="5">5 Estrellas</option>
                  </select>
                </div>
              </div>
              <div class="form-group">
                <label>Descripcion</label>
                <textarea v-model="form.descripcion" class="form-control" rows="2"></textarea>
              </div>
            </div>
            <div class="form-section">
              <h4>Ubicacion</h4>
              <div class="form-group">
                <label>Direccion</label>
                <input type="text" v-model="form.direccion" class="form-control" placeholder="Calle Principal, 123" />
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label>Ciudad</label>
                  <input type="text" v-model="form.ciudad" class="form-control" placeholder="Palma" />
                </div>
                <div class="form-group">
                  <label>Codigo Postal</label>
                  <input type="text" v-model="form.codigo_postal" class="form-control" placeholder="07001" />
                </div>
                <div class="form-group">
                  <label>Pais</label>
                  <input type="text" v-model="form.pais" class="form-control" placeholder="Espana" />
                </div>
              </div>
            </div>
            <div class="form-section">
              <h4>Contacto</h4>
              <div class="form-row">
                <div class="form-group">
                  <label>Telefono</label>
                  <input type="tel" v-model="form.telefono" class="form-control" placeholder="+34 971 123 456" />
                </div>
                <div class="form-group">
                  <label>Email</label>
                  <input type="email" v-model="form.email" class="form-control" placeholder="info@hotel.com" />
                </div>
              </div>
              <div class="form-group">
                <label>Pagina Web</label>
                <input type="url" v-model="form.web" class="form-control" placeholder="https://www.hotel.com" />
              </div>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-secondary" @click="closeModal">Cancelar</button>
              <button type="submit" class="btn btn-primary">{{ editingHotel ? 'Guardar' : 'Crear' }}</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { hotelesApi } from '../api'
const hoteles = ref([])
const loading = ref(true)
const showModal = ref(false)
const editingHotel = ref(null)
const defaultForm = { nombre: '', descripcion: '', direccion: '', ciudad: '', pais: 'Espana', codigo_postal: '', telefono: '', email: '', web: '', estrellas: 3 }
const form = ref({ ...defaultForm })
const cargarHoteles = async () => {
  loading.value = true
  try { const r = await hotelesApi.listar(); hoteles.value = r.data }
  catch (e) { /* Error silencioso */ }
  finally { loading.value = false }
}
const openModal = (hotel = null) => {
  if (hotel) { editingHotel.value = hotel; form.value = { ...hotel } }
  else { editingHotel.value = null; form.value = { ...defaultForm } }
  showModal.value = true
}
const closeModal = () => { showModal.value = false; editingHotel.value = null; form.value = { ...defaultForm } }
const guardar = async () => {
  try {
    if (editingHotel.value) { await hotelesApi.actualizar(editingHotel.value.id, form.value) }
    else { await hotelesApi.crear(form.value) }
    closeModal(); await cargarHoteles()
  } catch (e) { alert(e.response?.data?.detail || 'Error') }
}
const eliminar = async (id) => {
  if (confirm('Eliminar hotel?')) {
    try { await hotelesApi.eliminar(id); await cargarHoteles() }
    catch (e) { alert(e.response?.data?.detail || 'Error') }
  }
}
onMounted(cargarHoteles)
</script>
<style scoped>
.hoteles-view { padding: 20px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h1 { color: var(--primary-color); margin-bottom: 5px; }
.page-header p { color: #666; margin: 0; }
.hotels-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }
.hotel-card { background: white; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.hotel-header { display: flex; justify-content: space-between; margin-bottom: 10px; }
.hotel-stars { color: gold; }
.hotel-code { background: var(--primary-color); color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
.hotel-card h3 { margin: 0 0 15px 0; }
.hotel-info { font-size: 14px; color: #666; margin-bottom: 15px; }
.hotel-info p { margin: 5px 0; }
.hotel-actions { display: flex; gap: 10px; }
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
