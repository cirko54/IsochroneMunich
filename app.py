from flask import Flask, request, render_template, jsonify
from utils.graph_utils import create_graph, calculate_isochrones
import geopandas as gpd

app = Flask(__name__)

# Daten laden und Graph erstellen
stops_gdf = gpd.read_file('all_stops.geojson')
G = create_graph('stop_times.txt', 'trips.txt')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_stops', methods=['GET'])
def get_stops():
    # Haltestellen basierend auf Kartenbereich filtern
    bounds = request.args.get('bounds').split(',')
    min_lon, min_lat, max_lon, max_lat = map(float, bounds)
    filtered_stops = stops_gdf.cx[min_lon:max_lon, min_lat:max_lat]
    return jsonify(filtered_stops.to_dict('records'))

@app.route('/calculate_isochrones', methods=['GET'])
def calculate_isochrones_route():
    stop_id = request.args.get('stop_id')
    isochrone_times = [600, 900, 1200]  # 10, 15, 20 Minuten in Sekunden
    result = calculate_isochrones(G, stop_id, isochrone_times)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
