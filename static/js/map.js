// Initialisierung der Karte
var map = L.map('map').setView([48.1351, 11.5820], 12);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
}).addTo(map);

var stopsLayer = L.layerGroup().addTo(map);

function loadStops() {
    var bounds = map.getBounds();
    var zoom = map.getZoom();
    var boundsParam = `${bounds.getWest()},${bounds.getSouth()},${bounds.getEast()},${bounds.getNorth()}`;

    $.getJSON(`/get_stops?bounds=${boundsParam}&zoom=${zoom}`, function(data) {
        stopsLayer.clearLayers();
        data.forEach(function(stop) {
            var marker = L.marker([stop.stop_lat, stop.stop_lon])
                .addTo(stopsLayer)
                .bindPopup(`<strong>${stop.stop_name}</strong><br>ID: ${stop.stop_id}`)
                .on('click', function() {
                    calculateIsochrones(stop.stop_id);
                });
        });
    });
}

map.on('moveend', loadStops);
loadStops();

function calculateIsochrones(stop_id) {
    $.getJSON(`/calculate_isochrones?stop_id=${stop_id}`, function(data) {
        L.geoJSON(data, {
            style: function(feature) {
                return { color: feature.properties.color };
            }
        }).addTo(map);
    });
}
