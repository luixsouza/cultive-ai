<template>
  <div>
    <div v-if="loading">Carregando relatório...</div>
    <div v-if="error">{{ error }}</div>
    <div v-if="reportData">
      <AnalysisReport :data="reportData" />

      <h3>Mapa Interativo da Análise</h3>
      <MapComponent
        :layers="reportData.map_layers_urls"
        :aoi="reportData.aoi_geojson"
        :is-display-mode="true"
      />

      <a :href="downloadUrl" download class="download-button">
        Baixar Relatório HTML Completo
      </a>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import ApiService from "@/services/ApiService";
import AnalysisReport from "@/components/AnalysisReport.vue";
import MapComponent from "@/components/MapComponent.vue";

const props = defineProps({
  id: {
    type: [String, Number],
    required: true,
  },
});

const reportData = ref(null);
const loading = ref(true);
const error = ref(null);

const downloadUrl = computed(() => {
  return reportData.value
    ? ApiService.downloadReportUrl(reportData.value.id)
    : "#";
});

onMounted(async () => {
  try {
    const response = await ApiService.getAnalysisReport(props.id);
    reportData.value = response.data;
  } catch (err) {
    error.value = "Não foi possível carregar o relatório.";
    console.error(err);
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.download-button {
  display: inline-block;
  margin-top: 20px;
  padding: 12px 25px;
  background-color: #4caf50;
  color: white;
  text-decoration: none;
  border-radius: 5px;
}
</style>
