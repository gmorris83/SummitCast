import requests
import gpxpy
import io

from summit_waypoint import SummitWaypoint

# Load payload from file.

def parse():
    try:
        with open('lunar_round.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        print('File not found')
        return

# Parse file
def display_all_contents(contents):
    print(contents)

def parse_gpx(contents):
    gpx_file = io.StringIO(contents)
    gpx = gpxpy.parse(gpx_file)

    author_name = gpx.author_name
    route_name = gpx.name
    print(f'Name: {route_name} Created By: {author_name}')
    summits = []

    print(f'{len(gpx.waypoints)} Summits found...')
    for g in gpx.waypoints:
        elevation = get_elevation(g.latitude, g.longitude)
        summits.append(SummitWaypoint(g.latitude, g.longitude, elevation, g.name))

    return summits

def get_elevation(lat, lon):
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    return data['results'][0]['elevation']

def main():
    print("Running ")
    look_up = print("---- Loading Strava GPX File")
    contents = parse()
    # display route information

    # display summits from Strava and get elevation.
    summits = parse_gpx(contents)

    for s in summits:
        s.print_summit()

    # get weather for summits.
    # plot route on map
    # calculate time to run the route based on average pace.

    print("Complete.... ")

main()