<template>
  <header>
    <nav>
      <router-link to="/">Mapeamento</router-link>
      <a href="#" @click.prevent="logout" v-if="userIsLoggedIn">Sair</a>
    </nav>
  </header>
  <main>
    <router-view />
  </main>
</template>

<script setup>
import { ref, watchEffect } from "vue";
import { useRouter } from "vue-router";
import { isLoggedIn, removeToken } from "./services/auth";

const router = useRouter();
const userIsLoggedIn = ref(isLoggedIn());

watchEffect(() => {
  userIsLoggedIn.value = isLoggedIn();
});

function logout() {
  removeToken();
  userIsLoggedIn.value = false;
  router.push("/login");
}
</script>

<style scoped>
header {
  background-color: #fff;
  padding: 15px 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}
nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
nav a {
  font-weight: bold;
  color: var(--primary-color);
  text-decoration: none;
  padding: 5px 10px;
}
nav a.router-link-exact-active {
  color: var(--secondary-color);
  border-bottom: 2px solid var(--secondary-color);
}
</style>
