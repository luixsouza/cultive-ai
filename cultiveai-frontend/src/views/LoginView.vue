<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-bg via-green-50 to-slate-50 dark:from-bg-dark dark:via-slate-900 dark:to-slate-950 px-4">
    <div class="w-full max-w-sm bg-white dark:bg-slate-900 rounded-2xl p-8 md:p-10 shadow-xl border border-slate-100 dark:border-slate-800">
      <!-- Header -->
      <div class="text-center mb-7">
        <div class="inline-flex items-center justify-center w-14 h-14 bg-primary rounded-2xl mb-4">
          <span class="material-icons-round text-white text-3xl">eco</span>
        </div>
        <h1 class="text-2xl font-bold">
          <span class="text-primary">Cultive</span><span class="text-secondary">AI</span>
        </h1>
        <p class="text-slate-400 dark:text-slate-500 text-sm mt-1">Analise inteligente de pastagens</p>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label for="email" class="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1.5">Email</label>
          <input
            id="email"
            type="email"
            v-model="email"
            placeholder="seu@email.com"
            required
            autocomplete="email"
            class="w-full px-3.5 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 placeholder-slate-400 transition-colors"
          />
        </div>
        <div>
          <label for="password" class="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1.5">Senha</label>
          <input
            id="password"
            type="password"
            v-model="password"
            placeholder="Sua senha"
            required
            autocomplete="current-password"
            class="w-full px-3.5 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 placeholder-slate-400 transition-colors"
          />
        </div>
        <button
          type="submit"
          :disabled="loading"
          class="w-full py-3.5 bg-primary hover:bg-primary-dark text-white font-semibold rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed mt-2"
        >
          {{ loading ? "Entrando..." : "Entrar" }}
        </button>
        <p
          v-if="error"
          class="text-danger text-center text-sm bg-danger-bg dark:bg-red-900/30 px-4 py-2.5 rounded-xl"
        >
          {{ error }}
        </p>
      </form>

      <!-- Footer -->
      <p class="text-center text-sm text-slate-400 dark:text-slate-500 mt-6">
        Nao tem conta?
        <router-link to="/register" class="text-primary font-medium hover:underline">Criar conta</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import ApiService from "@/services/ApiService";
import { saveTokens } from "@/services/auth";

const email = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);
const router = useRouter();

async function handleLogin() {
  error.value = "";
  loading.value = true;
  try {
    const response = await ApiService.login(email.value, password.value);
    saveTokens(response.data.access_token, response.data.refresh_token);
    router.push("/");
  } catch (err) {
    error.value = err.response?.data?.detail || "Email ou senha invalidos.";
  } finally {
    loading.value = false;
  }
}
</script>
