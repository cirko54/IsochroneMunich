import pandas as pd
from geopy.distance import geodesic
from config import GROUP_RADIUS_METERS

def load_stops(min_lat, max_lat, min_lon, max_lon):
    stops = pd.read_csv('data/stops.txt', dtype={'stop_id': str, 'stop_name': str, 'stop_lat': float, 'stop_lon': float})
    stops_in_bounds = stops[
        (stops['stop_lat'] >= min_lat) & (stops['stop_lat'] <= max_lat) &
        (stops['stop_lon'] >= min_lon) & (stops['stop_lon'] <= max_lon)
    ]

    grouped_stops = []
    stop_groups = {}

    for _, stop in stops_in_bounds.iterrows():
        stop_name = stop['stop_name']
        stop_coords = (stop['stop_lat'], stop['stop_lon'])
        found_group = False

        if stop_name in stop_groups:
            for group in stop_groups[stop_name]:
                group_coords = (group['geometry']['coordinates'][1], group['geometry']['coordinates'][0])
                if geodesic(stop_coords, group_coords).meters < GROUP_RADIUS_METERS:
                    found_group = True
                    break

        if not found_group:
            stop_feature = {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [stop['stop_lon'], stop['stop_lat']]},
                "properties": {"stop_id": stop['stop_id'], "stop_name": stop_name}
            }
            grouped_stops.append(stop_feature)
            if stop_name not in stop_groups:
                stop_groups[stop_name] = []
            stop_groups[stop_name].append(stop_feature)

    return {"type": "FeatureCollection", "features": grouped_stops}
