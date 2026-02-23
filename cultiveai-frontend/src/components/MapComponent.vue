<template>
  <div class="relative rounded-xl md:rounded-2xl overflow-hidden isolate">
    <!-- Instructions for drawing mode -->
    <div
      v-if="!isDisplayMode && !hasDrawnArea && !drawLoading"
      class="absolute top-[72px] left-2 right-[60px] md:top-3 md:left-[52px] md:right-auto md:max-w-[260px] bg-white/95 backdrop-blur-md p-2.5 md:p-3.5 rounded-lg md:rounded-xl shadow-md z-[1000] text-xs md:text-[13px] leading-snug border border-primary/15"
    >
      <div class="flex items-center gap-1.5 mb-1.5 text-primary text-[13px] font-semibold">
        <span class="material-icons-round text-base">pin_drop</span>
        Como mapear a area
      </div>
      <ol class="m-0 pl-4 text-slate-500 space-y-0.5">
        <li>Use os botoes na barra de ferramentas acima</li>
        <li><b class="text-slate-700">Poligono:</b> clique nos vertices e finalize no primeiro ponto</li>
        <li><b class="text-slate-700">Retangulo:</b> clique e arraste para selecionar</li>
      </ol>
    </div>

    <!-- Loading draw tools -->
    <div
      v-if="drawLoading"
      class="absolute top-[72px] left-2 right-[60px] md:top-3 md:left-[52px] md:right-auto md:max-w-[260px] bg-white/95 backdrop-blur-md p-2.5 md:p-3.5 rounded-lg md:rounded-xl shadow-md z-[1000] text-xs md:text-[13px] border border-primary/15"
    >
      <div class="flex items-center gap-1.5 text-primary font-semibold">
        <div class="w-[18px] h-[18px] border-2 border-slate-200 border-t-primary rounded-full animate-spin"></div>
        Carregando ferramentas...
      </div>
    </div>

    <!-- Area info badge -->
    <div
      v-if="!isDisplayMode && hasDrawnArea"
      class="absolute top-2 left-2 right-2 md:top-3 md:left-1/2 md:right-auto md:-translate-x-1/2 bg-white/95 backdrop-blur-md px-3.5 md:px-4.5 py-2 md:py-2.5 rounded-full z-[1000] flex items-center justify-center gap-2.5 md:gap-3.5 shadow-md border border-primary/20"
    >
      <span class="flex items-center gap-1.5 text-primary text-[13px] md:text-sm">
        <span class="material-icons-round text-base">place</span>
        <strong>{{ drawnAreaHectares }} ha</strong> selecionados
      </span>
      <button
        @click="clearDrawnArea"
        class="bg-transparent border border-slate-200 text-slate-500 px-2.5 md:px-3 py-1 rounded-md text-[11px] md:text-xs cursor-pointer hover:bg-danger-bg hover:border-danger hover:text-red-700 transition-colors"
      >
        Limpar area
      </button>
    </div>

    <!-- Map container -->
    <div id="map-container" ref="mapContainer" class="h-[350px] md:h-[600px] w-full"></div>

    <!-- Filter controls for display mode -->
    <div
      v-if="isDisplayMode"
      class="absolute bottom-2 left-2 right-2 md:top-3 md:left-3 md:right-auto md:bottom-auto md:min-w-[170px] bg-white/95 backdrop-blur-md p-3 md:p-4 rounded-xl shadow-md z-[1000] border border-black/[.06]"
    >
      <h4 class="m-0 mb-2 md:mb-3 text-[11px] md:text-[13px] text-slate-700 uppercase tracking-wide font-semibold">Camadas de Analise</h4>
      <div class="flex flex-wrap md:flex-col gap-1">
        <button
          v-for="filter in availableFilters"
          :key="filter.key"
          :class="[
            'px-2.5 md:px-3 py-1.5 md:py-2 border rounded-md md:rounded-lg cursor-pointer text-left text-xs md:text-[13px] flex items-center gap-1.5 md:gap-2 transition-all',
            activeFilter === filter.key
              ? 'bg-primary-bg border-primary text-primary-dark font-medium'
              : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50 hover:border-slate-300'
          ]"
          @click="toggleFilter(filter.key)"
        >
          <span class="w-2 h-2 md:w-2.5 md:h-2.5 rounded-full shrink-0" :style="{ background: getFilterColor(filter.key) }"></span>
          {{ filter.name }}
        </button>
      </div>
      <div v-if="activeFilter" class="mt-2 md:mt-3 pt-2 md:pt-3 border-t border-slate-200">
        <label class="block text-[10px] md:text-[11px] text-slate-400 mb-1 md:mb-1.5">Opacidade: {{ Math.round(filterOpacity * 100) }}%</label>
        <input
          type="range"
          min="0"
          max="100"
          :value="filterOpacity * 100"
          @input="updateOpacity($event.target.value / 100)"
          class="opacity-slider w-full"
        />
      </div>
    </div>

    <!-- Legend -->
    <div
      v-if="isDisplayMode && activeFilter && getLegendItems().length > 0"
      class="absolute top-2 right-2 md:top-auto md:right-auto md:bottom-8 md:left-3 bg-white/95 backdrop-blur-md p-2 md:p-3 rounded-lg md:rounded-xl shadow-md z-[1000] border border-black/[.06]"
    >
      <h4 class="m-0 mb-1.5 md:mb-2 text-[10px] md:text-xs text-slate-700 font-semibold">{{ getLegendTitle() }}</h4>
      <div class="flex flex-col gap-0.5 md:gap-1">
        <div v-for="item in getLegendItems()" :key="item.label" class="flex items-center gap-1.5 md:gap-2 text-[10px] md:text-[11px] text-slate-500">
          <span class="w-4 md:w-5 h-2 md:h-2.5 rounded-sm shrink-0" :style="{ background: item.color }"></span>
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
/* Opacity slider - needs custom styling that Tailwind can't handle */
.opacity-slider {
  height: 4px;
  -webkit-appearance: none;
  appearance: none;
  background: #e0e0e0;
  border-radius: 2px;
  outline: none;
}

.opacity-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #2e7d32;
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
}

@media (min-width: 768px) {
  .opacity-slider::-webkit-slider-thumb {
    width: 16px;
    height: 16px;
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
