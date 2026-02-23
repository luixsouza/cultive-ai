<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-bg via-green-50 to-slate-50 dark:from-bg-dark dark:via-slate-900 dark:to-slate-950 px-4">
    <div class="w-full max-w-sm bg-white dark:bg-slate-900 rounded-2xl p-8 md:p-10 shadow-xl border border-slate-100 dark:border-slate-800">
      <!-- Header -->
      <div class="text-center mb-6">
        <div class="inline-flex items-center justify-center w-14 h-14 bg-primary rounded-2xl mb-4">
          <span class="material-icons-round text-white text-3xl">eco</span>
        </div>
        <h1 class="text-2xl font-bold text-slate-800 dark:text-white">Criar Conta</h1>
        <p class="text-slate-400 dark:text-slate-500 text-sm mt-1">Comece a analisar pastagens com IA</p>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleRegister" class="space-y-3.5">
        <div>
          <label for="name" class="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1.5">Nome completo</label>
          <input
            id="name"
            type="text"
            v-model="fullName"
            placeholder="Seu nome"
            autocomplete="name"
            class="w-full px-3.5 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 placeholder-slate-400 transition-colors"
          />
        </div>
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
            placeholder="Minimo 6 caracteres"
            required
            minlength="6"
            autocomplete="new-password"
            class="w-full px-3.5 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 placeholder-slate-400 transition-colors"
          />
        </div>
        <div>
          <label for="confirm" class="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1.5">Confirmar senha</label>
          <input
            id="confirm"
            type="password"
            v-model="confirmPassword"
            placeholder="Repita a senha"
            required
            minlength="6"
            autocomplete="new-password"
            class="w-full px-3.5 py-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 placeholder-slate-400 transition-colors"
          />
        </div>
        <button
          type="submit"
          :disabled="loading"
          class="w-full py-3.5 bg-primary hover:bg-primary-dark text-white font-semibold rounded-xl transition-colors disabled:opacity-50 disabled:cursor-not-allowed mt-1"
        >
          {{ loading ? "Criando conta..." : "Criar conta" }}
        </button>
        <p
          v-if="error"
          class="text-danger text-center text-sm bg-danger-bg dark:bg-red-900/30 px-4 py-2.5 rounded-xl"
        >
          {{ error }}
        </p>
        <p
          v-if="success"
          class="text-primary text-center text-sm bg-primary-bg dark:bg-green-900/30 px-4 py-2.5 rounded-xl"
        >
          {{ success }}
        </p>
      </form>

      <!-- Footer -->
      <p class="text-center text-sm text-slate-400 dark:text-slate-500 mt-6">
        Ja tem conta?
        <router-link to="/login" class="text-primary font-medium hover:underline">Fazer login</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import ApiService from "@/services/ApiService";

const fullName = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const error = ref("");
const success = ref("");
const loading = ref(false);
const router = useRouter();

async function handleRegister() {
  error.value = "";
  success.value = "";
  if (password.value !== confirmPassword.value) { error.value = "As senhas nao conferem."; return; }
  if (password.value.length < 6) { error.value = "A senha deve ter pelo menos 6 caracteres."; return; }
  loading.value = true;
  try {
    await ApiService.register(email.value, password.value, fullName.value || null);
    success.value = "Conta criada! Redirecionando...";
    setTimeout(() => router.push("/login"), 2000);
  } catch (err) {
    error.value = err.response?.data?.detail || "Erro ao criar conta. Tente novamente.";
  } finally {
    loading.value = false;
  }
}
</script>
