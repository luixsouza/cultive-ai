<template>
  <div class="dashboard-container">
    <!-- Welcome -->
    <div class="welcome-section">
      <div>
        <h1>Dashboard</h1>
        <p class="welcome-text">Visao geral da sua plataforma de analise de pastagens</p>
      </div>
      <router-link to="/analysis/new" class="btn-new-analysis">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
        Nova Analise
      </router-link>
    </div>

    <!-- Stats Cards -->
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon" style="background: var(--info-bg); color: var(--info-color);">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        </div>
        <div class="stat-info">
          <h3>{{ stats.clients }}</h3>
          <p>Clientes</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: var(--primary-bg); color: var(--primary-color);">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
        </div>
        <div class="stat-info">
          <h3>{{ stats.properties }}</h3>
          <p>Propriedades</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: var(--warning-bg); color: var(--warning-color);">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
        </div>
        <div class="stat-info">
          <h3>{{ stats.reports }}</h3>
          <p>Analises</p>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon" style="background: #fce4ec; color: #c2185b;">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="3" width="22" height="18" rx="2" ry="2"/><line x1="1" y1="9" x2="23" y2="9"/></svg>
        </div>
        <div class="stat-info">
          <h3>{{ formatArea(stats.totalArea) }}</h3>
          <p>Area Total (ha)</p>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="quick-actions">
      <h2>Acoes Rapidas</h2>
      <div class="actions-grid">
        <router-link to="/analysis/new" class="action-card action-primary">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
          <span>Nova Analise</span>
        </router-link>
        <router-link to="/clients" class="action-card">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
          <span>Gerenciar Clientes</span>
        </router-link>
        <router-link to="/properties" class="action-card">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
          <span>Gerenciar Propriedades</span>
        </router-link>
      </div>
    </div>

    <!-- Reports Section -->
    <div class="reports-section">
      <div class="section-header">
        <h2>Analises Recentes</h2>
        <div class="filters">
          <div class="search-wrapper">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#999" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Buscar analises..."
              @input="debouncedSearch"
            />
          </div>
          <select v-model="dateFilter" @change="loadReports" class="date-filter">
            <option value="">Todas as datas</option>
            <option value="7">Ultimos 7 dias</option>
            <option value="30">Ultimos 30 dias</option>
            <option value="90">Ultimos 90 dias</option>
          </select>
        </div>
      </div>

      <div v-if="loadingReports" class="loading-state">
        <div class="spinner"></div>
        <p>Carregando analises...</p>
      </div>

      <div v-else-if="reports.length === 0" class="empty-state">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
        <p>Nenhuma analise encontrada.</p>
        <router-link to="/analysis/new" class="btn-primary">
          Criar primeira analise
        </router-link>
      </div>

      <div v-else class="reports-list">
        <div v-for="report in reports" :key="report.id" class="report-card">
          <div class="report-main">
            <div class="report-info">
              <h3>{{ report.title || `Analise #${report.id}` }}</h3>
              <p class="report-date">{{ formatDate(report.created_at) }}</p>
              <div class="report-meta">
                <span v-if="report.aoi_area_hectares" class="meta-item">
                  <strong>Area:</strong> {{ report.aoi_area_hectares.toFixed(2) }} ha
                </span>
                <span v-if="report.ndvi_stats" class="meta-item">
                  <strong>NDVI:</strong> {{ report.ndvi_stats.mean?.toFixed(3) || 'N/A' }}
                </span>
              </div>
            </div>
            <div class="report-status">
              <span
                v-if="report.degradation_summary"
                class="status-badge"
                :class="getDegradationClass(report.degradation_summary)"
              >
                {{ getDegradationLabel(report.degradation_summary) }}
              </span>
            </div>
          </div>
          <div class="report-actions">
            <router-link :to="`/analysis/${report.id}`" class="btn-view">
              Ver Detalhes
            </router-link>
            <a :href="getDownloadUrl(report.id)" class="btn-download-sm" target="_blank">
              Download
            </a>
            <button class="btn-delete" @click="confirmDelete(report)">
              Excluir
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="closeDeleteModal">
      <div class="modal modal-sm">
        <h2>Confirmar Exclusao</h2>
        <p>
          Tem certeza que deseja excluir a analise
          <strong>{{ reportToDelete?.title || `#${reportToDelete?.id}` }}</strong>?
        </p>
        <div class="modal-actions">
          <button class="btn-secondary" @click="closeDeleteModal">Cancelar</button>
          <button class="btn-danger" @click="deleteReport" :disabled="deleting">
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

const stats = ref({ clients: 0, properties: 0, reports: 0, totalArea: 0 });
const reports = ref([]);
const loadingReports = ref(true);
const searchQuery = ref("");
const dateFilter = ref("");
const showDeleteModal = ref(false);
const reportToDelete = ref(null);
const deleting = ref(false);

let searchTimeout = null;

async function loadStats() {
  try {
    const [clientsRes, propertiesRes, reportsRes] = await Promise.all([
      ApiService.getClientsCount(),
      ApiService.getPropertiesCount(),
      ApiService.getAnalysisReports(),
    ]);
    stats.value.clients = clientsRes.data.count;
    stats.value.properties = propertiesRes.data.count;
    stats.value.reports = reportsRes.data.length;
    stats.value.totalArea = reportsRes.data.reduce((sum, r) => sum + (r.aoi_area_hectares || 0), 0);
  } catch (err) {
    console.error("Error loading stats:", err);
  }
}

async function loadReports() {
  loadingReports.value = true;
  try {
    const response = await ApiService.getAnalysisReports();
    let data = response.data;
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase();
      data = data.filter(
        (r) => (r.title && r.title.toLowerCase().includes(query)) || r.id.toString().includes(query)
      );
    }
    if (dateFilter.value) {
      const days = parseInt(dateFilter.value);
      const cutoff = new Date();
      cutoff.setDate(cutoff.getDate() - days);
      data = data.filter((r) => new Date(r.created_at) >= cutoff);
    }
    data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
    reports.value = data;
  } catch (err) {
    console.error("Error loading reports:", err);
  } finally {
    loadingReports.value = false;
  }
}

function debouncedSearch() {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => loadReports(), 300);
}

function formatDate(dateStr) {
  const date = new Date(dateStr);
  return date.toLocaleDateString("pt-BR", {
    day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit",
  });
}

function formatArea(area) {
  if (area >= 1000) return (area / 1000).toFixed(1) + "k";
  return area.toFixed(0);
}

function getDegradationClass(summary) {
  if (!summary) return "";
  const severePercent = (summary["1"]?.percentage || 0) + (summary["2"]?.percentage || 0);
  if (severePercent > 50) return "status-severe";
  if (severePercent > 25) return "status-moderate";
  return "status-good";
}

function getDegradationLabel(summary) {
  if (!summary) return "N/A";
  const severePercent = (summary["1"]?.percentage || 0) + (summary["2"]?.percentage || 0);
  if (severePercent > 50) return "Degradacao Severa";
  if (severePercent > 25) return "Degradacao Moderada";
  return "Pastagem Boa";
}

function getDownloadUrl(reportId) {
  return ApiService.downloadReportUrl(reportId);
}

function confirmDelete(report) {
  reportToDelete.value = report;
  showDeleteModal.value = true;
}

function closeDeleteModal() {
  showDeleteModal.value = false;
  reportToDelete.value = null;
}

async function deleteReport() {
  deleting.value = true;
  try {
    await ApiService.deleteAnalysisReport(reportToDelete.value.id);
    closeDeleteModal();
    await Promise.all([loadStats(), loadReports()]);
  } catch (err) {
    console.error("Error deleting report:", err);
  } finally {
    deleting.value = false;
  }
}

onMounted(async () => {
  await Promise.all([loadStats(), loadReports()]);
});
</script>

<style scoped>
/* === MOBILE-FIRST: base = mobile, min-width: 768px = desktop === */

.dashboard-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px 32px;
}

/* Welcome */
.welcome-section {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
}

.welcome-section h1 {
  margin: 0 0 4px;
  font-size: 20px;
}

.welcome-text {
  margin: 0;
  color: var(--text-muted);
  font-size: 13px;
}

.btn-new-analysis {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: var(--primary-color);
  color: white;
  padding: 12px 20px;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: 14px;
  text-decoration: none;
  transition: all var(--transition);
  width: 100%;
}

.btn-new-analysis:hover {
  background: var(--primary-dark);
  color: white;
}

/* Stats */
.stats-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
  margin-bottom: 24px;
}

.stat-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
  transition: all var(--transition);
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon svg {
  width: 18px;
  height: 18px;
}

.stat-info h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
}

.stat-info p {
  margin: 2px 0 0;
  color: var(--text-muted);
  font-size: 11px;
}

/* Quick Actions */
.quick-actions {
  margin-bottom: 24px;
}

.quick-actions h2 {
  margin-bottom: 12px;
  font-size: 16px;
}

.actions-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
}

.action-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 16px;
  text-align: center;
  text-decoration: none;
  color: var(--text-secondary);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
  transition: all var(--transition);
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
}

.action-card svg {
  opacity: 0.6;
  flex-shrink: 0;
  width: 24px;
  height: 24px;
}

.action-card span {
  font-size: 14px;
  font-weight: 500;
}

.action-primary {
  background: var(--primary-bg);
  border-color: transparent;
  color: var(--primary-color);
}

.action-primary svg {
  opacity: 1;
  stroke: var(--primary-color);
}

/* Reports */
.reports-section {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 16px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
}

.section-header {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  margin-bottom: 16px;
  gap: 10px;
}

.section-header h2 {
  margin: 0;
  font-size: 16px;
}

.filters {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-wrapper svg {
  position: absolute;
  left: 12px;
}

.search-wrapper input {
  padding: 10px 12px 10px 36px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  width: 100%;
  font-size: 14px;
  background: var(--bg-page);
}

.date-filter {
  padding: 10px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-size: 14px;
  background: var(--bg-page);
  width: 100%;
}

.loading-state {
  text-align: center;
  padding: 32px 16px;
  color: var(--text-muted);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 40px 16px;
  color: var(--text-muted);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.empty-state p {
  margin: 0;
}

.reports-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.report-card {
  border: 1px solid var(--border-light);
  border-radius: var(--radius-sm);
  padding: 14px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 10px;
  transition: all var(--transition);
}

.report-card:hover {
  background: var(--bg-page);
  border-color: var(--border-color);
}

.report-main {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
  flex: 1;
}

.report-info h3 {
  margin: 0 0 3px;
  font-size: 15px;
}

.report-date {
  color: var(--text-muted);
  font-size: 12px;
  margin: 0 0 4px;
}

.report-meta {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.meta-item {
  font-size: 12px;
  color: var(--text-secondary);
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  white-space: nowrap;
}

.status-severe { background: var(--danger-bg); color: #c62828; }
.status-moderate { background: var(--warning-bg); color: #ef6c00; }
.status-good { background: var(--primary-bg); color: var(--primary-color); }

.report-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.btn-view {
  padding: 8px 14px;
  background: var(--primary-color);
  color: white;
  border-radius: var(--radius-sm);
  text-decoration: none;
  font-size: 12px;
  font-weight: 500;
  transition: all var(--transition);
  flex: 1;
  text-align: center;
}

.btn-view:hover {
  background: var(--primary-dark);
  color: white;
}

.btn-download-sm {
  padding: 8px 14px;
  background: var(--bg-page);
  color: var(--text-secondary);
  border-radius: var(--radius-sm);
  text-decoration: none;
  font-size: 12px;
  border: 1px solid var(--border-color);
  flex: 1;
  text-align: center;
}

.btn-download-sm:hover {
  background: var(--border-light);
  color: var(--text-primary);
}

.btn-delete {
  padding: 8px 14px;
  background: none;
  color: var(--danger-color);
  border: 1px solid currentColor;
  border-radius: var(--radius-sm);
  font-size: 12px;
  cursor: pointer;
  flex: 1;
  text-align: center;
}

.btn-delete:hover {
  background: var(--danger-bg);
}

.btn-primary {
  display: inline-block;
  padding: 10px 20px;
  background: var(--primary-color);
  color: white;
  border-radius: var(--radius-sm);
  text-decoration: none;
  font-weight: 500;
  font-size: 14px;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: flex-end;
  justify-content: center;
  z-index: 1000;
  padding: 0;
}

.modal {
  background: white;
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  padding: 24px 20px;
  width: 100%;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: var(--shadow-lg);
}

.modal h2 {
  margin: 0 0 12px;
  font-size: 18px;
}

.modal p {
  color: var(--text-secondary);
  font-size: 14px;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

.btn-secondary {
  padding: 10px 18px;
  background: var(--bg-page);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 14px;
}

.btn-danger {
  padding: 10px 18px;
  background: var(--danger-color);
  color: white;
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: 14px;
}

/* === DESKTOP === */
@media (min-width: 768px) {
  .dashboard-container {
    padding: 0 24px 40px;
  }

  .welcome-section {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
  }

  .welcome-section h1 {
    font-size: 24px;
  }

  .btn-new-analysis {
    width: auto;
    padding: 10px 20px;
  }

  .btn-new-analysis:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(46, 125, 50, 0.25);
  }

  .stats-grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 32px;
  }

  .stat-card {
    padding: 20px;
    gap: 16px;
  }

  .stat-card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
  }

  .stat-icon {
    width: 48px;
    height: 48px;
  }

  .stat-icon svg {
    width: 22px;
    height: 22px;
  }

  .stat-info h3 {
    font-size: 26px;
  }

  .stat-info p {
    font-size: 13px;
  }

  .quick-actions h2 {
    font-size: 18px;
  }

  .actions-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
  }

  .action-card {
    flex-direction: column;
    padding: 20px;
    gap: 10px;
  }

  .action-card:hover {
    transform: translateY(-3px);
    box-shadow: var(--shadow-md);
    color: var(--primary-color);
    border-color: var(--primary-bg);
  }

  .action-card:hover svg {
    opacity: 1;
    stroke: var(--primary-color);
  }

  .action-primary:hover {
    background: var(--primary-color);
    color: white;
  }

  .action-primary:hover svg {
    stroke: white;
  }

  .reports-section {
    padding: 24px;
  }

  .section-header {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }

  .section-header h2 {
    font-size: 18px;
  }

  .filters {
    flex-direction: row;
    gap: 10px;
  }

  .search-wrapper input {
    width: 240px;
    font-size: 13px;
    padding: 9px 12px 9px 36px;
  }

  .date-filter {
    width: auto;
    font-size: 13px;
    padding: 9px 12px;
  }

  .report-card {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
  }

  .report-main {
    flex-direction: row;
    align-items: center;
    gap: 20px;
  }

  .report-actions {
    flex-wrap: nowrap;
  }

  .btn-view, .btn-download-sm, .btn-delete {
    flex: none;
    padding: 7px 14px;
  }

  .modal-overlay {
    align-items: center;
    padding: 20px;
  }

  .modal {
    border-radius: var(--radius-lg);
    padding: 28px;
    width: 400px;
    max-width: 90%;
    max-height: 90vh;
  }

  .btn-secondary, .btn-danger {
    font-size: 13px;
    padding: 9px 18px;
  }
}
</style>
