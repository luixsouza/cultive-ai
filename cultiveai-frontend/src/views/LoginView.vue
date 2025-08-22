<template>
  <div class="login-container">
    <h2>Login CultiveAI</h2>
    <form @submit.prevent="handleLogin">
      <input type="email" v-model="email" placeholder="Email" required />
      <input type="password" v-model="password" placeholder="Senha" required />
      <button type="submit">Entrar</button>
      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import ApiService from "@/services/ApiService";
import { saveToken } from "@/services/auth";

const email = ref("");
const password = ref("");
const error = ref("");
const router = useRouter();

async function handleLogin() {
  try {
    const response = await ApiService.login(email.value, password.value);
    saveToken(response.data.access_token);
    router.push("/");
  } catch (err) {
    error.value = "Email ou senha inválidos.";
    console.error(err);
  }
}
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
input {
  display: block;
  width: 95%;
  padding: 10px;
  margin-bottom: 10px;
}
.error {
  color: red;
}
</style>
