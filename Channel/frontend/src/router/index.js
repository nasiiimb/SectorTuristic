import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Hoteles from '../views/Hoteles.vue'
import Habitaciones from '../views/Habitaciones.vue'
import Disponibilidad from '../views/Disponibilidad.vue'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { public: true }
  },
  {
    path: '/',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/hoteles',
    name: 'Hoteles',
    component: Hoteles
  },
  {
    path: '/habitaciones',
    name: 'Habitaciones',
    component: Habitaciones
  },
  {
    path: '/disponibilidad',
    name: 'Disponibilidad',
    component: Disponibilidad
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Cache para validación de token (evitar verificación constante)
let tokenValidationCache = null
let tokenValidationTime = 0
const TOKEN_VALIDATION_CACHE_TIME = 5 * 60 * 1000 // 5 minutos

// Guard de navegación para proteger rutas
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const isPublic = to.meta.public

  // Si no hay token y la ruta no es pública, ir a login
  if (!token && !isPublic) {
    next('/login')
    return
  }
  
  // Si hay token pero está expirado (simple validación local)
  // Los JWT inválidos serán rechazados por el servidor cuando se use el token
  if (token && !isPublic) {
    try {
      // Decodificar el payload del JWT sin verificar firma (validación básica local)
      const parts = token.split('.')
      if (parts.length !== 3) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        next('/login')
        return
      }
      
      const payload = JSON.parse(atob(parts[1]))
      const expirationTime = payload.exp * 1000 // exp está en segundos, convertir a ms
      
      // Si el token está expirado, limpiar y ir a login
      if (Date.now() > expirationTime) {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        next('/login')
        return
      }
    } catch (error) {
      // Token mal formado, limpiar
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      next('/login')
      return
    }
  }
  
  // Si hay token válido y quiere ir a login, redirigir a dashboard
  if (token && to.path === '/login') {
    next('/')
    return
  }
  
  next()
})

export default router
