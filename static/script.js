// Initialise Map
const map = L.map('map', {
    worldCopyJump: false,
    maxBounds: [[-90, -180],[90,180]],
    maxBoundsViscosity: 1.0
}).setView([-41.5, 174], 5);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{
    maxZoom: 19,
    attribution:'&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

let quakeLayer = L.layerGroup().addTo(map);

// Filters
const magSlider = document.getElementById("mag-range");
const depthSlider = document.getElementById("depth-range");
const timeRange = document.getElementById("time-range");

const magOutput = document.getElementById("mag-value");
const depthOutput = document.getElementById("depth-value");
const timeOutput = document.getElementById("time-value");

// Key
function getDepthColor(depth){
    return depth > 70 ? "#d73027" :
           depth > 40 ? "#fc8d59" :
           depth > 20 ? "#fee08b" :
           "#91cf60";
}

//  Load Earthquake Data
async function loadEarthquakes(minMag=magSlider.value, maxDepth=depthSlider.value, numHours=timeRange.value){
    quakeLayer.clearLayers();
    const url = `/api/earthquakes?min_magnitude=${minMag}&max_depth=${maxDepth}&time_range_hours=${numHours}`;
    const res = await fetch(url);
    const quakes = await res.json();

    quakes.forEach(eq=>{
        const circle = L.circleMarker([eq.lat, eq.lon],{
            radius: Math.max(eq.depth/10, 4),
            fillColor: getDepthColor(eq.depth),
            color:"#00000040",
            weight:1,
            fillOpacity:0.8
        }).addTo(quakeLayer);

        circle.bindPopup(`<b>${eq.locality}</b><br>
            Mag: ${eq.magnitude.toFixed(2)}<br>
            Depth: ${eq.depth.toFixed(1)} km<br>
            Time: ${eq.time}`);
    });

    return quakes;
}

// ===== Update Summary =====
async function updateSummary(minMag=magSlider.value, maxDepth=depthSlider.value, numHours=timeRange.value){
    const url = `/api/summary?min_magnitude=${minMag}&max_depth=${maxDepth}&time_range_hours=${numHours}`;
    const res = await fetch(url);
    const stats = await res.json();

    document.getElementById("total-quakes-value").innerText = stats.total || 0;
    document.getElementById("largest-mag-value").innerText = stats.largest ? stats.largest.toFixed(1) : "—";

    document.getElementById("most-recent-location").innerText = stats.most_recent ? stats.most_recent[0] : "—";
    document.getElementById("most-recent-time").innerText = stats.most_recent ? stats.most_recent[1] : "—";
    document.getElementById("most-recent-mag").innerText = stats.most_recent ? stats.most_recent[2].toFixed(1) : "—";
}

// ===== Udate Charts =====
let lineChart = new Chart(document.getElementById("lineChart"), {type:"line", data:{labels:[], datasets:[{label:"Earthquakes", data:[], borderWidth:2, fill:false}]}});
let barChart = new Chart(document.getElementById("barChart"), {type:"bar", data:{labels:["M3-3.9","M4-4.9","M5-5.9","M6-6.9","M7+"], datasets:[{label:"Count", data:[0,0,0,0,0], borderWidth:1}]}});
let horizontalChart = new Chart(document.getElementById("horizontalChart"), {type:"bar", data:{labels:[], datasets:[{label:"Magnitude", data:[], borderWidth:1}]} , options:{indexAxis:"y"}});

async function updateCharts(){
    const url = `/api/charts?min_magnitude=${magSlider.value}&max_depth=${depthSlider.value}&time_range_hours=${timeRange.value}`;
    const res = await fetch(url);
    const data = await res.json();

    // Line chart
    lineChart.data.labels = data.time_labels;
    lineChart.data.datasets[0].data = data.time_values;
    lineChart.update();

    // Bar chart
    barChart.data.datasets[0].data = data.magnitude_counts;
    barChart.update();

    // Horizontal chart
    horizontalChart.data.labels = data.top_countries;
    horizontalChart.data.datasets[0].data = data.top_mags;
    horizontalChart.update();
}

// ===== HANDLER =====
async function refreshDashboard(){
    await loadEarthquakes();
    await updateSummary();
    await updateCharts();
}

// ===== EVENTS =====
magSlider.oninput = refreshDashboard;
depthSlider.oninput = refreshDashboard;
timeRange.onchange = refreshDashboard;

// ===== INITIAL LOAD =====
refreshDashboard();
console.log("✅ Dashboard loaded");
