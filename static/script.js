// ====================
// Initialise map
// ====================
const map = L.map("map").setView([-40.9, 174.9], 5);

L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 19,
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
}).addTo(map);

// ====================
// Grab filter elements
// ====================
const magSlider = document.getElementById("mag-range");
const magOutput = document.getElementById("mag-value");

const depthSlider = document.getElementById("depth-range");
const depthOutput = document.getElementById("depth-value");

const timeRange = document.getElementById("time-range");
const timeOutput = document.getElementById("time-value");

// Show starting values
magOutput.innerText = magSlider.value;
depthOutput.innerText = depthSlider.value;
timeOutput.innerText = timeRange.value;

// Update values when sliders move
magSlider.oninput = function () {
  magOutput.innerText = this.value;
  loadEarthquakes();
};

depthSlider.oninput = function () {
  depthOutput.innerText = this.value;
  loadEarthquakes();
};

timeRange.oninput = function () {
  timeOutput.innerText = this.value;
  loadEarthquakes();
};

// ====================
// Set Depth colours
// ====================
function getDepthColor(depth) {
  return depth > 70
    ? "#d73027"
    : depth > 40
    ? "#fc8d59"
    : depth > 20
    ? "#fee08b"
    : "#91cf60";
}
// ====================
// Setup Earthquake Layer
// ====================
let quakeLayer = L.layerGroup().addTo(map);

// Fetch and draw earthquakes
async function loadEarthquakes(
  minMag = magSlider.value,
  maxDepth = depthSlider.value,
  numHours = timeRange.value
) {
  // Clear old markers
  quakeLayer.clearLayers();

  const url = `/api/earthquakes?min_magnitude=${minMag}&max_depth=${maxDepth}&time_range_hours=${numHours}`;
  console.log("Fetching:", url);

  const response = await fetch(url);
  const quakes = await response.json();

  quakes.forEach((eq) => {
    const circle = L.circleMarker([eq.lat, eq.lon], {
      radius: eq.magnitude * 2,
      fillColor: getDepthColor(eq.depth),
      color: "#000",
      weight: 1,
      opacity: 1,
      fillOpacity: 0.7,
    }).addTo(quakeLayer);

    circle.bindPopup(
      `<b>${eq.locality}</b><br>
       Mag: ${eq.magnitude.toFixed(2)}<br>
       Depth: ${eq.depth.toFixed(1)} km<br>
       Time: ${eq.time}`
    );
  });
}


// ====================
// Fetch and Update Stats
// ====================
async function updateSummary(
  minMag = magSlider.value, 
  maxDepth = depthSlider.value, 
  numHours = timeRange.value) {
  const url = `/api/summary?min_magnitude=${minMag}&max_depth=${maxDepth}&time_range_hours=${numHours}`;
  const response = await fetch(url);
  const stats = await response.json();

  document.querySelector("#total-quakes-value").innerText = stats.total || 0;
  document.querySelector("#largest-mag-value").innerText = stats.largest ? stats.largest.toFixed(1) : "—";
  document.querySelector("#most-recent-value").innerText = stats.most_recent ? 
    `${stats.most_recent[0]} (${stats.most_recent[1]})` : "—";
}

// ====================
// Update Table
// ====================

async function updateTable(
  minMag = magSlider.value, 
  maxDepth = depthSlider.value, 
  numHours = timeRange.value
) {
  const url = `/api/earthquakes?min_magnitude=${minMag}&max_depth=${maxDepth}&time_range_hours=${numHours}`;
  const response = await fetch(url);
  const quakes = await response.json();

  const tbody = document.querySelector("#quake-table tbody");
  tbody.innerHTML = ""; // clear previous rows

  quakes.forEach((eq, index) => {
    const tr = document.createElement("tr");
    tr.dataset.rownum = index + 1;

    // Create table cells
    const tdNum = document.createElement("td");
    tdNum.innerText = index + 1;
    const tdMag = document.createElement("td");
    tdMag.innerText = eq.magnitude.toFixed(2);
    const tdDepth = document.createElement("td");
    tdDepth.innerText = eq.depth.toFixed(1);
    const tdTime = document.createElement("td");
    tdTime.innerText = eq.time;
    const tdLocality = document.createElement("td");
    tdLocality.innerText = eq.locality;

    // Append all cells to row
    tr.append(tdNum, tdMag, tdDepth, tdTime, tdLocality);

    // Append row to table body
    tbody.appendChild(tr);
  });
}

// ====================
// Load data
// ====================
loadEarthquakes();
updateSummary();
updateTable();

// ====================
// Update when filters move
// ====================
magSlider.oninput = function () {
  magOutput.innerText = this.value;
  loadEarthquakes();
  updateSummary();
  updateTable();
};

depthSlider.oninput = function () {
  depthOutput.innerText = this.value;
  loadEarthquakes();
  updateSummary();
  updateTable();
};

timeRange.oninput = function () {
  timeOutput.innerText = this.value;
  loadEarthquakes();
  updateSummary();
  updateTable();
};

console.log("✅ JS file loaded");
