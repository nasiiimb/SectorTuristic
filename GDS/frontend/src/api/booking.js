import axios from 'axios'

const API_URL = '/api'

export const bookingAPI = {
  async search(filters) {
    const response = await axios.get(`${API_URL}/search`, { params: filters })
    return response.data
  },

  async book(reservationData) {
    const token = localStorage.getItem('token')
    const response = await axios.post(`${API_URL}/book`, reservationData, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return response.data
  },

  async getMyReservations() {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${API_URL}/my-reservations`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return response.data
  },

  async getReservationByLocalizador(localizador) {
    const token = localStorage.getItem('token')
    const response = await axios.get(`${API_URL}/reservations/${localizador}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    return response.data
  },

  // Obtener regímenes de un hotel del WebService
  async getRegimenesHotel(idHotel) {
    const WEBSERVICE_URL = 'http://localhost:3000'
    const response = await axios.get(`${WEBSERVICE_URL}/api/regimenes/hotel/${idHotel}`)
    return response.data
  }
}

