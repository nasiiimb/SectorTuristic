<template>
  <div>
    <h1 class="page-title">Mis Reservas</h1>

    <div class="container">
      <!-- Loading -->
      <div v-if="loading" class="loading">
        <i class="fas fa-spinner fa-spin fa-3x"></i>
        <p>Cargando tus reservas...</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="alert alert-error">
        {{ error }}
      </div>

      <!-- Sin reservas -->
      <div v-else-if="reservations.length === 0" class="empty-state">
        <i class="fas fa-clipboard-list fa-4x"></i>
        <h3>No tienes reservas</h3>
        <p>¡Comienza a buscar y reserva tu hotel perfecto!</p>
        <router-link to="/" class="btn-primary" style="max-width: 300px; margin: 2rem auto;">
          Buscar Hoteles
        </router-link>
      </div>

      <!-- Lista de reservas -->
      <div v-else class="reservations-list">
        <div 
          v-for="reservation in reservations" 
          :key="reservation.id" 
          class="reservation-card"
        >
          <div class="reservation-header">
            <div>
              <div class="reservation-localizador">
                Localizador: {{ reservation.localizador_externo }}
              </div>
              <span class="room-origen" :class="reservation.origen.toLowerCase()">
                <i :class="reservation.origen === 'WebService' ? 'fas fa-globe' : 'fas fa-satellite-dish'"></i>
                {{ reservation.origen }}
              </span>
            </div>
            <span class="reservation-status" :class="reservation.estado">
              {{ formatStatus(reservation.estado) }}
            </span>
          </div>

          <div class="reservation-details">
            <div class="reservation-detail">
              <i class="fas fa-hotel"></i>
              <div>
                <strong>{{ reservation.hotel_nombre }}</strong><br/>
                <span style="font-size: 0.9rem;">{{ reservation.habitacion_tipo }}</span>
              </div>
            </div>
            
            <div class="reservation-detail">
              <i class="fas fa-calendar-check"></i>
              <div>
                <strong>Check-in:</strong><br/>
                {{ formatDate(reservation.fecha_entrada) }}
              </div>
            </div>
            
            <div class="reservation-detail">
              <i class="fas fa-calendar-times"></i>
              <div>
                <strong>Check-out:</strong><br/>
                {{ formatDate(reservation.fecha_salida) }}
              </div>
            </div>
            
            <div class="reservation-detail">
              <i class="fas fa-users"></i>
              <div>
                <strong>Personas:</strong><br/>
                {{ reservation.num_huespedes }}
              </div>
            </div>
            
            <div class="reservation-detail">
              <i class="fas fa-euro-sign"></i>
              <div>
                <strong>Total:</strong><br/>
                €{{ reservation.precio_total }}
              </div>
            </div>
            
            <div class="reservation-detail">
              <i class="fas fa-file-alt"></i>
              <div>
                <strong>Reservado:</strong><br/>
                {{ formatDateTime(reservation.created_at) }}
              </div>
            </div>
          </div>

          <!-- Información adicional si existe -->
          <div v-if="reservation.datos_adicionales" style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid #eee; color: var(--text-light); font-size: 0.9rem;">
            <div v-if="reservation.datos_adicionales.noches">
              Estancia de {{ reservation.datos_adicionales.noches }} 
              {{ reservation.datos_adicionales.noches === 1 ? 'noche' : 'noches' }}
            </div>
            <div v-if="reservation.datos_adicionales.precio_noche">
              Precio por noche: €{{ reservation.datos_adicionales.precio_noche }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { bookingAPI } from '../api/booking'

export default {
  name: 'MisReservas',
  data() {
    return {
      reservations: [],
      loading: false,
      error: null
    }
  },
  mounted() {
    this.loadReservations()
  },
  methods: {
    async loadReservations() {
      this.loading = true
      this.error = null
      
      try {
        const response = await bookingAPI.getMyReservations()
        console.log('[Mis Reservas] Respuesta completa:', response)
        
        // La respuesta tiene la estructura: { success, data: { reservas, total } }
        this.reservations = response.data?.reservas || []
        
        console.log('[Mis Reservas] Reservas cargadas:', this.reservations.length)
      } catch (error) {
        console.error('Error al cargar reservas:', error)
        this.error = 'Error al cargar tus reservas. Por favor, intenta de nuevo.'
        
        if (error.response?.status === 401) {
          this.error = 'Sesión expirada. Por favor, inicia sesión de nuevo.'
          setTimeout(() => {
            this.$router.push('/login')
          }, 2000)
        }
      } finally {
        this.loading = false
      }
    },
    
    formatStatus(status) {
      const statuses = {
        'confirmada': 'Confirmada',
        'cancelada': 'Cancelada',
        'completada': 'Completada',
        'pendiente': 'Pendiente'
      }
      return statuses[status] || status
    },
    
    formatDate(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('es-ES', { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
      })
    },
    
    formatDateTime(dateString) {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('es-ES', { 
        year: 'numeric', 
        month: 'short', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>
