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
🎨 Visualizer Tool - Genera visualizaciones para el sistema MovilityAI.

Esta herramienta crea representaciones visuales de:
- Mapas de rutas
- Gráficos de tráfico (mapas de calor)
- Dashboards de métricas
- Alertas urbanas con pines en mapa

Para la demo de la hackathon, genera datos estructurados en JSON
que pueden ser interpretados visualmente por la interfaz del ADK.
"""

import json
from typing import Dict, Any, List


def generate_route_map(origin: str, destination: str, segments: List[Dict]) -> str:
    """
    Genera un mapa visual de una ruta.
    
    Args:
        origin: Punto de origen
        destination: Punto de destino
        segments: Lista de segmentos de la ruta
        
    Returns:
        JSON string con la representación visual de la ruta
    """
    route_visualization = {
        "type": "route_map",
        "title": f"🗺️ Ruta: {origin} → {destination}",
        "map_data": {
            "origin": origin,
            "destination": destination,
            "segments": segments,
            "markers": [
                {"type": "start", "location": origin, "icon": "🟢"},
                {"type": "end", "location": destination, "icon": "🔴"},
            ]
        },
        "visual_style": {
            "line_color": "#4285F4",
            "line_width": 3,
            "animation": "path_trace"
        }
    }
    
    return json.dumps(route_visualization, indent=2, ensure_ascii=False)


def generate_traffic_heatmap(zone_data: List[Dict]) -> str:
    """
    Genera un mapa de calor de tráfico.
    
    Args:
        zone_data: Lista de zonas con información de tráfico
        
    Returns:
        JSON string con el mapa de calor
    """
    heatmap = {
        "type": "traffic_heatmap",
        "title": "🚦 Mapa de Tráfico en Tiempo Real",
        "zones": zone_data,
        "legend": {
            "low": {"color": "#4CAF50", "label": "Fluido", "icon": "🟢"},
            "medium": {"color": "#FFC107", "label": "Moderado", "icon": "🟡"},
            "high": {"color": "#FF9800", "label": "Congestionado", "icon": "🟠"},
            "critical": {"color": "#F44336", "label": "Crítico", "icon": "🔴"}
        },
        "last_updated": "Hace 2 minutos"
    }
    
    return json.dumps(heatmap, indent=2, ensure_ascii=False)


def generate_eco_dashboard(metrics: Dict[str, Any]) -> str:
    """
    Genera un dashboard de métricas ecológicas.
    
    Args:
        metrics: Diccionario con métricas ambientales
        
    Returns:
        JSON string con el dashboard
    """
    dashboard = {
        "type": "eco_dashboard",
        "title": "🌱 Tu Impacto Ambiental",
        "metrics": [
            {
                "name": "CO2 Ahorrado",
                "value": metrics.get("co2_saved_kg", 0),
                "unit": "kg",
                "icon": "🌍",
                "color": "#4CAF50"
            },
            {
                "name": "Calorías Quemadas",
                "value": metrics.get("calories_burned", 0),
                "unit": "kcal",
                "icon": "🔥",
                "color": "#FF5722"
            },
            {
                "name": "Equivalente en Árboles",
                "value": metrics.get("trees_equivalent", 0),
                "unit": "árboles",
                "icon": "🌳",
                "color": "#8BC34A"
            },
            {
                "name": "Puntuación Eco",
                "value": metrics.get("eco_score", 0),
                "unit": "/100",
                "icon": "⭐",
                "color": "#FFC107"
            }
        ],
        "achievements": [
            "🏆 Eco-Warrior: 10 viajes sostenibles",
            "🚴 Ciclista Urbano: 50km en bicicleta",
            "🚇 Metro Master: 20 viajes en metro"
        ],
        "charts": {
            "type": "progress_ring",
            "value": metrics.get("eco_score", 0),
            "max": 100
        }
    }
    
    return json.dumps(dashboard, indent=2, ensure_ascii=False)


def generate_event_alerts(events: List[Dict]) -> str:
    """
    Genera alertas visuales de eventos urbanos.
    
    Args:
        events: Lista de eventos urbanos
        
    Returns:
        JSON string con las alertas visualizadas
    """
    alerts = {
        "type": "event_alerts",
        "title": "⚠️ Alertas Urbanas Activas",
        "events": [],
        "map_markers": []
    }
    
    for event in events:
        alert = {
            "severity": event.get("severity", "medium"),
            "type": event.get("event_type", "general"),
            "location": event.get("location", ""),
            "description": event.get("description", ""),
            "icon": _get_event_icon(event.get("event_type")),
            "time": event.get("start_time", "Ahora")
        }
        alerts["events"].append(alert)
        
        # Agregar marcador al mapa
        alerts["map_markers"].append({
            "location": event.get("location", ""),
            "icon": _get_event_icon(event.get("event_type")),
            "popup": event.get("description", "")
        })
    
    return json.dumps(alerts, indent=2, ensure_ascii=False)


def _get_event_icon(event_type: str) -> str:
    """Retorna el icono apropiado para cada tipo de evento."""
    icons = {
        "protesta": "✊",
        "accidente": "🚨",
        "obra_vial": "🚧",
        "evento_masivo": "🎉",
        "clima_adverso": "⛈️",
        "cierre_vial": "🚫",
        "metro_fuera_servicio": "🚇❌"
    }
    return icons.get(event_type, "📍")


def generate_insight_chart(data: Dict[str, Any]) -> str:
    """
    Genera gráficos de analítica urbana.
    
    Args:
        data: Datos de analítica
        
    Returns:
        JSON string con los gráficos
    """
    chart = {
        "type": "analytics_dashboard",
        "title": "📊 Analítica de Movilidad Urbana",
        "charts": [
            {
                "chart_type": "bar",
                "title": "Zonas más Congestionadas",
                "data": data.get("congested_zones", []),
                "color": "#FF5722"
            },
            {
                "chart_type": "line",
                "title": "Tendencia de Tráfico (24h)",
                "data": data.get("traffic_trend", []),
                "color": "#2196F3"
            },
            {
                "chart_type": "pie",
                "title": "Distribución Modal",
                "data": data.get("mode_distribution", []),
                "colors": ["#4CAF50", "#2196F3", "#FFC107", "#FF5722"]
            }
        ],
        "summary": data.get("summary", "Datos agregados de la última hora")
    }
    
    return json.dumps(chart, indent=2, ensure_ascii=False)
