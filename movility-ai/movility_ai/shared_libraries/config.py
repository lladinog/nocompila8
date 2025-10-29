import os

def env(key: str, default: str = "") -> str:
    return os.getenv(key, default)

OSRM_BASE_URL = env("OSRM_BASE_URL", "https://routing.openstreetmap.de")
OSRM_PROFILES = {
    "car": env("OSRM_PROFILE_CAR", "/routed-car"),
    "bike": env("OSRM_PROFILE_BIKE", "/routed-bike"),
    "foot": env("OSRM_PROFILE_FOOT", "/routed-foot"),
}

OPENWEATHER_API_KEY = env("OPENWEATHER_API_KEY", "")
OPENWEATHER_BASE_URL = env("OPENWEATHER_BASE_URL", "https://api.openweathermap.org")

METRO_GTFS_URL = env(
    "METRO_GTFS_URL",
    "https://datosabiertos-metrodemedellin.opendata.arcgis.com/api/download/v1/items/0557214a4b5c4a1d90d36eb97ba54249/relationships?format=zip"
)

ENCICLA_STATIONS_URL = env("ENCICLA_STATIONS_URL", "https://www.datos.gov.co/resource/hmuf-kqju.json")
