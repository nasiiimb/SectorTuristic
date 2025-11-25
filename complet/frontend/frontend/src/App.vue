<script setup></script>

<template>
  <h1>You did it!</h1>
  <p>
    Visit <a href="https://vuejs.org/" target="_blank" rel="noopener">vuejs.org</a> to read the
    documentation
  </p>
  <div>
    <nav>
      <router-link to="/">Login</router-link>
      <router-link to="/verificar">Verificación</router-link>
    </nav>
    <router-view></router-view>
  </div>
</template>

<style scoped></style>
