import axios from 'axios'

const API_URL = 'http://127.0.0.1:8001/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para añadir token en header Authorization (estándar Bearer)
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth
export const authApi = {
  login: (data) => api.post('/auth/login', data),
  register: (data) => api.post('/auth/register', data),
  logout: () => api.post('/auth/logout'),
  me: () => api.get('/auth/me')
}

// Hoteles
export const hotelesApi = {
  listar: (params = {}) => api.get('/hoteles', { params }),
  obtener: (id) => api.get(`/hoteles/${id}`),
  crear: (data) => api.post('/hoteles', data),
  actualizar: (id, data) => api.put(`/hoteles/${id}`, data),
  eliminar: (id) => api.delete(`/hoteles/${id}`)
}

// Habitaciones
export const habitacionesApi = {
  listar: (params = {}) => api.get('/habitaciones', { params }),
  obtener: (id) => api.get(`/habitaciones/${id}`),
  crear: (data) => api.post('/habitaciones', data),
  actualizar: (id, data) => api.put(`/habitaciones/${id}`, data),
  eliminar: (id) => api.delete(`/habitaciones/${id}`)
}

// Disponibilidad
export const disponibilidadApi = {
  listar: (params = {}) => api.get('/disponibilidad', { params }),
  crear: (data) => api.post('/disponibilidad', data),
  crearBulk: (data) => api.post('/disponibilidad/bulk', data),
  actualizar: (id, data) => api.put(`/disponibilidad/${id}`, data),
  eliminar: (id) => api.delete(`/disponibilidad/${id}`)
}

// Health check
export const healthCheck = () => axios.get('http://127.0.0.1:8001/health')

export default api
