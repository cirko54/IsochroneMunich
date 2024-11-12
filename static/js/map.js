document.addEventListener("DOMContentLoaded", function() {
    // Initialisieren der Karte und Zentrierung auf München
    // Initialize map with custom zoom control positioning
const map = L.map('map', {
    zoomControl: true
}).setView([48.1351, 11.5820], 10);

// Adjust CSS if necessary to ensure map controls aren’t obscured

    // Hinzufügen von OpenStreetMap-Tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Separate Layer für Marker-Clustering und Isochronen
    var markerClusterGroup = L.markerClusterGroup();
    var isochroneLayer = L.layerGroup();  // Separater Layer für Isochronen
    map.addLayer(markerClusterGroup);
    map.addLayer(isochroneLayer);


    // Funktion zum Laden der Haltestellen im aktuellen Kartenbereich
let selectedStopId = null;
const markers = L.markerClusterGroup();  // Initialize the cluster group

function loadStops() {
    const currentZoom = map.getZoom();
    console.log(`Current zoom level: ${currentZoom}`);

    // Only load markers if zoom level is 13 or higher
    if (currentZoom < 13) {
        console.log("Zoom level too low, clearing markers.");
        markers.clearLayers();  // Clear markers if zoomed out
        return;
    }

    const bounds = map.getBounds();
    const url = `/get_stops?min_lat=${bounds.getSouth()}&max_lat=${bounds.getNorth()}&min_lon=${bounds.getWest()}&max_lon=${bounds.getEast()}`;
    console.log(`Fetching stops within bounds: ${bounds}`);

    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log("Stops data received:", data);

            // Clear previous markers to avoid duplicates
            markers.clearLayers();

            // Add new markers to the cluster group
            data.features.forEach(feature => {
                const coordinates = feature.geometry.coordinates;
                const stopName = feature.properties.stop_name;
                const stopId = feature.properties.stop_id;

                const marker = L.marker([coordinates[1], coordinates[0]])
                    .bindPopup(`<b>${stopName}</b>`)
                    .on('click', () => {
                        selectedStopId = stopId;
                        console.log(`Selected stop: ${stopName} (${stopId})`);
                    });

                markers.addLayer(marker);  // Add marker to the cluster group
            });

            // Add the cluster group to the map if it's not already added
            if (!map.hasLayer(markers)) {
                map.addLayer(markers);
                console.log("Markers layer added to map.");
            }
        })
        .catch(error => console.error('Error loading stops:', error));
}

// Load stops on initial map load and when the map view changes
map.on('moveend', loadStops);
map.on('zoomend', loadStops);  // Trigger loadStops on zoom change
loadStops();

document.getElementById('calculate-button').addEventListener('click', () => {
    if (!selectedStopId) {
        alert("No stop selected. Select a stop first.");
        return;
    }
    calculateIsochrone(selectedStopId);
});

function calculateIsochrone(stopId) {
    const maxTravelTime = document.getElementById('max-travel-time').value;
    const transportMode = document.getElementById('transport-mode').value;

    fetch(`/calculate_isochrone?combined_id=${stopId}&max_travel_time=${maxTravelTime}&transport_mode=${transportMode}`)
        .then(response => response.json())
        .then(data => {
            // Handle data (display isochrone on map, etc.)
            displayIsochrone(data);
        })
        .catch(error => console.error('Error calculating isochrone:', error));
}

    // Haltestellen initial laden und bei Kartenbewegung neu laden
    loadStops();
    map.on('moveend', loadStops);
});
