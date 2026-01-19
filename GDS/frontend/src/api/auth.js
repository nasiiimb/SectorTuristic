import axios from 'axios'

const API_URL = '/api/auth'

export const authAPI = {
  async register(data) {
    const response = await axios.post(`${API_URL}/register`, data)
    // Guardar token después del registro
    if (response.data.data?.token) {
      localStorage.setItem('token', response.data.data.token)
    }
    return response.data
  },

  async login(email, password) {
    const response = await axios.post(`${API_URL}/login`, { email, password })
    // Guardar token después del login
    if (response.data.data?.token) {
      localStorage.setItem('token', response.data.data.token)
    }
    return response.data
  },

  async getProfile() {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${API_URL}/profile`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return response.data
  },

  logout() {
    localStorage.removeItem('token')
  },

  isAuthenticated() {
    return !!localStorage.getItem('token')
  }
}
