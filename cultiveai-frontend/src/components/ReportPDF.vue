<template>
  <div id="report-pdf-content" ref="reportEl">
    <!-- Header -->
    <div class="rpt-header">
      <div class="rpt-logo">
        <span class="rpt-logo-icon">&#x1F33F;</span>
        CULTIVEAI
      </div>
      <h1 class="rpt-title">Relatório de Análise de Pastagem</h1>
      <p class="rpt-subtitle">Análise automatizada por sensoriamento remoto e inteligência artificial</p>
      <div class="rpt-meta">
        <span class="rpt-meta-item">
          <strong>Data:</strong> {{ formatDate(data.created_at) }}
        </span>
        <span v-if="data.property_name" class="rpt-meta-item">
          <strong>Propriedade:</strong> {{ data.property_name }}
        </span>
        <span class="rpt-meta-item">
          <strong>Plataforma:</strong> CultiveAI
        </span>
      </div>
    </div>

    <!-- Summary Stats -->
    <div class="rpt-section">
      <h2 class="rpt-section-title">Resumo da Análise</h2>
      <div class="rpt-grid-4">
        <div class="rpt-stat-card">
          <div class="rpt-stat-label">Período Analisado</div>
          <div class="rpt-stat-text">
            {{ data.analysis_period?.start_date || 'N/A' }}<br>a {{ data.analysis_period?.end_date || 'N/A' }}
          </div>
        </div>
        <div class="rpt-stat-card">
          <div class="rpt-stat-label">Área Total</div>
          <div class="rpt-stat-value">{{ data.aoi_area_hectares?.toFixed(2) || '0' }} <span class="rpt-stat-unit">ha</span></div>
        </div>
        <div class="rpt-stat-card">
          <div class="rpt-stat-label">Imagem de Satélite</div>
          <div class="rpt-stat-text" style="word-break: break-all; font-size: 11px;">
            {{ data.satellite_image_info?.id || 'N/A' }}
          </div>
        </div>
        <div class="rpt-stat-card">
          <div class="rpt-stat-label">Cobertura de Nuvens</div>
          <div class="rpt-stat-value">
            {{ data.satellite_image_info?.cloud_percentage != null ? data.satellite_image_info.cloud_percentage.toFixed(1) : 'N/A' }}<span class="rpt-stat-unit">%</span>
          </div>
        </div>
      </div>
    </div>

    <!-- NDVI Statistics -->
    <div class="rpt-section">
      <h2 class="rpt-section-title">Índices de Vegetação (NDVI)</h2>
      <p class="rpt-description">
        O NDVI (Índice de Vegetação por Diferença Normalizada) varia de -1 a 1.
        Valores acima de 0.5 indicam vegetação densa e saudável; valores abaixo de 0.3 indicam solo exposto ou vegetação degradada.
      </p>
      <div class="rpt-grid-4">
        <div class="rpt-ndvi-card" style="border-left: 4px solid #dc2626;">
          <div class="rpt-ndvi-label">Mínimo</div>
          <div class="rpt-ndvi-value" style="color: #dc2626;">{{ data.ndvi_stats?.min?.toFixed(4) || 'N/A' }}</div>
        </div>
        <div class="rpt-ndvi-card" style="border-left: 4px solid #d97706;">
          <div class="rpt-ndvi-label">Médio</div>
          <div class="rpt-ndvi-value" style="color: #d97706;">{{ data.ndvi_stats?.mean?.toFixed(4) || 'N/A' }}</div>
        </div>
        <div class="rpt-ndvi-card" style="border-left: 4px solid #16a34a;">
          <div class="rpt-ndvi-label">Máximo</div>
          <div class="rpt-ndvi-value" style="color: #16a34a;">{{ data.ndvi_stats?.max?.toFixed(4) || 'N/A' }}</div>
        </div>
        <div class="rpt-ndvi-card" style="border-left: 4px solid #6366f1;">
          <div class="rpt-ndvi-label">Saúde Geral</div>
          <div class="rpt-ndvi-value" :style="{ color: healthColor }">{{ healthLabel }}</div>
        </div>
      </div>
    </div>

    <!-- Degradation Distribution -->
    <div v-if="degradationItems.length > 0" class="rpt-section">
      <h2 class="rpt-section-title">Distribuição da Saúde da Pastagem</h2>

      <!-- Visual bars -->
      <div class="rpt-deg-bars">
        <div v-for="item in degradationItems" :key="item.label" class="rpt-deg-bar-row">
          <div class="rpt-deg-bar-label">
            <span class="rpt-dot" :style="{ background: item.color }"></span>
            {{ item.label }}
          </div>
          <div class="rpt-deg-bar-track">
            <div class="rpt-deg-bar-fill" :style="{ width: item.percentage + '%', background: item.color }"></div>
          </div>
          <div class="rpt-deg-bar-pct">{{ item.percentage.toFixed(1) }}%</div>
        </div>
      </div>

      <!-- Detailed table -->
      <table class="rpt-table">
        <thead>
          <tr>
            <th>Classe</th>
            <th style="text-align: right;">Porcentagem</th>
            <th style="text-align: right;">Área (ha)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in degradationItems" :key="'t-' + item.label">
            <td>
              <span class="rpt-dot" :style="{ background: item.color }"></span>
              {{ item.label }}
            </td>
            <td style="text-align: right;">{{ item.percentage.toFixed(2) }}%</td>
            <td style="text-align: right;">{{ item.area.toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- AI Diagnosis -->
    <div v-if="data.ai_description" class="rpt-section">
      <h2 class="rpt-section-title">Diagnóstico por Inteligência Artificial</h2>
      <div class="rpt-ai-box">
        <div class="rpt-ai-header">
          <span class="rpt-ai-icon">&#x1F916;</span>
          <div>
            <strong>Análise Detalhada</strong><br>
            <span style="font-size: 11px; color: #64748b;">Gerado automaticamente pelo CultiveAI com base nos dados de sensoriamento remoto</span>
          </div>
        </div>
        <div class="rpt-ai-body" v-html="renderedAI"></div>
      </div>
    </div>

    <!-- Footer -->
    <div class="rpt-footer">
      <p>Relatório gerado automaticamente pela plataforma <strong>CultiveAI</strong></p>
      <p>Dados: Sentinel-2 (Copernicus/ESA) &bull; Processamento: Google Earth Engine &bull; IA: Modelo de linguagem</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { marked } from "marked";

const props = defineProps({
  data: { type: Object, required: true },
});

const degradationColors = {
  "Degradação Severa": "#a50026",
  "Degradação Moderada": "#d73027",
  "Pastagem Estressada": "#fdae61",
  "Pastagem Boa": "#66bd63",
  "Pastagem Excelente": "#1a9641",
  "Não Classificado": "#CCCCCC",
  "Degradacao Severa": "#a50026",
  "Degradacao Moderada": "#d73027",
};

const degradationItems = computed(() => {
  const summary = props.data?.degradation_summary;
  if (!Array.isArray(summary)) return [];
  return summary
    .map((item) => ({
      label: item.class_name || "Desconhecida",
      percentage: item.percentage || 0,
      area: item.area_hectares || 0,
      color: degradationColors[item.class_name] || "#999",
    }))
    .sort((a, b) => b.percentage - a.percentage);
});

const healthLabel = computed(() => {
  const mean = props.data?.ndvi_stats?.mean;
  if (mean == null) return "N/A";
  if (mean >= 0.5) return "Excelente";
  if (mean >= 0.4) return "Boa";
  if (mean >= 0.3) return "Moderada";
  if (mean >= 0.2) return "Estressada";
  return "Degradada";
});

const healthColor = computed(() => {
  const mean = props.data?.ndvi_stats?.mean;
  if (mean == null) return "#94a3b8";
  if (mean >= 0.5) return "#16a34a";
  if (mean >= 0.4) return "#22c55e";
  if (mean >= 0.3) return "#d97706";
  if (mean >= 0.2) return "#f97316";
  return "#dc2626";
});

const renderedAI = computed(() => {
  if (!props.data?.ai_description) return "";
  return marked(props.data.ai_description);
});

function formatDate(dateStr) {
  if (!dateStr) return "N/A";
  let str = dateStr;
  if (!str.endsWith("Z") && !str.includes("+")) str += "Z";
  return new Date(str).toLocaleDateString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    timeZone: "America/Sao_Paulo",
  });
}
</script>

<style scoped>
/* All styles are scoped and self-contained for html2pdf rendering.
   No Tailwind classes - pure CSS for reliable PDF output. */

#report-pdf-content {
  font-family: "Segoe UI", -apple-system, sans-serif;
  color: #1e293b;
  background: #fff;
  width: 740px; /* ~A4 at 96dpi minus margins */
  line-height: 1.5;
  font-size: 13px;
}

/* Header */
.rpt-header {
  background: linear-gradient(135deg, #2D6A4F 0%, #40916C 100%);
  color: white;
  padding: 28px 32px 22px;
  border-radius: 0 0 12px 12px;
}
.rpt-logo {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  opacity: 0.8;
  margin-bottom: 8px;
}
.rpt-logo-icon { margin-right: 4px; }
.rpt-title {
  font-size: 22px;
  font-weight: 800;
  margin: 0 0 2px;
}
.rpt-subtitle {
  font-size: 12px;
  opacity: 0.8;
  margin: 0;
}
.rpt-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 14px;
  padding-top: 12px;
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  font-size: 12px;
}
.rpt-meta-item strong { margin-right: 4px; }

/* Sections */
.rpt-section {
  padding: 0 32px;
  margin-top: 22px;
  page-break-inside: avoid;
}
.rpt-section-title {
  font-size: 15px;
  font-weight: 700;
  color: #2D6A4F;
  padding-bottom: 6px;
  margin: 0 0 12px;
  border-bottom: 2px solid #d1fae5;
}
.rpt-description {
  font-size: 11px;
  color: #64748b;
  margin: 0 0 12px;
  line-height: 1.5;
}

/* Stats Grid */
.rpt-grid-4 {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}
.rpt-stat-card {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 8px;
  padding: 10px 12px;
}
.rpt-stat-label {
  font-size: 9px;
  font-weight: 700;
  color: #166534;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  margin-bottom: 4px;
}
.rpt-stat-value {
  font-size: 20px;
  font-weight: 800;
  color: #1e293b;
}
.rpt-stat-unit {
  font-size: 11px;
  font-weight: 500;
  color: #64748b;
}
.rpt-stat-text {
  font-size: 12px;
  font-weight: 600;
  color: #1e293b;
  line-height: 1.4;
}

/* NDVI cards */
.rpt-ndvi-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 10px 12px;
}
.rpt-ndvi-label {
  font-size: 9px;
  font-weight: 700;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.6px;
  margin-bottom: 4px;
}
.rpt-ndvi-value {
  font-size: 18px;
  font-weight: 800;
}

/* Degradation bars */
.rpt-deg-bars { margin-bottom: 14px; }
.rpt-deg-bar-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}
.rpt-deg-bar-label {
  font-size: 12px;
  font-weight: 500;
  color: #334155;
  width: 160px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 6px;
}
.rpt-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  display: inline-block;
  flex-shrink: 0;
}
.rpt-deg-bar-track {
  flex: 1;
  height: 16px;
  background: #f1f5f9;
  border-radius: 8px;
  overflow: hidden;
}
.rpt-deg-bar-fill {
  height: 100%;
  border-radius: 8px;
  min-width: 3px;
}
.rpt-deg-bar-pct {
  font-size: 12px;
  font-weight: 700;
  color: #334155;
  width: 50px;
  text-align: right;
  flex-shrink: 0;
}

/* Table */
.rpt-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
  margin-top: 4px;
}
.rpt-table thead th {
  background: #2D6A4F;
  color: white;
  padding: 8px 12px;
  text-align: left;
  font-weight: 600;
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.rpt-table tbody td {
  padding: 8px 12px;
  border-bottom: 1px solid #e2e8f0;
}
.rpt-table tbody tr:nth-child(even) {
  background: #f8fafc;
}

/* AI Report */
.rpt-ai-box {
  background: #f0fdf4;
  border-left: 4px solid #2D6A4F;
  border-radius: 0 10px 10px 0;
  padding: 18px 22px;
}
.rpt-ai-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid #d1fae5;
}
.rpt-ai-icon { font-size: 24px; }
.rpt-ai-body { font-size: 12px; line-height: 1.65; color: #374151; }
.rpt-ai-body :deep(h1),
.rpt-ai-body :deep(h2),
.rpt-ai-body :deep(h3),
.rpt-ai-body :deep(h4) {
  color: #2D6A4F;
  margin-top: 14px;
  margin-bottom: 4px;
}
.rpt-ai-body :deep(h2) {
  font-size: 14px;
  padding-bottom: 4px;
  border-bottom: 1px solid #bbf7d0;
}
.rpt-ai-body :deep(h3) { font-size: 13px; }
.rpt-ai-body :deep(p) { margin: 5px 0; }
.rpt-ai-body :deep(ul),
.rpt-ai-body :deep(ol) { padding-left: 18px; margin: 5px 0; }
.rpt-ai-body :deep(li) { margin: 2px 0; }
.rpt-ai-body :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin: 10px 0;
  font-size: 11px;
}
.rpt-ai-body :deep(th),
.rpt-ai-body :deep(td) {
  padding: 6px 8px;
  border: 1px solid #d1fae5;
  text-align: left;
}
.rpt-ai-body :deep(th) {
  background: #dcfce7;
  font-weight: 600;
  color: #166534;
}
.rpt-ai-body :deep(strong) { font-weight: 600; }

/* Footer */
.rpt-footer {
  text-align: center;
  padding: 18px 32px;
  margin-top: 24px;
  border-top: 2px solid #d1fae5;
  color: #94a3b8;
  font-size: 10px;
}
.rpt-footer p { margin: 2px 0; }
.rpt-footer strong { color: #2D6A4F; }
</style>
