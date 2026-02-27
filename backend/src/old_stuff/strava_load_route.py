import requests
import polyline

ACCESS_TOKEN = "7965c3c7e009709a41f16b802e0b5780c701733b"
ROUTE_ID = '3406267604191386846'
#https://www.strava.com/routes/3360377804620477768

# The Lunar Round
#https://www.strava.com/routes/3406267604191386846


def get_route(route_id):
    url = f"https://www.strava.com/api/v3/routes/{route_id}"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    return response.json()

def get_route_from_file():
    try:
        with open('lunar_round.json', 'r') as file:
            return file.read()
    except FileNotFoundError:
        print('File not found')
    return

def decode_route(polyline_str: str):
    """
    Decode encoded polyline into list of (lat, lon) tuples.
    """
    return polyline.decode(polyline_str)

def decode_route_coordinates(route_data: str):
    encoded_polyline = route_data["map"]["summary_polyline"]
    coords = polyline.decode(encoded_polyline)
    return coords


def main():
    #route = get_route(ROUTE_ID)
    #ROUTE_ID = input('Enter Strava Route ID:\n')
    #ACCESS_TOKEN = input('Enter Strava Access Token:\n')
    route = get_route_from_file()
   # cods = decode_route(route);

    print(f'Here is the {route}')

    # print("Route name:", route["name"])
    # print("Distance (km):", route["distance"] / 1000)
    # print("Elevation gain (m):", route["elevation_gain"])

    coordinates = decode_route_coordinates(route)
    print("First 5 coordinates:", coordinates[:5])

main()