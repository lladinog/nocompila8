import requests
from movility_ai.shared_libraries.config import OPENWEATHER_API_KEY, OPENWEATHER_BASE_URL

def get_weather(lat: float, lon: float) -> dict:
    if not OPENWEATHER_API_KEY:
        return {"error": "OPENWEATHER_API_KEY not configured"}
    url = f"{OPENWEATHER_BASE_URL}/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}&units=metric&lang=es"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.json()
