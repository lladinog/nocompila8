# Copyright 2025 MovilityAI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tools para PathFinder Agent - Integración con APIs de Google y datos locales"""

import os
from typing import Dict, List, Any, Optional
from datetime import datetime
import json

# Datos hardcodeados para hackathon (reemplazar con APIs reales)
ENCICLA_STATIONS_MOCK = [
    {"id": 1, "name": "Estación Parque Lleras", "lat": 6.2088, "lon": -75.5664, "bikes_available": 12, "docks_available": 8},
    {"id": 2, "name": "Estación Universidad de Antioquia", "lat": 6.2676, "lon": -75.5694, "bikes_available": 5, "docks_available": 15},
    {"id": 3, "name": "Estación Parque de las Luces", "lat": 6.2512, "lon": -75.5698, "bikes_available": 8, "docks_available": 12},
    {"id": 4, "name": "Estación Terminal del Norte", "lat": 6.2758, "lon": -75.5674, "bikes_available": 15, "docks_available": 5},
    {"id": 5, "name": "Estación Laureles", "lat": 6.2447, "lon": -75.5956, "bikes_available": 10, "docks_available": 10},
]

# Tarifas del Metro de Medellín (2025)
METRO_FARES = {
    "tarifa_unica": 3150,  # COP - Tarifa única integrada (Metro + Metrocable + Tranvía + Buses integrados)
    "tarifa_estudiante": 1700,  # COP - Tarifa reducida para estudiantes
    "tarifa_adulto_mayor": 1575,  # COP - Tarifa reducida para adultos mayores
    "tarjeta_civica": 2500,  # COP - Tarjeta Cívica (10 viajes)
    "encicla": 0,  # COP - EnCicla es gratis (sistema de bicicletas públicas)
    "integracion_bus": 3150,  # COP - Integración Metro + Bus (tarifa única)
}

METRO_LINES_MOCK = {
    "linea_a": ["Niquía", "Bello", "Madera", "Acevedo", "Tricentenario", "Caribe", "Universidad", "Hospital", "Prado", "Parque Berrío", "San Antonio", "Alpujarra", "Exposiciones", "Industriales", "Poblado", "Aguacatala", "Ayurá", "Envigado", "Itagüí", "Sabaneta", "La Estrella"],
    "linea_b": ["San Antonio", "Cisneros", "Parque Berrío"],
    "metrocable_k": ["Acevedo", "Andalucía", "Popular", "Santo Domingo"],
    "metrocable_j": ["San Javier", "Juan XXIII", "Vallejuelos", "La Aurora"],
    "metrocable_l": ["Santo Domingo", "El Tambo", "Carpinelo", "La Sierra"],
    "metrocable_h": ["Oriente", "Villa Sierra", "Cabañas", "Miraflores"],
    "metrocable_m": ["El Pinal", "La Montaña"],
    "tranvia": ["San Antonio", "San José", "Pabellón del Agua", "Buenos Aires", "Miraflores", "Loyola", "Alejandro Echavarría", "Oriente"],
}

WEATHER_MOCK_DATA = {
    "clear": {"condition": "Despejado", "temp": 24, "rain_probability": 5},
    "cloudy": {"condition": "Nublado", "temp": 22, "rain_probability": 30},
    "rainy": {"condition": "Lluvioso", "temp": 19, "rain_probability": 85},
}


def get_route_google_maps(origin: str, destination: str, mode: str = "driving") -> Dict[str, Any]:
    """
    Obtiene información de ruta usando Google Maps API (simulado con datos mock).
    
    Args:
        origin: Dirección o coordenadas de origen
        destination: Dirección o coordenadas de destino
        mode: Modo de transporte (driving, walking, bicycling, transit)
    
    Returns:
        Diccionario con información de la ruta
    """
    # TODO: Integrar con Google Maps Directions API real
    # import googlemaps
    # gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))
    # result = gmaps.directions(origin, destination, mode=mode)
    
    # Mock data para hackathon
    mock_routes = {
        "driving": {
            "duration": 25,  # minutos
            "distance": 12.5,  # km
            "cost": 15000,  # COP (taxi aproximado)
            "steps": [
                {"instruction": "Dirígete al norte por Cra. 43A", "duration": 5, "distance": 2.1},
                {"instruction": "Gira a la derecha en Cl. 10", "duration": 8, "distance": 4.3},
                {"instruction": "Continúa por Av. El Poblado", "duration": 12, "distance": 6.1},
            ]
        },
        "walking": {
            "duration": 95,
            "distance": 7.2,
            "cost": 0,
            "steps": [
                {"instruction": "Camina hacia el norte", "duration": 30, "distance": 2.4},
                {"instruction": "Gira a la izquierda", "duration": 40, "distance": 3.0},
                {"instruction": "Continúa recto", "duration": 25, "distance": 1.8},
            ]
        },
        "bicycling": {
            "duration": 35,
            "distance": 8.5,
            "cost": 0,
            "steps": [
                {"instruction": "Toma la cicloruta de la Cra. 43A", "duration": 15, "distance": 4.0},
                {"instruction": "Continúa por cicloruta Av. El Poblado", "duration": 20, "distance": 4.5},
            ]
        },
        "transit": {
            "duration": 40,
            "distance": 11.0,
            "cost": METRO_FARES["tarifa_unica"],  # Tarifa única integrada Metro de Medellín
            "steps": [
                {"instruction": "Camina a estación Universidad", "duration": 5, "distance": 0.4, "mode": "walking"},
                {"instruction": "Toma Metro Línea A hacia La Estrella", "duration": 25, "distance": 9.5, "mode": "metro"},
                {"instruction": "Baja en estación Poblado", "duration": 1, "distance": 0, "mode": "metro"},
                {"instruction": "Camina al destino", "duration": 9, "distance": 1.1, "mode": "walking"},
            ],
            "fare_info": {
                "tipo": "Tarifa única integrada",
                "valor": METRO_FARES["tarifa_unica"],
                "incluye": "Metro + Metrocable + Tranvía + Buses integrados",
                "descuentos": {
                    "estudiantes": METRO_FARES["tarifa_estudiante"],
                    "adulto_mayor": METRO_FARES["tarifa_adulto_mayor"],
                }
            }
        }
    }
    
    return mock_routes.get(mode, mock_routes["driving"])


def get_weather_conditions(location: str = "Medellín") -> Dict[str, Any]:
    """
    Obtiene condiciones climáticas actuales y pronóstico.
    
    Args:
        location: Ciudad o coordenadas
    
    Returns:
        Diccionario con información del clima
    """
    # TODO: Integrar con OpenWeather API real
    # import requests
    # api_key = os.getenv('OPENWEATHER_API_KEY')
    # url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}"
    # response = requests.get(url)
    # return response.json()
    
    # Mock data para hackathon
    hour = datetime.now().hour
    
    # Simular clima según hora del día
    if 6 <= hour < 12:
        weather = WEATHER_MOCK_DATA["clear"]
    elif 12 <= hour < 16:
        weather = WEATHER_MOCK_DATA["cloudy"]
    else:
        weather = WEATHER_MOCK_DATA["rainy"]
    
    return {
        "location": location,
        "current": weather,
        "timestamp": datetime.now().isoformat(),
        "forecast_3h": WEATHER_MOCK_DATA["rainy" if hour >= 15 else "clear"],
    }


def get_encicla_stations(lat: Optional[float] = None, lon: Optional[float] = None, radius_km: float = 2.0) -> List[Dict[str, Any]]:
    """
    Obtiene estaciones de EnCicla cercanas.
    
    Args:
        lat: Latitud de referencia
        lon: Longitud de referencia
        radius_km: Radio de búsqueda en kilómetros
    
    Returns:
        Lista de estaciones con disponibilidad
    """
    # TODO: Integrar con API real de EnCicla si existe
    # Por ahora retornamos todas las estaciones mock
    
    if lat and lon:
        # Filtrar por distancia (implementación simplificada)
        # En producción usar fórmula de Haversine
        return ENCICLA_STATIONS_MOCK[:3]
    
    return ENCICLA_STATIONS_MOCK


def calculate_multimodal_route(
    origin: str,
    destination: str,
    preferences: Dict[str, Any],
    current_time: Optional[str] = None
) -> Dict[str, Any]:
    """
    Calcula ruta multimodal óptima combinando varios modos de transporte.
    
    Args:
        origin: Origen del viaje
        destination: Destino del viaje
        preferences: Preferencias del usuario (priority, use_bike, max_budget, etc.)
        current_time: Hora del viaje (ISO format)
    
    Returns:
        Ruta multimodal completa con todos los detalles
    """
    # Obtener datos de contexto
    weather = get_weather_conditions("Medellín")
    
    # Simular análisis de tráfico según hora
    if not current_time or current_time.lower() == 'now':
        hour = datetime.now().hour
    else:
        try:
            hour = datetime.fromisoformat(current_time).hour
        except (ValueError, AttributeError):
            hour = datetime.now().hour
    
    traffic_factor = 1.5 if (7 <= hour <= 9) or (17 <= hour <= 19) else 1.0
    
    # Obtener rutas base de cada modo
    walking = get_route_google_maps(origin, destination, "walking")
    bicycling = get_route_google_maps(origin, destination, "bicycling")
    transit = get_route_google_maps(origin, destination, "transit")
    driving = get_route_google_maps(origin, destination, "driving")
    
    # Ajustar tiempos por tráfico
    driving["duration"] = int(driving["duration"] * traffic_factor)
    
    # Calcular scores de sostenibilidad (kg CO2)
    co2_per_km = {
        "walking": 0,
        "bicycling": 0,
        "transit": 0.05,  # Metro es muy eficiente
        "driving": 0.12,  # Promedio carro gasolina
    }
    
    # Determinar mejor ruta según preferencias
    priority = preferences.get("priority", "time")
    use_bike = preferences.get("use_bike", True)
    max_budget = preferences.get("max_budget", 10000)
    
    # Opciones de rutas
    routes = []
    
    # Opción 1: Solo transporte público
    if transit["cost"] <= max_budget:
        routes.append({
            "name": "Ruta Metro/Bus",
            "segments": transit["steps"],
            "total_duration": transit["duration"],
            "total_cost": transit["cost"],
            "cost_breakdown": {
                "tarifa": METRO_FARES["tarifa_unica"],
                "descripcion": "Tarifa única integrada (Metro + Metrocable + Tranvía + Buses)",
                "descuentos_disponibles": {
                    "Estudiantes": f"${METRO_FARES['tarifa_estudiante']} COP",
                    "Adultos mayores": f"${METRO_FARES['tarifa_adulto_mayor']} COP",
                }
            },
            "co2_kg": round(transit["distance"] * co2_per_km["transit"], 2),
            "score": calculate_route_score(transit["duration"], transit["cost"], transit["distance"] * co2_per_km["transit"], priority),
        })
    
    # Opción 2: Bici + Metro (si acepta bici y no llueve mucho)
    if use_bike and weather["current"]["rain_probability"] < 50:
        encicla_stations = get_encicla_stations()
        multimodal_duration = int(bicycling["duration"] * 0.3 + transit["duration"] * 0.7)
        multimodal_cost = transit["cost"]
        
        routes.append({
            "name": "Ruta Bici + Metro",
            "segments": [
                {"instruction": f"Toma bici en {encicla_stations[0]['name']}", "duration": int(bicycling["duration"] * 0.3), "mode": "bicycling"},
                {"instruction": "Deja bici y toma Metro", "duration": int(transit["duration"] * 0.7), "mode": "transit"},
            ],
            "total_duration": multimodal_duration,
            "total_cost": multimodal_cost,
            "cost_breakdown": {
                "encicla": METRO_FARES["encicla"],
                "metro": METRO_FARES["tarifa_unica"],
                "total": multimodal_cost,
                "nota": "EnCicla es GRATIS 🚲 - Solo pagas el Metro"
            },
            "co2_kg": round(bicycling["distance"] * 0.3 * co2_per_km["bicycling"] + transit["distance"] * 0.7 * co2_per_km["transit"], 2),
            "score": calculate_route_score(multimodal_duration, multimodal_cost, 0, priority),
        })
    
    # Opción 3: Caminata (si es factible)
    if walking["duration"] < 60:
        routes.append({
            "name": "Ruta a Pie",
            "segments": walking["steps"],
            "total_duration": walking["duration"],
            "total_cost": 0,
            "co2_kg": 0,
            "score": calculate_route_score(walking["duration"], 0, 0, priority),
        })
    
    # Ordenar rutas por score
    routes.sort(key=lambda x: x["score"], reverse=True)
    
    # Agregar alertas
    alerts = []
    if weather["current"]["rain_probability"] > 70:
        alerts.append("⚠️ Alta probabilidad de lluvia - considera transporte techado")
    if traffic_factor > 1.3:
        alerts.append("🚦 Hora pico - tráfico pesado esperado")
    
    return {
        "recommended_route": routes[0] if routes else None,
        "alternative_routes": routes[1:3] if len(routes) > 1 else [],
        "weather": weather,
        "alerts": alerts,
        "timestamp": datetime.now().isoformat(),
    }


def calculate_route_score(duration: int, cost: int, co2: float, priority: str) -> float:
    """
    Calcula score de una ruta según prioridad del usuario.
    
    Args:
        duration: Duración en minutos
        cost: Costo en COP
        co2: Emisiones en kg CO2
        priority: time, cost, sustainability
    
    Returns:
        Score (mayor es mejor)
    """
    if priority == "time":
        return 1000 / (duration + 1)
    elif priority == "cost":
        return 1000 / (cost + 1)
    elif priority == "sustainability":
        return 100 / (co2 + 0.1)
    else:
        # Balance
        return (500 / (duration + 1)) + (300 / (cost + 1)) + (200 / (co2 + 0.1))
