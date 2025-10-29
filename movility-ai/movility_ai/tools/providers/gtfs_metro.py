# movility_ai/tools/providers/gtfs_metro.py
import os, time, requests
from typing import Tuple, Dict, Any, List

# Config
MIRRORS = [
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass-api.de/api/interpreter",
    "https://overpass.osm.ch/api/interpreter",
    "https://overpass.openstreetmap.ru/api/interpreter",
]
ENV_MIRROR = os.getenv("OVERPASS_URL", "").strip()
OVERPASS_TIMEOUT = float(os.getenv("OVERPASS_TIMEOUT_S", "60"))
OVERPASS_RETRIES = int(os.getenv("OVERPASS_RETRIES", "2"))
SLEEP_BETWEEN = float(os.getenv("OVERPASS_SLEEP_S", "1.5"))
UA = os.getenv("OVERPASS_UA", "MovilityAI/1.0 (contact: dev@example.com)")

NOMINATIM_URL = os.getenv("NOMINATIM_URL", "https://nominatim.openstreetmap.org/search")

class SimpleMetroGTFS:
    """
    Obtiene estaciones del Metro de Medellín dinámicamente (online):
    1) Overpass con {{geocodeArea:Medellín}}
    2) Overpass con resolución de área por nombre
    3) Nominatim -> bbox -> Overpass por bbox
    Sin caché y sin hardcode.
    """
    def __init__(self, src_url: str = ""):
        self.stops: Dict[str, tuple] = {}
        self._load_dynamic_or_fail()

    # HTTP helpers
    def _mirrors(self) -> List[str]:
        return [ENV_MIRROR] if ENV_MIRROR else MIRRORS

    def _post_overpass(self, query: str) -> dict:
        last = None
        headers = {"User-Agent": UA, "Accept": "application/json"}
        for base in self._mirrors():
            for _ in range(OVERPASS_RETRIES):
                try:
                    r = requests.post(base, data={"data": query}, headers=headers, timeout=OVERPASS_TIMEOUT)
                    if r.status_code != 200:
                        last = f"{base} -> HTTP {r.status_code}: {r.text[:200]}"
                        time.sleep(SLEEP_BETWEEN)
                        continue
                    return r.json()
                except Exception as e:
                    last = f"{base} -> {type(e).__name__}: {e}"
                    time.sleep(SLEEP_BETWEEN)
        raise RuntimeError(f"Overpass falló en todos los mirrors. Último: {last}")

    def _get_nominatim_bbox(self, q="Medellín, Antioquia, Colombia") -> tuple:
        headers = {"User-Agent": UA, "Accept": "application/json"}
        params = {"q": q, "format": "json", "limit": 1, "addressdetails": 0}
        r = requests.get(NOMINATIM_URL, params=params, headers=headers, timeout=30)
        r.raise_for_status()
        arr = r.json()
        if not arr:
            raise RuntimeError("Nominatim no devolvió resultados para Medellín.")
        # bbox viene como [south, north, west, east] o [minlat, maxlat, minlon, maxlon]
        bbox = arr[0].get("boundingbox")
        if not bbox or len(bbox) != 4:
            raise RuntimeError("Nominatim no devolvió un bounding box válido.")
        south, north, west, east = map(float, bbox)
        return south, west, north, east  # devolver en (minlat, minlon, maxlat, maxlon)

    # Load chain
    def _load_dynamic_or_fail(self):
        # Overpass geocodeArea
        if self._try_overpass_geocodearea():
            return
        # Overpass by area name
        if self._try_overpass_named_area():
            return
        # Nominatim -> bbox -> Overpass (bbox)
        if self._try_nominatim_then_overpass_bbox():
            return
        raise RuntimeError("No fue posible obtener estaciones del Metro (Overpass/Nominatim fallaron).")

    def _parse_elements_into_stops(self, elements: List[dict]) -> int:
        idx = 1
        for el in elements:
            if el.get("type") != "node":
                continue
            lat = el.get("lat"); lon = el.get("lon")
            tags = el.get("tags", {}) or {}
            name = tags.get("name") or tags.get("ref") or f"Estación {idx}"
            sid = str(el.get("id") or idx)
            if lat and lon:
                self.stops[sid] = (name, float(lat), float(lon))
                idx += 1
        return len(self.stops)

    def _try_overpass_geocodearea(self) -> bool:
        query = r"""
        [out:json][timeout:60];
        area({{geocodeArea:Medellín}})->.a;
        (
          node(area.a)["railway"="station"]["subway"="yes"];
          node(area.a)["public_transport"="station"]["subway"="yes"];
          node(area.a)["railway"="station"]["network"~"(?i)medell"];
        );
        out body;
        """
        try:
            js = self._post_overpass(query)
            if self._parse_elements_into_stops(js.get("elements", [])) > 0:
                return True
            return False
        except Exception:
            return False

    def _try_overpass_named_area(self) -> bool:
        # Busca un área administrativa “Medellín” (6/7/8) y la usa como area.a
        query_area = r"""
        [out:json][timeout:60];
        area["boundary"="administrative"]["name"~"(?i)medell[ií]n"]["admin_level"~"6|7|8"];
        out ids;
        """
        try:
            areas = self._post_overpass(query_area)
            ids = [el["id"] for el in areas.get("elements", []) if el.get("type") == "area"]
            if not ids:
                return False
            area_id = ids[0]
            query_nodes = f"""
            [out:json][timeout:60];
            node(area:{area_id})["railway"="station"]["subway"="yes"];
            node(area:{area_id})["public_transport"="station"]["subway"="yes"];
            node(area:{area_id})["railway"="station"]["network"~"(?i)medell"];
            out body;
            """
            js = self._post_overpass(query_nodes)
            return self._parse_elements_into_stops(js.get("elements", [])) > 0
        except Exception:
            return False

    def _try_nominatim_then_overpass_bbox(self) -> bool:
        try:
            minlat, minlon, maxlat, maxlon = self._get_nominatim_bbox()
        except Exception:
            return False
        # Consulta por bbox (más simple, muchos mirrors aceptan esto sin 400)
        query = f"""
        [out:json][timeout:60];
        (
          node["railway"="station"]["subway"="yes"]({minlat},{minlon},{maxlat},{maxlon});
          node["public_transport"="station"]["subway"="yes"]({minlat},{minlon},{maxlat},{maxlon});
          node["railway"="station"]["network"~"(?i)medell"]({minlat},{minlon},{maxlat},{maxlon});
        );
        out body;
        """
        try:
            js = self._post_overpass(query)
            return self._parse_elements_into_stops(js.get("elements", [])) > 0
        except Exception:
            return False

    # API pública
    def nearest_stop(self, lat: float, lon: float) -> Tuple[str, Dict[str, Any]]:
        from math import radians, sin, cos, asin, sqrt
        if not self.stops:
            raise RuntimeError("No hay estaciones del Metro disponibles (sin datos).")
        def hav(a,b,c,d):
            R=6371000
            dlat=radians(c-a); dlon=radians(d-b)
            sa=sin(dlat/2)**2+cos(radians(a))*cos(radians(c))*sin(dlon/2)**2
            return 2*R*asin(sqrt(sa))
        min_id, min_d = None, 1e12
        for sid,(name,slat,slon) in self.stops.items():
            d = hav(lat,lon,slat,slon)
            if d < min_d:
                min_id, min_d = sid, d
        name, slat, slon = self.stops[min_id]
        return min_id, {"stop_name": name, "lat": slat, "lon": slon, "distance_m": min_d}
