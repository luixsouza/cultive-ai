<template>
  <div class="page-container">
    <!-- Loading state -->
    <div v-if="loading" class="loading-state">
      <div class="spinner-lg"></div>
      <p>Carregando relatorio...</p>
    </div>

    <!-- Error state -->
    <div v-if="error" class="error-state">
      <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
      <p>{{ error }}</p>
      <router-link to="/" class="btn-back">Voltar ao Dashboard</router-link>
    </div>

    <!-- Report content -->
    <div v-if="reportData && !loading" class="report-content">
      <!-- Header -->
      <div class="report-header">
        <div class="header-info">
          <h1>Relatorio de Analise</h1>
          <p class="report-date">
            {{ formatDate(reportData.created_at) }}
            <span v-if="reportData.property_name" class="property-badge">
              {{ reportData.property_name }}
            </span>
          </p>
        </div>
        <div class="header-actions">
          <a :href="downloadUrl" download class="btn-download">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
            Baixar
          </a>
          <router-link to="/analysis/new" class="btn-secondary">Nova Analise</router-link>
        </div>
      </div>

      <!-- Stats cards -->
      <div class="stats-cards">
        <div class="stat-card">
          <div class="stat-icon" style="background: var(--primary-bg); color: var(--primary-color);">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="1" y="3" width="22" height="18" rx="2" ry="2"/><line x1="1" y1="9" x2="23" y2="9"/></svg>
          </div>
          <div class="stat-content">
            <span class="stat-value">{{ reportData.aoi_area_hectares?.toFixed(2) || '0' }}</span>
            <span class="stat-label">Hectares</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon" style="background: #e8f5e9; color: #2e7d32;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z"/></svg>
          </div>
          <div class="stat-content">
            <span class="stat-value">{{ reportData.ndvi_stats?.mean?.toFixed(3) || 'N/A' }}</span>
            <span class="stat-label">NDVI Medio</span>
          </div>
        </div>
        <div class="stat-card" :class="getHealthClass(reportData.ndvi_stats?.mean)">
          <div class="stat-icon health-icon-bg">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
          </div>
          <div class="stat-content">
            <span class="stat-value">{{ getHealthLabel(reportData.ndvi_stats?.mean) }}</span>
            <span class="stat-label">Saude da Vegetacao</span>
          </div>
        </div>
      </div>

      <!-- Map Section -->
      <div class="map-section">
        <div class="section-title">
          <h2>Mapa da Area Analisada</h2>
          <p>Use as camadas a esquerda para visualizar diferentes indices</p>
        </div>
        <div class="map-container-highlight">
          <MapComponent
            :layers="reportData.map_layers_urls"
            :aoi="reportData.aoi_geojson"
            :is-display-mode="true"
          />
        </div>
      </div>

      <!-- AI Report -->
      <div class="ai-report-section">
        <div class="section-title">
          <h2>Diagnostico Tecnico</h2>
          <p>Relatorio gerado por inteligencia artificial</p>
        </div>
        <div class="ai-report-body" v-html="renderMarkdown(reportData.ai_description)"></div>
      </div>

      <!-- Final actions -->
      <div class="final-actions">
        <a :href="downloadUrl" download class="btn-primary-lg">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
          Baixar Relatorio Completo
        </a>
        <router-link to="/analysis/new" class="btn-secondary-lg">Realizar Nova Analise</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import ApiService from "@/services/ApiService";
import MapComponent from "@/components/MapComponent.vue";
import { marked } from "marked";

const props = defineProps({
  id: { type: [String, Number], required: true },
});

const reportData = ref(null);
const loading = ref(true);
const error = ref(null);

const downloadUrl = computed(() => {
  return reportData.value ? ApiService.downloadReportUrl(reportData.value.id) : "#";
});

function formatDate(dateStr) {
  if (!dateStr) return '';
  return new Date(dateStr).toLocaleDateString('pt-BR', {
    day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit',
  });
}

function getHealthClass(ndviMean) {
  if (!ndviMean) return '';
  if (ndviMean >= 0.5) return 'health-excellent';
  if (ndviMean >= 0.4) return 'health-good';
  if (ndviMean >= 0.3) return 'health-moderate';
  if (ndviMean >= 0.2) return 'health-stressed';
  return 'health-degraded';
}

function getHealthLabel(ndviMean) {
  if (!ndviMean) return 'N/A';
  if (ndviMean >= 0.5) return 'Excelente';
  if (ndviMean >= 0.4) return 'Boa';
  if (ndviMean >= 0.3) return 'Moderada';
  if (ndviMean >= 0.2) return 'Estressada';
  return 'Degradada';
}

function renderMarkdown(text) {
  if (!text) return '';
  return marked(text);
}

onMounted(async () => {
  try {
    const response = await ApiService.getAnalysisReport(props.id);
    reportData.value = response.data;
  } catch (err) {
    error.value = "Nao foi possivel carregar o relatorio.";
    console.error(err);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
/* === MOBILE-FIRST === */

.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px 32px;
}

/* Loading / Error */
.loading-state, .error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  gap: 16px;
  color: var(--text-muted);
}

.spinner-lg {
  width: 36px;
  height: 36px;
  border: 3px solid var(--border-color);
  border-top-color: var(--primary-color);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.btn-back {
  display: inline-block;
  background: var(--primary-color);
  color: white;
  padding: 10px 20px;
  border-radius: var(--radius-sm);
  font-weight: 500;
}

/* Header */
.report-header {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--border-light);
}

.header-info h1 {
  margin: 0 0 6px;
  font-size: 20px;
}

.report-date {
  color: var(--text-muted);
  font-size: 13px;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.property-badge {
  background: var(--info-bg);
  color: var(--info-color);
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.header-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
}

.btn-download {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: var(--primary-color);
  color: white;
  padding: 12px 18px;
  border-radius: var(--radius-sm);
  font-weight: 500;
  font-size: 14px;
  transition: all var(--transition);
}

.btn-download:hover {
  background: var(--primary-dark);
  color: white;
}

.btn-secondary {
  background: var(--bg-page);
  color: var(--text-secondary);
  padding: 12px 18px;
  border-radius: var(--radius-sm);
  font-weight: 500;
  font-size: 14px;
  border: 1px solid var(--border-color);
  text-align: center;
}

.btn-secondary:hover {
  background: var(--border-light);
  color: var(--text-primary);
}

/* Stats */
.stats-cards {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
  margin-bottom: 20px;
}

.stat-card {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 14px;
  display: flex;
  align-items: center;
  gap: 12px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
}

.stat-icon {
  width: 42px;
  height: 42px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.stat-icon svg {
  width: 20px;
  height: 20px;
}

.stat-content {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 20px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
}

.stat-label {
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 3px;
}

/* Health classes */
.health-excellent .stat-value { color: #1a9850; }
.health-excellent .health-icon-bg { background: #e8f5e9; color: #1a9850; }
.health-good .stat-value { color: #66bd63; }
.health-good .health-icon-bg { background: #e8f5e9; color: #66bd63; }
.health-moderate .stat-value { color: #d4a017; }
.health-moderate .health-icon-bg { background: #fff8e1; color: #d4a017; }
.health-stressed .stat-value { color: #fc8d59; }
.health-stressed .health-icon-bg { background: #fff3e0; color: #fc8d59; }
.health-degraded .stat-value { color: #d73027; }
.health-degraded .health-icon-bg { background: #ffebee; color: #d73027; }

/* Map Section */
.map-section {
  margin-bottom: 20px;
}

.section-title {
  margin-bottom: 10px;
}

.section-title h2 {
  margin: 0 0 4px;
  font-size: 16px;
}

.section-title p {
  margin: 0;
  color: var(--text-muted);
  font-size: 12px;
}

.map-container-highlight {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  border: 2px solid var(--primary-color);
}

.map-container-highlight :deep(#map-container) {
  height: 350px;
}

/* AI Report */
.ai-report-section {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  padding: 16px;
  margin-bottom: 20px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
}

.ai-report-section .section-title {
  margin-bottom: 14px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border-light);
}

.ai-report-body {
  line-height: 1.7;
  color: var(--text-secondary);
  font-size: 14px;
}

.ai-report-body :deep(h2) {
  color: var(--primary-color);
  font-size: 16px;
  margin-top: 20px;
  margin-bottom: 6px;
}

.ai-report-body :deep(h3) {
  color: var(--text-primary);
  font-size: 14px;
  margin-top: 16px;
  margin-bottom: 4px;
}

.ai-report-body :deep(ul),
.ai-report-body :deep(ol) {
  padding-left: 20px;
  margin: 6px 0;
}

.ai-report-body :deep(li) {
  margin: 4px 0;
}

.ai-report-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 12px 0;
  font-size: 12px;
  display: block;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

.ai-report-body :deep(th),
.ai-report-body :deep(td) {
  padding: 8px 10px;
  border: 1px solid var(--border-color);
  text-align: left;
  white-space: nowrap;
}

.ai-report-body :deep(th) {
  background: var(--bg-page);
  font-weight: 600;
  color: var(--text-primary);
}

.ai-report-body :deep(strong) {
  color: var(--text-primary);
}

.ai-report-body :deep(hr) {
  border: none;
  border-top: 1px solid var(--border-light);
  margin: 20px 0;
}

/* Final Actions */
.final-actions {
  display: flex;
  flex-direction: column;
  gap: 10px;
  padding: 20px 0;
  border-top: 1px solid var(--border-light);
}

.btn-primary-lg {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: var(--primary-color);
  color: white;
  padding: 14px 20px;
  border-radius: var(--radius-sm);
  font-weight: 600;
  font-size: 15px;
  transition: all var(--transition);
}

.btn-primary-lg:hover {
  background: var(--primary-dark);
  color: white;
}

.btn-secondary-lg {
  background: var(--bg-page);
  color: var(--text-secondary);
  padding: 14px 20px;
  border-radius: var(--radius-sm);
  font-weight: 500;
  font-size: 15px;
  border: 1px solid var(--border-color);
  text-align: center;
}

.btn-secondary-lg:hover {
  background: var(--border-light);
  color: var(--text-primary);
}

/* === DESKTOP === */
@media (min-width: 768px) {
  .page-container {
    padding: 0 24px 40px;
  }

  .loading-state, .error-state {
    min-height: 400px;
  }

  .spinner-lg {
    width: 40px;
    height: 40px;
  }

  .report-header {
    flex-direction: row;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 24px;
    padding-bottom: 20px;
    gap: 16px;
  }

  .header-info h1 {
    font-size: 24px;
  }

  .report-date {
    font-size: 14px;
  }

  .header-actions {
    flex-direction: row;
    width: auto;
    gap: 10px;
  }

  .btn-download {
    font-size: 13px;
    padding: 10px 18px;
  }

  .btn-download:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(46, 125, 50, 0.25);
  }

  .btn-secondary {
    font-size: 13px;
    padding: 10px 18px;
  }

  .stats-cards {
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 28px;
  }

  .stat-card {
    padding: 20px;
    gap: 14px;
  }

  .stat-icon {
    width: 48px;
    height: 48px;
  }

  .stat-icon svg {
    width: 22px;
    height: 22px;
  }

  .stat-value {
    font-size: 22px;
  }

  .stat-label {
    font-size: 12px;
  }

  .map-section {
    margin-bottom: 28px;
  }

  .section-title h2 {
    font-size: 18px;
  }

  .section-title p {
    font-size: 13px;
  }

  .map-container-highlight :deep(#map-container) {
    height: 600px;
  }

  .ai-report-section {
    padding: 28px;
    margin-bottom: 28px;
  }

  .ai-report-section .section-title {
    margin-bottom: 20px;
    padding-bottom: 16px;
  }

  .ai-report-body :deep(h2) {
    font-size: 17px;
    margin-top: 24px;
    margin-bottom: 8px;
  }

  .ai-report-body :deep(h3) {
    font-size: 15px;
    margin-top: 20px;
    margin-bottom: 6px;
  }

  .ai-report-body :deep(ul),
  .ai-report-body :deep(ol) {
    padding-left: 24px;
  }

  .ai-report-body :deep(table) {
    font-size: 14px;
    display: table;
  }

  .ai-report-body :deep(th),
  .ai-report-body :deep(td) {
    padding: 10px 14px;
    white-space: normal;
  }

  .final-actions {
    flex-direction: row;
    justify-content: center;
    gap: 14px;
    padding: 28px 0;
  }

  .btn-primary-lg {
    padding: 14px 28px;
  }

  .btn-primary-lg:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(46, 125, 50, 0.3);
  }

  .btn-secondary-lg {
    padding: 14px 28px;
  }
}
</style>
