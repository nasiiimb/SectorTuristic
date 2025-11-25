import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/Login.vue';
import Verificacion from '../views/Verificacion.vue';

const routes = [
  { path: '/', name: 'Login', component: Login },
  { path: '/verificar', name: 'Verificacion', component: Verificacion, meta: { requiresAuth: true } }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Middleware para proteger rutas
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');
  if (to.meta.requiresAuth && !token) {
    next('/');
  } else {
    next();
  }
});

export default router;
