from flask import Flask, jsonify, request, render_template
from modules.stop_loader import load_stops
from modules.isochrone_calculator import calculate_isochrone

app = Flask(__name__)

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
