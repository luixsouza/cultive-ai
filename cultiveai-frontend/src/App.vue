<template>
  <div class="min-h-screen bg-bg-page dark:bg-bg-dark transition-colors duration-300">
    <!-- Header -->
    <header
      v-if="userIsLoggedIn"
      class="sticky top-0 z-50 bg-white/80 dark:bg-slate-900/80 ios-blur px-5 py-3 flex items-center justify-between border-b border-slate-200 dark:border-slate-800 no-print"
    >
      <router-link to="/" class="flex items-center gap-2">
        <div class="bg-primary p-1.5 rounded-lg">
          <span class="material-icons-round text-white text-xl">eco</span>
        </div>
        <h1 class="text-xl font-bold tracking-tight">
          <span class="text-primary">Cultive</span><span class="text-secondary">AI</span>
        </h1>
      </router-link>

      <!-- Desktop nav -->
      <nav class="hidden md:flex items-center gap-1">
        <router-link
          to="/"
          :class="[
            'px-3.5 py-2 rounded-lg text-sm font-medium transition-colors',
            isActive('/') ? 'bg-primary-bg text-primary' : 'text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800'
          ]"
        >Dashboard</router-link>
        <router-link
          to="/clients"
          :class="[
            'px-3.5 py-2 rounded-lg text-sm font-medium transition-colors',
            isActive('/clients') ? 'bg-primary-bg text-primary' : 'text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800'
          ]"
        >Clientes</router-link>
        <router-link
          to="/properties"
          :class="[
            'px-3.5 py-2 rounded-lg text-sm font-medium transition-colors',
            isActive('/properties') ? 'bg-primary-bg text-primary' : 'text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800'
          ]"
        >Propriedades</router-link>
        <router-link
          to="/analysis/new"
          :class="[
            'px-3.5 py-2 rounded-lg text-sm font-medium transition-colors ml-1',
            isActive('/analysis/new') ? 'bg-primary text-white' : 'bg-primary-bg text-primary hover:bg-primary hover:text-white'
          ]"
        >Nova Analise</router-link>
      </nav>

      <!-- Right side -->
      <div class="flex items-center gap-3">
        <button
          class="p-2 rounded-full hover:bg-slate-200 dark:hover:bg-slate-800 transition-colors"
          @click="toggleDarkMode"
        >
          <span class="material-icons-round text-slate-600 dark:text-slate-300 text-xl">
            {{ darkMode ? 'light_mode' : 'dark_mode' }}
          </span>
        </button>
        <!-- Desktop logout -->
        <a
          href="#"
          @click.prevent="logout"
          class="hidden md:flex items-center gap-1 text-slate-400 hover:text-danger text-sm font-medium px-2 py-1.5 rounded-lg hover:bg-danger-bg transition-colors"
        >
          <span class="material-icons-round text-base">logout</span>
          Sair
        </a>
        <div
          class="w-9 h-9 rounded-full bg-accent flex items-center justify-center text-primary font-bold border-2 border-white dark:border-slate-700 shadow-sm text-sm"
        >
          {{ userInitial }}
        </div>
      </div>
    </header>

    <!-- Main content -->
    <main
      :class="[
        userIsLoggedIn
          ? 'pt-4 md:pt-6 pb-28 md:pb-8'
          : 'min-h-screen'
      ]"
    >
      <router-view />
    </main>

    <!-- Bottom Navigation (mobile) -->
    <nav
      v-if="userIsLoggedIn"
      class="fixed bottom-0 left-0 right-0 z-50 bg-white/90 dark:bg-slate-900/90 ios-blur border-t border-slate-200 dark:border-slate-800 px-6 pb-6 pt-3 flex justify-between items-center md:hidden no-print"
    >
      <router-link
        to="/"
        :class="['flex flex-col items-center gap-1', isActive('/') ? 'text-primary' : 'text-slate-400 dark:text-slate-500']"
      >
        <span class="material-icons-round">dashboard</span>
        <span class="text-[10px] font-medium">Inicio</span>
      </router-link>
      <router-link
        to="/clients"
        :class="['flex flex-col items-center gap-1', isActive('/clients') ? 'text-primary' : 'text-slate-400 dark:text-slate-500']"
      >
        <span class="material-icons-round">person_search</span>
        <span class="text-[10px] font-medium">Clientes</span>
      </router-link>
      <router-link
        to="/properties"
        :class="['flex flex-col items-center gap-1', isActive('/properties') ? 'text-primary' : 'text-slate-400 dark:text-slate-500']"
      >
        <span class="material-icons-round">landscape</span>
        <span class="text-[10px] font-medium">Propriedades</span>
      </router-link>
      <button
        @click="logout"
        class="flex flex-col items-center gap-1 text-slate-400 dark:text-slate-500"
      >
        <span class="material-icons-round">logout</span>
        <span class="text-[10px] font-medium">Sair</span>
      </button>
    </nav>

    <!-- FAB - Nova Analise (mobile) -->
    <router-link
      v-if="userIsLoggedIn"
      to="/analysis/new"
      class="fixed bottom-24 right-5 w-14 h-14 bg-secondary text-white rounded-full shadow-2xl flex items-center justify-center hover:scale-110 active:scale-95 transition-all z-40 md:hidden no-print"
    >
      <span class="material-icons-round">add_chart</span>
    </router-link>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from "vue";
import { useRouter, useRoute } from "vue-router";
import { isLoggedIn, removeToken, getToken, parseJwt } from "./services/auth";

const router = useRouter();
const route = useRoute();
const userIsLoggedIn = ref(isLoggedIn());
const userEmail = ref("");
const darkMode = ref(localStorage.getItem("darkMode") === "true");

const userInitial = computed(() =>
  userEmail.value ? userEmail.value[0].toUpperCase() : "U"
);

function updateLoginState() {
  userIsLoggedIn.value = isLoggedIn();
  if (userIsLoggedIn.value) {
    const token = getToken();
    const payload = parseJwt(token);
    userEmail.value = payload?.sub || "";
  } else {
    userEmail.value = "";
  }
}

function isActive(path) {
  if (path === "/") return route.path === "/";
  return route.path.startsWith(path);
}

function toggleDarkMode() {
  darkMode.value = !darkMode.value;
  document.documentElement.classList.toggle("dark", darkMode.value);
  localStorage.setItem("darkMode", darkMode.value);
}

function logout() {
  removeToken();
  userIsLoggedIn.value = false;
  userEmail.value = "";
  router.push("/login");
}

watch(
  () => route.path,
  () => updateLoginState()
);

onMounted(() => {
  updateLoginState();
  if (darkMode.value) {
    document.documentElement.classList.add("dark");
  }
});
</script>
