# Copyright 2025 Google LLC
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

"""
🎲 Data Mock Tool - Genera datos simulados coherentes para la demo.

Esta herramienta provee respuestas controladas y realistas para simular:
- APIs de tráfico
- Servicios de rutas
- Datos de clima
- Estado del metro
- Eventos urbanos

Los datos son coherentes entre llamadas y visualmente atractivos.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from movility_ai.shared_libraries.constants import (
    MEDELLIN_ZONES,
    TRANSPORT_MODES,
    TRAFFIC_LEVELS,
    EVENT_TYPES
)


def generate_mock_route(origin: str, destination: str, preferred_mode: str = None) -> Dict[str, Any]:
    """
    Genera una ruta simulada entre dos puntos.
    
    Args:
        origin: Punto de origen
        destination: Punto de destino
        preferred_mode: Modo de transporte preferido
        
    Returns:
        Diccionario con información de la ruta simulada
    """
    modes = [preferred_mode] if preferred_mode else random.sample(TRANSPORT_MODES, 3)
    
    # Generar segmentos de ruta simulados
    segments = []
    total_time = 0
    total_distance = 0
    total_cost = 0
    
    for i, mode in enumerate(modes):
        duration = random.randint(5, 20)
        distance = random.uniform(1.0, 5.0)
        cost = _calculate_mock_cost(mode, distance)
        
        segment = {
            "mode": mode,
            "from_location": origin if i == 0 else f"Punto intermedio {i}",
            "to_location": destination if i == len(modes) - 1 else f"Punto intermedio {i+1}",
            "duration_minutes": duration,
            "distance_km": round(distance, 2),
            "cost_cop": cost,
            "instructions": _generate_instructions(mode, origin, destination)
        }
        segments.append(segment)
        
        total_time += duration
        total_distance += distance
        total_cost += cost
    
    # Calcular eco score basado en los modos utilizados
    eco_score = _calculate_eco_score(modes)
    
    return {
        "origin": {"name": origin, "lat": 6.2442, "lng": -75.5812},
        "destination": {"name": destination, "lat": 6.2308, "lng": -75.5906},
        "segments": segments,
        "total_duration_minutes": total_time,
        "total_distance_km": round(total_distance, 2),
        "total_cost_cop": total_cost,
        "eco_score": eco_score
    }


def generate_mock_traffic(zone: str = None) -> List[Dict[str, Any]]:
    """
    Genera datos simulados de tráfico para una o múltiples zonas.
    
    Args:
        zone: Zona específica (opcional)
        
    Returns:
        Lista de información de tráfico por zona
    """
    zones = [zone] if zone else random.sample(MEDELLIN_ZONES, 8)
    traffic_data = []
    
    for z in zones:
        level = random.choice(list(TRAFFIC_LEVELS.keys()))
        speed = _get_speed_for_level(level)
        
        # Generar algunos incidentes aleatorios
        incidents = []
        if random.random() > 0.7:  # 30% de probabilidad de incidentes
            incidents = [random.choice([
                "Accidente menor reportado",
                "Vía lenta por obras",
                "Alto flujo vehicular",
                "Cierre parcial de carril"
            ])]
        
        traffic_data.append({
            "zone": z,
            "level": level,
            "average_speed_kmh": speed,
            "incidents": incidents,
            "last_updated": datetime.now().isoformat(),
            **TRAFFIC_LEVELS[level]  # Incluye color y label
        })
    
    return traffic_data


def generate_mock_events() -> List[Dict[str, Any]]:
    """
    Genera eventos urbanos simulados.
    
    Returns:
        Lista de eventos urbanos activos
    """
    num_events = random.randint(2, 5)
    events = []
    
    for _ in range(num_events):
        event_type = random.choice(EVENT_TYPES)
        zone = random.choice(MEDELLIN_ZONES)
        
        event = {
            "event_type": event_type,
            "location": {
                "name": zone,
                "lat": 6.2442 + random.uniform(-0.1, 0.1),
                "lng": -75.5812 + random.uniform(-0.1, 0.1)
            },
            "description": _generate_event_description(event_type, zone),
            "severity": random.choice(["low", "medium", "high"]),
            "start_time": (datetime.now() - timedelta(minutes=random.randint(10, 120))).strftime("%H:%M"),
            "affected_zones": [zone] + random.sample([z for z in MEDELLIN_ZONES if z != zone], random.randint(0, 2))
        }
        
        # Algunos eventos tienen tiempo de finalización
        if random.random() > 0.5:
            event["end_time"] = (datetime.now() + timedelta(minutes=random.randint(30, 180))).strftime("%H:%M")
        
        events.append(event)
    
    return events


def generate_mock_eco_metrics(user_trips: int = None) -> Dict[str, Any]:
    """
    Genera métricas ecológicas simuladas.
    
    Args:
        user_trips: Número de viajes realizados (opcional)
        
    Returns:
        Diccionario con métricas ambientales
    """
    trips = user_trips if user_trips else random.randint(10, 50)
    
    return {
        "co2_saved_kg": round(trips * random.uniform(0.5, 2.5), 2),
        "calories_burned": trips * random.randint(50, 200),
        "trees_equivalent": round(trips * random.uniform(0.01, 0.05), 2),
        "eco_score": min(100, trips * random.randint(2, 4)),
        "sustainable_trips": trips
    }


def generate_mock_insights() -> Dict[str, Any]:
    """
    Genera datos de analítica urbana simulados.
    
    Returns:
        Diccionario con datos de analítica
    """
    return {
        "congested_zones": [
            {"zone": "El Poblado", "congestion_level": 85},
            {"zone": "Centro", "congestion_level": 78},
            {"zone": "Laureles", "congestion_level": 65},
            {"zone": "Estadio", "congestion_level": 60},
            {"zone": "Envigado", "congestion_level": 55},
        ],
        "traffic_trend": [
            {"hour": f"{h}:00", "level": random.randint(30, 90)} 
            for h in range(24)
        ],
        "mode_distribution": [
            {"mode": "Metro", "percentage": 35},
            {"mode": "Bus", "percentage": 30},
            {"mode": "Carro", "percentage": 20},
            {"mode": "Bicicleta", "percentage": 10},
            {"mode": "Caminando", "percentage": 5},
        ],
        "summary": f"Datos agregados de las últimas 24 horas. {random.randint(50000, 100000)} viajes analizados."
    }


# Helper functions

def _calculate_mock_cost(mode: str, distance_km: float) -> int:
    """Calcula el costo aproximado según el modo de transporte."""
    costs = {
        "metro": 3200,
        "metrocable": 3200,
        "bus": 2900,
        "tranvia": 3200,
        "bicicleta": 0,
        "caminando": 0,
        "carro": int(distance_km * 2000),  # ~2000 COP por km
        "moto": int(distance_km * 1500),   # ~1500 COP por km
    }
    return costs.get(mode, 0)


def _calculate_eco_score(modes: List[str]) -> int:
    """Calcula una puntuación ecológica basada en los modos de transporte."""
    eco_values = {
        "caminando": 100,
        "bicicleta": 95,
        "metro": 85,
        "metrocable": 85,
        "tranvia": 80,
        "bus": 70,
        "moto": 40,
        "carro": 30,
    }
    scores = [eco_values.get(mode, 50) for mode in modes]
    return int(sum(scores) / len(scores))


def _get_speed_for_level(level: str) -> float:
    """Retorna velocidad promedio según el nivel de tráfico."""
    speeds = {
        "low": random.uniform(40, 60),
        "medium": random.uniform(25, 40),
        "high": random.uniform(15, 25),
        "critical": random.uniform(5, 15),
    }
    return round(speeds.get(level, 30), 1)


def _generate_instructions(mode: str, origin: str, destination: str) -> List[str]:
    """Genera instrucciones paso a paso simuladas."""
    instructions = {
        "metro": [
            f"Dirígete a la estación de metro más cercana",
            f"Toma la línea hacia {destination}",
            f"Bájate en la estación {destination}"
        ],
        "bus": [
            f"Camina hasta el paradero más cercano",
            f"Toma la ruta que va hacia {destination}",
            f"Bájate en {destination}"
        ],
        "bicicleta": [
            f"Sal en bicicleta desde {origin}",
            f"Sigue por la cicloruta principal",
            f"Llega a {destination}"
        ],
        "caminando": [
            f"Camina desde {origin}",
            f"Sigue las indicaciones hacia {destination}",
            f"Llega a tu destino"
        ],
    }
    return instructions.get(mode, [f"Viaja de {origin} a {destination} en {mode}"])


def _generate_event_description(event_type: str, zone: str) -> str:
    """Genera una descripción para un evento urbano."""
    descriptions = {
        "protesta": f"Manifestación pacífica en {zone}. Vías cerradas.",
        "accidente": f"Accidente de tránsito reportado en {zone}.",
        "obra_vial": f"Trabajos de mantenimiento vial en {zone}.",
        "evento_masivo": f"Evento cultural/deportivo en {zone}.",
        "clima_adverso": f"Lluvia fuerte afectando movilidad en {zone}.",
        "cierre_vial": f"Cierre temporal de vía principal en {zone}.",
        "metro_fuera_servicio": f"Servicio de metro suspendido temporalmente en {zone}.",
    }
    return descriptions.get(event_type, f"Evento en {zone}")
