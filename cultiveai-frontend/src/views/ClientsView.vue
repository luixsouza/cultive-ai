<template>
  <div class="page-container">
    <div class="page-header">
      <div>
        <h1>Clientes</h1>
        <p class="page-subtitle">Gerencie seus clientes e suas propriedades</p>
      </div>
      <button class="btn-primary" @click="openCreateModal">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Novo Cliente
      </button>
    </div>

    <div class="search-bar">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <input
        type="text"
        v-model="searchQuery"
        placeholder="Buscar por nome, documento, email ou cidade..."
        @input="debouncedSearch"
      />
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Carregando clientes...</p>
    </div>

    <div v-else-if="clients.length === 0" class="empty-state">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
      <p>Nenhum cliente encontrado.</p>
      <button class="btn-primary" @click="openCreateModal">Adicionar primeiro cliente</button>
    </div>

    <div v-else class="cards-grid">
      <div v-for="client in clients" :key="client.id" class="item-card">
        <div class="card-top">
          <div class="card-avatar" style="background: var(--info-bg); color: var(--info-color);">
            {{ client.name?.[0]?.toUpperCase() || 'C' }}
          </div>
          <div class="card-title-area">
            <h3>{{ client.name }}</h3>
            <span v-if="client.city || client.state" class="card-location">
              {{ client.city }}{{ client.state ? ` - ${client.state}` : "" }}
            </span>
          </div>
          <div class="card-actions">
            <button class="btn-icon" @click="openEditModal(client)" title="Editar">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
            </button>
            <button class="btn-icon btn-icon-danger" @click="confirmDelete(client)" title="Excluir">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>
            </button>
          </div>
        </div>
        <div class="card-details">
          <p v-if="client.document"><strong>Doc:</strong> {{ client.document }}</p>
          <p v-if="client.email"><strong>Email:</strong> {{ client.email }}</p>
          <p v-if="client.phone"><strong>Tel:</strong> {{ client.phone }}</p>
        </div>
        <div class="card-footer">
          <span class="badge-count">{{ client.properties_count || 0 }} propriedade(s)</span>
          <router-link :to="`/clients/${client.id}/properties`" class="btn-link">Ver propriedades</router-link>
        </div>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal">
        <h2>{{ editingClient ? "Editar Cliente" : "Novo Cliente" }}</h2>
        <form @submit.prevent="saveClient">
          <div class="form-group">
            <label>Nome *</label>
            <input v-model="form.name" type="text" required placeholder="Nome do cliente" />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>CPF/CNPJ</label>
              <input v-model="form.document" type="text" placeholder="000.000.000-00" />
            </div>
            <div class="form-group">
              <label>Telefone</label>
              <input v-model="form.phone" type="text" placeholder="(00) 00000-0000" />
            </div>
          </div>
          <div class="form-group">
            <label>Email</label>
            <input v-model="form.email" type="email" placeholder="email@exemplo.com" />
          </div>
          <div class="form-group">
            <label>Endereco</label>
            <input v-model="form.address" type="text" placeholder="Rua, numero" />
          </div>
          <div class="form-row">
            <div class="form-group">
              <label>Cidade</label>
              <input v-model="form.city" type="text" />
            </div>
            <div class="form-group">
              <label>Estado</label>
              <select v-model="form.state">
                <option value="">Selecione</option>
                <option v-for="uf in states" :key="uf" :value="uf">{{ uf }}</option>
              </select>
            </div>
          </div>
          <div class="form-group">
            <label>Observacoes</label>
            <textarea v-model="form.notes" rows="3" placeholder="Notas adicionais..."></textarea>
          </div>
          <p v-if="formError" class="form-error">{{ formError }}</p>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="closeModal">Cancelar</button>
            <button type="submit" class="btn-primary" :disabled="saving">
              {{ saving ? "Salvando..." : "Salvar" }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="closeDeleteModal">
      <div class="modal modal-sm">
        <h2>Confirmar Exclusao</h2>
        <p>Tem certeza que deseja excluir o cliente <strong>{{ clientToDelete?.name }}</strong>?</p>
        <p class="warning-text">Todas as propriedades e relatorios associados serao excluidos.</p>
        <div class="modal-actions">
          <button class="btn-secondary" @click="closeDeleteModal">Cancelar</button>
          <button class="btn-danger" @click="deleteClient" :disabled="deleting">
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

let searchTimeout = null;

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
  showModal.value = true;
}

function openEditModal(client) {
  editingClient.value = client;
  form.value = { ...client };
  formError.value = "";
  showModal.value = true;
}

function closeModal() { showModal.value = false; editingClient.value = null; }

async function saveClient() {
  formError.value = "";
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

<style scoped>
/* === MOBILE-FIRST === */

.page-container { max-width: 1200px; margin: 0 auto; padding: 0 16px 32px; }

.page-header {
  display: flex; flex-direction: column; gap: 12px;
  margin-bottom: 16px;
}
.page-header h1 { margin: 0 0 4px; font-size: 20px; }
.page-subtitle { margin: 0; color: var(--text-muted); font-size: 13px; }

.btn-primary {
  display: inline-flex; align-items: center; justify-content: center; gap: 6px;
  background: var(--primary-color); color: white; border: none;
  padding: 12px 18px; border-radius: var(--radius-sm);
  font-size: 14px; font-weight: 600; cursor: pointer;
  transition: all var(--transition); width: 100%;
}
.btn-primary:hover:not(:disabled) { background: var(--primary-dark); }

.search-bar {
  position: relative; display: flex; align-items: center; margin-bottom: 16px;
}
.search-bar svg { position: absolute; left: 14px; }
.search-bar input {
  width: 100%; padding: 12px 14px 12px 40px;
  border: 1px solid var(--border-color); border-radius: var(--radius-sm);
  font-size: 16px; background: var(--bg-card);
}

.loading-state, .empty-state {
  text-align: center; padding: 40px 16px; color: var(--text-muted);
  display: flex; flex-direction: column; align-items: center; gap: 12px;
}
.spinner {
  width: 32px; height: 32px; border: 3px solid var(--border-color);
  border-top-color: var(--primary-color); border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.cards-grid { display: grid; grid-template-columns: 1fr; gap: 12px; }

.item-card {
  background: var(--bg-card); border-radius: var(--radius-md); padding: 16px;
  box-shadow: var(--shadow-sm); border: 1px solid var(--border-light);
  transition: all var(--transition);
}

.card-top { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 12px; }
.card-avatar {
  width: 36px; height: 36px; border-radius: var(--radius-sm);
  display: flex; align-items: center; justify-content: center;
  font-weight: 700; font-size: 14px; flex-shrink: 0;
}
.card-title-area { flex: 1; min-width: 0; }
.card-title-area h3 { margin: 0 0 2px; font-size: 15px; color: var(--text-primary); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.card-location { font-size: 12px; color: var(--text-muted); }

.card-actions { display: flex; gap: 4px; }
.btn-icon {
  background: none; border: 1px solid var(--border-color);
  width: 34px; height: 34px;
  border-radius: var(--radius-sm); cursor: pointer; display: flex;
  align-items: center; justify-content: center; color: var(--text-muted);
  transition: all var(--transition);
}
.btn-icon:hover { background: var(--bg-page); color: var(--text-primary); border-color: var(--text-muted); }
.btn-icon-danger:hover { background: var(--danger-bg); color: var(--danger-color); border-color: var(--danger-color); }

.card-details p { margin: 4px 0; font-size: 13px; color: var(--text-secondary); }
.card-details strong { color: var(--text-primary); font-weight: 500; }

.card-footer {
  display: flex; justify-content: space-between; align-items: center;
  margin-top: 12px; padding-top: 12px; border-top: 1px solid var(--border-light);
}
.badge-count { font-size: 12px; color: var(--text-muted); }
.btn-link { color: var(--primary-color); font-size: 13px; font-weight: 500; }
.btn-link:hover { text-decoration: underline; }

/* Modal - bottom sheet on mobile */
.modal-overlay {
  position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.4); backdrop-filter: blur(4px);
  display: flex; align-items: flex-end; justify-content: center; z-index: 1000;
}
.modal {
  background: white; border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  padding: 24px 20px; width: 100%; max-height: 90vh; overflow-y: auto;
  box-shadow: var(--shadow-lg);
}
.modal-sm { width: 100%; }
.modal h2 { margin: 0 0 16px; font-size: 18px; }

.form-group { margin-bottom: 14px; }
.form-group label { display: block; margin-bottom: 5px; font-size: 13px; font-weight: 500; color: var(--text-secondary); }
.form-group input, .form-group select, .form-group textarea {
  width: 100%; padding: 12px; border: 1px solid var(--border-color);
  border-radius: var(--radius-sm); font-size: 16px; background: var(--bg-page);
}
.form-row { display: grid; grid-template-columns: 1fr; gap: 14px; }

.modal-actions { display: flex; justify-content: flex-end; gap: 10px; margin-top: 20px; }
.btn-secondary {
  padding: 10px 18px; background: var(--bg-page); color: var(--text-secondary);
  border: 1px solid var(--border-color); border-radius: var(--radius-sm); cursor: pointer; font-size: 14px;
}
.btn-danger {
  padding: 10px 18px; background: var(--danger-color); color: white;
  border: none; border-radius: var(--radius-sm); cursor: pointer; font-size: 14px;
}

.form-error { color: var(--danger-color); font-size: 13px; margin: 0; }
.warning-text { color: var(--warning-color); font-size: 13px; }

/* === DESKTOP === */
@media (min-width: 768px) {
  .page-container { padding: 0 24px 40px; }

  .page-header {
    flex-direction: row; justify-content: space-between; align-items: center;
  }

  .page-header h1 { font-size: 24px; }

  .btn-primary { width: auto; font-size: 13px; padding: 10px 18px; }
  .btn-primary:hover:not(:disabled) { transform: translateY(-1px); }

  .search-bar input { font-size: 14px; padding: 11px 14px 11px 40px; }

  .cards-grid { grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 16px; }

  .item-card { padding: 20px; }
  .item-card:hover { box-shadow: var(--shadow-md); border-color: var(--border-color); }

  .card-avatar { width: 40px; height: 40px; font-size: 16px; }

  .modal-overlay { align-items: center; }
  .modal {
    border-radius: var(--radius-lg); padding: 28px;
    width: 500px; max-width: 90%;
  }
  .modal-sm { width: 400px; }

  .form-group input, .form-group select, .form-group textarea {
    font-size: 14px; padding: 10px 12px;
  }

  .form-row { grid-template-columns: 1fr 1fr; }

  .btn-secondary, .btn-danger { font-size: 13px; padding: 9px 18px; }
}
</style>
