import requests
from typing import List, Dict, Any
from movility_ai.shared_libraries.config import ENCICLA_STATIONS_URL

def get_stations(limit: int = 200) -> List[Dict[str, Any]]:
    url = f"{ENCICLA_STATIONS_URL}?$limit={limit}"
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    data = r.json()
    out = []
    for row in data:
        out.append({
            "id": row.get("id") or row.get("codigo") or row.get("objectid"),
            "name": row.get("nombre") or row.get("estacion") or row.get("nombre_estacion"),
            "lat": float(row.get("lat") or row.get("latitude") or row.get("y")) if row.get("lat") or row.get("latitude") or row.get("y") else None,
            "lon": float(row.get("lon") or row.get("longitude") or row.get("x")) if row.get("lon") or row.get("longitude") or row.get("x") else None,
            "municipio": row.get("municipio") or row.get("ciudad"),
            "tipo": row.get("tipo") or row.get("tipo_estacion"),
        })
    return [s for s in out if s["lat"] and s["lon"]]
