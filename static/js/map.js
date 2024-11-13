document.addEventListener("DOMContentLoaded", function() {
    // Initialisieren der Karte und Zentrierung auf München
    // Initialize map with custom zoom control positioning
// Initialisieren der Leaflet-Karte
const map = L.map('map').setView([48.137154, 11.576124], 13);  // Zentrum auf München setzen

// Tile-Layer hinzufügen (OpenStreetMap als Beispiel)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// Cluster-Gruppe erstellen für die Karte
const markers = L.markerClusterGroup();
map.addLayer(markers);

let selectedClusterId = null;  // Speichern der ausgewählten Cluster-ID für Berechnungen

// Funktion zum Laden der Cluster im aktuellen Kartenbereich
function loadClustersInView() {
    const bounds = map.getBounds();
    const minLat = bounds.getSouth();
    const maxLat = bounds.getNorth();
    const minLon = bounds.getWest();
    const maxLon = bounds.getEast();

    fetch(`/get_clusters_by_area?min_lat=${minLat}&max_lat=${maxLat}&min_lon=${minLon}&max_lon=${maxLon}`)
        .then(response => response.json())
        .then(data => {
            console.log("Cluster data received:", data);  // Debug-Ausgabe

            markers.clearLayers();  // Vorherige Marker entfernen

            data.features.forEach(feature => {
                const coords = feature.geometry.coordinates;
                const marker = L.marker([coords[1], coords[0]]);

                const stopNames = feature.properties.stop_names.join(", ");
                marker.bindPopup(`Cluster ID: ${feature.properties.cluster_id}<br>Haltestellen: ${stopNames}`);

                markers.addLayer(marker);

                marker.on('click', () => {
                    selectedClusterId = feature.properties.cluster_id;
                    console.log("Selected Cluster:", selectedClusterId);
                });
            });

            map.addLayer(markers);
        })
        .catch(error => console.error("Error loading clusters:", error));
}

// Initiales Laden und Aktualisierung bei Kartenbewegungen
map.on('moveend', loadClustersInView);
loadClustersInView();

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

});
