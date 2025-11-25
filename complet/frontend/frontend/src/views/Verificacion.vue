<template>
  <div>
    <h2>Verificar Token</h2>
    <button @click="verifyToken">Verificar</button>
    <p>{{ message }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return { message: '' };
  },
  methods: {
    async verifyToken() {
      const token = localStorage.getItem('token');
      try {
        const res = await axios.post('http://localhost:5000/verify', {}, {
          headers: { Authorization: `Bearer ${token}` }
        });
        this.message = res.data.message;
      } catch (err) {
        this.message = 'Token inválido o expirado';
      }
    }
  }
};
</script>
