import axios from 'axios'

const API_URL = 'http://localhost:8010/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Interceptor para añadir el token
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Auth
export const register = (data) => api.post('/auth/register', data)
export const login = (data) => api.post('/auth/login', data)
export const getProfile = () => api.get('/auth/profile')

// Search & Booking
export const searchAvailability = (params) => api.get('/search', { params })
export const createBooking = (data) => api.post('/book', data)
export const getMyReservations = () => api.get('/my-reservations')
export const getReservationByLocalizador = (localizador) => api.get(`/reservations/${localizador}`)

export default api
