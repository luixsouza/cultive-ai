<template>
  <div class="map-wrapper">
    <!-- Instructions for drawing mode -->
    <div v-if="!isDisplayMode && !hasDrawnArea && !drawLoading" class="map-instructions">
      <div class="instructions-header">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2e7d32" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
        <strong>Como mapear a area</strong>
      </div>
      <ol>
        <li>Use os botoes na barra de ferramentas acima</li>
        <li><b>Poligono:</b> clique nos vertices e finalize no primeiro ponto</li>
        <li><b>Retangulo:</b> clique e arraste para selecionar</li>
      </ol>
    </div>

    <!-- Loading draw tools -->
    <div v-if="drawLoading" class="map-instructions">
      <div class="instructions-header">
        <div class="mini-spinner"></div>
        <strong>Carregando ferramentas...</strong>
      </div>
    </div>

    <!-- Area info badge -->
    <div v-if="!isDisplayMode && hasDrawnArea" class="area-info">
      <span class="area-badge">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s-8-4.5-8-11.8A8 8 0 0 1 12 2a8 8 0 0 1 8 8.2c0 7.3-8 11.8-8 11.8z"/></svg>
        <strong>{{ drawnAreaHectares }} ha</strong> selecionados
      </span>
      <button class="btn-clear" @click="clearDrawnArea">Limpar area</button>
    </div>

    <!-- Map container -->
    <div id="map-container" ref="mapContainer"></div>

    <!-- Filter controls for display mode -->
    <div v-if="isDisplayMode" class="filter-controls">
      <h4>Camadas de Analise</h4>
      <div class="filter-buttons">
        <button
          v-for="filter in availableFilters"
          :key="filter.key"
          :class="['filter-btn', { active: activeFilter === filter.key }]"
          @click="toggleFilter(filter.key)"
        >
          <span class="filter-dot" :style="{ background: getFilterColor(filter.key) }"></span>
          {{ filter.name }}
        </button>
      </div>
      <div v-if="activeFilter" class="opacity-control">
        <label>Opacidade: {{ Math.round(filterOpacity * 100) }}%</label>
        <input type="range" min="0" max="100" :value="filterOpacity * 100" @input="updateOpacity($event.target.value / 100)" />
      </div>
    </div>

    <!-- Legend -->
    <div v-if="isDisplayMode && activeFilter && getLegendItems().length > 0" class="map-legend">
      <h4>{{ getLegendTitle() }}</h4>
      <div class="legend-items">
        <div v-for="item in getLegendItems()" :key="item.label" class="legend-item">
          <span class="legend-color" :style="{ background: item.color }"></span>
          <span>{{ item.label }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from "vue";
import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css";
import L from "leaflet";

// CRITICAL FIX: Set L globally so leaflet-draw plugin can find it
// when loaded via dynamic import. This must happen before leaflet-draw executes.
window.L = L;

// Fix Leaflet default marker icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon-2x.png",
  iconUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-icon.png",
  shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/images/marker-shadow.png",
});

const props = defineProps({
  isDisplayMode: { type: Boolean, default: false },
  layers: { type: Object, default: () => ({}) },
  aoi: { type: Object, default: null },
});

const emit = defineEmits(["area-drawn"]);

const mapContainer = ref(null);
const hasDrawnArea = ref(false);
const drawnAreaSize = ref(0);
const activeFilter = ref(null);
const filterOpacity = ref(0.8);
const drawLoading = ref(false);

let map = null;
let drawnItems = null;
let currentOverlayLayer = null;

const drawnAreaHectares = computed(() => drawnAreaSize.value.toFixed(2));

const availableFilters = computed(() => {
  const filters = [];
  if (props.layers.ndvi_url) filters.push({ key: "ndvi", name: "NDVI", url: props.layers.ndvi_url });
  if (props.layers.degradation_url) filters.push({ key: "degradation", name: "Degradacao", url: props.layers.degradation_url });
  if (props.layers.ndmi_url) filters.push({ key: "ndmi", name: "Umidade", url: props.layers.ndmi_url });
  if (props.layers.savi_url) filters.push({ key: "savi", name: "SAVI", url: props.layers.savi_url });
  if (props.layers.slope_url) filters.push({ key: "slope", name: "Declividade", url: props.layers.slope_url });
  if (props.layers.rgb_url) filters.push({ key: "rgb", name: "Satelite", url: props.layers.rgb_url });
  return filters;
});

const legendData = {
  ndvi: { title: "NDVI - Vegetacao", items: [{ color: "#d73027", label: "Baixo (< 0.2)" }, { color: "#fee08b", label: "Medio (0.2 - 0.5)" }, { color: "#1a9850", label: "Alto (> 0.5)" }] },
  degradation: { title: "Nivel de Degradacao", items: [{ color: "#a50026", label: "Severa" }, { color: "#fdae61", label: "Moderada" }, { color: "#1a9641", label: "Conservada" }] },
  ndmi: { title: "Umidade (NDMI)", items: [{ color: "#a50026", label: "Seco" }, { color: "#74add1", label: "Umido" }] },
  savi: { title: "SAVI", items: [{ color: "#d73027", label: "Baixo" }, { color: "#1a9850", label: "Alto" }] },
  slope: { title: "Declividade", items: [{ color: "#33a02c", label: "Plano" }, { color: "#e31a1c", label: "Ingreme" }] },
  rgb: { title: "Imagem de Satelite", items: [] },
};

const filterColors = {
  ndvi: "#1a9850", degradation: "#d73027", ndmi: "#74add1",
  savi: "#33a02c", slope: "#e31a1c", rgb: "#1976d2",
};

function getFilterColor(key) {
  return filterColors[key] || "#666";
}
function getLegendTitle() {
  return legendData[activeFilter.value]?.title || "";
}
function getLegendItems() {
  return legendData[activeFilter.value]?.items || [];
}

function toggleFilter(filterKey) {
  if (activeFilter.value === filterKey) {
    activeFilter.value = null;
    if (currentOverlayLayer && map) {
      map.removeLayer(currentOverlayLayer);
      currentOverlayLayer = null;
    }
  } else {
    activeFilter.value = filterKey;
    applyFilter(filterKey);
  }
}

function applyFilter(filterKey) {
  if (currentOverlayLayer && map) map.removeLayer(currentOverlayLayer);
  const filter = availableFilters.value.find((f) => f.key === filterKey);
  if (filter && filter.url) {
    currentOverlayLayer = L.tileLayer(filter.url, { opacity: filterOpacity.value });
    currentOverlayLayer.addTo(map);
  }
}

function updateOpacity(value) {
  filterOpacity.value = value;
  if (currentOverlayLayer) currentOverlayLayer.setOpacity(value);
}

onMounted(() => {
  initMap();
});

onUnmounted(() => {
  if (map) {
    map.remove();
    map = null;
  }
});

function initMap() {
  // In display mode with AOI, initialize directly at the AOI bounds
  // so the map NEVER shows the default zoomed-out view.
  if (props.isDisplayMode && props.aoi) {
    const aoiBounds = L.geoJSON(props.aoi).getBounds();
    map = L.map("map-container", {
      zoomControl: true,
      doubleClickZoom: false,
    });
    map.fitBounds(aoiBounds, { padding: [50, 50], maxZoom: 17 });
  } else {
    map = L.map("map-container", {
      center: [-16.0, -49.5],
      zoom: 6,
      zoomControl: true,
      doubleClickZoom: false,
    });
  }

  L.tileLayer(
    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    { attribution: "Esri", maxZoom: 19 }
  ).addTo(map);

  L.tileLayer(
    "https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}{r}.png",
    { maxZoom: 19, pane: "overlayPane" }
  ).addTo(map);

  if (props.isDisplayMode) {
    setupDisplayMode();
  } else {
    // CRITICAL: Use dynamic import for leaflet-draw.
    // Static import was failing because Vite hoists all imports and
    // leaflet-draw could not find the global L object at module load time.
    // Dynamic import runs AFTER window.L = L has been set.
    drawLoading.value = true;
    import("leaflet-draw").then(() => {
      drawLoading.value = false;

      // FIX: Prevent polygon from being limited to 3 vertices.
      // Two problems in leaflet-draw on Windows 11:
      //
      // 1) L.Browser.touch is often TRUE on Windows 11 (even without a
      //    touch screen) because modern browsers expose touch APIs for
      //    pointer-event compat. In _endPoint(), if touch is true AND the
      //    click is within 10px of the first vertex, _finishShape() is
      //    called instead of addVertex() — silently closing the polygon.
      //
      // 2) _updateFinishHandler binds dblclick on the last marker after the
      //    3rd vertex. Fast successive clicks can fire as dblclick, auto-
      //    closing the polygon at exactly 3 vertices.
      //
      // Solution: Override _endPoint to always call addVertex (never the
      // touch-based auto-finish), and override _updateFinishHandler to
      // skip the dblclick binding. Users finish by clicking the first
      // vertex or the "Finish" toolbar button.

      L.Draw.Polyline.prototype._endPoint = function (clientX, clientY, e) {
        if (this._mouseDownOrigin) {
          var dragCheckDistance = L.point(clientX, clientY)
            .distanceTo(this._mouseDownOrigin);

          // maxPoints limit — keep original behavior
          if (
            this.options.maxPoints > 1 &&
            this.options.maxPoints == this._markers.length + 1
          ) {
            this.addVertex(e.latlng);
            this._finishShape();
          }
          // REMOVED: the `lastPtDistance < 10 && L.Browser.touch` branch
          // that silently called _finishShape() on "touch" devices.
          else if (
            Math.abs(dragCheckDistance) < 9 * (window.devicePixelRatio || 1)
          ) {
            this.addVertex(e.latlng);
          }
          this._enableNewMarkers();
        }
        this._mouseDownOrigin = null;
      };

      L.Draw.Polygon.prototype._updateFinishHandler = function () {
        var markerCount = this._markers.length;
        // First vertex click → close the polygon (standard)
        if (markerCount === 1) {
          this._markers[0].on("click", this._finishShape, this);
        }
        // Do NOT bind dblclick on the last marker
      };

      setupDrawMode();
    }).catch((err) => {
      drawLoading.value = false;
      console.error("Erro ao carregar ferramentas de desenho:", err);
    });
  }
}

function setupDrawMode() {
  drawnItems = new L.FeatureGroup();
  map.addLayer(drawnItems);

  if (typeof L.Control.Draw === "undefined") {
    console.error("L.Control.Draw nao disponivel");
    return;
  }

  const drawControl = new L.Control.Draw({
    position: "topright",
    draw: {
      polyline: false,
      circle: false,
      circlemarker: false,
      marker: false,
      polygon: {
        allowIntersection: true,
        showArea: true,
        shapeOptions: {
          color: "#2e7d32",
          weight: 3,
          fillColor: "#4caf50",
          fillOpacity: 0.15,
        },
      },
      rectangle: {
        showArea: true,
        shapeOptions: {
          color: "#2e7d32",
          weight: 3,
          fillColor: "#4caf50",
          fillOpacity: 0.15,
        },
      },
    },
    edit: {
      featureGroup: drawnItems,
      remove: true,
    },
  });

  map.addControl(drawControl);

  map.on(L.Draw.Event.CREATED, function (e) {
    drawnItems.clearLayers();
    drawnItems.addLayer(e.layer);

    try {
      const latlngs = e.layer.getLatLngs();
      const coords = Array.isArray(latlngs[0]) ? latlngs[0] : latlngs;
      const area = L.GeometryUtil.geodesicArea(coords);
      drawnAreaSize.value = area / 10000;
    } catch (err) {
      drawnAreaSize.value = 0;
    }

    hasDrawnArea.value = true;

    // Zoom to highlight the drawn area with a smooth animation
    try {
      map.flyToBounds(e.layer.getBounds(), {
        padding: [60, 60],
        maxZoom: 16,
        duration: 0.8,
      });
    } catch (err) {
      /* ignore */
    }

    emit("area-drawn", e.layer.toGeoJSON());
  });

  map.on(L.Draw.Event.EDITED, function (e) {
    e.layers.eachLayer(function (layer) {
      try {
        const latlngs = layer.getLatLngs();
        const coords = Array.isArray(latlngs[0]) ? latlngs[0] : latlngs;
        const area = L.GeometryUtil.geodesicArea(coords);
        drawnAreaSize.value = area / 10000;
        emit("area-drawn", layer.toGeoJSON());
      } catch (err) {
        /* ignore */
      }
    });
  });

  map.on(L.Draw.Event.DELETED, function () {
    hasDrawnArea.value = false;
    drawnAreaSize.value = 0;
    emit("area-drawn", null);
  });

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (pos) => map.setView([pos.coords.latitude, pos.coords.longitude], 12),
      () => map.setView([-16.68, -49.25], 10)
    );
  }
}

function setupDisplayMode() {
  if (props.aoi) {
    const aoiLayer = L.geoJSON(props.aoi, {
      style: {
        color: "#ef5350",
        weight: 3,
        fillOpacity: 0.08,
        dashArray: "8, 4",
      },
    }).addTo(map);

    // Fallback: ensure bounds are applied after the browser has laid out the
    // container (initMap fitBounds can silently fail if container has 0 size).
    setTimeout(() => {
      map.invalidateSize();
      map.fitBounds(aoiLayer.getBounds(), { padding: [50, 50], maxZoom: 17 });
    }, 300);
  } else {
    console.warn("[MapComponent] display mode sem aoi_geojson — backend retornou sem esse campo?");
  }

  if (props.layers.ndvi_url) {
    activeFilter.value = "ndvi";
    setTimeout(() => applyFilter("ndvi"), 400);
  }
}

function clearDrawnArea() {
  if (drawnItems) {
    drawnItems.clearLayers();
    hasDrawnArea.value = false;
    drawnAreaSize.value = 0;
    emit("area-drawn", null);
  }
}
</script>

<style scoped>
/* === MOBILE-FIRST === */

.map-wrapper {
  position: relative;
  border-radius: 10px;
  overflow: hidden;
}

#map-container {
  height: 350px;
  width: 100%;
}

.map-instructions {
  position: absolute;
  top: 8px;
  left: 8px;
  right: 60px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  padding: 10px 12px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  font-size: 12px;
  line-height: 1.4;
  border: 1px solid rgba(46, 125, 50, 0.15);
}

.instructions-header {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 6px;
  color: #2e7d32;
  font-size: 13px;
}

.map-instructions ol {
  margin: 0;
  padding-left: 16px;
}

.map-instructions li {
  margin: 3px 0;
  color: #555;
}

.mini-spinner {
  width: 18px;
  height: 18px;
  border: 2px solid #e0e0e0;
  border-top-color: #2e7d32;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.area-info {
  position: absolute;
  top: 8px;
  left: 8px;
  right: 8px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  padding: 8px 14px;
  border-radius: 20px;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(46, 125, 50, 0.2);
}

.area-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #2e7d32;
  font-size: 13px;
}

.btn-clear {
  background: none;
  border: 1px solid #e0e0e0;
  color: #666;
  padding: 4px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 11px;
  transition: all 0.2s;
}

.btn-clear:hover {
  background: #ffebee;
  border-color: #ef5350;
  color: #c62828;
}

.filter-controls {
  position: absolute;
  bottom: 8px;
  left: 8px;
  right: 8px;
  color: #333;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  padding: 12px;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.12);
  z-index: 1000;
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.filter-controls h4 {
  margin: 0 0 8px;
  font-size: 11px;
  color: #333;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.filter-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.filter-btn {
  padding: 6px 10px;
  border: 1px solid #e8e8e8;
  background: white;
  color: #333;
  border-radius: 6px;
  cursor: pointer;
  text-align: left;
  font-size: 12px;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.2s;
}

.filter-btn:hover {
  background: #f5f5f5;
  border-color: #ccc;
}

.filter-btn.active {
  background: #e8f5e9;
  border-color: #2e7d32;
  color: #1b5e20;
  font-weight: 500;
}

.filter-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.opacity-control {
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid #eee;
}

.opacity-control label {
  display: block;
  font-size: 10px;
  color: #888;
  margin-bottom: 4px;
}

.opacity-control input[type="range"] {
  width: 100%;
  height: 4px;
  -webkit-appearance: none;
  appearance: none;
  background: #e0e0e0;
  border-radius: 2px;
  outline: none;
}

.opacity-control input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #2e7d32;
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
}

.map-legend {
  position: absolute;
  top: 8px;
  right: 8px;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(8px);
  padding: 8px 10px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.map-legend h4 {
  margin: 0 0 6px;
  font-size: 10px;
  color: #333;
  font-weight: 600;
}

.legend-items {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  color: #555;
}

.legend-color {
  width: 16px;
  height: 8px;
  border-radius: 2px;
  flex-shrink: 0;
}

/* === DESKTOP === */
@media (min-width: 768px) {
  .map-wrapper {
    border-radius: 12px;
  }

  #map-container {
    height: 600px;
  }

  .map-instructions {
    top: 12px;
    left: 12px;
    right: auto;
    max-width: 260px;
    padding: 14px 16px;
    border-radius: 10px;
    font-size: 13px;
  }

  .area-info {
    top: 12px;
    left: 50%;
    right: auto;
    transform: translateX(-50%);
    padding: 10px 18px;
    border-radius: 24px;
    gap: 14px;
  }

  .area-badge {
    font-size: 14px;
  }

  .btn-clear {
    font-size: 12px;
    padding: 4px 12px;
  }

  .filter-controls {
    top: 12px;
    left: 12px;
    right: auto;
    bottom: auto;
    min-width: 170px;
    padding: 16px;
    border-radius: 12px;
  }

  .filter-controls h4 {
    font-size: 13px;
    margin-bottom: 12px;
  }

  .filter-buttons {
    flex-direction: column;
    flex-wrap: nowrap;
  }

  .filter-btn {
    padding: 8px 12px;
    font-size: 13px;
    border-radius: 8px;
    gap: 8px;
  }

  .filter-dot {
    width: 10px;
    height: 10px;
  }

  .opacity-control {
    margin-top: 12px;
    padding-top: 12px;
  }

  .opacity-control label {
    font-size: 11px;
    margin-bottom: 6px;
  }

  .opacity-control input[type="range"]::-webkit-slider-thumb {
    width: 16px;
    height: 16px;
  }

  .map-legend {
    top: auto;
    right: auto;
    bottom: 30px;
    left: 12px;
    padding: 12px 14px;
    border-radius: 10px;
  }

  .map-legend h4 {
    font-size: 12px;
    margin-bottom: 8px;
  }

  .legend-items {
    gap: 4px;
  }

  .legend-item {
    font-size: 11px;
    gap: 8px;
  }

  .legend-color {
    width: 20px;
    height: 10px;
  }
}
</style>

<!-- Non-scoped styles for Leaflet Draw toolbar icons -->
<style>
.leaflet-draw-toolbar a {
  background-image: url("https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/images/spritesheet.png") !important;
  background-color: #fff !important;
  background-size: 300px 30px;
  border-radius: 4px;
}

.leaflet-retina .leaflet-draw-toolbar a {
  background-image: url("https://cdnjs.cloudflare.com/ajax/libs/leaflet.draw/1.0.4/images/spritesheet-2x.png") !important;
  background-size: 300px 30px;
}

.leaflet-draw-toolbar {
  margin-top: 12px !important;
}

.leaflet-draw-actions a {
  background-image: none !important;
  color: #fff;
}

.leaflet-draw-actions {
  background: #555;
  border-radius: 4px;
}

.leaflet-draw-tooltip {
  background: rgba(0, 0, 0, 0.75);
  border: none;
  border-radius: 6px;
  color: white;
  font-size: 12px;
  padding: 6px 10px;
}
</style>
