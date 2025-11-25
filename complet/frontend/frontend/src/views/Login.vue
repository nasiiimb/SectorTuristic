<template>
  <div>
    <h2>Login</h2>
    <input v-model="email" placeholder="Email" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="login">Entrar</button>
    <p v-if="error">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return { email: '', password: '', error: '' };
  },
  methods: {
    async login() {
      try {
        const res = await axios.post('http://localhost:5000/login', {
          email: this.email,
          password: this.password
        });
        localStorage.setItem('token', res.data.token);
        alert('Login correcto');
      } catch (err) {
        this.error = 'Credenciales inválidas';
      }
    }
  }
};
</script>
