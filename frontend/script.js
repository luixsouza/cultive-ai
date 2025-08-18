let map;
let drawnItems;
let selectedPolygon;
const geeLayers = []; 
let activeLayerControl = null;
let overlayLayers = {};
const API_URL = 'http://127.0.0.1:8000/analyze';

const analyzeBtn = document.getElementById('analyzeBtn');
const loader = document.getElementById('loader');
const resultsContainer = document.getElementById('results-container');
const tabButtonsContainer = document.querySelector('.tab-buttons');
const tabContentContainer = document.querySelector('.tab-content');

const esriSatellite = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: 'Tiles &copy; Esri'
});
const cartoDB_Positron = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
});
const baseMaps = { "Satélite": esriSatellite, "Minimalista": cartoDB_Positron };

map = L.map('map', { center: [-16.357, -49.495], zoom: 13, layers: [esriSatellite] });

drawnItems = new L.FeatureGroup();
map.addLayer(drawnItems);
map.addControl(new L.Control.Draw({
    edit: { featureGroup: drawnItems },
    draw: { polygon: { shapeOptions: { color: '#00aaff' } }, polyline: false, rectangle: false, circle: false, marker: false, circlemarker: false }
}));

const icons = {
    summary: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20V10M18 20V4M6 20V16"></path></svg>`,
    ai: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 8V4H8"></path><rect x="4" y="12" width="16" height="8"></rect><path d="M4 12v-2a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>`,
    layer: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline></svg>`
};

const legendData = {
    'Classificação de Degradação': { title: 'Saúde da Pastagem', colors: ['#a50026', '#d73027', '#fdae61', '#66bd63', '#1a9641'], labels: ['Severa', 'Moderada', 'Estressada', 'Boa', 'Excelente'] },
    'Índice NDVI (Vigor)': { title: 'Vigor (NDVI)', colors: ['#d73027', '#fee08b', '#91cf60', '#1a9850'], labels: ['Baixo', '', '', 'Alto'] },
    'Índice NDMI (Umidade)': { title: 'Umidade (NDMI)', colors: ['#a50026', '#ffffbf', '#74add1', '#313695'], labels: ['Muito Seco', '', '', 'Muito Úmido'] },
    'Índice SAVI (Solo Exposto)': { title: 'Índice SAVI', colors: ['#a50026', '#fee08b', '#a6d96a', '#1a9850'], labels: ['Solo Exposto', '', '', 'Vegetação Densa'] },
    'Declividade do Terreno': { title: 'Declividade', colors: ['#33a02c', '#fdbf6f', '#e31a1c'], labels: ['Plano', 'Médio', 'Íngreme'] }
};

function openTab(tabId) {
    document.querySelectorAll('.tab-pane').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab-button').forEach(button => button.classList.remove('active'));
    
    const tabPane = document.getElementById(tabId + '-tab');
    const tabButton = document.getElementById(tabId + '-button');
    if (tabPane) tabPane.classList.add('active');
    if (tabButton) tabButton.classList.add('active');

    for (const layerName in overlayLayers) {
        if (map.hasLayer(overlayLayers[layerName])) {
            map.removeLayer(overlayLayers[layerName]);
        }
    }
    if (overlayLayers[tabId]) {
        map.addLayer(overlayLayers[tabId]);
    }
}

map.on(L.Draw.Event.CREATED, (e) => { drawnItems.clearLayers(); drawnItems.addLayer(e.layer); selectedPolygon = e.layer; analyzeBtn.disabled = false; });
map.on('draw:deleted', () => { selectedPolygon = null; analyzeBtn.disabled = true; clearPreviousAnalysis(); });

analyzeBtn.addEventListener('click', async () => {
    if (!selectedPolygon) return alert('Por favor, desenhe uma área no mapa primeiro.');
    clearPreviousAnalysis();
    loader.classList.remove('hidden');
    try {
        const response = await fetch(API_URL, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type: "FeatureCollection", features: [selectedPolygon.toGeoJSON()] }),
        });
        if (!response.ok) throw new Error((await response.json()).detail || 'Erro na API');
        const data = await response.json();
        displayResults(data);
        overlayGeeLayers(data.map_layers);
    } catch (error) {
        alert(`Falha na análise: ${error.message}`);
    } finally {
        loader.classList.add('hidden');
    }
});

function displayResults(data) {
    tabButtonsContainer.innerHTML = `
        <button id="summary-button" class="tab-button" onclick="openTab('summary')">${icons.summary} Resumo</button>
        <button id="ai-button" class="tab-button" onclick="openTab('ai')">${icons.ai} Análise IA</button>
    `;
    tabContentContainer.innerHTML = `
        <div id="summary-tab" class="tab-pane"></div>
        <div id="ai-tab" class="tab-pane"></div>
    `;

    document.getElementById('summary-tab').innerHTML = `
        <h4>Informações Gerais</h4>
        <ul>
            <li><strong>Período:</strong> ${data.analysis_period.start_date} a ${data.analysis_period.end_date}</li>
            <li><strong>Área Total:</strong> ${data.aoi_area_hectares.toFixed(2)} ha</li>
        </ul>
        <h4>Distribuição da Área</h4><ul>${data.degradation_summary.map(item => 
            `<li><strong>${item.class_name}:</strong> ${item.percentage.toFixed(1)}% (${item.area_hectares.toFixed(2)} ha)</li>`
        ).join('')}</ul>`;
    
    document.getElementById('ai-tab').innerHTML = `<h4>Análise da Inteligência Artificial</h4><p>${data.ai_description.replace(/\n/g, '<br>')}</p>`;

    resultsContainer.classList.remove('hidden');
    openTab('summary');
}

function overlayGeeLayers(layerUrls) {
    const layerConfigs = [
        { name: 'Classificação de Degradação', url: layerUrls.degradation_url, default: true },
        { name: 'Índice NDVI (Vigor)', url: layerUrls.ndvi_url },
        { name: 'Índice NDMI (Umidade)', url: layerUrls.ndmi_url },
        { name: 'Índice SAVI (Solo Exposto)', url: layerUrls.savi_url },
        { name: 'Declividade do Terreno', url: layerUrls.slope_url },
    ];

    layerConfigs.forEach(config => {
        if (config.url) {
            const geeLayer = L.tileLayer(config.url, { opacity: 0.75 });
            overlayLayers[config.name] = geeLayer;

            if (config.default) geeLayer.addTo(map);

            tabButtonsContainer.innerHTML += `<button id="${config.name}-button" class="tab-button" onclick="openTab('${config.name}')">${icons.layer} ${config.name}</button>`;
            
            const legendInfo = legendData[config.name];
            let legendHTML = '<h4>Legenda</h4>';
            if (legendInfo) {
                legendHTML += legendInfo.labels.map((label, index) => `
                    <div class="legend-item">
                        <span class="legend-color" style="background:${legendInfo.colors[index]}"></span>
                        ${label}
                    </div>
                `).join('');
            }
            tabContentContainer.innerHTML += `<div id="${config.name}-tab" class="tab-pane">${legendHTML}</div>`;
        }
    });

    map.on('baselayerchange', (e) => { });
    map.on('overlayadd', (e) => { openTab(e.name); });
}

function clearPreviousAnalysis() {
    resultsContainer.classList.add('hidden');
    tabButtonsContainer.innerHTML = '';
    tabContentContainer.innerHTML = '';
    
    for (const layerName in overlayLayers) {
        if (map.hasLayer(overlayLayers[layerName])) {
            map.removeLayer(overlayLayers[layerName]);
        }
    }
    overlayLayers = {};
}