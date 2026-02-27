import requests
import gpxpy
import io

def get_strava_route_waypoints(route_id, access_token, only_summits=True, top_n=None, elevation_threshold=None):
    """
    Fetch all waypoints from a Strava route using GPX export.

    Parameters:
    - route_id: Strava route ID
    - access_token: OAuth access token
    - only_summits: if True, return only the highest points
    - top_n: if set, return only the top N highest points (overrides elevation_threshold)
    - elevation_threshold: if set, return points above this elevation (meters)

    Returns:
    - List of tuples: [(lat, lon, elevation), ...]
    """
    url = f"https://www.strava.com/api/v3/routes/{route_id}/export_gpx"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    gpx_file = io.StringIO(response.text)
    gpx = gpxpy.parse(gpx_file)

    summits = [];

    for g in gpx.waypoints:
        print('Summits found')
        print(g)

    # Extract all points
    waypoints = [
        (point.latitude, point.longitude, point.elevation, point.name)
        for track in gpx.tracks
        for segment in track.segments
        for point in segment.points
    ]

    if not only_summits:
        return waypoints

    # Filter points for summits
    filtered = waypoints

    if elevation_threshold is not None:
        filtered = [p for p in filtered if p[2] and p[2] >= elevation_threshold]

    if top_n is not None:
        filtered = sorted(filtered, key=lambda x: x[2] or 0, reverse=True)[:top_n]

    # Optional: local maxima smoothing (ignore tiny fluctuations)
    # Uncomment if needed:
    # window = 3
    # local_maxima = []
    # for i in range(window, len(filtered) - window):
    #     window_points = filtered[i - window:i + window + 1]
    #     center_point = filtered[i]
    #     if center_point[2] == max(p[2] for p in window_points):
    #         local_maxima.append(center_point)
    # filtered = local_maxima

    return filtered


# -----------------------------
# Example usage
ACCESS_TOKEN = "128b04290d9ff1aea6a58722666f0c085ff2dc9b"
ROUTE_ID = 3360377804620477768

# Get all waypoints
all_points = get_strava_route_waypoints(ROUTE_ID, ACCESS_TOKEN, only_summits=False)
print(f"All waypoints: {len(all_points)}")
print("First 5 points:", all_points[:5])

# Get only summits (top 5 highest points)
summits = get_strava_route_waypoints(ROUTE_ID, ACCESS_TOKEN, only_summits=True, top_n=5)
print(f"Summits found: {len(summits)}")
print(summits)