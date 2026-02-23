<template>
  <div class="max-w-5xl mx-auto px-4 md:px-6">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3 mb-4">
      <div>
        <h1 class="text-xl md:text-2xl font-bold text-slate-800 dark:text-white">Propriedades</h1>
        <p v-if="clientFilter" class="text-slate-400 dark:text-slate-500 text-sm mt-0.5">
          Cliente: {{ clientFilter.name }}
          <button @click="clearClientFilter" class="text-primary text-xs underline ml-2 cursor-pointer">Limpar filtro</button>
        </p>
        <p v-else class="text-slate-400 dark:text-slate-500 text-sm mt-0.5">Gerencie propriedades rurais e inicie analises</p>
      </div>
      <button
        @click="openCreateModal"
        class="w-full md:w-auto inline-flex items-center justify-center gap-1.5 bg-primary hover:bg-primary-dark text-white px-4 py-3 md:py-2.5 rounded-xl font-semibold text-sm transition-all cursor-pointer"
      >
        <span class="material-icons-round text-lg">add_home_work</span>
        Nova Propriedade
      </button>
    </div>

    <!-- Filters -->
    <div class="flex flex-col md:flex-row gap-2 md:gap-3 mb-4">
      <div class="relative flex-1">
        <span class="material-icons-round absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-lg">search</span>
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Buscar por nome, cidade ou cliente..."
          @input="debouncedSearch"
          class="w-full pl-11 pr-4 py-3 md:py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-200 text-sm placeholder-slate-400"
        />
      </div>
      <select
        v-model="selectedClientId"
        @change="loadProperties"
        class="w-full md:w-60 px-3.5 py-3 md:py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-200 text-sm"
      >
        <option :value="null">Todos os clientes</option>
        <option v-for="client in allClients" :key="client.id" :value="client.id">{{ client.name }}</option>
      </select>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="flex flex-col items-center justify-center py-12 text-slate-400 dark:text-slate-500 gap-3">
      <div class="w-8 h-8 border-3 border-slate-200 dark:border-slate-700 border-t-primary rounded-full animate-spin"></div>
      <p class="text-sm">Carregando propriedades...</p>
    </div>

    <!-- Empty -->
    <div v-else-if="properties.length === 0" class="flex flex-col items-center justify-center py-12 text-slate-400 dark:text-slate-500 gap-3">
      <span class="material-icons-round text-5xl text-slate-300 dark:text-slate-600">holiday_village</span>
      <p class="text-sm">Nenhuma propriedade encontrada.</p>
      <button @click="openCreateModal" class="mt-1 bg-primary text-white px-5 py-2.5 rounded-xl font-medium text-sm hover:bg-primary-dark transition-colors cursor-pointer">
        Adicionar primeira propriedade
      </button>
    </div>

    <!-- Cards Grid -->
    <div v-else class="grid grid-cols-1 md:grid-cols-[repeat(auto-fill,minmax(340px,1fr))] gap-3 md:gap-4">
      <div
        v-for="prop in properties"
        :key="prop.id"
        class="bg-white dark:bg-slate-900 rounded-2xl p-4 md:p-5 shadow-sm border border-slate-100 dark:border-slate-800 hover:shadow-md hover:border-slate-200 dark:hover:border-slate-700 transition-all"
      >
        <!-- Top row -->
        <div class="flex items-start gap-3 mb-3">
          <div class="w-9 h-9 md:w-10 md:h-10 rounded-xl bg-primary-bg dark:bg-green-900/30 flex items-center justify-center text-primary font-bold text-sm shrink-0">
            {{ prop.name?.[0]?.toUpperCase() || 'P' }}
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="text-[15px] font-semibold text-slate-800 dark:text-white truncate">{{ prop.name }}</h3>
            <span class="text-xs text-slate-400 dark:text-slate-500">{{ prop.client_name }}</span>
          </div>
          <div class="flex gap-1">
            <button @click="openEditModal(prop)" title="Editar" class="w-8 h-8 rounded-lg border border-slate-200 dark:border-slate-700 flex items-center justify-center text-slate-400 hover:text-primary hover:border-primary/30 hover:bg-primary-bg dark:hover:bg-green-900/20 transition-colors cursor-pointer">
              <span class="material-icons-round text-base">edit</span>
            </button>
            <button @click="confirmDelete(prop)" title="Excluir" class="w-8 h-8 rounded-lg border border-slate-200 dark:border-slate-700 flex items-center justify-center text-slate-400 hover:text-danger hover:border-danger/30 hover:bg-danger-bg dark:hover:bg-red-900/20 transition-colors cursor-pointer">
              <span class="material-icons-round text-base">delete</span>
            </button>
          </div>
        </div>

        <!-- Details -->
        <div class="space-y-1 text-[13px] text-slate-500 dark:text-slate-400">
          <p v-if="prop.total_area_hectares"><span class="font-medium text-slate-700 dark:text-slate-300">Area:</span> {{ prop.total_area_hectares.toFixed(2) }} ha</p>
          <p v-if="prop.city || prop.state">
            <span class="font-medium text-slate-700 dark:text-slate-300">Local:</span> {{ prop.city }}{{ prop.state ? ` - ${prop.state}` : "" }}
          </p>
        </div>

        <!-- Footer -->
        <div class="flex justify-between items-center mt-3 pt-3 border-t border-slate-100 dark:border-slate-800">
          <span class="text-xs text-slate-400 dark:text-slate-500">{{ prop.reports_count || 0 }} analise(s)</span>
          <router-link :to="`/analysis/new?property=${prop.id}`" class="text-primary text-xs font-medium hover:underline">
            Nova analise
          </router-link>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-end md:items-center justify-center z-[1000]" @click.self="closeModal">
      <div class="bg-white dark:bg-slate-900 w-full md:w-[500px] md:max-w-[90%] rounded-t-2xl md:rounded-2xl p-6 md:p-7 shadow-2xl max-h-[90vh] overflow-y-auto">
        <h2 class="text-lg font-bold text-slate-800 dark:text-white mb-4">{{ editingProperty ? "Editar Propriedade" : "Nova Propriedade" }}</h2>
        <form @submit.prevent="saveProperty" class="space-y-3.5">
          <div>
            <label class="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1.5">Cliente *</label>
            <select v-model="form.client_id" required class="w-full px-3.5 py-3 md:py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 text-sm">
              <option :value="null" disabled>Selecione um cliente</option>
              <option v-for="client in allClients" :key="client.id" :value="client.id">{{ client.name }}</option>
            </select>
          </div>
          <div>
            <label class="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1.5">Nome da Propriedade *</label>
            <input v-model="form.name" type="text" required placeholder="Ex: Fazenda Boa Vista" class="w-full px-3.5 py-3 md:py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 placeholder-slate-400 text-sm" />
          </div>
          <div>
            <label class="block text-xs font-medium text-slate-500 dark:text-slate-400 mb-1.5">Area Total (hectares)</label>
            <input v-model.number="form.total_area_hectares" type="number" step="0.01" min="0" placeholder="0.00" class="w-full px-3.5 py-3 md:py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-slate-200 placeholder-slate-400 text-sm" />
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
          Tem certeza que deseja excluir <strong class="text-slate-700 dark:text-slate-200">{{ propertyToDelete?.name }}</strong>?
        </p>
        <p class="text-warning text-xs mt-2">Todas as analises associadas serao excluidas.</p>
        <div class="flex justify-end gap-2.5 mt-5">
          <button @click="closeDeleteModal" class="px-4 py-2.5 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 rounded-xl text-sm font-medium border border-slate-200 dark:border-slate-700 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors cursor-pointer">
            Cancelar
          </button>
          <button @click="deleteProperty" :disabled="deleting" class="px-4 py-2.5 bg-danger text-white rounded-xl text-sm font-medium hover:bg-red-700 transition-colors disabled:opacity-50 cursor-pointer">
            {{ deleting ? "Excluindo..." : "Excluir" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import ApiService from "@/services/ApiService";

const route = useRoute();
const properties = ref([]);
const allClients = ref([]);
const clientFilter = ref(null);
const loading = ref(true);
const searchQuery = ref("");
const selectedClientId = ref(null);
const showModal = ref(false);
const showDeleteModal = ref(false);
const editingProperty = ref(null);
const propertyToDelete = ref(null);
const saving = ref(false);
const deleting = ref(false);
const formError = ref("");

const states = [
  "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA",
  "MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN",
  "RS","RO","RR","SC","SP","SE","TO"
];

const form = ref({
  client_id: null, name: "", total_area_hectares: null,
  city: "", state: "", notes: "",
});

let searchTimeout = null;

async function loadClients() {
  try {
    const response = await ApiService.getClients({ limit: 1000 });
    allClients.value = response.data;
  } catch (err) {
    console.error("Error loading clients:", err);
  }
}

async function loadProperties() {
  loading.value = true;
  try {
    const params = {};
    if (searchQuery.value) params.search = searchQuery.value;
    if (selectedClientId.value) params.client_id = selectedClientId.value;
    const response = await ApiService.getProperties(params);
    properties.value = response.data;
  } catch (err) {
    console.error("Error loading properties:", err);
  } finally {
    loading.value = false;
  }
}

function debouncedSearch() {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => loadProperties(), 300);
}

function clearClientFilter() {
  selectedClientId.value = null;
  clientFilter.value = null;
  loadProperties();
}

function openCreateModal() {
  editingProperty.value = null;
  form.value = { client_id: selectedClientId.value, name: "", total_area_hectares: null, city: "", state: "", notes: "" };
  formError.value = "";
  showModal.value = true;
}

function openEditModal(prop) {
  editingProperty.value = prop;
  form.value = { client_id: prop.client_id, name: prop.name, total_area_hectares: prop.total_area_hectares, city: prop.city || "", state: prop.state || "", notes: prop.notes || "" };
  formError.value = "";
  showModal.value = true;
}

function closeModal() { showModal.value = false; editingProperty.value = null; }

async function saveProperty() {
  formError.value = "";
  saving.value = true;
  try {
    const data = { ...form.value };
    if (editingProperty.value) {
      delete data.client_id;
      await ApiService.updateProperty(editingProperty.value.id, data);
    } else {
      await ApiService.createProperty(data);
    }
    closeModal();
    await loadProperties();
  } catch (err) {
    formError.value = err.response?.data?.detail || "Erro ao salvar propriedade.";
  } finally {
    saving.value = false;
  }
}

function confirmDelete(prop) { propertyToDelete.value = prop; showDeleteModal.value = true; }
function closeDeleteModal() { showDeleteModal.value = false; propertyToDelete.value = null; }

async function deleteProperty() {
  deleting.value = true;
  try {
    await ApiService.deleteProperty(propertyToDelete.value.id);
    closeDeleteModal();
    await loadProperties();
  } catch (err) {
    console.error("Error deleting property:", err);
  } finally {
    deleting.value = false;
  }
}

onMounted(async () => {
  await loadClients();
  const clientId = route.params.clientId;
  if (clientId) {
    selectedClientId.value = parseInt(clientId);
    const client = allClients.value.find(c => c.id === selectedClientId.value);
    if (client) clientFilter.value = client;
  }
  await loadProperties();
});
</script>
