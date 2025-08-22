<template>
  <div class="report-container">
    <h1>Relatório de Análise #{{ data.id }}</h1>
    <div class="grid">
      <div class="grid-item">
        <strong>Período:</strong><br />{{ data.analysis_period.start_date }} a
        {{ data.analysis_period.end_date }}
      </div>
      <div class="grid-item">
        <strong>Área Total:</strong><br />{{
          data.aoi_area_hectares.toFixed(2)
        }}
        ha
      </div>
      <div class="grid-item">
        <strong>ID da Imagem:</strong><br />{{ data.satellite_image_info.id }}
      </div>
      <div class="grid-item">
        <strong>Nuvens:</strong><br />{{
          data.satellite_image_info.cloud_percentage.toFixed(2)
        }}%
      </div>
    </div>

    <h2>Diagnóstico por IA</h2>
    <div class="ai-report" v-html="formattedAiDescription"></div>

    <h2>Distribuição da Saúde da Pastagem</h2>
    <table>
      <thead>
        <tr>
          <th>Classe</th>
          <th>% da Área</th>
          <th>Área (ha)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in data.degradation_summary" :key="item.class_name">
          <td>{{ item.class_name }}</td>
          <td>{{ item.percentage.toFixed(2) }}%</td>
          <td>{{ item.area_hectares.toFixed(2) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { marked } from "marked";

const props = defineProps({
  data: {
    type: Object,
    required: true,
  },
});

const formattedAiDescription = computed(() => {
  return marked(props.data.ai_description);
});
</script>

<style scoped>
.report-container {
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
h1,
h2 {
  color: #2e7d32;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}
.grid-item {
  background: #e8f5e9;
  padding: 15px;
  border-radius: 5px;
}
.ai-report {
  background: #f1f8e9;
  padding: 20px;
  border-left: 5px solid #689f38;
  border-radius: 5px;
  margin-top: 15px;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 15px;
}
th,
td {
  text-align: left;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}
th {
  background-color: #388e3c;
  color: white;
}
</style>
