<template>
  <div class="max-w-5xl mx-auto px-4 md:px-6">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3 mb-4">
      <div>
        <h1 class="text-xl md:text-2xl font-bold text-slate-800 dark:text-white">Clientes</h1>
        <p class="text-slate-400 dark:text-slate-500 text-sm mt-0.5">Gerencie seus clientes e suas propriedades</p>
      </div>
      <button
        @click="openCreateModal"
        class="w-full md:w-auto inline-flex items-center justify-center gap-1.5 bg-primary hover:bg-primary-dark text-white px-4 py-3 md:py-2.5 rounded-xl font-semibold text-sm transition-all cursor-pointer"
      >
        <span class="material-icons-round text-lg">person_add</span>
        Novo Cliente
      </button>
    </div>

    <!-- Search -->
    <div class="relative mb-4">
      <span class="material-icons-round absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-lg">search</span>
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Buscar por nome, documento, email ou cidade..."
        @input="debouncedSearch"
        class="w-full pl-11 pr-4 py-3 md:py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-200 text-sm placeholder-slate-400"
      />
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-12 text-slate-400 dark:text-slate-500 gap-3">
      <div class="w-8 h-8 border-3 border-slate-200 dark:border-slate-700 border-t-primary rounded-full animate-spin"></div>
      <p class="text-sm">Carregando clientes...</p>
    </div>

    <!-- Empty -->
    <div v-else-if="clients.length === 0" class="flex flex-col items-center justify-center py-12 text-slate-400 dark:text-slate-500 gap-3">
      <span class="material-icons-round text-5xl text-slate-300 dark:text-slate-600">person_off</span>
      <p class="text-sm">Nenhum cliente encontrado.</p>
      <button @click="openCreateModal" class="mt-1 bg-primary text-white px-5 py-2.5 rounded-xl font-medium text-sm hover:bg-primary-dark transition-colors cursor-pointer">
        Adicionar primeiro cliente
      </button>
    </div>

    <!-- Cards Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-[repeat(auto-fill,minmax(340px,1fr))] gap-3 md:gap-4">
      <div
        v-for="client in clients"
        :key="client.id"
        class="bg-white dark:bg-slate-900 rounded-2xl p-4 md:p-5 shadow-sm border border-slate-100 dark:border-slate-800 hover:shadow-md hover:border-slate-200 dark:hover:border-slate-700 transition-all"
      >
        <!-- Top row -->
        <div class="flex items-start gap-3 mb-3">
          <div class="w-9 h-9 md:w-10 md:h-10 rounded-xl bg-info-bg dark:bg-blue-900/30 flex items-center justify-center text-info font-bold text-sm shrink-0">
            {{ client.name?.[0]?.toUpperCase() || 'C' }}
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="text-[15px] font-semibold text-slate-800 dark:text-white truncate">{{ client.name }}</h3>
            <span v-if="client.city || client.state" class="text-xs text-slate-400 dark:text-slate-500">
              {{ client.city }}{{ client.state ? ` - ${client.state}` : "" }}
            </span>
          </div>
          <div class="flex gap-1">
            <button @click="openEditModal(client)" title="Editar" class="w-8 h-8 rounded-lg border border-slate-200 dark:border-slate-700 flex items-center justify-center text-slate-400 hover:text-primary hover:border-primary/30 hover:bg-primary-bg dark:hover:bg-green-900/20 transition-colors cursor-pointer">
              <span class="material-icons-round text-base">edit</span>
            </button>
            <button @click="confirmDelete(client)" title="Excluir" class="w-8 h-8 rounded-lg border border-slate-200 dark:border-slate-700 flex items-center justify-center text-slate-400 hover:text-danger hover:border-danger/30 hover:bg-danger-bg dark:hover:bg-red-900/20 transition-colors cursor-pointer">
              <span class="material-icons-round text-base">delete</span>
            </button>
          </div>
        </div>

        <!-- Details -->
        <div class="space-y-1 text-[13px] text-slate-500 dark:text-slate-400">
          <p v-if="client.document"><span class="font-medium text-slate-700 dark:text-slate-300">Doc:</span> {{ formatDocument(client.document) }}</p>
          <p v-if="client.email"><span class="font-medium text-slate-700 dark:text-slate-300">Email:</span> {{ client.email }}</p>
          <p v-if="client.phone"><span class="font-medium text-slate-700 dark:text-slate-300">Tel:</span> {{ formatPhone(client.phone) }}</p>
        </div>

        <!-- Footer -->
        <div class="flex justify-between items-center mt-3 pt-3 border-t border-slate-100 dark:border-slate-800">
          <span class="text-xs text-slate-400 dark:text-slate-500">{{ client.properties_count || 0 }} propriedade(s)</span>
          <router-link :to="`/clients/${client.id}/properties`" class="text-primary text-xs font-medium hover:underline">
            Ver propriedades
          </router-link>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-end md:items-center justify-center z-[1000]" @click.self="closeModal">
      <div class="bg-white dark:bg-slate-900 w-full md:w-[500px] md:max-w-[90%] rounded-t-2xl md:rounded-2xl p-6 md:p-7 shadow-2xl max-h-[90vh] overflow-y-auto">
        <h2 class="text-lg font-bold text-slate-800 dark:text-white mb-4">{{ editingClient ? "Editar Cliente" : "Novo Cliente" }}</h2>
        <form @submit.prevent="saveClient" class="space-y-3.5">
          <div>
            <label class="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1.5">Nome *</label>
            <input v-model="form.name" type="text" required placeholder="Nome do cliente" class="w-full px-3.5 py-3 md:py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 placeholder-slate-400 text-sm" />
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
            <div>
              <label class="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1.5">CPF/CNPJ</label>
              <input :value="form.document" @input="onDocumentInput" type="text" placeholder="000.000.000-00" :maxlength="18" :class="['w-full px-3.5 py-3 md:py-2.5 rounded-xl border bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 placeholder-slate-400 text-sm', fieldErrors.document ? 'border-danger' : 'border-slate-200 dark:border-slate-700']" />
              <p v-if="fieldErrors.document" class="text-danger text-[11px] mt-1">{{ fieldErrors.document }}</p>
            </div>
            <div>
              <label class="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1.5">Telefone</label>
              <input :value="form.phone" @input="onPhoneInput" type="text" placeholder="(00) 00000-0000" :maxlength="15" :class="['w-full px-3.5 py-3 md:py-2.5 rounded-xl border bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 placeholder-slate-400 text-sm', fieldErrors.phone ? 'border-danger' : 'border-slate-200 dark:border-slate-700']" />
              <p v-if="fieldErrors.phone" class="text-danger text-[11px] mt-1">{{ fieldErrors.phone }}</p>
            </div>
          </div>
          <div>
            <label class="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1.5">Email</label>
            <input v-model="form.email" type="email" placeholder="email@exemplo.com" class="w-full px-3.5 py-3 md:py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 placeholder-slate-400 text-sm" />
          </div>
          <div>
            <label class="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1.5">Endereco</label>
            <input v-model="form.address" type="text" placeholder="Rua, numero" class="w-full px-3.5 py-3 md:py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 placeholder-slate-400 text-sm" />
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
            <div>
              <label class="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1.5">Cidade</label>
              <input v-model="form.city" type="text" class="w-full px-3.5 py-3 md:py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 text-sm" />
            </div>
            <div>
              <label class="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1.5">Estado</label>
              <select v-model="form.state" class="w-full px-3.5 py-3 md:py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 text-sm">
                <option value="">Selecione</option>
                <option v-for="uf in states" :key="uf" :value="uf">{{ uf }}</option>
              </select>
            </div>
          </div>
          <div>
            <label class="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1.5">Observacoes</label>
            <textarea v-model="form.notes" rows="3" placeholder="Notas adicionais..." class="w-full px-3.5 py-3 md:py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 placeholder-slate-400 text-sm resize-none"></textarea>
          </div>
          <p v-if="formError" class="text-danger text-sm">{{ formError }}</p>
          <div class="flex justify-end gap-2.5 pt-2">
            <button type="button" @click="closeModal" class="px-4 py-2.5 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 rounded-xl text-sm font-medium border border-slate-200 dark:border-slate-700 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors cursor-pointer">
              Cancelar
            </button>
            <button type="submit" :disabled="saving" class="px-4 py-2.5 bg-primary text-white rounded-xl text-sm font-medium hover:bg-primary-dark transition-colors disabled:opacity-50 cursor-pointer">
              {{ saving ? "Salvando..." : "Salvar" }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Modal -->
    <div v-if="showDeleteModal" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-end md:items-center justify-center z-[1000]" @click.self="closeDeleteModal">
      <div class="bg-white dark:bg-slate-900 w-full md:w-[400px] md:max-w-[90%] rounded-t-2xl md:rounded-2xl p-6 md:p-7 shadow-2xl">
        <h2 class="text-lg font-bold text-slate-800 dark:text-white mb-3">Confirmar Exclusao</h2>
        <p class="text-slate-500 dark:text-slate-400 text-sm">
          Tem certeza que deseja excluir o cliente <strong class="text-slate-700 dark:text-slate-200">{{ clientToDelete?.name }}</strong>?
        </p>
        <p class="text-warning text-xs mt-2">Todas as propriedades e relatorios associados serao excluidos.</p>
        <div class="flex justify-end gap-2.5 mt-5">
          <button @click="closeDeleteModal" class="px-4 py-2.5 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 rounded-xl text-sm font-medium border border-slate-200 dark:border-slate-700 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors cursor-pointer">
            Cancelar
          </button>
          <button @click="deleteClient" :disabled="deleting" class="px-4 py-2.5 bg-danger text-white rounded-xl text-sm font-medium hover:bg-red-700 transition-colors disabled:opacity-50 cursor-pointer">
            {{ deleting ? "Excluindo..." : "Excluir" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import ApiService from "@/services/ApiService";

const clients = ref([]);
const loading = ref(true);
const searchQuery = ref("");
const showModal = ref(false);
const showDeleteModal = ref(false);
const editingClient = ref(null);
const clientToDelete = ref(null);
const saving = ref(false);
const deleting = ref(false);
const formError = ref("");

const states = [
  "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA",
  "MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN",
  "RS","RO","RR","SC","SP","SE","TO"
];

const form = ref({
  name: "", document: "", phone: "", email: "",
  address: "", city: "", state: "", notes: "",
});
const fieldErrors = ref({});

let searchTimeout = null;

// --- Masks ---
function maskCPF(v) {
  return v.replace(/(\d{3})(\d)/, "$1.$2").replace(/(\d{3})(\d)/, "$1.$2").replace(/(\d{3})(\d{1,2})$/, "$1-$2");
}
function maskCNPJ(v) {
  return v.replace(/(\d{2})(\d)/, "$1.$2").replace(/(\d{3})(\d)/, "$1.$2").replace(/(\d{3})(\d)/, "$1/$2").replace(/(\d{4})(\d{1,2})$/, "$1-$2");
}
function maskPhone(v) {
  if (v.length <= 10) {
    return v.replace(/(\d{2})(\d)/, "($1) $2").replace(/(\d{4})(\d{1,4})$/, "$1-$2");
  }
  return v.replace(/(\d{2})(\d)/, "($1) $2").replace(/(\d{5})(\d{1,4})$/, "$1-$2");
}

function onDocumentInput(e) {
  const digits = e.target.value.replace(/\D/g, "").slice(0, 14);
  form.value.document = digits.length <= 11 ? maskCPF(digits) : maskCNPJ(digits);
  fieldErrors.value.document = "";
}

function onPhoneInput(e) {
  const digits = e.target.value.replace(/\D/g, "").slice(0, 11);
  form.value.phone = digits.length > 0 ? maskPhone(digits) : "";
  fieldErrors.value.phone = "";
}

// --- Validators ---
function validateCPF(cpf) {
  const d = cpf.replace(/\D/g, "");
  if (d.length !== 11) return false;
  if (/^(\d)\1{10}$/.test(d)) return false;
  let sum = 0;
  for (let i = 0; i < 9; i++) sum += parseInt(d[i]) * (10 - i);
  let rest = (sum * 10) % 11;
  if (rest === 10) rest = 0;
  if (rest !== parseInt(d[9])) return false;
  sum = 0;
  for (let i = 0; i < 10; i++) sum += parseInt(d[i]) * (11 - i);
  rest = (sum * 10) % 11;
  if (rest === 10) rest = 0;
  return rest === parseInt(d[10]);
}

function validateCNPJ(cnpj) {
  const d = cnpj.replace(/\D/g, "");
  if (d.length !== 14) return false;
  if (/^(\d)\1{13}$/.test(d)) return false;
  const weights1 = [5,4,3,2,9,8,7,6,5,4,3,2];
  const weights2 = [6,5,4,3,2,9,8,7,6,5,4,3,2];
  let sum = 0;
  for (let i = 0; i < 12; i++) sum += parseInt(d[i]) * weights1[i];
  let rest = sum % 11;
  if (rest < 2) rest = 0; else rest = 11 - rest;
  if (rest !== parseInt(d[12])) return false;
  sum = 0;
  for (let i = 0; i < 13; i++) sum += parseInt(d[i]) * weights2[i];
  rest = sum % 11;
  if (rest < 2) rest = 0; else rest = 11 - rest;
  return rest === parseInt(d[13]);
}

function validatePhone(phone) {
  const d = phone.replace(/\D/g, "");
  return d.length === 10 || d.length === 11;
}

function validateForm() {
  fieldErrors.value = {};
  let valid = true;

  if (form.value.document) {
    const digits = form.value.document.replace(/\D/g, "");
    if (digits.length <= 11) {
      if (!validateCPF(digits)) {
        fieldErrors.value.document = "CPF invalido";
        valid = false;
      }
    } else {
      if (!validateCNPJ(digits)) {
        fieldErrors.value.document = "CNPJ invalido";
        valid = false;
      }
    }
  }

  if (form.value.phone) {
    if (!validatePhone(form.value.phone)) {
      fieldErrors.value.phone = "Telefone invalido. Use (00) 00000-0000";
      valid = false;
    }
  }

  return valid;
}

function formatDocument(doc) {
  if (!doc) return doc;
  const d = doc.replace(/\D/g, "");
  if (d.length === 11) return maskCPF(d);
  if (d.length === 14) return maskCNPJ(d);
  return doc;
}

function formatPhone(phone) {
  if (!phone) return phone;
  const d = phone.replace(/\D/g, "");
  if (d.length >= 10) return maskPhone(d);
  return phone;
}

async function loadClients() {
  loading.value = true;
  try {
    const params = {};
    if (searchQuery.value) params.search = searchQuery.value;
    const response = await ApiService.getClients(params);
    clients.value = response.data;
  } catch (err) {
    console.error("Error loading clients:", err);
  } finally {
    loading.value = false;
  }
}

function debouncedSearch() {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => loadClients(), 300);
}

function openCreateModal() {
  editingClient.value = null;
  form.value = { name: "", document: "", phone: "", email: "", address: "", city: "", state: "", notes: "" };
  formError.value = "";
  fieldErrors.value = {};
  showModal.value = true;
}

function openEditModal(client) {
  editingClient.value = client;
  form.value = { ...client };
  formError.value = "";
  fieldErrors.value = {};
  showModal.value = true;
}

function closeModal() { showModal.value = false; editingClient.value = null; }

async function saveClient() {
  formError.value = "";
  if (!validateForm()) return;
  saving.value = true;
  try {
    if (editingClient.value) {
      await ApiService.updateClient(editingClient.value.id, form.value);
    } else {
      await ApiService.createClient(form.value);
    }
    closeModal();
    await loadClients();
  } catch (err) {
    formError.value = err.response?.data?.detail || "Erro ao salvar cliente.";
  } finally {
    saving.value = false;
  }
}

function confirmDelete(client) { clientToDelete.value = client; showDeleteModal.value = true; }
function closeDeleteModal() { showDeleteModal.value = false; clientToDelete.value = null; }

async function deleteClient() {
  deleting.value = true;
  try {
    await ApiService.deleteClient(clientToDelete.value.id);
    closeDeleteModal();
    await loadClients();
  } catch (err) {
    console.error("Error deleting client:", err);
  } finally {
    deleting.value = false;
  }
}

onMounted(() => loadClients());
</script>
