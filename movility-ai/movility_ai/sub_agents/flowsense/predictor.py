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

"""Predictor de tráfico para FlowSense Agent"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import random

# Zonas clave de Medellín con patrones de tráfico
MEDELLIN_ZONES = {
    "centro": {
        "name": "Centro (Av. Oriental, San Juan, La Playa)",
        "base_congestion": 0.6,
        "peak_hours": [(7, 9), (17, 19)],
        "peak_multiplier": 1.8,
    },
    "poblado": {
        "name": "El Poblado (Av. El Poblado, Loma de Los Balsos)",
        "base_congestion": 0.5,
        "peak_hours": [(7, 9), (17, 20)],
        "peak_multiplier": 2.0,
    },
    "laureles": {
        "name": "Laureles (Av. 33, Av. Nutibara)",
        "base_congestion": 0.4,
        "peak_hours": [(7, 9), (17, 19)],
        "peak_multiplier": 1.6,
    },
    "autopista_norte": {
        "name": "Autopista Norte",
        "base_congestion": 0.5,
        "peak_hours": [(6, 9), (16, 19)],
        "peak_multiplier": 2.2,
    },
    "av_80": {
        "name": "Avenida 80",
        "base_congestion": 0.6,
        "peak_hours": [(7, 9), (17, 19)],
        "peak_multiplier": 1.9,
    },
    "las_palmas": {
        "name": "Vía Las Palmas",
        "base_congestion": 0.3,
        "peak_hours": [(8, 10), (18, 20)],
        "peak_multiplier": 1.7,
    },
    "estadio": {
        "name": "Zona Estadio Atanasio Girardot",
        "base_congestion": 0.3,
        "peak_hours": [],  # Variable por eventos
        "peak_multiplier": 1.0,
    },
}

# Eventos que afectan el tráfico (mock data)
TRAFFIC_EVENTS_MOCK = [
    {
        "id": 1,
        "type": "accident",
        "location": "Autopista Norte con Calle 67",
        "severity": "high",
        "description": "Accidente con dos vehículos, carril izquierdo bloqueado",
        "start_time": "2025-10-29T07:30:00",
        "estimated_end": "2025-10-29T09:00:00",
    },
    {
        "id": 2,
        "type": "construction",
        "location": "Av. El Poblado entre Calles 10 y 16",
        "severity": "medium",
        "description": "Obras de repavimentación, un carril cerrado",
        "start_time": "2025-10-29T06:00:00",
        "estimated_end": "2025-10-29T18:00:00",
    },
    {
        "id": 3,
        "type": "event",
        "location": "Estadio Atanasio Girardot",
        "severity": "high",
        "description": "Partido Atlético Nacional vs Medellín - 20:00h",
        "start_time": "2025-10-29T18:00:00",
        "estimated_end": "2025-10-29T23:00:00",
    },
]


def predict_traffic_congestion(
    target_time: Optional[str] = None,
    zone: Optional[str] = None,
    weather_condition: Optional[str] = None
) -> Dict[str, Any]:
    """
    Predice niveles de congestión para zonas de Medellín.
    
    Args:
        target_time: Hora para la predicción (ISO format), None para ahora
        zone: Zona específica o None para toda la ciudad
        weather_condition: Condición climática (clear, cloudy, rainy)
    
    Returns:
        Predicción de congestión por zona
    """
    # Determinar hora objetivo
    if target_time:
        dt = datetime.fromisoformat(target_time)
    else:
        dt = datetime.now()
    
    hour = dt.hour
    day_of_week = dt.weekday()  # 0=Monday, 6=Sunday
    is_weekend = day_of_week >= 5
    
    # Factor climático
    weather_factor = {
        "clear": 1.0,
        "cloudy": 1.1,
        "rainy": 1.4,
        None: 1.0,
    }.get(weather_condition, 1.0)
    
    # Factor fin de semana
    weekend_factor = 0.6 if is_weekend else 1.0
    
    # Calcular congestión por zona
    zones_status = {}
    
    target_zones = [zone] if zone else list(MEDELLIN_ZONES.keys())
    
    for zone_id in target_zones:
        if zone_id not in MEDELLIN_ZONES:
            continue
            
        zone_data = MEDELLIN_ZONES[zone_id]
        base = zone_data["base_congestion"]
        
        # Verificar si estamos en hora pico
        is_peak = any(start <= hour < end for start, end in zone_data["peak_hours"])
        peak_factor = zone_data["peak_multiplier"] if is_peak else 1.0
        
        # Calcular nivel de congestión (0-1)
        congestion_level = base * peak_factor * weather_factor * weekend_factor
        congestion_level = min(congestion_level, 1.0)  # Cap at 1.0
        
        # Clasificar nivel
        if congestion_level < 0.3:
            status = "FLUIDO"
            emoji = "🟢"
        elif congestion_level < 0.6:
            status = "MODERADO"
            emoji = "🟡"
        elif congestion_level < 0.8:
            status = "CONGESTIONADO"
            emoji = "🟠"
        else:
            status = "CRÍTICO"
            emoji = "🔴"
        
        # Determinar causa principal
        causes = []
        if is_peak:
            causes.append("Hora pico")
        if weather_condition == "rainy":
            causes.append("Lluvia")
        if is_weekend and zone_id in ["poblado", "laureles"]:
            causes.append("Zona de ocio fin de semana")
        if not causes:
            causes.append("Tráfico normal")
        
        zones_status[zone_id] = {
            "name": zone_data["name"],
            "level": congestion_level,
            "status": status,
            "emoji": emoji,
            "causes": causes,
            "avg_speed_kmh": int(50 * (1 - congestion_level)),  # Velocidad estimada
        }
    
    # Predicción a 30 y 60 minutos
    prediction_30 = predict_future_traffic(dt + timedelta(minutes=30), zones_status, weather_condition)
    prediction_60 = predict_future_traffic(dt + timedelta(minutes=60), zones_status, weather_condition)
    
    return {
        "timestamp": dt.isoformat(),
        "current_conditions": zones_status,
        "prediction_30min": prediction_30,
        "prediction_60min": prediction_60,
        "general_status": calculate_general_status(zones_status),
    }


def predict_future_traffic(
    future_time: datetime,
    current_zones: Dict[str, Any],
    weather_condition: Optional[str]
) -> Dict[str, str]:
    """
    Predice cómo evolucionará el tráfico en 30-60 min.
    """
    future_hour = future_time.hour
    predictions = {}
    
    for zone_id, data in current_zones.items():
        zone_info = MEDELLIN_ZONES[zone_id]
        
        # Verificar si entrará o saldrá de hora pico
        is_currently_peak = any(start <= datetime.now().hour < end for start, end in zone_info["peak_hours"])
        will_be_peak = any(start <= future_hour < end for start, end in zone_info["peak_hours"])
        
        if not is_currently_peak and will_be_peak:
            predictions[zone_id] = "Aumentará congestión (entrando a hora pico)"
        elif is_currently_peak and not will_be_peak:
            predictions[zone_id] = "Mejorará (saliendo de hora pico)"
        else:
            predictions[zone_id] = "Se mantendrá similar"
    
    return predictions


def get_traffic_events(zone: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Obtiene eventos que afectan el tráfico (accidentes, obras, eventos masivos).
    
    Args:
        zone: Filtrar por zona específica
    
    Returns:
        Lista de eventos activos
    """
    current_time = datetime.now()
    
    # Filtrar eventos activos
    active_events = []
    for event in TRAFFIC_EVENTS_MOCK:
        start = datetime.fromisoformat(event["start_time"])
        end = datetime.fromisoformat(event["estimated_end"])
        
        if start <= current_time <= end:
            active_events.append(event)
    
    return active_events


def get_historical_patterns(zone: str, day_of_week: int, hour: int) -> Dict[str, Any]:
    """
    Obtiene patrones históricos de tráfico para una zona.
    
    Args:
        zone: Identificador de zona
        day_of_week: Día de la semana (0=lunes, 6=domingo)
        hour: Hora del día (0-23)
    
    Returns:
        Datos históricos de la zona
    """
    if zone not in MEDELLIN_ZONES:
        return {"error": f"Zona {zone} no encontrada"}
    
    zone_data = MEDELLIN_ZONES[zone]
    is_peak = any(start <= hour < end for start, end in zone_data["peak_hours"])
    
    return {
        "zone": zone_data["name"],
        "day_of_week": day_of_week,
        "hour": hour,
        "is_typical_peak_hour": is_peak,
        "average_congestion": zone_data["base_congestion"] * (zone_data["peak_multiplier"] if is_peak else 1.0),
        "historical_note": "Basado en patrones de tráfico típicos de Medellín",
    }


def analyze_weather_impact(weather_condition: str) -> Dict[str, Any]:
    """
    Analiza el impacto del clima en el tráfico.
    
    Args:
        weather_condition: Condición climática (clear, cloudy, rainy)
    
    Returns:
        Análisis del impacto climático
    """
    impacts = {
        "clear": {
            "impact_level": "low",
            "multiplier": 1.0,
            "description": "Condiciones normales, sin impacto significativo en el tráfico",
            "recommendations": ["Tráfico fluido esperado"],
        },
        "cloudy": {
            "impact_level": "low",
            "multiplier": 1.1,
            "description": "Leve incremento en precaución de conductores",
            "recommendations": ["Posible lentitud menor en algunas zonas"],
        },
        "rainy": {
            "impact_level": "high",
            "multiplier": 1.4,
            "description": "Lluvia causa reducción de velocidad y aumento de accidentes",
            "recommendations": [
                "Evite zonas propensas a inundación",
                "Considere retrasar viajes no urgentes",
                "Use transporte público cuando sea posible",
            ],
        },
    }
    
    return impacts.get(weather_condition, impacts["clear"])


def calculate_general_status(zones_status: Dict[str, Any]) -> str:
    """
    Calcula el estado general de la ciudad basado en todas las zonas.
    """
    avg_congestion = sum(z["level"] for z in zones_status.values()) / len(zones_status)
    
    if avg_congestion < 0.3:
        return "FLUIDO"
    elif avg_congestion < 0.6:
        return "MODERADO"
    elif avg_congestion < 0.8:
        return "CONGESTIONADO"
    else:
        return "CRÍTICO"
