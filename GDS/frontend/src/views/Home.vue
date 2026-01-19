<template>
  <div>
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1>Encuentra tu hotel perfecto</h1>
        <p>Buscamos en múltiples proveedores para ofrecerte las mejores opciones</p>
      </div>
    </section>

    <!-- Search Bar -->
    <div class="container">
      <div class="search-bar">
        <form @submit.prevent="handleSearch" class="search-form">
          <div class="search-group">
            <label>Destino</label>
            <input 
              v-model="filters.ciudad" 
              type="text" 
              placeholder="Ciudad o país"
            />
          </div>
          
          <div class="search-group">
            <label>Fecha Entrada</label>
            <input 
              v-model="filters.fecha_entrada" 
              type="date" 
              required
              :min="today"
            />
          </div>
          
          <div class="search-group">
            <label>Fecha Salida</label>
            <input 
              v-model="filters.fecha_salida" 
              type="date" 
              required
              :min="filters.fecha_entrada || today"
            />
          </div>
          
          <div class="search-group">
            <label>Personas</label>
            <input 
              v-model.number="filters.personas" 
              type="number" 
              min="1" 
              max="10" 
              required
            />
          </div>
          
          <button type="submit" class="btn-search" :disabled="loading">
            {{ loading ? 'Buscando...' : 'Buscar' }}
          </button>
        </form>
      </div>
    </div>

    <!-- Featured Info -->
    <div class="container mt-2">
      <div class="text-center">
        <h2>Sistema de Reservas Integrado</h2>
        <p style="color: var(--text-light); margin-top: 1rem;">
          Conectamos con WebService y Channel Manager para ofrecerte la mayor disponibilidad
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {
      filters: {
        ciudad: '',
        fecha_entrada: '',
        fecha_salida: '',
        personas: 2
      },
      loading: false,
      today: new Date().toISOString().split('T')[0]
    }
  },
  methods: {
    async handleSearch() {
      if (!this.filters.fecha_entrada || !this.filters.fecha_salida) {
        alert('Por favor, selecciona las fechas de entrada y salida')
        return
      }
      
      if (this.filters.fecha_salida <= this.filters.fecha_entrada) {
        alert('La fecha de salida debe ser posterior a la fecha de entrada')
        return
      }

      this.loading = true
      
      try {
        // Redirigir a página de resultados con los filtros
        this.$router.push({
          name: 'Search',
          query: {
            ...this.filters
          }
        })
      } catch (error) {
        console.error('Error en búsqueda:', error)
        alert('Error al realizar la búsqueda')
      } finally {
        this.loading = false
      }
    }
  }
}
</script>
