<template>
  <div class="page-container">
    <div class="page-header">
      <div>
        <h1>Nova Analise de Pastagem</h1>
        <p class="page-subtitle">Desenhe a area de interesse no mapa para iniciar a analise com IA</p>
      </div>
    </div>

    <!-- Steps indicator -->
    <div class="steps-bar">
      <div :class="['step', { active: true, done: drawnGeoJSON }]">
        <span class="step-num">1</span>
        <span>Selecionar area</span>
      </div>
      <div class="step-line" :class="{ done: drawnGeoJSON }"></div>
      <div :class="['step', { active: drawnGeoJSON && !loading }]">
        <span class="step-num">2</span>
        <span>Configurar</span>
      </div>
      <div class="step-line" :class="{ done: loading }"></div>
      <div :class="['step', { active: loading }]">
        <span class="step-num">3</span>
        <span>Analisar</span>
      </div>
    </div>

    <!-- Options -->
    <div class="options-row">
      <div class="option-group">
        <label>Vincular a uma propriedade (opcional):</label>
        <select v-model="selectedPropertyId">
          <option :value="null">Nenhuma propriedade</option>
          <option v-for="prop in properties" :key="prop.id" :value="prop.id">
            {{ prop.name }} ({{ prop.client_name }})
          </option>
        </select>
      </div>
    </div>

    <!-- Map -->
    <div class="map-section">
      <MapComponent @area-drawn="onAreaDrawn" />
    </div>

    <!-- Actions -->
    <div class="actions-bar">
      <button
        class="btn-analyze"
        @click="startAnalysis"
        :disabled="!drawnGeoJSON || loading"
      >
        <svg v-if="!loading" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <div v-if="loading" class="btn-spinner"></div>
        {{ loading ? "Analisando... (pode levar alguns minutos)" : "Analisar Area Selecionada" }}
      </button>
      <router-link to="/" class="btn-cancel">Cancelar</router-link>
    </div>

    <div v-if="error" class="error-banner">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>
      {{ error }}
    </div>

    <div v-if="loading" class="loading-banner">
      <div class="loading-pulse"></div>
      <div>
        <p><strong>Analise em andamento</strong></p>
        <p class="loading-detail">
          Processando imagens de satelite, calculando indices de vegetacao
          e gerando relatorio com IA.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import ApiService from "@/services/ApiService";
import MapComponent from "@/components/MapComponent.vue";

const route = useRoute();
const router = useRouter();

const drawnGeoJSON = ref(null);
const loading = ref(false);
const error = ref("");
const properties = ref([]);
const selectedPropertyId = ref(null);

async function loadProperties() {
  try {
    const response = await ApiService.getProperties({ limit: 1000 });
    properties.value = response.data;
    const propertyParam = route.query.property;
    if (propertyParam) {
      selectedPropertyId.value = parseInt(propertyParam);
    }
  } catch (err) {
    console.error("Error loading properties:", err);
  }
}

function onAreaDrawn(geojson) {
  if (geojson) {
    drawnGeoJSON.value = {
      type: "FeatureCollection",
      features: [geojson],
    };
  } else {
    drawnGeoJSON.value = null;
  }
  error.value = "";
}

async function startAnalysis() {
  if (!drawnGeoJSON.value) {
    error.value = "Por favor, desenhe uma area no mapa primeiro.";
    return;
  }
  loading.value = true;
  error.value = "";
  try {
    const response = await ApiService.analyzeArea(
      drawnGeoJSON.value,
      selectedPropertyId.value
    );
    const reportId = response.data.id;
    router.push({ name: "AnalysisView", params: { id: reportId } });
  } catch (err) {
    console.error("Erro ao iniciar a analise:", err);
    error.value =
      err.response?.data?.detail || "Ocorreu um erro ao processar a analise.";
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  loadProperties();
});
</script>

<style scoped>
/* === MOBILE-FIRST === */

.page-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 16px 32px;
}

.page-header {
  margin-bottom: 16px;
}

.page-header h1 {
  margin: 0 0 4px;
  font-size: 20px;
}

.page-subtitle {
  margin: 0;
  color: var(--text-muted);
  font-size: 13px;
}

/* Steps */
.steps-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 16px;
  padding: 12px 0;
}

.step {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  border-radius: 24px;
  font-size: 12px;
  color: var(--text-muted);
  background: var(--bg-card);
  border: 1px solid var(--border-light);
  transition: all var(--transition);
}

.step.active {
  color: var(--primary-color);
  background: var(--primary-bg);
  border-color: transparent;
  font-weight: 500;
}

.step.done {
  color: var(--primary-color);
}

.step-num {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: var(--border-color);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: 700;
}

.step.active .step-num,
.step.done .step-num {
  background: var(--primary-color);
}

.step-line {
  display: none;
}

/* Options */
.options-row {
  background: var(--bg-card);
  padding: 12px 14px;
  border-radius: var(--radius-md);
  margin-bottom: 12px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
}

.option-group {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 8px;
}

.option-group label {
  font-weight: 500;
  color: var(--text-secondary);
  font-size: 13px;
}

.option-group select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-size: 16px;
  background: var(--bg-page);
}

/* Map */
.map-section {
  background: var(--bg-card);
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border-light);
  margin-bottom: 16px;
}

/* Actions */
.actions-bar {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: stretch;
}

.btn-analyze {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: var(--primary-color);
  color: white;
  border: none;
  padding: 14px 20px;
  border-radius: var(--radius-sm);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition);
  width: 100%;
}

.btn-analyze:hover:not(:disabled) {
  background: var(--primary-dark);
}

.btn-analyze:disabled {
  background: #bbb;
  cursor: not-allowed;
}

.btn-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.btn-cancel {
  background: var(--bg-page);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  padding: 14px 20px;
  border-radius: var(--radius-sm);
  text-decoration: none;
  font-size: 15px;
  text-align: center;
  transition: all var(--transition);
}

.btn-cancel:hover {
  background: var(--border-light);
  color: var(--text-primary);
}

/* Messages */
.error-banner {
  display: flex;
  align-items: center;
  gap: 10px;
  background: var(--danger-bg);
  color: #c62828;
  padding: 12px 14px;
  border-radius: var(--radius-sm);
  margin-top: 12px;
  font-size: 13px;
}

.loading-banner {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  background: var(--info-bg);
  padding: 14px;
  border-radius: var(--radius-sm);
  margin-top: 12px;
}

.loading-pulse {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--info-color);
  margin-top: 4px;
  flex-shrink: 0;
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}

.loading-banner p {
  margin: 0;
  color: #1565c0;
  font-size: 13px;
}

.loading-banner p + p {
  margin-top: 4px;
}

.loading-detail {
  color: var(--text-muted) !important;
  font-size: 12px !important;
}

/* === DESKTOP === */
@media (min-width: 768px) {
  .page-container {
    padding: 0 24px 40px;
  }

  .page-header h1 {
    font-size: 24px;
  }

  .page-subtitle {
    font-size: 14px;
  }

  .steps-bar {
    flex-wrap: nowrap;
    gap: 0;
    margin-bottom: 20px;
    padding: 16px 0;
  }

  .step {
    padding: 8px 16px;
    font-size: 13px;
    gap: 8px;
  }

  .step-num {
    width: 22px;
    height: 22px;
    font-size: 11px;
  }

  .step-line {
    display: block;
    width: 32px;
    height: 2px;
    background: var(--border-color);
    transition: background var(--transition);
  }

  .step-line.done {
    background: var(--primary-color);
  }

  .options-row {
    padding: 14px 20px;
    margin-bottom: 16px;
  }

  .option-group {
    flex-direction: row;
    align-items: center;
    gap: 14px;
  }

  .option-group label {
    font-size: 14px;
    white-space: nowrap;
  }

  .option-group select {
    flex: 1;
    max-width: 400px;
    font-size: 14px;
    padding: 9px 12px;
  }

  .map-section {
    margin-bottom: 20px;
  }

  .actions-bar {
    flex-direction: row;
    align-items: center;
    gap: 12px;
  }

  .btn-analyze {
    width: auto;
    padding: 14px 28px;
    font-size: 16px;
  }

  .btn-analyze:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(46, 125, 50, 0.3);
  }

  .btn-cancel {
    width: auto;
    padding: 14px 24px;
  }

  .error-banner {
    padding: 14px 20px;
    font-size: 14px;
  }

  .loading-banner {
    padding: 18px 20px;
    gap: 14px;
  }

  .loading-banner p {
    font-size: 14px;
  }

  .loading-detail {
    font-size: 13px !important;
  }
}
</style>
