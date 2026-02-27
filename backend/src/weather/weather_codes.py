from enum import Enum

class WeatherCode(Enum):
    CLEAR_SKY = 0
    MAINLY_CLEAR = 1
    PARTLY_CLOUDY = 2
    OVERCAST = 3
    FOG = 45
    DEPOSITING_RIME_FOG = 48
    LIGHT_DRIZZLE = 51
    MODERATE_DRIZZLE = 53
    DENSE_DRIZZLE = 55
    LIGHT_FREEZING_DRIZZLE = 56
    DENSE_FREEZING_DRIZZLE = 57
    SLIGHT_RAIN = 61
    MODERATE_RAIN = 63
    HEAVY_RAIN = 65
    LIGHT_FREEZING_RAIN = 66
    HEAVY_FREEZING_RAIN = 67
    SLIGHT_SNOW_FALL = 71
    MODERATE_SNOW_FALL = 73
    HEAVY_SNOW_FALL = 75
    SNOW_GRAINS = 77
    SLIGHT_RAIN_SHOWERS = 80
    MODERATE_RAIN_SHOWERS = 81
    VIOLENT_RAIN_SHOWERS = 82
    SLIGHT_SNOW_SHOWERS = 85
    HEAVY_SNOW_SHOWERS = 86
    THUNDERSTORM = 95
    THUNDERSTORM_SLIGHT_HAIL = 96
    THUNDERSTORM_HEAVY_HAIL = 99

    @classmethod
    def text(cls, code: int) -> str:
        """Return human-readable text for a weather code."""
        for member in cls:
            if member.value == code:
                return member.name.replace("_", " ").title()
        return "Unknown"