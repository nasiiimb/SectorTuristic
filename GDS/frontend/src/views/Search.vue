<template>
  <div>
    <h1 class="page-title">Resultados de Búsqueda</h1>

    <div class="container">
      <!-- Filtros aplicados -->
      <div class="alert alert-info" v-if="appliedFilters">
        <strong>Búsqueda:</strong> 
        {{ appliedFilters.ciudad || 'Todos los destinos' }} | 
        {{ formatDate(appliedFilters.fecha_entrada) }} - {{ formatDate(appliedFilters.fecha_salida) }} | 
        {{ appliedFilters.personas }} {{ appliedFilters.personas === 1 ? 'persona' : 'personas' }}
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading">
        <i class="fas fa-spinner fa-spin fa-3x"></i>
        <p>Buscando disponibilidad en nuestros proveedores...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="alert alert-error">
        {{ error }}
      </div>

      <!-- Sin resultados -->
      <div v-else-if="rooms.length === 0" class="empty-state">
        <i class="fas fa-hotel fa-4x"></i>
        <h3>No encontramos habitaciones disponibles</h3>
        <p>Intenta modificar tus criterios de búsqueda</p>
        <router-link to="/" class="btn-primary" style="max-width: 300px; margin: 2rem auto;">
          Nueva Búsqueda
        </router-link>
      </div>

      <!-- Resultados -->
      <div v-else class="rooms-grid">
        <div v-for="room in rooms" :key="room.id" class="room-card">
          <span class="room-origen" :class="room.origen.toLowerCase()">
            <i :class="room.origen.toLowerCase() === 'webservice' ? 'fas fa-globe' : 'fas fa-satellite-dish'"></i>
            {{ room.origen }}
          </span>
          
          <img 
            :src="room.foto_url || 'https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=800'" 
            :alt="room.nombre" 
            class="room-image"
          />
          
          <div class="room-content">
            <div class="room-hotel">{{ room.hotel }}</div>
            <h3 class="room-title">{{ room.nombre }}</h3>
            <p class="room-description">{{ room.descripcion }}</p>
            
            <div class="room-features">
              <span><i class="fas fa-users"></i> {{ room.capacidad || appliedFilters.personas }} personas</span>
              <span v-if="room.servicios && room.servicios.length"><i class="fas fa-star"></i> {{ Array.isArray(room.servicios) ? room.servicios.join(', ') : room.servicios }}</span>
            </div>
            
            <div class="room-footer">
              <div>
                <span class="room-price-label">Por noche</span>
                <div class="room-price">€{{ room.precio }}</div>
              </div>
              <button @click="handleReserve(room)" class="btn-reserve">
                Reservar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de selección de régimen -->
    <RegimenModal
      v-if="selectedRoom && selectedRoom.origen === 'WebService'"
      :visible="showRegimenModal"
      :room="selectedRoom"
      :hotelId="selectedRoom.idHotel"
      :nights="calculateNights()"
      :roomPrice="selectedRoom.precio"
      @confirm="handleRegimenConfirm"
      @close="closeRegimenModal"
    />
  </div>
</template>

<script>
import { bookingAPI } from '../api/booking'
import { authAPI } from '../api/auth'
import RegimenModal from '../components/RegimenModal.vue'

export default {
  name: 'Resultados',
  components: {
    RegimenModal
  },
  data() {
    return {
      rooms: [],
      loading: false,
      error: null,
      appliedFilters: null,
      showRegimenModal: false,
      selectedRoom: null
    }
  },
  mounted() {
    this.appliedFilters = { ...this.$route.query }
    this.searchRooms()
  },
  watch: {
    '$route.query': {
      handler() {
        this.appliedFilters = { ...this.$route.query }
        this.searchRooms()
      },
      deep: true
    }
  },
  methods: {
    async searchRooms() {
      this.loading = true
      this.error = null
      
      try {
        console.log('[Frontend] Iniciando búsqueda con filtros:', this.appliedFilters)
        const response = await bookingAPI.search(this.appliedFilters)
        console.log('[Frontend] Respuesta recibida:', response)
        
        // La respuesta puede venir en response.data.habitaciones o directamente response.habitaciones
        if (response.success && response.data) {
          this.rooms = response.data.habitaciones || []
          console.log(`[Frontend] ${this.rooms.length} habitaciones cargadas`)
        } else {
          this.rooms = response.habitaciones || []
          console.log(`[Frontend] ${this.rooms.length} habitaciones cargadas (formato alternativo)`)
        }
      } catch (error) {
        console.error('[Frontend] Error al buscar habitaciones:', error)
        console.error('[Frontend] Error response:', error.response?.data)
        this.error = error.response?.data?.message || 'Error al cargar las habitaciones. Por favor, intenta de nuevo.'
      } finally {
        this.loading = false
      }
    },
    
    handleReserve(room) {
      // Verificar autenticación
      if (!authAPI.isAuthenticated()) {
        if (confirm('Debes iniciar sesión para reservar. ¿Ir a la página de inicio de sesión?')) {
          this.$router.push({
            name: 'Login',
            query: { redirect: this.$route.fullPath }
          })
        }
        return
      }

      // Si es WebService, abrir modal de régimen
      if (room.origen === 'WebService') {
        console.log('[Resultados] Abriendo modal para room:', room)
        console.log('[Resultados] room.idHotel:', room.idHotel)
        this.selectedRoom = room
        this.showRegimenModal = true
        return
      }

      // Si es Channel, proceder con la confirmación directa
      const nights = this.calculateNights()
      const total = (room.precio * nights).toFixed(2)
      
      const message = `¿Confirmar reserva?

Hotel: ${room.hotel}
Habitación: ${room.nombre}
Entrada: ${this.formatDate(this.appliedFilters.fecha_entrada)}
Salida: ${this.formatDate(this.appliedFilters.fecha_salida)}
Noches: ${nights}
Personas: ${this.appliedFilters.personas}

Total: €${total}`

      if (!confirm(message)) return

      this.confirmReservation(room, nights, total)
    },

    handleRegimenConfirm({ regimen, totalPrice }) {
      // Cerrar el modal
      this.showRegimenModal = false
      
      // Confirmar la reserva con el régimen seleccionado
      const nights = this.calculateNights()
      this.confirmReservation(this.selectedRoom, nights, totalPrice, regimen)
      
      // Limpiar selección
      this.selectedRoom = null
    },

    closeRegimenModal() {
      this.showRegimenModal = false
      this.selectedRoom = null
    },
    
    async confirmReservation(room, nights, total, regimen = null) {
      try {
        const reservationData = {
          origen: room.origen,
          habitacion_id: room.id,
          hotel_nombre: room.hotel,
          habitacion_tipo: room.nombre,
          fecha_entrada: this.appliedFilters.fecha_entrada,
          fecha_salida: this.appliedFilters.fecha_salida,
          num_huespedes: parseInt(this.appliedFilters.personas),
          precio_total: parseFloat(total)
        }

        // Datos específicos según el origen
        if (room.origen === 'Channel') {
          reservationData.hotel_id = room.hotelId // ⬅️ Agregar hotel_id para Channel
        } else if (room.origen === 'WebService') {
          // El régimen viene como objeto { codigo, nombre, precio, idPrecioRegimen }
          // pero el WebService espera solo el código
          reservationData.regimen = regimen.codigo // ⬅️ Enviar solo el código del régimen
          reservationData.idHotel = room.idHotel
        }

        console.log('[Reserva] Datos enviados:', reservationData)

        const response = await bookingAPI.book(reservationData)
        
        alert(`¡Reserva confirmada!
        
Localizador: ${response.data.localizador || response.data.reserva?.id}

Puedes ver tus reservas en "Mis Reservas"`)
        
        this.$router.push('/mis-reservas')
        
      } catch (error) {
        console.error('Error al reservar:', error)
        const errorMsg = error.response?.data?.message || error.message
        alert('Error al procesar la reserva: ' + errorMsg)
        console.log('Detalles del error:', error.response?.data)
      }
    },
    
    calculateNights() {
      const entrada = new Date(this.appliedFilters.fecha_entrada)
      const salida = new Date(this.appliedFilters.fecha_salida)
      const diff = salida - entrada
      return Math.ceil(diff / (1000 * 60 * 60 * 24))
    },
    
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString + 'T00:00:00')
      return date.toLocaleDateString('es-ES', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      })
    }
  }
}
</script>
