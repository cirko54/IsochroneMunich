import json
import os

from flask import Flask, jsonify, request, render_template
from modules.stop_loader import load_stops
from modules.isochrone_calculator import calculate_isochrone

app = Flask(__name__)

# Pfad zur stop_clusters.json-Datei
CLUSTERS_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'stop_clusters.json')

from flask import request, jsonify
import json

# Laden der vorbereiteten Cluster
with open('data/stop_clusters.json') as f:
    clusters_data = json.load(f)

@app.route('/get_clusters_by_area', methods=['GET'])
def get_clusters_by_area():
    min_lat = float(request.args.get('min_lat'))
    max_lat = float(request.args.get('max_lat'))
    min_lon = float(request.args.get('min_lon'))
    max_lon = float(request.args.get('max_lon'))

    # Filtern der Cluster, die im angegebenen Koordinatenbereich liegen
    filtered_clusters = [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": cluster["center"]},
            "properties": {
                "cluster_id": cluster_id,
                "stop_names": cluster["stop_names"]
            }
        }
        for cluster_id, cluster in clusters_data.items()
        if min_lat <= cluster["center"][0] <= max_lat and min_lon <= cluster["center"][1] <= max_lon
    ]

    return jsonify({"type": "FeatureCollection", "features": filtered_clusters})

@app.route('/get_clusters')
def get_clusters():
    with open('data/stop_clusters.json') as f:
        clusters = json.load(f)

    # Wandeln Sie die Daten in das GeoJSON-Format um
    features = [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": cluster["center"]},
            "properties": {"cluster_id": cluster_id}
        }
        for cluster_id, cluster in clusters.items()
    ]
    return jsonify({"type": "FeatureCollection", "features": features})


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_stops', methods=['GET'])
def get_stops():
    # Pass request parameters to the `load_stops` function
    min_lat = float(request.args.get('min_lat', 47.0))
    max_lat = float(request.args.get('max_lat', 49.0))
    min_lon = float(request.args.get('min_lon', 10.0))
    max_lon = float(request.args.get('max_lon', 12.5))
    stops = load_stops(min_lat, max_lat, min_lon, max_lon)
    return jsonify(stops)

@app.route('/calculate_isochrone', methods=['GET'])
def calculate_isochrone_route():
    # Extract parameters and pass them to `calculate_isochrone`
    stop_id = request.args.get('stop_id')
    max_travel_time = int(request.args.get('max_travel_time', 15))
    transport_mode = request.args.get('transport_mode', 'public_transport')
    isochrone_data = calculate_isochrone(stop_id, max_travel_time, transport_mode)
    return jsonify(isochrone_data)

if __name__ == "__main__":
    app.run(debug=True)
