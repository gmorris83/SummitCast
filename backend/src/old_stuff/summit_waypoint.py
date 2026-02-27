class SummitWaypoint:
    def __init__(self, lat, lon, elev, name):
        self.lat = lat
        self.lon = lon
        self.elev = elev
        self.name = name

    def set_weather(self, weather):
        self.weather = weather

    def get_weather(self):
        return self.weather

    def print_summit(self):
        print(f'Name: {self.name} elev: {self.elev} lat: {self.lat} lon: {self.lon}')