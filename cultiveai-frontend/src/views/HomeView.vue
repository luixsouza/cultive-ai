<template>
  <div>
    <h1>CultiveAI - Mapeamento de Pastagens</h1>
    <p>Desenhe a área de interesse no mapa para iniciar a análise.</p>
    <MapComponent @area-drawn="onAreaDrawn" />
    <button @click="startAnalysis" :disabled="!drawnGeoJSON || loading">
      {{ loading ? "Analisando..." : "Analisar Área" }}
    </button>
    <div v-if="error" style="color: red; margin-top: 10px">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import ApiService from "@/services/ApiService";
import MapComponent from "@/components/MapComponent.vue";

const drawnGeoJSON = ref(null);
const loading = ref(false);
const error = ref("");
const router = useRouter();

function onAreaDrawn(geojson) {
  drawnGeoJSON.value = {
    type: "FeatureCollection",
    features: [geojson],
  };
  error.value = "";
}

async function startAnalysis() {
  if (!drawnGeoJSON.value) {
    error.value = "Por favor, desenhe uma área no mapa primeiro.";
    return;
  }
  loading.value = true;
  error.value = "";
  try {
    const response = await ApiService.analyzeArea(drawnGeoJSON.value);
    const reportId = response.data.id;
    router.push({ name: "AnalysisView", params: { id: reportId } });
  } catch (err) {
    console.error("Erro ao iniciar a análise:", err);
    error.value =
      err.response?.data?.detail || "Ocorreu um erro ao processar a análise.";
  } finally {
    loading.value = false;
  }
}
</script>
