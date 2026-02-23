<template>
  <div class="max-w-5xl mx-auto px-4 md:px-6">
    <!-- Header -->
    <div class="mb-4">
      <h1 class="text-xl md:text-2xl font-bold text-slate-800 dark:text-white">Nova Analise de Pastagem</h1>
      <p class="text-slate-400 dark:text-slate-500 text-sm mt-0.5">Desenhe a area de interesse no mapa para iniciar a analise com IA</p>
    </div>

    <!-- Steps indicator -->
    <div class="flex items-center justify-center flex-wrap md:flex-nowrap gap-1.5 md:gap-0 mb-4 md:mb-5 py-3 md:py-4">
      <div :class="[
        'flex items-center gap-1.5 md:gap-2 px-3 md:px-4 py-1.5 md:py-2 rounded-full text-xs md:text-[13px] border transition-colors',
        true ? 'text-primary bg-primary-bg dark:bg-green-900/20 border-transparent font-medium' : 'text-slate-400 bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-700'
      ]">
        <span :class="['w-5 h-5 md:w-[22px] md:h-[22px] rounded-full flex items-center justify-center text-[10px] md:text-[11px] font-bold text-white', drawnGeoJSON ? 'bg-primary' : 'bg-primary']">1</span>
        <span>Selecionar area</span>
      </div>
      <div :class="['hidden md:block w-8 h-0.5 transition-colors', drawnGeoJSON ? 'bg-primary' : 'bg-slate-200 dark:bg-slate-700']"></div>
      <div :class="[
        'flex items-center gap-1.5 md:gap-2 px-3 md:px-4 py-1.5 md:py-2 rounded-full text-xs md:text-[13px] border transition-colors',
        drawnGeoJSON && !loading ? 'text-primary bg-primary-bg dark:bg-green-900/20 border-transparent font-medium' : 'text-slate-400 dark:text-slate-500 bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-700'
      ]">
        <span :class="['w-5 h-5 md:w-[22px] md:h-[22px] rounded-full flex items-center justify-center text-[10px] md:text-[11px] font-bold text-white', drawnGeoJSON ? 'bg-primary' : 'bg-slate-300 dark:bg-slate-600']">2</span>
        <span>Configurar</span>
      </div>
      <div :class="['hidden md:block w-8 h-0.5 transition-colors', loading ? 'bg-primary' : 'bg-slate-200 dark:bg-slate-700']"></div>
      <div :class="[
        'flex items-center gap-1.5 md:gap-2 px-3 md:px-4 py-1.5 md:py-2 rounded-full text-xs md:text-[13px] border transition-colors',
        loading ? 'text-primary bg-primary-bg dark:bg-green-900/20 border-transparent font-medium' : 'text-slate-400 dark:text-slate-500 bg-white dark:bg-slate-900 border-slate-200 dark:border-slate-700'
      ]">
        <span :class="['w-5 h-5 md:w-[22px] md:h-[22px] rounded-full flex items-center justify-center text-[10px] md:text-[11px] font-bold text-white', loading ? 'bg-primary' : 'bg-slate-300 dark:bg-slate-600']">3</span>
        <span>Analisar</span>
      </div>
    </div>

    <!-- Property selector -->
    <div class="bg-white dark:bg-slate-900 rounded-2xl p-3.5 md:px-5 md:py-4 shadow-sm border border-slate-100 dark:border-slate-800 mb-3 md:mb-4">
      <div class="flex flex-col md:flex-row md:items-center gap-2 md:gap-3.5">
        <label class="text-sm font-medium text-slate-600 dark:text-slate-300 md:whitespace-nowrap">Vincular a uma propriedade (opcional):</label>
        <select
          v-model="selectedPropertyId"
          class="w-full md:flex-1 md:max-w-md px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-700 dark:text-slate-200 text-sm"
        >
          <option :value="null">Nenhuma propriedade</option>
          <option v-for="prop in properties" :key="prop.id" :value="prop.id">
            {{ prop.name }} ({{ prop.client_name }})
          </option>
        </select>
      </div>
    </div>

    <!-- Map -->
    <div class="bg-white dark:bg-slate-900 rounded-2xl overflow-hidden shadow-md border border-slate-100 dark:border-slate-800 mb-4 md:mb-5">
      <MapComponent @area-drawn="onAreaDrawn" />
    </div>

    <!-- Actions -->
    <div class="flex flex-col md:flex-row gap-2.5 md:gap-3 md:items-center">
      <button
        @click="startAnalysis"
        :disabled="!drawnGeoJSON || loading"
        class="inline-flex items-center justify-center gap-2 w-full md:w-auto bg-primary hover:bg-primary-dark text-white px-6 py-3.5 md:py-3 rounded-xl font-semibold text-[15px] md:text-base transition-all disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer hover:not-disabled:-translate-y-0.5 hover:not-disabled:shadow-lg"
      >
        <span v-if="!loading" class="material-icons-round text-lg">satellite_alt</span>
        <div v-if="loading" class="w-[18px] h-[18px] border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
        {{ loading ? "Analisando... (pode levar alguns minutos)" : "Analisar Area Selecionada" }}
      </button>
      <router-link
        to="/"
        class="w-full md:w-auto text-center px-6 py-3.5 md:py-3 bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 rounded-xl text-[15px] md:text-base border border-slate-200 dark:border-slate-700 hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors"
      >
        Cancelar
      </router-link>
    </div>

    <!-- Error banner -->
    <div v-if="error" class="flex items-center gap-2.5 bg-danger-bg dark:bg-red-900/30 text-red-700 dark:text-red-400 px-4 py-3 rounded-xl mt-3 text-sm">
      <span class="material-icons-round text-lg">error</span>
      {{ error }}
    </div>

    <!-- Loading banner -->
    <div v-if="loading" class="flex items-start gap-3 bg-info-bg dark:bg-blue-900/30 px-4 py-3.5 rounded-xl mt-3">
      <div class="w-3 h-3 rounded-full bg-info mt-1 shrink-0 animate-pulse"></div>
      <div>
        <p class="text-info dark:text-blue-400 text-sm font-medium">Analise em andamento</p>
        <p class="text-slate-400 dark:text-slate-500 text-xs mt-1">
          Processando imagens de satelite, calculando indices de vegetacao e gerando relatorio com IA.
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
