from typing import Dict, Any, Tuple, List
from dataclasses import dataclass
from movility_ai.sub_agents.route_planner.prompt import ROUTE_PLANNER_INSTR
from movility_ai.tools.providers.osrm import OSRMClient
from movility_ai.tools.providers.openweather import get_weather
from movility_ai.tools.providers.gtfs_metro import SimpleMetroGTFS
from movility_ai.tools.providers.encicla import get_stations


@dataclass
class Leg:
    mode: str
    summary: str
    duration_min: float
    distance_km: float
    geometry: str
    metadata: Dict[str, Any]


class RoutePlanner:
    def __init__(self):
        self.osrm = OSRMClient()
        self.metro = SimpleMetroGTFS()

    def _osrm_leg(self, a: Tuple[float,float], b: Tuple[float,float], profile: str) -> Leg:
        js = self.osrm.route([a,b], profile="bike" if profile=="bike" else ("foot" if profile=="foot" else "car"))
        r0 = js["routes"][0]
        return Leg(
            mode=profile,
            summary=f"{profile} segment",
            duration_min=r0["duration"]/60,
            distance_km=r0["distance"]/1000,
            geometry=r0["geometry"],
            metadata={"osrm": r0}
        )

    def plan(self, origin: Tuple[float,float], dest: Tuple[float,float], prefer: str = "time") -> Dict[str, Any]:
        # Weather
        weather = {"note": "configure OPENWEATHER_API_KEY for weather"}
        try:
            weather = get_weather(origin[0], origin[1])
        except Exception:
            pass

        # Nearest metro stops
        try:
            o_sid, o_stop = self.metro.nearest_stop(*origin)
            d_sid, d_stop = self.metro.nearest_stop(*dest)
        except Exception:
            o_sid = d_sid = None
            o_stop = d_stop = None

        # EnCicla stations (optional; nearest to O/D)
        try:
            stations = get_stations()
        except Exception:
            stations = []

        # Simple multimodal plan
        legs: List[Leg] = []
        if o_stop and d_stop:
            mode_first_last = "foot"
            if isinstance(weather, dict):
                try:
                    cond = (weather.get("weather") or [{}])[0].get("main","")
                    if cond.lower() not in ["rain","thunderstorm"]:
                        mode_first_last = "bike"
                except Exception:
                    pass

            legs.append(self._osrm_leg(origin, (o_stop["lat"], o_stop["lon"]), mode_first_last))
            metro_leg = Leg(
                mode="metro",
                summary=f"Metro entre {o_stop['stop_name']} y {d_stop['stop_name']} (aprox.)",
                duration_min=18.0,
                distance_km=8.0,
                geometry="",
                metadata={"origin_stop_id": o_sid, "dest_stop_id": d_sid, "note": "Duración promedio estimada"}
            )
            legs.append(metro_leg)
            legs.append(self._osrm_leg((d_stop["lat"], d_stop["lon"]), dest, mode_first_last))
        else:
            legs.append(self._osrm_leg(origin, dest, "bike"))

        total_min = sum(l.duration_min for l in legs)
        total_km = sum(l.distance_km for l in legs if l.distance_km)

        return {
            "summary": {
                "duration_min": round(total_min,1),
                "distance_km": round(total_km,2),
                "weather": weather if isinstance(weather, dict) else {"raw": weather},
            },
            "legs": [l.__dict__ for l in legs],
            "notes": ["Plan aproximado; para horarios exactos integrar GTFS-RT cuando esté disponible."],
        }


# Export agent-like interface
class AgentShim:
    model = "gemini-2.5-flash"
    name = "route_planner_agent"
    description = "Planificador de Rutas Inteligente (Metro + Bus + Bici + Caminata) con datos abiertos."
    instruction = ROUTE_PLANNER_INSTR
    tools = []

    def __init__(self):
        self.planner = RoutePlanner()

    def plan_route(self, origin_lat, origin_lon, dest_lat, dest_lon, prefer="time"):
        return self.planner.plan((origin_lat, origin_lon), (dest_lat, dest_lon), prefer=prefer)


route_planner_agent = AgentShim()
