<template>
  <div class="app-container">
    <header v-if="userIsLoggedIn" class="app-header">
      <nav>
        <div class="nav-top">
          <router-link to="/" class="brand">
            <span class="brand-icon">🌿</span>
            <span class="brand-text">CultiveAI</span>
          </router-link>
          <div class="nav-right-mobile">
            <button class="menu-toggle" @click="menuOpen = !menuOpen" aria-label="Menu">
              <svg v-if="!menuOpen" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
              <svg v-else width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
          </div>
          <!-- Desktop nav -->
          <div class="nav-links-desktop">
            <router-link to="/" :class="{ active: isActive('/') }">Dashboard</router-link>
            <router-link to="/clients" :class="{ active: isActive('/clients') }">Clientes</router-link>
            <router-link to="/properties" :class="{ active: isActive('/properties') }">Propriedades</router-link>
            <router-link to="/analysis/new" :class="['nav-cta', { active: isActive('/analysis/new') }]">Nova Analise</router-link>
          </div>
          <div class="nav-user-desktop">
            <div class="user-avatar">{{ userInitial }}</div>
            <span class="user-email">{{ userEmail }}</span>
            <a href="#" @click.prevent="logout" class="logout-btn">Sair</a>
          </div>
        </div>
        <!-- Mobile menu -->
        <div v-if="menuOpen" class="nav-mobile-menu">
          <router-link to="/" @click="menuOpen = false" :class="{ active: isActive('/') }">Dashboard</router-link>
          <router-link to="/clients" @click="menuOpen = false" :class="{ active: isActive('/clients') }">Clientes</router-link>
          <router-link to="/properties" @click="menuOpen = false" :class="{ active: isActive('/properties') }">Propriedades</router-link>
          <router-link to="/analysis/new" @click="menuOpen = false" :class="{ active: isActive('/analysis/new') }">Nova Analise</router-link>
          <div class="mobile-user">
            <span v-if="userEmail">{{ userEmail }}</span>
            <a href="#" @click.prevent="logout; menuOpen = false" class="logout-link">Sair da conta</a>
          </div>
        </div>
      </nav>
    </header>
    <main :class="{ 'no-header': !userIsLoggedIn }">
      <router-view />
    </main>
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
const menuOpen = ref(false);

const userInitial = computed(() => userEmail.value ? userEmail.value[0].toUpperCase() : "U");

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

function logout() {
  removeToken();
  userIsLoggedIn.value = false;
  userEmail.value = "";
  router.push("/login");
}

watch(() => route.path, () => { updateLoginState(); menuOpen.value = false; });
onMounted(() => updateLoginState());
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  background-color: var(--bg-page);
}

/* Header */
.app-header {
  background: var(--bg-card);
  padding: 0 16px;
  box-shadow: 0 1px 0 var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
}

nav {
  max-width: 1400px;
  margin: 0 auto;
}

.nav-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 52px;
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  text-decoration: none;
}

.brand-icon { font-size: 20px; }
.brand-text {
  font-size: 17px;
  font-weight: 700;
  color: var(--primary-color);
  letter-spacing: -0.3px;
}

/* Mobile menu toggle */
.menu-toggle {
  background: none;
  border: none;
  padding: 6px;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
}

/* Desktop nav hidden on mobile */
.nav-links-desktop, .nav-user-desktop {
  display: none;
}

/* Mobile menu */
.nav-mobile-menu {
  display: flex;
  flex-direction: column;
  padding: 8px 0 16px;
  border-top: 1px solid var(--border-light);
}

.nav-mobile-menu a {
  display: block;
  padding: 12px 8px;
  color: var(--text-secondary);
  font-size: 15px;
  font-weight: 500;
  border-radius: var(--radius-sm);
  transition: all var(--transition);
}

.nav-mobile-menu a.active {
  background: var(--primary-bg);
  color: var(--primary-color);
}

.mobile-user {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--border-light);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.mobile-user span {
  font-size: 13px;
  color: var(--text-muted);
  padding: 0 8px;
}

.logout-link {
  color: var(--danger-color) !important;
  font-size: 14px;
}

/* Desktop: min-width 768px */
@media (min-width: 768px) {
  .app-header { padding: 0 24px; }
  .nav-top { height: 56px; }
  .menu-toggle, .nav-right-mobile { display: none; }
  .nav-mobile-menu { display: none !important; }

  .nav-links-desktop {
    display: flex;
    gap: 2px;
  }

  .nav-links-desktop a {
    color: var(--text-secondary);
    text-decoration: none;
    padding: 7px 14px;
    border-radius: var(--radius-sm);
    font-size: 13px;
    font-weight: 500;
    transition: all var(--transition);
  }

  .nav-links-desktop a:hover {
    background: var(--bg-page);
    color: var(--text-primary);
  }

  .nav-links-desktop a.active {
    background: var(--primary-bg);
    color: var(--primary-color);
  }

  .nav-links-desktop a.nav-cta {
    background: var(--primary-bg);
    color: var(--primary-color);
  }

  .nav-links-desktop a.nav-cta.active {
    background: var(--primary-color);
    color: white;
  }

  .nav-user-desktop {
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .user-avatar {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: var(--primary-bg);
    color: var(--primary-color);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 600;
  }

  .user-email {
    color: var(--text-muted);
    font-size: 13px;
  }

  .logout-btn {
    color: var(--text-muted);
    font-size: 13px;
    padding: 5px 10px;
    border-radius: var(--radius-sm);
  }

  .logout-btn:hover {
    background: var(--danger-bg);
    color: var(--danger-color);
  }
}

main {
  padding: 16px 0;
  min-height: calc(100vh - 52px);
}

main.no-header {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

@media (min-width: 768px) {
  main {
    padding: 24px 0;
    min-height: calc(100vh - 56px);
  }
}
</style>
