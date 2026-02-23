<template>
  <div class="max-w-5xl mx-auto px-4 md:px-6">
    <!-- Welcome -->
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3 mb-5 md:mb-7">
      <div>
        <h1 class="text-xl md:text-2xl font-bold text-slate-800 dark:text-white">Dashboard</h1>
        <p class="text-slate-400 dark:text-slate-500 text-sm mt-0.5">Visao geral da sua plataforma de analise de pastagens</p>
      </div>
      <router-link
        to="/analysis/new"
        class="hidden md:inline-flex items-center gap-2 bg-primary hover:bg-primary-dark text-white px-5 py-2.5 rounded-xl font-semibold text-sm transition-all hover:-translate-y-0.5 hover:shadow-lg"
      >
        <span class="material-icons-round text-lg">add_chart</span>
        Nova Analise
      </router-link>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4 mb-6 md:mb-8">
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-3.5 md:p-5 flex items-center gap-3 md:gap-4 shadow-sm border border-slate-100 dark:border-slate-800 transition-all hover:shadow-md hover:-translate-y-0.5">
        <div class="w-10 h-10 md:w-12 md:h-12 rounded-xl bg-info-bg dark:bg-blue-900/30 flex items-center justify-center shrink-0">
          <span class="material-icons-round text-info text-xl md:text-2xl">groups</span>
        </div>
        <div>
          <h3 class="text-xl md:text-2xl font-bold text-slate-800 dark:text-white leading-none">{{ stats.clients }}</h3>
          <p class="text-slate-400 dark:text-slate-500 text-[11px] md:text-xs mt-0.5">Clientes</p>
        </div>
      </div>
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-3.5 md:p-5 flex items-center gap-3 md:gap-4 shadow-sm border border-slate-100 dark:border-slate-800 transition-all hover:shadow-md hover:-translate-y-0.5">
        <div class="w-10 h-10 md:w-12 md:h-12 rounded-xl bg-primary-bg dark:bg-green-900/30 flex items-center justify-center shrink-0">
          <span class="material-icons-round text-primary text-xl md:text-2xl">landscape</span>
        </div>
        <div>
          <h3 class="text-xl md:text-2xl font-bold text-slate-800 dark:text-white leading-none">{{ stats.properties }}</h3>
          <p class="text-slate-400 dark:text-slate-500 text-[11px] md:text-xs mt-0.5">Propriedades</p>
        </div>
      </div>
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-3.5 md:p-5 flex items-center gap-3 md:gap-4 shadow-sm border border-slate-100 dark:border-slate-800 transition-all hover:shadow-md hover:-translate-y-0.5">
        <div class="w-10 h-10 md:w-12 md:h-12 rounded-xl bg-warning-bg dark:bg-orange-900/30 flex items-center justify-center shrink-0">
          <span class="material-icons-round text-warning text-xl md:text-2xl">analytics</span>
        </div>
        <div>
          <h3 class="text-xl md:text-2xl font-bold text-slate-800 dark:text-white leading-none">{{ stats.reports }}</h3>
          <p class="text-slate-400 dark:text-slate-500 text-[11px] md:text-xs mt-0.5">Analises</p>
        </div>
      </div>
      <div class="bg-white dark:bg-slate-900 rounded-2xl p-3.5 md:p-5 flex items-center gap-3 md:gap-4 shadow-sm border border-slate-100 dark:border-slate-800 transition-all hover:shadow-md hover:-translate-y-0.5">
        <div class="w-10 h-10 md:w-12 md:h-12 rounded-xl bg-pink-50 dark:bg-pink-900/30 flex items-center justify-center shrink-0">
          <span class="material-icons-round text-pink-600 text-xl md:text-2xl">straighten</span>
        </div>
        <div>
          <h3 class="text-xl md:text-2xl font-bold text-slate-800 dark:text-white leading-none">{{ formatArea(stats.totalArea) }}</h3>
          <p class="text-slate-400 dark:text-slate-500 text-[11px] md:text-xs mt-0.5">Area Total (ha)</p>
        </div>
      </div>
    </div>

    <!-- Quick Actions -->
    <div class="mb-6 md:mb-8">
      <h2 class="text-base md:text-lg font-bold text-slate-800 dark:text-white mb-3">Acoes Rapidas</h2>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
        <router-link
          to="/analysis/new"
          class="flex items-center md:flex-col md:items-center gap-3 md:gap-2.5 bg-primary-bg dark:bg-green-900/20 rounded-2xl p-4 md:p-5 text-primary font-medium text-sm transition-all hover:-translate-y-0.5 hover:shadow-md hover:bg-primary hover:text-white group"
        >
          <span class="material-icons-round text-2xl md:text-3xl group-hover:text-white">add_chart</span>
          <span>Nova Analise</span>
        </router-link>
        <router-link
          to="/clients"
          class="flex items-center md:flex-col md:items-center gap-3 md:gap-2.5 bg-white dark:bg-slate-900 rounded-2xl p-4 md:p-5 text-slate-600 dark:text-slate-300 font-medium text-sm shadow-sm border border-slate-100 dark:border-slate-800 transition-all hover:-translate-y-0.5 hover:shadow-md hover:text-primary hover:border-primary-bg"
        >
          <span class="material-icons-round text-2xl md:text-3xl opacity-60 group-hover:opacity-100">person_search</span>
          <span>Gerenciar Clientes</span>
        </router-link>
        <router-link
          to="/properties"
          class="flex items-center md:flex-col md:items-center gap-3 md:gap-2.5 bg-white dark:bg-slate-900 rounded-2xl p-4 md:p-5 text-slate-600 dark:text-slate-300 font-medium text-sm shadow-sm border border-slate-100 dark:border-slate-800 transition-all hover:-translate-y-0.5 hover:shadow-md hover:text-primary hover:border-primary-bg"
        >
          <span class="material-icons-round text-2xl md:text-3xl opacity-60 group-hover:opacity-100">landscape</span>
          <span>Gerenciar Propriedades</span>
        </router-link>
      </div>
    </div>

    <!-- Reports Section -->
    <div class="bg-white dark:bg-slate-900 rounded-2xl p-4 md:p-6 shadow-sm border border-slate-100 dark:border-slate-800">
      <!-- Header + Filters -->
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3 mb-4 md:mb-5">
        <h2 class="text-base md:text-lg font-bold text-slate-800 dark:text-white">Analises Recentes</h2>
        <div class="flex flex-col md:flex-row gap-2 md:gap-2.5">
          <div class="relative">
            <span class="material-icons-round absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-lg">search</span>
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Buscar analises..."
              @input="debouncedSearch"
              class="w-full md:w-60 pl-10 pr-3 py-2.5 md:py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-200 text-sm placeholder-slate-400"
            />
          </div>
          <select
            v-model="dateFilter"
            @change="loadReports"
            class="w-full md:w-auto px-3 py-2.5 md:py-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-200 text-sm"
          >
            <option value="">Todas as datas</option>
            <option value="7">Ultimos 7 dias</option>
            <option value="30">Ultimos 30 dias</option>
            <option value="90">Ultimos 90 dias</option>
          </select>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loadingReports" class="flex flex-col items-center justify-center py-10 text-slate-400 dark:text-slate-500 gap-3">
        <div class="w-8 h-8 border-3 border-slate-200 dark:border-slate-700 border-t-primary rounded-full animate-spin"></div>
        <p class="text-sm">Carregando analises...</p>
      </div>

      <!-- Empty -->
      <div v-else-if="reports.length === 0" class="flex flex-col items-center justify-center py-12 text-slate-400 dark:text-slate-500 gap-3">
        <span class="material-icons-round text-5xl text-slate-300 dark:text-slate-600">description</span>
        <p class="text-sm">Nenhuma analise encontrada.</p>
        <router-link
          to="/analysis/new"
          class="mt-1 inline-flex items-center gap-1.5 bg-primary text-white px-5 py-2.5 rounded-xl font-medium text-sm hover:bg-primary-dark transition-colors"
        >
          Criar primeira analise
        </router-link>
      </div>

      <!-- Reports List -->
      <div v-else class="space-y-2.5">
        <div
          v-for="report in reports"
          :key="report.id"
          class="flex flex-col md:flex-row md:items-center md:justify-between gap-3 border border-slate-100 dark:border-slate-800 rounded-xl p-3.5 md:px-5 md:py-4 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors"
        >
          <!-- Info -->
          <div class="flex flex-col md:flex-row md:items-center gap-2 md:gap-5 flex-1">
            <div>
              <h3 class="text-sm font-semibold text-slate-800 dark:text-white">{{ report.title || `Analise #${report.id}` }}</h3>
              <p class="text-xs text-slate-400 dark:text-slate-500 mt-0.5">{{ formatDate(report.created_at) }}</p>
              <div class="flex gap-3 mt-1">
                <span v-if="report.aoi_area_hectares" class="text-xs text-slate-500 dark:text-slate-400">
                  <strong>Area:</strong> {{ report.aoi_area_hectares.toFixed(2) }} ha
                </span>
                <span v-if="report.ndvi_stats" class="text-xs text-slate-500 dark:text-slate-400">
                  <strong>NDVI:</strong> {{ report.ndvi_stats.mean?.toFixed(3) || 'N/A' }}
                </span>
              </div>
            </div>
            <span
              v-if="report.degradation_summary"
              :class="[
                'self-start px-3 py-1 rounded-full text-[11px] font-semibold whitespace-nowrap',
                getDegradationClass(report.degradation_summary)
              ]"
            >
              {{ getDegradationLabel(report.degradation_summary) }}
            </span>
          </div>

          <!-- Actions -->
          <div class="flex gap-2">
            <router-link
              :to="`/analysis/${report.id}`"
              class="flex-1 md:flex-none text-center px-3.5 py-2 bg-primary text-white rounded-lg text-xs font-medium hover:bg-primary-dark transition-colors"
            >
              Ver Detalhes
            </router-link>
            <a
              :href="getDownloadUrl(report.id)"
              target="_blank"
              class="flex-1 md:flex-none text-center px-3.5 py-2 bg-slate-50 dark:bg-slate-800 text-slate-600 dark:text-slate-300 rounded-lg text-xs border border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-700 transition-colors"
            >
              Download
            </a>
            <button
              @click="confirmDelete(report)"
              class="flex-1 md:flex-none text-center px-3.5 py-2 text-danger border border-danger/30 rounded-lg text-xs hover:bg-danger-bg dark:hover:bg-red-900/20 transition-colors cursor-pointer"
            >
              Excluir
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div
      v-if="showDeleteModal"
      class="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-end md:items-center justify-center z-[1000] p-0 md:p-5"
      @click.self="closeDeleteModal"
    >
      <div class="bg-white dark:bg-slate-900 w-full md:w-[400px] md:max-w-[90%] rounded-t-2xl md:rounded-2xl p-6 md:p-7 shadow-2xl">
        <h2 class="text-lg font-bold text-slate-800 dark:text-white mb-3">Confirmar Exclusao</h2>
        <p class="text-slate-500 dark:text-slate-400 text-sm">
          Tem certeza que deseja excluir a analise
          <strong class="text-slate-700 dark:text-slate-200">{{ reportToDelete?.title || `#${reportToDelete?.id}` }}</strong>?
        </p>
        <div class="flex justify-end gap-2.5 mt-5">
          <button
            @click="closeDeleteModal"
            class="px-4 py-2.5 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 rounded-xl text-sm font-medium border border-slate-200 dark:border-slate-700 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors cursor-pointer"
          >
            Cancelar
          </button>
          <button
            @click="deleteReport"
            :disabled="deleting"
            class="px-4 py-2.5 bg-danger text-white rounded-xl text-sm font-medium hover:bg-red-700 transition-colors disabled:opacity-50 cursor-pointer"
          >
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
  let str = dateStr;
  if (!str.endsWith('Z') && !str.includes('+') && !/\d{2}-\d{2}$/.test(str)) {
    str += 'Z';
  }
  return new Date(str).toLocaleDateString("pt-BR", {
    day: "2-digit", month: "2-digit", year: "numeric", hour: "2-digit", minute: "2-digit",
    timeZone: "America/Sao_Paulo",
  });
}

function formatArea(area) {
  if (area >= 1000) return (area / 1000).toFixed(1) + "k";
  return area.toFixed(0);
}

function getDegradationClass(summary) {
  if (!summary) return "";
  const severePercent = (summary["1"]?.percentage || 0) + (summary["2"]?.percentage || 0);
  if (severePercent > 50) return "bg-danger-bg dark:bg-red-900/30 text-red-700 dark:text-red-400";
  if (severePercent > 25) return "bg-warning-bg dark:bg-orange-900/30 text-orange-700 dark:text-orange-400";
  return "bg-primary-bg dark:bg-green-900/30 text-primary";
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
