<template>
  <div class="max-w-5xl mx-auto px-4 md:px-6">
    <!-- Loading state -->
    <div v-if="loading" class="flex flex-col items-center justify-center min-h-[300px] md:min-h-[400px] gap-4 text-slate-400 dark:text-slate-500">
      <div class="w-9 h-9 md:w-10 md:h-10 border-3 border-slate-200 dark:border-slate-700 border-t-primary rounded-full animate-spin"></div>
      <p class="text-sm">Carregando relatorio...</p>
    </div>

    <!-- Error state -->
    <div v-if="error" class="flex flex-col items-center justify-center min-h-[300px] md:min-h-[400px] gap-4 text-slate-400 dark:text-slate-500">
      <span class="material-icons-round text-5xl text-slate-300 dark:text-slate-600">error_outline</span>
      <p class="text-sm">{{ error }}</p>
      <router-link to="/" class="bg-primary text-white px-5 py-2.5 rounded-xl font-medium text-sm hover:bg-primary-dark transition-colors">
        Voltar ao Dashboard
      </router-link>
    </div>

    <!-- Report content -->
    <div v-if="reportData && !loading" class="analysis-content">
      <!-- Print-only header (hidden on screen, visible on print) -->
      <div class="print-only-header">
        <div class="print-header-top">
          <div class="print-logo">&#x1F33F; CULTIVEAI</div>
          <div class="print-header-title">Relatório de Análise de Pastagem</div>
        </div>
        <div class="print-header-meta">
          <span>Data: {{ formatDate(reportData.created_at) }}</span>
          <span v-if="reportData.property_name">Propriedade: {{ reportData.property_name }}</span>
          <span>Análise automatizada por sensoriamento remoto e IA</span>
        </div>
      </div>

      <!-- Header -->
      <div class="flex flex-col md:flex-row md:justify-between md:items-start gap-3 md:gap-4 mb-5 md:mb-6 pb-4 md:pb-5 border-b border-slate-100 dark:border-slate-800 print-compact-header">
        <div>
          <h1 class="text-xl md:text-2xl font-bold text-slate-800 dark:text-white mb-1.5">Relatorio de Analise de Pastagem</h1>
          <p class="text-slate-400 dark:text-slate-500 text-sm flex items-center gap-2 flex-wrap">
            <span class="material-icons-round text-base">calendar_today</span>
            {{ formatDate(reportData.created_at) }}
            <span v-if="reportData.property_name" class="bg-info-bg dark:bg-blue-900/30 text-info px-2.5 py-0.5 rounded-full text-xs font-medium">
              {{ reportData.property_name }}
            </span>
          </p>
        </div>
        <div class="flex flex-col md:flex-row gap-2 w-full md:w-auto print-hide">
          <button
            @click="downloadPDF"
            :disabled="generatingPdf"
            class="inline-flex items-center justify-center gap-1.5 bg-primary hover:bg-primary-dark text-white px-4 py-2.5 rounded-xl font-medium text-sm transition-all hover:-translate-y-0.5 hover:shadow-lg disabled:opacity-60 disabled:pointer-events-none"
          >
            <span v-if="generatingPdf" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
            <span v-else class="material-icons-round text-base">picture_as_pdf</span>
            {{ generatingPdf ? 'Gerando PDF...' : 'Baixar PDF' }}
          </button>
          <button
            @click="printPage"
            class="inline-flex items-center justify-center gap-1.5 px-4 py-2.5 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 rounded-xl text-sm font-medium border border-slate-200 dark:border-slate-700 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
          >
            <span class="material-icons-round text-base">print</span>
            Imprimir
          </button>
          <button
            @click="saveScreenshot"
            :disabled="generatingScreenshot"
            class="inline-flex items-center justify-center gap-1.5 px-4 py-2.5 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 rounded-xl text-sm font-medium border border-slate-200 dark:border-slate-700 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors disabled:opacity-60"
          >
            <span v-if="generatingScreenshot" class="w-4 h-4 border-2 border-slate-400/30 border-t-slate-400 rounded-full animate-spin"></span>
            <span v-else class="material-icons-round text-base">image</span>
            {{ generatingScreenshot ? 'Salvando...' : 'Salvar Imagem' }}
          </button>
        </div>
      </div>

      <!-- Summary Grid (Period, Area, Satellite, Cloud) -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-2.5 md:gap-4 mb-5 md:mb-7">
        <div class="bg-primary-bg dark:bg-green-900/20 rounded-2xl p-3.5 md:p-4">
          <p class="text-[11px] md:text-xs text-primary-dark dark:text-green-400 font-medium mb-1">Periodo Analisado</p>
          <p class="text-sm md:text-[15px] font-semibold text-slate-800 dark:text-white leading-snug">
            {{ reportData.analysis_period?.start_date || 'N/A' }}<br>a {{ reportData.analysis_period?.end_date || 'N/A' }}
          </p>
        </div>
        <div class="bg-primary-bg dark:bg-green-900/20 rounded-2xl p-3.5 md:p-4">
          <p class="text-[11px] md:text-xs text-primary-dark dark:text-green-400 font-medium mb-1">Area Total</p>
          <p class="text-xl md:text-2xl font-bold text-slate-800 dark:text-white leading-none">{{ reportData.aoi_area_hectares?.toFixed(2) || '0' }}</p>
          <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">hectares</p>
        </div>
        <div class="bg-primary-bg dark:bg-green-900/20 rounded-2xl p-3.5 md:p-4">
          <p class="text-[11px] md:text-xs text-primary-dark dark:text-green-400 font-medium mb-1">Imagem de Satelite</p>
          <p class="text-xs md:text-sm font-medium text-slate-700 dark:text-slate-200 break-all leading-snug">
            {{ reportData.satellite_image_info?.id?.split('_').pop() || 'N/A' }}
          </p>
        </div>
        <div class="bg-primary-bg dark:bg-green-900/20 rounded-2xl p-3.5 md:p-4">
          <p class="text-[11px] md:text-xs text-primary-dark dark:text-green-400 font-medium mb-1">Cobertura de Nuvens</p>
          <p class="text-xl md:text-2xl font-bold text-slate-800 dark:text-white leading-none">
            {{ reportData.satellite_image_info?.cloud_percentage != null ? reportData.satellite_image_info.cloud_percentage.toFixed(2) : 'N/A' }}<span class="text-sm font-medium">%</span>
          </p>
        </div>
      </div>

      <!-- NDVI + Health Stats -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-2.5 md:gap-4 mb-5 md:mb-7">
        <div class="bg-white dark:bg-slate-900 rounded-2xl p-3.5 md:p-5 shadow-sm border border-slate-100 dark:border-slate-800">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-8 h-8 rounded-lg bg-red-50 dark:bg-red-900/30 flex items-center justify-center">
              <span class="material-icons-round text-red-500 text-base">trending_down</span>
            </div>
            <span class="text-[11px] text-slate-400 dark:text-slate-500">NDVI Min</span>
          </div>
          <span class="text-lg md:text-xl font-bold text-slate-800 dark:text-white">{{ reportData.ndvi_stats?.min?.toFixed(3) || 'N/A' }}</span>
        </div>
        <div class="bg-white dark:bg-slate-900 rounded-2xl p-3.5 md:p-5 shadow-sm border border-slate-100 dark:border-slate-800">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-8 h-8 rounded-lg bg-amber-50 dark:bg-amber-900/30 flex items-center justify-center">
              <span class="material-icons-round text-amber-500 text-base">remove</span>
            </div>
            <span class="text-[11px] text-slate-400 dark:text-slate-500">NDVI Medio</span>
          </div>
          <span class="text-lg md:text-xl font-bold text-slate-800 dark:text-white">{{ reportData.ndvi_stats?.mean?.toFixed(3) || 'N/A' }}</span>
        </div>
        <div class="bg-white dark:bg-slate-900 rounded-2xl p-3.5 md:p-5 shadow-sm border border-slate-100 dark:border-slate-800">
          <div class="flex items-center gap-2 mb-2">
            <div class="w-8 h-8 rounded-lg bg-green-50 dark:bg-green-900/30 flex items-center justify-center">
              <span class="material-icons-round text-green-500 text-base">trending_up</span>
            </div>
            <span class="text-[11px] text-slate-400 dark:text-slate-500">NDVI Max</span>
          </div>
          <span class="text-lg md:text-xl font-bold text-slate-800 dark:text-white">{{ reportData.ndvi_stats?.max?.toFixed(3) || 'N/A' }}</span>
        </div>
        <div class="bg-white dark:bg-slate-900 rounded-2xl p-3.5 md:p-5 shadow-sm border border-slate-100 dark:border-slate-800">
          <div class="flex items-center gap-2 mb-2">
            <div :class="['w-8 h-8 rounded-lg flex items-center justify-center', getHealthIconClass(reportData.ndvi_stats?.mean)]">
              <span class="material-icons-round text-base">monitor_heart</span>
            </div>
            <span class="text-[11px] text-slate-400 dark:text-slate-500">Saude Geral</span>
          </div>
          <span :class="['text-lg md:text-xl font-bold', getHealthTextClass(reportData.ndvi_stats?.mean)]">
            {{ getHealthLabel(reportData.ndvi_stats?.mean) }}
          </span>
        </div>
      </div>

      <!-- Degradation Distribution -->
      <div v-if="reportData.degradation_summary && reportData.degradation_summary.length > 0" class="bg-white dark:bg-slate-900 rounded-2xl p-4 md:p-6 mb-5 md:mb-7 shadow-sm border border-slate-100 dark:border-slate-800">
        <h2 class="text-base md:text-lg font-bold text-slate-800 dark:text-white mb-4">Distribuicao da Saude da Pastagem</h2>

        <!-- Visual bars -->
        <div class="space-y-3 mb-5">
          <div v-for="item in degradationItems" :key="item.label" class="flex items-center gap-3">
            <div class="w-3 h-3 rounded-full shrink-0" :style="{ background: item.color }"></div>
            <div class="flex-1 min-w-0">
              <div class="flex justify-between items-baseline mb-1">
                <span class="text-sm font-medium text-slate-700 dark:text-slate-200">{{ item.label }}</span>
                <span class="text-xs text-slate-400 dark:text-slate-500">{{ item.percentage.toFixed(1) }}% ({{ item.area.toFixed(2) }} ha)</span>
              </div>
              <div class="w-full h-2.5 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
                <div class="h-full rounded-full transition-all duration-500" :style="{ width: item.percentage + '%', background: item.color }"></div>
              </div>
            </div>
          </div>
        </div>

        <!-- Table -->
        <div class="overflow-x-auto -mx-4 md:mx-0">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-slate-200 dark:border-slate-700">
                <th class="text-left py-2.5 px-4 md:px-3 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide">Classe</th>
                <th class="text-right py-2.5 px-4 md:px-3 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide">%</th>
                <th class="text-right py-2.5 px-4 md:px-3 text-xs font-semibold text-slate-500 dark:text-slate-400 uppercase tracking-wide">Area (ha)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in degradationItems" :key="'t-' + item.label" class="border-b border-slate-100 dark:border-slate-800 last:border-0">
                <td class="py-2.5 px-4 md:px-3 text-slate-700 dark:text-slate-200 font-medium">
                  <span class="inline-flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full shrink-0" :style="{ background: item.color }"></span>
                    {{ item.label }}
                  </span>
                </td>
                <td class="py-2.5 px-4 md:px-3 text-right text-slate-600 dark:text-slate-300 tabular-nums">{{ item.percentage.toFixed(2) }}%</td>
                <td class="py-2.5 px-4 md:px-3 text-right text-slate-600 dark:text-slate-300 tabular-nums">{{ item.area.toFixed(2) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Map Section -->
      <div class="mb-5 md:mb-7">
        <div class="mb-2.5">
          <h2 class="text-base md:text-lg font-bold text-slate-800 dark:text-white">Mapa da Area Analisada</h2>
          <p class="text-slate-400 dark:text-slate-500 text-xs md:text-[13px] mt-0.5">Use as camadas para visualizar diferentes indices</p>
        </div>
        <div class="bg-white dark:bg-slate-900 rounded-2xl overflow-hidden shadow-md border-2 border-primary">
          <MapComponent
            :layers="reportData.map_layers_urls"
            :aoi="reportData.aoi_geojson"
            :is-display-mode="true"
          />
        </div>
      </div>

      <!-- AI Report -->
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-4 md:p-7 mb-5 md:mb-7 shadow-sm border border-slate-100 dark:border-slate-800">
        <div class="flex items-center gap-2.5 mb-3.5 md:mb-5 pb-3 md:pb-4 border-b border-slate-100 dark:border-slate-800">
          <div class="w-9 h-9 rounded-xl bg-primary-bg dark:bg-green-900/30 flex items-center justify-center shrink-0">
            <span class="material-icons-round text-primary text-lg">smart_toy</span>
          </div>
          <div>
            <h2 class="text-base md:text-lg font-bold text-slate-800 dark:text-white">Diagnostico por Inteligencia Artificial</h2>
            <p class="text-slate-400 dark:text-slate-500 text-xs md:text-[13px]">Analise detalhada gerada automaticamente pelo CultiveAI</p>
          </div>
        </div>
        <div class="ai-report-body leading-relaxed text-slate-600 dark:text-slate-300 text-sm" v-html="renderMarkdown(reportData.ai_description)"></div>
      </div>

      <!-- Final actions -->
      <div class="flex flex-col md:flex-row md:justify-center gap-2.5 md:gap-3.5 py-5 md:py-7 border-t border-slate-100 dark:border-slate-800 print-hide">
        <button
          @click="downloadPDF"
          :disabled="generatingPdf"
          class="inline-flex items-center justify-center gap-2 bg-primary hover:bg-primary-dark text-white px-6 py-3.5 rounded-xl font-semibold text-[15px] transition-all hover:-translate-y-0.5 hover:shadow-lg disabled:opacity-60 disabled:pointer-events-none"
        >
          <span v-if="generatingPdf" class="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
          <span v-else class="material-icons-round text-lg">picture_as_pdf</span>
          {{ generatingPdf ? 'Gerando PDF...' : 'Baixar Relatorio PDF' }}
        </button>
        <router-link
          to="/analysis/new"
          class="text-center px-6 py-3.5 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 rounded-xl text-[15px] font-medium border border-slate-200 dark:border-slate-700 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
        >
          Realizar Nova Analise
        </router-link>
      </div>

      <!-- Print-only footer -->
      <div class="print-only-footer">
        <p>Relatório gerado pela plataforma <strong>CultiveAI</strong> — Dados: Sentinel-2 (Copernicus/ESA) | Google Earth Engine | IA</p>
      </div>

      <!-- Hidden PDF render container (off-screen) -->
      <div class="pdf-offscreen">
        <ReportPDF v-if="reportData" :data="reportData" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import ApiService from "@/services/ApiService";
import MapComponent from "@/components/MapComponent.vue";
import ReportPDF from "@/components/ReportPDF.vue";
import { marked } from "marked";
import html2canvas from "html2canvas";

const props = defineProps({
  id: { type: [String, Number], required: true },
});

const reportData = ref(null);
const loading = ref(true);
const error = ref(null);
const generatingPdf = ref(false);
const generatingScreenshot = ref(false);

const degradationColors = {
  "Degradação Severa": "#a50026",
  "Degradação Moderada": "#d73027",
  "Pastagem Estressada": "#fdae61",
  "Pastagem Boa": "#66bd63",
  "Pastagem Excelente": "#1a9641",
  "Não Classificado": "#CCCCCC",
  // Fallbacks without accents
  "Degradacao Severa": "#a50026",
  "Degradacao Moderada": "#d73027",
};

const degradationItems = computed(() => {
  if (!reportData.value?.degradation_summary) return [];
  const summary = reportData.value.degradation_summary;
  if (!Array.isArray(summary)) return [];

  return summary.map((item) => ({
    label: item.class_name || "Desconhecida",
    percentage: item.percentage || 0,
    area: item.area_hectares || 0,
    color: degradationColors[item.class_name] || "#999",
  })).sort((a, b) => b.percentage - a.percentage);
});

function formatDate(dateStr) {
  if (!dateStr) return '';
  // Backend stores UTC but may omit 'Z' suffix - ensure proper parsing
  let str = dateStr;
  if (!str.endsWith('Z') && !str.includes('+') && !/\d{2}-\d{2}$/.test(str)) {
    str += 'Z';
  }
  return new Date(str).toLocaleDateString('pt-BR', {
    day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit',
    timeZone: 'America/Sao_Paulo',
  });
}

function getHealthIconClass(ndviMean) {
  if (!ndviMean) return 'bg-slate-100 dark:bg-slate-800 text-slate-400';
  if (ndviMean >= 0.5) return 'bg-green-50 dark:bg-green-900/30 text-green-600';
  if (ndviMean >= 0.4) return 'bg-green-50 dark:bg-green-900/30 text-green-500';
  if (ndviMean >= 0.3) return 'bg-amber-50 dark:bg-amber-900/30 text-amber-600';
  if (ndviMean >= 0.2) return 'bg-orange-50 dark:bg-orange-900/30 text-orange-500';
  return 'bg-red-50 dark:bg-red-900/30 text-red-600';
}

function getHealthTextClass(ndviMean) {
  if (!ndviMean) return 'text-slate-400';
  if (ndviMean >= 0.5) return 'text-green-600 dark:text-green-400';
  if (ndviMean >= 0.4) return 'text-green-500 dark:text-green-400';
  if (ndviMean >= 0.3) return 'text-amber-600 dark:text-amber-400';
  if (ndviMean >= 0.2) return 'text-orange-500 dark:text-orange-400';
  return 'text-red-600 dark:text-red-400';
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

async function downloadPDF() {
  generatingPdf.value = true;
  try {
    const html2pdf = (await import("html2pdf.js")).default;
    const element = document.getElementById("report-pdf-content");
    if (!element) return;

    const opt = {
      margin: [8, 6, 8, 6],
      filename: `relatorio_cultiveai_${props.id}.pdf`,
      image: { type: "jpeg", quality: 0.95 },
      html2canvas: { scale: 2, useCORS: true, logging: false },
      jsPDF: { unit: "mm", format: "a4", orientation: "portrait" },
      pagebreak: { mode: ["avoid-all", "css", "legacy"] },
    };

    await html2pdf().set(opt).from(element).save();
  } catch (err) {
    console.error("Erro ao gerar PDF:", err);
  } finally {
    generatingPdf.value = false;
  }
}

function printPage() {
  window.print();
}

async function saveScreenshot() {
  generatingScreenshot.value = true;
  try {
    const element = document.querySelector(".analysis-content");
    if (!element) {
      console.error("Elemento .analysis-content nao encontrado");
      return;
    }

    const canvas = await html2canvas(element, {
      scale: 2,
      useCORS: true,
      allowTaint: true,
      logging: false,
      backgroundColor: "#ffffff",
    });

    const link = document.createElement("a");
    link.download = `analise_cultiveai_${props.id}.png`;
    link.href = canvas.toDataURL("image/png");
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  } catch (err) {
    console.error("Erro ao gerar screenshot:", err);
    alert("Erro ao salvar imagem. Tente novamente.");
  } finally {
    generatingScreenshot.value = false;
  }
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
/* ===== Screen styles ===== */

/* Hidden on screen, shown on print */
.print-only-header,
.print-only-footer {
  display: none;
}

/* PDF off-screen container */
.pdf-offscreen {
  position: fixed;
  left: -9999px;
  top: 0;
  z-index: -1;
}

/* Markdown rendered content - needs :deep() for v-html */
.ai-report-body :deep(h2) {
  color: var(--color-primary);
  font-size: 16px;
  font-weight: 700;
  margin-top: 20px;
  margin-bottom: 6px;
  padding-bottom: 6px;
  border-bottom: 1px solid #e2e8f0;
}

.ai-report-body :deep(h3) {
  font-size: 14px;
  font-weight: 600;
  margin-top: 16px;
  margin-bottom: 4px;
}

.ai-report-body :deep(h4) {
  font-size: 13px;
  font-weight: 600;
  margin-top: 12px;
  margin-bottom: 4px;
}

.ai-report-body :deep(p) {
  margin: 6px 0;
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
  border: 1px solid #e2e8f0;
  text-align: left;
  white-space: nowrap;
}

.ai-report-body :deep(th) {
  background: #f0fdf4;
  font-weight: 600;
  color: var(--color-primary-dark);
}

:where(.dark) .ai-report-body :deep(h2) {
  border-bottom-color: #334155;
}

:where(.dark) .ai-report-body :deep(th) {
  background: #1e293b;
  color: #86efac;
}

:where(.dark) .ai-report-body :deep(th),
:where(.dark) .ai-report-body :deep(td) {
  border-color: #334155;
}

.ai-report-body :deep(strong) {
  font-weight: 600;
}

.ai-report-body :deep(hr) {
  border: none;
  border-top: 1px solid #e2e8f0;
  margin: 20px 0;
}

:where(.dark) .ai-report-body :deep(hr) {
  border-top-color: #334155;
}

.ai-report-body :deep(em) {
  color: #94a3b8;
  font-size: 0.9em;
}

@media (min-width: 768px) {
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
}

/* ===== Print styles ===== */
@media print {
  /* Show print-only elements */
  .print-only-header {
    display: block !important;
    margin-bottom: 16px;
  }
  .print-only-footer {
    display: block !important;
    margin-top: 24px;
    padding-top: 12px;
    border-top: 2px solid #d1fae5;
    text-align: center;
    font-size: 10px;
    color: #94a3b8;
  }
  .print-only-footer strong {
    color: #2D6A4F;
  }

  /* Print header styling */
  .print-header-top {
    background: linear-gradient(135deg, #2D6A4F, #40916C) !important;
    color: white !important;
    padding: 20px 24px !important;
    border-radius: 10px !important;
    margin-bottom: 8px;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }
  .print-logo {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    opacity: 0.85;
    margin-bottom: 6px;
  }
  .print-header-title {
    font-size: 22px;
    font-weight: 800;
    color: white !important;
  }
  .print-header-meta {
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    font-size: 11px;
    color: #475569;
    padding: 8px 4px;
    border-bottom: 2px solid #d1fae5;
    margin-bottom: 4px;
  }
  .print-header-meta span {
    color: #475569 !important;
  }

  /* Hide the on-screen header (date/buttons row) */
  .print-compact-header {
    display: none !important;
  }

  /* Hide PDF off-screen container */
  .pdf-offscreen {
    display: none !important;
  }

  /* Force light colors */
  .analysis-content {
    color: #1e293b !important;
    background: white !important;
  }

  .analysis-content * {
    color-adjust: exact !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }

  /* Force card backgrounds */
  .analysis-content :deep(.bg-primary-bg),
  .analysis-content :deep([class*="bg-primary-bg"]) {
    background-color: #E8F5E9 !important;
  }
  .analysis-content :deep(.bg-white),
  .analysis-content :deep([class*="bg-white"]) {
    background-color: white !important;
  }

  /* Better spacing for print */
  .analysis-content > div {
    margin-bottom: 12px !important;
  }

  /* Page breaks */
  .analysis-content > div {
    page-break-inside: avoid;
  }

  /* Remove shadows */
  .analysis-content :deep(.shadow-sm),
  .analysis-content :deep(.shadow-md) {
    box-shadow: none !important;
  }

  /* Ensure dark mode text is readable */
  .analysis-content :deep([class*="dark:"]) {
    color: #1e293b !important;
  }
  .analysis-content :deep([class*="text-slate-"]) {
    color: #334155 !important;
  }
  .analysis-content :deep([class*="text-white"]) {
    color: #1e293b !important;
  }

  /* AI report print */
  .ai-report-body :deep(h2) {
    color: #2D6A4F !important;
    border-bottom-color: #d1fae5 !important;
  }
  .ai-report-body :deep(th) {
    background: #f0fdf4 !important;
    color: #1B4332 !important;
    border-color: #e2e8f0 !important;
  }
  .ai-report-body :deep(td) {
    border-color: #e2e8f0 !important;
    color: #334155 !important;
  }
}
</style>
