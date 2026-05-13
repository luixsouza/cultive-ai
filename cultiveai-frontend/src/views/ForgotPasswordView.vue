<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-bg via-green-50 to-slate-50 dark:from-bg-dark dark:via-slate-900 dark:to-slate-950 px-4 py-10">
    <div class="relative w-full max-w-5xl flex flex-col md:flex-row md:items-stretch">
      <!-- Left card: branding -->
      <div
        class="relative md:w-1/2 md:-mr-6 md:mt-4 md:mb-16 overflow-hidden shadow-2xl text-white bg-gradient-to-br from-primary-dark via-primary to-primary-light p-10 md:p-12 z-0"
      >
        <div class="absolute -bottom-24 -right-24 w-80 h-80 rounded-full bg-secondary/40 blur-3xl pointer-events-none"></div>
        <div class="absolute -top-20 -left-20 w-72 h-72 rounded-full bg-accent/25 blur-3xl pointer-events-none"></div>
        <svg class="absolute bottom-0 left-0 w-full opacity-25 pointer-events-none" viewBox="0 0 400 200" preserveAspectRatio="none">
          <path d="M0,140 C90,30 220,210 400,90 L400,200 L0,200 Z" fill="#95D5B2" />
          <path d="M0,160 C120,80 240,220 400,120 L400,200 L0,200 Z" fill="#FFFFFF" opacity="0.18" />
        </svg>

        <div class="relative flex flex-col justify-between min-h-[460px]">
          <div class="flex items-center gap-3">
            <div class="bg-white/15 backdrop-blur-sm p-2.5 ring-1 ring-white/30">
              <span class="material-icons-round text-white text-3xl">eco</span>
            </div>
            <h1 class="text-2xl font-bold tracking-tight">
              <span class="text-white">Cultive</span><span class="text-accent">AI</span>
            </h1>
          </div>

          <div class="mt-10">
            <h2 class="text-4xl md:text-5xl leading-tight">
              <span class="font-light">Recupere o acesso</span><br />
              <span class="font-extrabold">Sem Complicação</span>
            </h2>
            <p class="text-white/85 mt-5 text-sm md:text-base leading-relaxed max-w-md">
              Informe seu email cadastrado e enviaremos um link seguro para você redefinir sua senha em segundos.
            </p>
            <router-link
              to="/login"
              class="inline-flex items-center gap-2 mt-7 px-6 py-2.5 bg-white/10 hover:bg-white/20 backdrop-blur-sm ring-1 ring-white/40 text-sm font-medium transition-colors"
            >
              <span class="material-icons-round text-base">arrow_back</span>
              Voltar ao login
            </router-link>
          </div>

          <div class="flex items-center gap-2 mt-10">
            <span class="w-3 h-1 rounded-full bg-white/40"></span>
            <span class="w-8 h-1 rounded-full bg-white"></span>
            <span class="w-3 h-1 rounded-full bg-white/40"></span>
          </div>
        </div>
      </div>

      <!-- Right card: form -->
      <div
        class="relative md:w-1/2 md:-ml-6 md:mt-16 md:mb-4 bg-white dark:bg-slate-900 shadow-2xl border border-slate-100 dark:border-slate-800 p-8 md:p-12 md:pl-14 flex flex-col justify-center z-10"
      >
        <h1 class="text-3xl md:text-4xl font-bold text-slate-800 dark:text-white">Esqueceu a senha?</h1>
        <p class="text-slate-400 dark:text-slate-500 text-sm mt-2 leading-relaxed">
          Sem problema. Informe seu email para receber as instruções de redefinição.
        </p>

        <form @submit.prevent="handleSubmit" class="space-y-4 mt-7">
          <div class="border-l-4 border-primary bg-slate-50 dark:bg-slate-800 px-4 py-2.5">
            <label for="email" class="block text-[10px] tracking-[0.18em] font-semibold text-slate-400 mb-0.5">EMAIL</label>
            <input
              id="email"
              type="email"
              v-model="email"
              placeholder="seu@email.com"
              required
              autocomplete="email"
              class="w-full bg-transparent text-slate-800 dark:text-slate-200 placeholder-slate-400 outline-none"
            />
          </div>

          <button
            type="submit"
            :disabled="loading || sent"
            class="w-full py-3.5 bg-gradient-to-r from-primary-dark via-primary to-primary-light hover:opacity-95 text-white font-semibold tracking-[0.22em] text-sm shadow-lg shadow-primary/25 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed mt-2"
          >
            {{ loading ? "ENVIANDO..." : sent ? "LINK ENVIADO" : "ENVIAR LINK" }}
          </button>

          <p
            v-if="sent"
            class="text-primary text-center text-sm bg-primary-bg dark:bg-green-900/30 px-4 py-2.5"
          >
            Se o email existir em nossa base, você receberá um link em instantes.
          </p>
          <p
            v-if="error"
            class="text-danger text-center text-sm bg-danger-bg dark:bg-red-900/30 px-4 py-2.5"
          >
            {{ error }}
          </p>
        </form>

        <p class="text-center text-sm text-slate-400 dark:text-slate-500 mt-8">
          Lembrou da senha?
          <router-link to="/login" class="text-primary font-semibold hover:underline">Entrar</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const email = ref("");
const error = ref("");
const sent = ref(false);
const loading = ref(false);

async function handleSubmit() {
  error.value = "";
  loading.value = true;
  try {
    // TODO: integrar com endpoint do backend quando disponível
    await new Promise((resolve) => setTimeout(resolve, 800));
    sent.value = true;
  } catch (err) {
    error.value = err.response?.data?.detail || "Não foi possível enviar o link. Tente novamente.";
  } finally {
    loading.value = false;
  }
}
</script>
