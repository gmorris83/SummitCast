class ConvertUnits:

    @staticmethod
    def c_to_f(c):
        return (c * 9 / 5) + 32 if c is not None else None

    @staticmethod
    def meters_to_km(m):
        return m / 1000 if m is not None else None

    @staticmethod
    def meters_to_miles(m):
        return m / 1609.344 if m is not None else None

    @staticmethod
    def ms_to_kph(ms):
        return ms * 3.6 if ms is not None else None

    @staticmethod
    def ms_to_mph(ms):
        return ms * 2.23694 if ms is not None else None