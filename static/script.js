// ====================
// Wait for DOM to load
// ====================
document.addEventListener("DOMContentLoaded", () => {
    // Grab filter elements
    const magSlider = document.getElementById("mag-range");
    const depthSlider = document.getElementById("depth-range");
    const timeRange = document.getElementById("time-range");

    const magOutput = document.getElementById("mag-value");
    const depthOutput = document.getElementById("depth-value");
    const timeOutput = document.getElementById("time-value");

    // Update displayed values initially
    magOutput.innerText = magSlider.value;
    depthOutput.innerText = depthSlider.value;
    timeOutput.innerText = timeRange.value;

    // Initialize map once
    const map = L.map('map', {
        worldCopyJump: false,
        maxBounds: [
            [-90, -180],
            [90, 180]
        ],
        maxBoundsViscosity: 1.0
    }).setView([-41.5, 174], 5);

    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

    // Layer for earthquake markers
    const quakeLayer = L.layerGroup().addTo(map);

    // ====================
    // Depth color function
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
    // Load earthquakes
    // ====================
    async function loadEarthquakes() {
        const minMag = magSlider.value;
        const maxDepth = depthSlider.value;
        const numHours = timeRange.value;

        quakeLayer.clearLayers();

        const url = `/api/earthquakes?min_magnitude=${minMag}&max_depth=${maxDepth}&time_range_hours=${numHours}`;
        try {
            const response = await fetch(url);
            const quakes = await response.json();

            quakes.forEach(eq => {
                const circle = L.circleMarker([eq.lat, eq.lon], {
                    radius: Math.max(eq.depth / 10, 4),
                    fillColor: getDepthColor(eq.depth),
                    color: "#00000040",
                    weight: 1,
                    fillOpacity: 0.8
                }).addTo(quakeLayer);

                circle.bindPopup(
                    `<b>${eq.locality}</b><br>
                     Mag: ${eq.magnitude.toFixed(2)}<br>
                     Depth: ${eq.depth.toFixed(1)} km<br>
                     Time: ${eq.time}`
                );
            });
        } catch (err) {
            console.error("Failed to load earthquakes:", err);
        }
    }

    // ====================
    // Update summary stats
    // ====================
    async function updateSummary() {
        const minMag = magSlider.value;
        const maxDepth = depthSlider.value;
        const numHours = timeRange.value;

        const url = `/api/summary?min_magnitude=${minMag}&max_depth=${maxDepth}&time_range_hours=${numHours}`;
        try {
            const response = await fetch(url);
            const stats = await response.json();

            document.querySelector("#total-quakes-value").innerText = stats.total || 0;
            document.querySelector("#largest-mag-value").innerText = stats.largest ? stats.largest.toFixed(1) : "—";
            document.querySelector("#most-recent-value").innerText = stats.most_recent
                ? `${stats.most_recent[0]} (${stats.most_recent[1]})`
                : "—";
        } catch (err) {
            console.error("Failed to load summary:", err);
        }
    }

    // ====================
    // Refresh dashboard
    // ====================
    async function refreshDashboard() {
        magOutput.innerText = magSlider.value;
        depthOutput.innerText = depthSlider.value;
        timeOutput.innerText = timeRange.value;

        await loadEarthquakes();
        await updateSummary();
        // Add chart update calls if needed:
        // updateTable();
        // updateChart();
    }

    // ====================
    // Event listeners
    // ====================
    magSlider.addEventListener("input", refreshDashboard);
    depthSlider.addEventListener("input", refreshDashboard);
    timeRange.addEventListener("change", refreshDashboard);

    // Initial load
    refreshDashboard();
    console.log("✅ Dashboard JS loaded");
});
