<template>
  <div class="disponibilidad-view">
    <div class="page-header">
      <div>
        <h1>Disponibilidad</h1>
        <p>Gestiona disponibilidad y precios por fecha</p>
      </div>
    </div>
    <div class="filter-bar">
      <div class="filter-group">
        <label>Hotel:</label>
        <select v-model="selectedHotel" class="form-control" @change="onHotelChange">
          <option :value="null">Seleccionar hotel</option>
          <option v-for="hotel in hoteles" :key="hotel.id" :value="hotel.id">{{ hotel.nombre }}</option>
        </select>
      </div>
      <div class="filter-group" v-if="selectedHotel">
        <label>Tipo Habitacion:</label>
        <select v-model="selectedHabitacion" class="form-control" @change="cargarDisponibilidad">
          <option :value="null">Seleccionar tipo</option>
          <option v-for="hab in habitacionesFiltradas" :key="hab.id" :value="hab.id">{{ hab.nombre }} ({{ hab.codigo }})</option>
        </select>
      </div>
      <div class="filter-group" v-if="selectedHabitacion">
        <label>Mes:</label>
        <div class="month-nav">
          <button class="btn btn-sm" @click="mesAnterior">Ant</button>
          <span class="month-label">{{ mesActualLabel }}</span>
          <button class="btn btn-sm" @click="mesSiguiente">Sig</button>
        </div>
      </div>
    </div>
    <div class="card" v-if="selectedHabitacion">
      <div class="card-header">
        <h3>Calendario</h3>
        <button class="btn btn-primary" @click="openBulkModal">+ Actualizar Rango</button>
      </div>
      <div class="card-body">
        <div v-if="loading" class="loading">Cargando...</div>
        <div v-else class="calendar-grid">
          <div class="calendar-header">
            <div>Dom</div>
            <div>Lun</div>
            <div>Mar</div>
            <div>Mie</div>
            <div>Jue</div>
            <div>Vie</div>
            <div>Sab</div>
          </div>
          <div class="calendar-body">
            <div v-for="(day, index) in diasCalendario" :key="index" class="calendar-day" :class="{ 'other-month': !day.currentMonth, 'has-data': day.disponibilidad, 'no-availability': day.disponibilidad && day.disponibilidad.cantidad_disponible === 0 }" @click="day.currentMonth && openDayModal(day)">
              <div class="day-number">{{ day.day }}</div>
              <div v-if="day.disponibilidad && day.currentMonth" class="day-info">
                <div class="day-quantity">{{ day.disponibilidad.cantidad_disponible }} hab</div>
                <div class="day-price">{{ day.disponibilidad.precio.toFixed(0) }} EUR</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="empty-state" v-else-if="hoteles.length === 0">
      <div class="empty-icon">H</div>
      <h3>No hay hoteles</h3>
      <router-link to="/hoteles" class="btn btn-primary">Ir a Hoteles</router-link>
    </div>
    <div class="empty-state" v-else-if="!selectedHotel">
      <div class="empty-icon">D</div>
      <h3>Selecciona un hotel</h3>
    </div>
    <div class="empty-state" v-else-if="habitacionesFiltradas.length === 0">
      <div class="empty-icon">R</div>
      <h3>No hay tipos de habitacion</h3>
      <router-link to="/habitaciones" class="btn btn-primary">Ir a Habitaciones</router-link>
    </div>
    <div class="empty-state" v-else>
      <div class="empty-icon">D</div>
      <h3>Selecciona un tipo de habitacion</h3>
    </div>
    <div class="modal-overlay" v-if="showDayModal" @click.self="closeDayModal">
      <div class="modal">
        <div class="modal-header">
          <h3>{{ selectedDay ? formatDate(selectedDay.date) : '' }}</h3>
          <button class="btn-close" @click="closeDayModal">X</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarDia">
            <div class="form-group">
              <label>Cantidad Disponible</label>
              <input type="number" v-model.number="dayForm.cantidad_disponible" class="form-control" min="0">
            </div>
            <div class="form-group">
              <label>Precio (EUR)</label>
              <input type="number" v-model.number="dayForm.precio" class="form-control" min="0" step="0.01">
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-secondary" @click="closeDayModal">Cancelar</button>
              <button type="submit" class="btn btn-primary">Guardar</button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="modal-overlay" v-if="showBulkModal" @click.self="closeBulkModal">
      <div class="modal">
        <div class="modal-header">
          <h3>Actualizar Rango</h3>
          <button class="btn-close" @click="closeBulkModal">X</button>
        </div>
        <div class="modal-body">
          <form @submit.prevent="guardarRango">
            <div class="form-group">
              <label>Fecha Inicio</label>
              <input type="date" v-model="bulkForm.fecha_inicio" class="form-control" required>
            </div>
            <div class="form-group">
              <label>Fecha Fin</label>
              <input type="date" v-model="bulkForm.fecha_fin" class="form-control" required>
            </div>
            <div class="form-group">
              <label>Cantidad Disponible</label>
              <input type="number" v-model.number="bulkForm.cantidad_disponible" class="form-control" min="0" required>
            </div>
            <div class="form-group">
              <label>Precio (EUR)</label>
              <input type="number" v-model.number="bulkForm.precio" class="form-control" min="0" step="0.01" required>
            </div>
            <div class="form-actions">
              <button type="button" class="btn btn-secondary" @click="closeBulkModal">Cancelar</button>
              <button type="submit" class="btn btn-primary">Aplicar</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, computed, onMounted } from 'vue'
import { hotelesApi, habitacionesApi, disponibilidadApi } from '../api'
const hoteles = ref([])
const habitaciones = ref([])
const disponibilidad = ref([])
const loading = ref(false)
const selectedHotel = ref(null)
const selectedHabitacion = ref(null)
const currentMonth = ref(new Date())
const showDayModal = ref(false)
const showBulkModal = ref(false)
const selectedDay = ref(null)
const dayForm = ref({ cantidad_disponible: 0, precio: 0 })
const bulkForm = ref({ fecha_inicio: '', fecha_fin: '', cantidad_disponible: 10, precio: 100 })
const habitacionesFiltradas = computed(() => {
  if (!selectedHotel.value) return []
  return habitaciones.value.filter(h => h.hotel_id === selectedHotel.value)
})
const mesActualLabel = computed(() => currentMonth.value.toLocaleDateString('es-ES', { year: 'numeric', month: 'long' }))
const diasCalendario = computed(() => {
  const year = currentMonth.value.getFullYear()
  const month = currentMonth.value.getMonth()
  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)
  const days = []
  const startDayOfWeek = firstDay.getDay()
  for (let i = startDayOfWeek - 1; i >= 0; i--) {
    const date = new Date(year, month, -i)
    days.push({ day: date.getDate(), date, currentMonth: false, disponibilidad: null })
  }
  for (let i = 1; i <= lastDay.getDate(); i++) {
    const date = new Date(year, month, i)
    const dateStr = formatDateISO(date)
    const disp = disponibilidad.value.find(d => d.fecha === dateStr)
    days.push({ day: i, date, currentMonth: true, disponibilidad: disp })
  }
  const remainingDays = 42 - days.length
  for (let i = 1; i <= remainingDays; i++) {
    const date = new Date(year, month + 1, i)
    days.push({ day: i, date, currentMonth: false, disponibilidad: null })
  }
  return days
})
const cargarHoteles = async () => { const response = await hotelesApi.listar(); hoteles.value = response.data }
const cargarHabitaciones = async () => { const response = await habitacionesApi.listar(); habitaciones.value = response.data }
const cargarDisponibilidad = async () => {
  if (!selectedHabitacion.value) { disponibilidad.value = []; return }
  loading.value = true
  const year = currentMonth.value.getFullYear()
  const month = currentMonth.value.getMonth()
  const fechaInicio = formatDateISO(new Date(year, month, 1))
  const fechaFin = formatDateISO(new Date(year, month + 1, 0))
  const response = await disponibilidadApi.listar({ tipo_habitacion_id: selectedHabitacion.value, fecha_inicio: fechaInicio, fecha_fin: fechaFin })
  disponibilidad.value = response.data
  loading.value = false
}
const onHotelChange = () => { selectedHabitacion.value = null; disponibilidad.value = [] }
const mesAnterior = () => { currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() - 1, 1); cargarDisponibilidad() }
const mesSiguiente = () => { currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() + 1, 1); cargarDisponibilidad() }
const formatDateISO = (date) => date.toISOString().split('T')[0]
const formatDate = (date) => date.toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
const openDayModal = (day) => {
  selectedDay.value = day
  if (day.disponibilidad) { dayForm.value = { cantidad_disponible: day.disponibilidad.cantidad_disponible, precio: day.disponibilidad.precio } }
  else { dayForm.value = { cantidad_disponible: 10, precio: 100 } }
  showDayModal.value = true
}
const closeDayModal = () => { showDayModal.value = false; selectedDay.value = null }
const guardarDia = async () => {
  await disponibilidadApi.crear({ tipo_habitacion_id: selectedHabitacion.value, fecha: formatDateISO(selectedDay.value.date), cantidad_disponible: dayForm.value.cantidad_disponible, precio: dayForm.value.precio })
  closeDayModal()
  cargarDisponibilidad()
}
const openBulkModal = () => {
  const today = new Date()
  bulkForm.value = { fecha_inicio: formatDateISO(today), fecha_fin: formatDateISO(new Date(today.getFullYear(), today.getMonth() + 1, 0)), cantidad_disponible: 10, precio: 100 }
  showBulkModal.value = true
}
const closeBulkModal = () => { showBulkModal.value = false }
const guardarRango = async () => {
  await disponibilidadApi.crearBulk({ tipo_habitacion_id: selectedHabitacion.value, fecha_inicio: bulkForm.value.fecha_inicio, fecha_fin: bulkForm.value.fecha_fin, cantidad_disponible: bulkForm.value.cantidad_disponible, precio: bulkForm.value.precio })
  closeBulkModal()
  cargarDisponibilidad()
}
onMounted(async () => { await cargarHoteles(); await cargarHabitaciones() })
</script>
<style scoped>
.disponibilidad-view { padding: 20px; }
.page-header { margin-bottom: 20px; }
.page-header h1 { color: var(--primary-color); margin-bottom: 5px; }
.page-header p { color: #666; margin: 0; }
.filter-bar { display: flex; gap: 20px; align-items: flex-end; margin-bottom: 20px; padding: 15px; background: white; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05); flex-wrap: wrap; }
.filter-group { display: flex; flex-direction: column; gap: 5px; }
.filter-group label { font-weight: 500; color: #555; font-size: 14px; }
.month-nav { display: flex; align-items: center; gap: 10px; }
.month-label { min-width: 150px; text-align: center; font-weight: 500; text-transform: capitalize; }
.card { background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); overflow: hidden; }
.card-header { padding: 20px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
.card-header h3 { margin: 0; color: var(--primary-color); }
.card-body { padding: 20px; }
.calendar-grid { border: 1px solid #eee; border-radius: 8px; overflow: hidden; }
.calendar-header { display: grid; grid-template-columns: repeat(7, 1fr); background: var(--primary-color); color: white; }
.calendar-header > div { padding: 10px; text-align: center; font-weight: 500; }
.calendar-body { display: grid; grid-template-columns: repeat(7, 1fr); }
.calendar-day { min-height: 80px; padding: 8px; border: 1px solid #eee; cursor: pointer; transition: background 0.2s; }
.calendar-day:hover { background: #f8f9fa; }
.calendar-day.other-month { background: #fafafa; color: #ccc; cursor: default; }
.calendar-day.has-data { background: #e8f5e9; }
.calendar-day.no-availability { background: #ffebee; }
.day-number { font-weight: 600; margin-bottom: 4px; }
.day-info { font-size: 11px; }
.day-quantity { color: var(--primary-color); }
.day-price { color: #666; }
.empty-state { text-align: center; padding: 60px 20px; background: white; border-radius: 12px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); }
.empty-icon { font-size: 64px; margin-bottom: 20px; font-weight: bold; color: var(--primary-color); }
.empty-state h3 { color: var(--primary-color); margin-bottom: 10px; }
.btn { padding: 10px 20px; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; text-decoration: none; display: inline-block; }
.btn-sm { padding: 5px 10px; }
.btn-primary { background: var(--primary-color); color: white; }
.btn-primary:hover { background: var(--primary-hover); }
.btn-secondary { background: #6c757d; color: white; }
.form-control { padding: 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 14px; min-width: 150px; }
.form-control:focus { outline: none; border-color: var(--primary-color); }
.modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0, 0, 0, 0.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: white; border-radius: 12px; width: 100%; max-width: 400px; max-height: 90vh; overflow-y: auto; }
.modal-header { padding: 20px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
.modal-header h3 { margin: 0; color: var(--primary-color); text-transform: capitalize; }
.btn-close { background: none; border: none; font-size: 24px; cursor: pointer; color: #666; }
.modal-body { padding: 20px; }
.form-group { margin-bottom: 15px; }
.form-group label { display: block; margin-bottom: 5px; font-weight: 500; color: #555; }
.form-group .form-control { width: 100%; box-sizing: border-box; }
.form-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }
.loading { text-align: center; padding: 40px; color: #666; }
</style>
