<template>
  <div
    id="map-container"
    style="height: 500px; width: 100%; border-radius: 8px; margin-top: 20px"
  ></div>
</template>

<script setup>
import { onMounted, watch } from "vue";
import "leaflet/dist/leaflet.css";
import "leaflet-draw/dist/leaflet.draw.css";
import L from "leaflet";
import "leaflet-draw";

const props = defineProps({
  isDisplayMode: { type: Boolean, default: false },
  layers: { type: Object, default: () => ({}) },
  aoi: { type: Object, default: null },
});

const emit = defineEmits(["area-drawn"]);

let map;

onMounted(() => {
  map = L.map("map-container").setView([-16.35, -49.44], 13);
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap",
  }).addTo(map);

  if (props.isDisplayMode) {
    setupDisplayMode();
  } else {
    setupDrawMode();
  }
});

function setupDrawMode() {
  const drawnItems = new L.FeatureGroup();
  map.addLayer(drawnItems);
  const drawControl = new L.Control.Draw({
    edit: { featureGroup: drawnItems },
    draw: {
      polygon: true,
      polyline: false,
      rectangle: false,
      circle: false,
      marker: false,
      circlemarker: false,
    },
  });
  map.addControl(drawControl);

  map.on(L.Draw.Event.CREATED, (event) => {
    const layer = event.layer;
    drawnItems.clearLayers();
    drawnItems.addLayer(layer);
    emit("area-drawn", layer.toGeoJSON());
  });
}

function setupDisplayMode() {
  if (props.aoi) {
    const aoiLayer = L.geoJSON(props.aoi, {
      style: { color: "#ff7800", weight: 3, opacity: 0.8, fillOpacity: 0.1 },
    }).addTo(map);
    map.fitBounds(aoiLayer.getBounds());
  }

  const layerControl = L.control.layers().addTo(map);

  if (props.layers.rgb_url) {
    const rgbLayer = L.tileLayer(props.layers.rgb_url, {
      attribution: "Sentinel-2",
    });
    layerControl.addBaseLayer(rgbLayer, "Satélite (RGB)");
    rgbLayer.addTo(map);
  }

  const overlayLayers = {
    NDVI: props.layers.ndvi_url,
    Degradação: props.layers.degradation_url,
    NDMI: props.layers.ndmi_url,
    SAVI: props.layers.savi_url,
    Declividade: props.layers.slope_url,
    MapBiomas: props.layers.mapbiomas_url,
  };

  for (const [name, url] of Object.entries(overlayLayers)) {
    if (url) {
      layerControl.addOverlay(
        L.tileLayer(url, { attribution: "CultiveAI" }),
        name
      );
    }
  }
}
</script>
