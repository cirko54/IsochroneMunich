import networkx as nx
import pandas as pd
from shapely.geometry import Point, Polygon

def create_graph(stop_times_path, trips_path):
    G = nx.DiGraph()
    stop_times = pd.read_csv(stop_times_path)
    trips = pd.read_csv(trips_path)

    for i in range(1, len(stop_times)):
        if stop_times.loc[i-1, 'trip_id'] == stop_times.loc[i, 'trip_id']:
            start_time = int(stop_times.loc[i-1, 'arrival_time'])
            end_time = int(stop_times.loc[i, 'departure_time'])
            travel_time = end_time - start_time
            G.add_edge(stop_times.loc[i-1, 'stop_id'], stop_times.loc[i, 'stop_id'], weight=travel_time)
    return G

def calculate_isochrones(G, stop_id, isochrone_times):
    isochrones = []
    for time in isochrone_times:
        reachable_nodes = nx.single_source_dijkstra_path_length(G, stop_id, cutoff=time, weight='weight')
        coords = [
            (G.nodes[node].get('lon', 0), G.nodes[node].get('lat', 0)) for node in reachable_nodes
            if 'lon' in G.nodes[node] and 'lat' in G.nodes[node]
        ]
        polygon = Polygon(coords) if len(coords) > 2 else Point(coords[0])  # Sicherstellen, dass ein Polygon erzeugt wird
        isochrones.append({
            "type": "Feature",
            "geometry": polygon.__geo_interface__,
            "properties": {"color": "blue" if time == 600 else "green" if time == 900 else "orange"}
        })
    return {"type": "FeatureCollection", "features": isochrones}
