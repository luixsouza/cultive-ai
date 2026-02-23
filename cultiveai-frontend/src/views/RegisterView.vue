<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <span class="auth-logo">🌿</span>
        <h1>Criar Conta</h1>
        <p>Comece a analisar pastagens com IA</p>
      </div>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="name">Nome completo</label>
          <input id="name" type="text" v-model="fullName" placeholder="Seu nome" autocomplete="name" />
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input id="email" type="email" v-model="email" placeholder="seu@email.com" required autocomplete="email" />
        </div>
        <div class="form-group">
          <label for="password">Senha</label>
          <input id="password" type="password" v-model="password" placeholder="Minimo 6 caracteres" required minlength="6" autocomplete="new-password" />
        </div>
        <div class="form-group">
          <label for="confirm">Confirmar senha</label>
          <input id="confirm" type="password" v-model="confirmPassword" placeholder="Repita a senha" required minlength="6" autocomplete="new-password" />
        </div>
        <button type="submit" class="btn-submit" :disabled="loading">
          {{ loading ? "Criando conta..." : "Criar conta" }}
        </button>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <p v-if="success" class="success-msg">{{ success }}</p>
      </form>
      <p class="auth-footer">
        Ja tem conta? <router-link to="/login">Fazer login</router-link>
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

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0f7f0 0%, #e8f5e9 50%, #f5f5f5 100%);
  padding: 16px;
}

.auth-card {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: var(--radius-lg);
  padding: 32px 24px;
  box-shadow: var(--shadow-lg);
}

.auth-header { text-align: center; margin-bottom: 24px; }
.auth-logo { font-size: 36px; display: block; margin-bottom: 10px; }
.auth-header h1 { font-size: 22px; color: var(--primary-color); margin: 0 0 4px; }
.auth-header p { color: var(--text-muted); font-size: 14px; margin: 0; }

.form-group { margin-bottom: 14px; }
.form-group label { display: block; margin-bottom: 6px; font-size: 13px; font-weight: 500; color: var(--text-secondary); }
.form-group input {
  display: block; width: 100%; padding: 12px 14px;
  border: 1px solid var(--border-color); border-radius: var(--radius-sm);
  background: var(--bg-page); color: var(--text-primary);
}

.btn-submit {
  width: 100%; padding: 14px;
  background: var(--primary-color); color: white; border: none;
  border-radius: var(--radius-sm); font-size: 16px; font-weight: 600; margin-top: 4px;
}
.btn-submit:hover:not(:disabled) { background: var(--primary-dark); }
.btn-submit:disabled { background: #bbb; }

.error-msg {
  color: var(--danger-color); text-align: center; margin-top: 14px;
  font-size: 13px; background: var(--danger-bg); padding: 10px; border-radius: var(--radius-sm);
}
.success-msg {
  color: var(--primary-color); text-align: center; margin-top: 14px;
  font-size: 13px; background: var(--primary-bg); padding: 10px; border-radius: var(--radius-sm);
}

.auth-footer { text-align: center; margin: 20px 0 0; font-size: 14px; color: var(--text-muted); }
.auth-footer a { color: var(--primary-color); font-weight: 500; }

@media (min-width: 768px) {
  .auth-card { padding: 36px; }
}
</style>
