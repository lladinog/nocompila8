import requests
from typing import List, Tuple, Dict, Any
from urllib.parse import quote
from movility_ai.shared_libraries.config import OSRM_BASE_URL, OSRM_PROFILES

class OSRMClient:
    def __init__(self, base_url: str = OSRM_BASE_URL):
        self.base_url = base_url.rstrip("/")

    def route(self, coords: List[Tuple[float, float]], profile: str = "car", overview: str = "full") -> Dict[str, Any]:
        if profile not in OSRM_PROFILES:
            raise ValueError(f"Unsupported profile: {profile}")
        profile_path = OSRM_PROFILES[profile]
        coord_str = ";".join([f"{lon},{lat}" for lat, lon in coords])
        url = f"{self.base_url}{profile_path}/route/v1/{profile}/{quote(coord_str)}?overview={overview}&geometries=polyline&annotations=duration,distance"
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        return r.json()
