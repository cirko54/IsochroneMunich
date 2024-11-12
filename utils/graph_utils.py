def calculate_isochrones(G, stop_id, isochrone_times):
    isochrones = []
    for time in isochrone_times:
        reachable_nodes = nx.single_source_dijkstra_path_length(G, stop_id, cutoff=time, weight='weight')
        coords = [
            (G.nodes[node].get('lon', 0), G.nodes[node].get('lat', 0)) for node in reachable_nodes
            if 'lon' in G.nodes[node] and 'lat' in G.nodes[node]
        ]
        polygon = Polygon(coords) if len(coords) > 2 else Point(coords[0])
        isochrones.append({
            "type": "Feature",
            "geometry": polygon.__geo_interface__,
            "properties": {"color": "blue" if time == 600 else "green" if time == 900 else "orange"}
        })
    return {"type": "FeatureCollection", "features": isochrones}
