<template>
  <transition name="modal">
    <div v-if="isVisible" class="modal-overlay" @click.self="close">
      <div class="modal-container">
        <div class="modal-header">
          <h2>Selecciona tu régimen de alojamiento</h2>
          <button @click="close" class="modal-close">&times;</button>
        </div>

        <div class="modal-body">
          <!-- Loading -->
          <div v-if="loading" class="loading-spinner">
            <i class="fas fa-spinner fa-spin fa-2x"></i>
            <p>Cargando regímenes...</p>
          </div>

          <!-- Error -->
          <div v-else-if="error" class="alert alert-error">
            {{ error }}
          </div>

          <!-- Lista de regímenes -->
          <div v-else-if="regimenes.length > 0" class="regimenes-list">
            <div 
              v-for="regimen in regimenes" 
              :key="regimen.idPrecioRegimen"
              class="regimen-card"
              :class="{ selected: selectedRegimen?.idPrecioRegimen === regimen.idPrecioRegimen }"
              @click="selectRegimen(regimen)"
            >
              <div class="regimen-info">
                <div class="regimen-header">
                  <h3>{{ regimen.nombre }}</h3>
                  <div class="regimen-badge">{{ regimen.codigo }}</div>
                </div>
                <p class="regimen-description">
                  {{ getRegimenDescripcion(regimen.codigo) }}
                </p>
              </div>
              <div class="regimen-price">
                <div class="price-label">Por noche</div>
                <div class="price-amount">€{{ regimen.precio.toFixed(2) }}</div>
              </div>
              <div v-if="selectedRegimen?.idPrecioRegimen === regimen.idPrecioRegimen" class="selected-check">
                <i class="fas fa-check-circle"></i>
              </div>
            </div>
          </div>

          <!-- Sin regímenes -->
          <div v-else class="no-regimenes">
            <i class="fas fa-exclamation-triangle fa-3x"></i>
            <p>No hay regímenes disponibles para este hotel</p>
          </div>

          <!-- Resumen del precio -->
          <div v-if="selectedRegimen && !loading" class="price-summary">
            <div class="summary-row">
              <span>Habitación ({{ nights }} noches)</span>
              <span>€{{ (roomPrice * nights).toFixed(2) }}</span>
            </div>
            <div class="summary-row">
              <span>{{ selectedRegimen.nombre }} ({{ nights }} noches)</span>
              <span>€{{ (selectedRegimen.precio * nights).toFixed(2) }}</span>
            </div>
            <div class="summary-row total">
              <span><strong>Total</strong></span>
              <span><strong>€{{ totalPrice.toFixed(2) }}</strong></span>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button @click="close" class="btn-secondary">Cancelar</button>
          <button 
            @click="confirm" 
            class="btn-primary" 
            :disabled="!selectedRegimen || loading"
          >
            Confirmar reserva
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import axios from 'axios'

export default {
  name: 'RegimenModal',
  props: {
    visible: {
      type: Boolean,
      required: true
    },
    room: {
      type: Object,
      required: true
    },
    hotelId: {
      type: Number,
      required: true
    },
    nights: {
      type: Number,
      required: true
    },
    roomPrice: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      isVisible: this.visible,
      regimenes: [],
      selectedRegimen: null,
      loading: false,
      error: null
    }
  },
  computed: {
    totalPrice() {
      if (!this.selectedRegimen) return this.roomPrice * this.nights
      return (this.roomPrice * this.nights) + (this.selectedRegimen.precio * this.nights)
    }
  },
  watch: {
    visible(newVal) {
      console.log('[RegimenModal] Visible cambió a:', newVal)
      console.log('[RegimenModal] hotelId:', this.hotelId)
      console.log('[RegimenModal] room:', this.room)
      
      this.isVisible = newVal
      if (newVal) {
        if (!this.hotelId) {
          console.error('[RegimenModal] ERROR: No se proporcionó hotelId')
          this.error = 'No se puede cargar los regímenes: falta el ID del hotel'
          return
        }
        this.loadRegimenes()
      }
    }
  },
  mounted() {
    console.log('[RegimenModal] MOUNTED - hotelId:', this.hotelId, 'visible:', this.visible)
    // Como el componente se crea con v-if cuando visible=true, 
    // podemos cargar directamente en mounted
    if (this.visible && this.hotelId) {
      this.loadRegimenes()
    }
  },
  methods: {
    async loadRegimenes() {
      this.loading = true
      this.error = null
      this.selectedRegimen = null

      try {
        console.log('[RegimenModal] Cargando regímenes para hotel ID:', this.hotelId)
        const WEBSERVICE_URL = 'http://localhost:3000'
        const response = await axios.get(`${WEBSERVICE_URL}/api/regimenes/hotel/${this.hotelId}`)
        
        console.log('[RegimenModal] Respuesta completa:', response.data)
        
        // La respuesta tiene la estructura: { hotel: {...}, regimenes: [...] }
        // Cada régimen en el array tiene: { idPrecioRegimen, regimen: { idRegimen, codigo }, precio }
        const regimenesData = response.data.regimenes || []
        
        // Transformar al formato esperado por el modal
        this.regimenes = regimenesData.map(item => ({
          codigo: item.regimen.codigo,
          nombre: this.getRegimenNombre(item.regimen.codigo),
          precio: item.precio,
          idPrecioRegimen: item.idPrecioRegimen
        }))
        
        console.log('[RegimenModal] Regímenes parseados:', this.regimenes)
        
        if (this.regimenes.length === 0) {
          this.error = 'No hay regímenes disponibles para este hotel'
        }
      } catch (error) {
        console.error('Error al cargar regímenes:', error)
        this.error = 'Error al cargar los regímenes disponibles'
        this.regimenes = []
      } finally {
        this.loading = false
      }
    },

    selectRegimen(regimen) {
      this.selectedRegimen = regimen
    },

    confirm() {
      if (!this.selectedRegimen) return
      
      this.$emit('confirm', {
        regimen: this.selectedRegimen,
        totalPrice: this.totalPrice
      })
      
      this.close()
    },

    close() {
      this.isVisible = false
      this.$emit('close')
    },

    getRegimenNombre(codigo) {
      const nombres = {
        'SA': 'Solo Alojamiento',
        'AD': 'Alojamiento y Desayuno',
        'MP': 'Media Pensión',
        'PC': 'Pensión Completa',
        'TI': 'Todo Incluido'
      }
      return nombres[codigo] || codigo
    },

    getRegimenDescripcion(codigo) {
      const descripciones = {
        'AD': 'Incluye alojamiento y desayuno buffet',
        'MP': 'Incluye desayuno y cena',
        'PC': 'Incluye desayuno, comida y cena',
        'TI': 'Todas las comidas y bebidas incluidas'
      }
      return descripciones[codigo] || ''
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  padding: 1rem;
  overflow-y: auto;
}

.modal-container {
  background: white;
  border-radius: 12px;
  max-width: 700px;
  width: 100%;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--primary-color);
}

.modal-close {
  background: none;
  border: none;
  font-size: 2rem;
  color: #999;
  cursor: pointer;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.modal-close:hover {
  background: #f5f5f5;
  color: #333;
}

.modal-body {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.loading-spinner {
  text-align: center;
  padding: 3rem;
  color: var(--accent-color);
}

.regimenes-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.regimen-card {
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.regimen-card:hover {
  border-color: var(--accent-color);
  box-shadow: 0 4px 12px rgba(147, 51, 234, 0.1);
  transform: translateY(-2px);
}

.regimen-card.selected {
  border-color: var(--accent-color);
  background: linear-gradient(135deg, rgba(147, 51, 234, 0.05) 0%, rgba(107, 70, 193, 0.05) 100%);
  box-shadow: 0 4px 12px rgba(147, 51, 234, 0.2);
}

.regimen-info {
  flex: 1;
}

.regimen-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 0.5rem;
}

.regimen-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: var(--primary-color);
}

.regimen-badge {
  background: var(--accent-color);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.regimen-description {
  margin: 0;
  color: var(--text-light);
  font-size: 0.9rem;
}

.regimen-price {
  text-align: right;
  margin-left: 1rem;
}

.price-label {
  font-size: 0.85rem;
  color: var(--text-light);
  margin-bottom: 0.25rem;
}

.price-amount {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--accent-color);
}

.selected-check {
  position: absolute;
  top: 1rem;
  right: 1rem;
  color: var(--accent-color);
  font-size: 1.5rem;
}

.price-summary {
  margin-top: 1.5rem;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  color: var(--text-color);
}

.summary-row.total {
  border-top: 2px solid #ddd;
  margin-top: 0.5rem;
  padding-top: 1rem;
  font-size: 1.2rem;
  color: var(--primary-color);
}

.no-regimenes {
  text-align: center;
  padding: 3rem;
  color: var(--text-light);
}

.no-regimenes i {
  color: #ffa500;
  margin-bottom: 1rem;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #eee;
}

.btn-secondary {
  padding: 0.75rem 1.5rem;
  border: 1px solid #ddd;
  background: white;
  color: var(--text-color);
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-secondary:hover {
  background: #f5f5f5;
}

.btn-primary {
  padding: 0.75rem 1.5rem;
  border: none;
  background: linear-gradient(135deg, var(--accent-color) 0%, var(--secondary-color) 100%);
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(147, 51, 234, 0.3);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Animación del modal */
.modal-enter-active, .modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from, .modal-leave-to {
  opacity: 0;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.3s ease;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.9);
}
</style>
