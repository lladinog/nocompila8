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

"""Analytics y visualizaciones para Insight Agent"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import json

# Datos simulados agregados de movilidad (mock para hackathon)
MOBILITY_DATA_MOCK = {
    "daily_trips": 1_250_000,  # Viajes diarios en Medellín
    "avg_trip_duration": 38,  # minutos
    "avg_trip_cost": 3500,  # COP
    "avg_co2_per_trip": 2.5,  # kg
    "public_transport_share": 0.52,  # 52% usa transporte público
    "private_vehicle_share": 0.35,  # 35% vehículo privado
    "active_mobility_share": 0.13,  # 13% bici/caminata
    "peak_morning_hours": (7, 9),
    "peak_evening_hours": (17, 19),
}

ZONE_STATISTICS_MOCK = {
    "centro": {
        "daily_trips": 350000,
        "avg_congestion": 0.68,
        "peak_congestion": 0.85,
        "avg_speed_kmh": 18,
        "main_issues": ["Exceso de vehículos particulares", "Infraestructura vial limitada"],
    },
    "poblado": {
        "daily_trips": 280000,
        "avg_congestion": 0.62,
        "peak_congestion": 0.88,
        "avg_speed_kmh": 22,
        "main_issues": ["Crecimiento urbano acelerado", "Vías de doble sentido limitadas"],
    },
    "autopista_norte": {
        "daily_trips": 420000,
        "avg_congestion": 0.71,
        "peak_congestion": 0.92,
        "avg_speed_kmh": 25,
        "main_issues": ["Corredor principal sobrecargado", "Accidentes frecuentes"],
    },
    "laureles": {
        "daily_trips": 180000,
        "avg_congestion": 0.48,
        "peak_congestion": 0.70,
        "avg_speed_kmh": 28,
        "main_issues": ["Congestión en conectores principales"],
    },
    "av_80": {
        "daily_trips": 390000,
        "avg_congestion": 0.66,
        "peak_congestion": 0.82,
        "avg_speed_kmh": 20,
        "main_issues": ["Tráfico de carga pesada", "Conexión múltiples municipios"],
    },
}


def generate_mobility_dashboard(period_days: int = 30) -> Dict[str, Any]:
    """
    Genera dashboard general de movilidad urbana.
    
    Args:
        period_days: Número de días a analizar (default 30)
    
    Returns:
        Dashboard con KPIs, tendencias y insights
    """
    total_trips = MOBILITY_DATA_MOCK["daily_trips"] * period_days
    
    # Calcular métricas clave
    dashboard = {
        "period": {
            "days": period_days,
            "start_date": (datetime.now() - timedelta(days=period_days)).strftime("%Y-%m-%d"),
            "end_date": datetime.now().strftime("%Y-%m-%d"),
        },
        "kpis": {
            "total_trips": total_trips,
            "daily_avg_trips": MOBILITY_DATA_MOCK["daily_trips"],
            "avg_trip_duration_min": MOBILITY_DATA_MOCK["avg_trip_duration"],
            "avg_trip_cost_cop": MOBILITY_DATA_MOCK["avg_trip_cost"],
            "avg_co2_per_trip_kg": MOBILITY_DATA_MOCK["avg_co2_per_trip"],
            "total_co2_tons": round(total_trips * MOBILITY_DATA_MOCK["avg_co2_per_trip"] / 1000, 2),
        },
        "modal_split": {
            "public_transport": {
                "percentage": MOBILITY_DATA_MOCK["public_transport_share"] * 100,
                "trips": int(total_trips * MOBILITY_DATA_MOCK["public_transport_share"]),
            },
            "private_vehicle": {
                "percentage": MOBILITY_DATA_MOCK["private_vehicle_share"] * 100,
                "trips": int(total_trips * MOBILITY_DATA_MOCK["private_vehicle_share"]),
            },
            "active_mobility": {
                "percentage": MOBILITY_DATA_MOCK["active_mobility_share"] * 100,
                "trips": int(total_trips * MOBILITY_DATA_MOCK["active_mobility_share"]),
            },
        },
        "peak_hours": {
            "morning": f"{MOBILITY_DATA_MOCK['peak_morning_hours'][0]}:00 - {MOBILITY_DATA_MOCK['peak_morning_hours'][1]}:00",
            "evening": f"{MOBILITY_DATA_MOCK['peak_evening_hours'][0]}:00 - {MOBILITY_DATA_MOCK['peak_evening_hours'][1]}:00",
        },
        "top_critical_zones": analyze_critical_zones(limit=5),
        "trends": {
            "congestion_trend": "Incremento del 8% vs mes anterior",
            "public_transport_trend": "Estable (+2%)",
            "sustainability_trend": "Mejora leve en movilidad activa (+5%)",
        },
        "key_insights": [
            "La Autopista Norte concentra el 34% del tráfico vehicular de la ciudad",
            "El uso de bicicleta aumentó 15% en zonas con nueva infraestructura de ciclorrutas",
            "Las horas pico se extienden 30 min más que hace 5 años",
            "El 68% de la congestión es evitable con mejor distribución modal",
        ],
        "recommendations": [
            "Implementar carriles exclusivos de bus en corredores críticos",
            "Expandir red de ciclorrutas para conectar zonas de alta demanda",
            "Fomentar teletrabajo en horas pico (políticas públicas)",
            "Optimizar semáforos inteligentes en zonas críticas",
        ],
    }
    
    return dashboard


def analyze_critical_zones(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Identifica y analiza las zonas más críticas de la ciudad.
    
    Args:
        limit: Número máximo de zonas a retornar
    
    Returns:
        Lista de zonas ordenadas por criticidad
    """
    zones_with_score = []
    
    for zone_id, data in ZONE_STATISTICS_MOCK.items():
        # Score de criticidad (mayor congestión + más viajes = más crítico)
        criticality_score = (data["avg_congestion"] * 0.5 + data["peak_congestion"] * 0.5) * (data["daily_trips"] / 100000)
        
        zones_with_score.append({
            "zone_id": zone_id,
            "name": zone_id.replace("_", " ").title(),
            "criticality_score": round(criticality_score, 2),
            "daily_trips": data["daily_trips"],
            "avg_congestion_pct": round(data["avg_congestion"] * 100, 1),
            "peak_congestion_pct": round(data["peak_congestion"] * 100, 1),
            "avg_speed_kmh": data["avg_speed_kmh"],
            "main_issues": data["main_issues"],
        })
    
    # Ordenar por criticidad
    zones_with_score.sort(key=lambda x: x["criticality_score"], reverse=True)
    
    return zones_with_score[:limit]


def generate_temporal_analysis(zone: Optional[str] = None) -> Dict[str, Any]:
    """
    Genera análisis de patrones temporales de tráfico.
    
    Args:
        zone: Zona específica o None para toda la ciudad
    
    Returns:
        Análisis temporal detallado
    """
    # Distribución horaria simplificada (mock)
    hourly_distribution = {}
    for hour in range(24):
        if 7 <= hour <= 9 or 17 <= hour <= 19:
            traffic_level = "high"
            volume_pct = 85
        elif 10 <= hour <= 16:
            traffic_level = "medium"
            volume_pct = 55
        elif 20 <= hour <= 23 or 6 <= hour < 7:
            traffic_level = "low"
            volume_pct = 35
        else:
            traffic_level = "very_low"
            volume_pct = 15
        
        hourly_distribution[hour] = {
            "traffic_level": traffic_level,
            "volume_percentage": volume_pct,
        }
    
    # Distribución semanal
    weekly_pattern = {
        "monday": {"volume_index": 100, "note": "Día más congestionado de la semana"},
        "tuesday": {"volume_index": 98, "note": "Similar a lunes"},
        "wednesday": {"volume_index": 96, "note": "Leve descenso"},
        "thursday": {"volume_index": 97, "note": "Repunte"},
        "friday": {"volume_index": 105, "note": "Pico semanal (salida de ciudad)"},
        "saturday": {"volume_index": 65, "note": "Tráfico enfocado en zonas comerciales"},
        "sunday": {"volume_index": 50, "note": "Menor volumen de la semana"},
    }
    
    return {
        "zone": zone or "Toda la ciudad",
        "hourly_distribution": hourly_distribution,
        "weekly_pattern": weekly_pattern,
        "peak_hours_detail": {
            "morning_peak": {
                "hours": "7:00 - 9:00",
                "avg_duration_min": 120,
                "main_direction": "Hacia centro y sur (zonas laborales)",
            },
            "evening_peak": {
                "hours": "17:00 - 19:30",
                "avg_duration_min": 150,
                "main_direction": "Hacia norte y occidente (zonas residenciales)",
            },
        },
        "insights": [
            "El pico vespertino dura 30 minutos más que el matutino",
            "Los viernes la congestión aumenta 20% por salida hacia municipios cercanos",
            "Entre 10am-3pm hay ventana de oportunidad para movilidad",
        ],
    }


def calculate_sustainability_metrics(period_days: int = 30) -> Dict[str, Any]:
    """
    Calcula métricas de sostenibilidad del sistema de movilidad.
    
    Args:
        period_days: Período de análisis en días
    
    Returns:
        Métricas ambientales y de sostenibilidad
    """
    total_trips = MOBILITY_DATA_MOCK["daily_trips"] * period_days
    
    # Emisiones por modo de transporte (kg CO2 por viaje)
    co2_by_mode = {
        "private_vehicle": 4.2,
        "public_transport": 0.8,
        "active_mobility": 0.0,
    }
    
    # Calcular emisiones totales
    emissions = {}
    for mode, share_key in [
        ("private_vehicle", "private_vehicle_share"),
        ("public_transport", "public_transport_share"),
        ("active_mobility", "active_mobility_share"),
    ]:
        trips = total_trips * MOBILITY_DATA_MOCK[share_key]
        co2_tons = (trips * co2_by_mode[mode]) / 1000
        emissions[mode] = {
            "trips": int(trips),
            "co2_tons": round(co2_tons, 2),
            "co2_per_trip_kg": co2_by_mode[mode],
        }
    
    total_co2_tons = sum(e["co2_tons"] for e in emissions.values())
    
    # Calcular potencial de mejora
    if MOBILITY_DATA_MOCK["private_vehicle_share"] > 0.25:
        # Simular escenario optimizado (25% menos autos particulares)
        improved_private = MOBILITY_DATA_MOCK["private_vehicle_share"] * 0.75
        improved_public = MOBILITY_DATA_MOCK["public_transport_share"] + (MOBILITY_DATA_MOCK["private_vehicle_share"] - improved_private)
        
        potential_co2_reduction = (
            total_trips * (MOBILITY_DATA_MOCK["private_vehicle_share"] - improved_private) * (co2_by_mode["private_vehicle"] - co2_by_mode["public_transport"])
        ) / 1000
    else:
        potential_co2_reduction = 0
    
    return {
        "period_days": period_days,
        "total_trips": total_trips,
        "emissions_by_mode": emissions,
        "total_emissions_tons": round(total_co2_tons, 2),
        "avg_emissions_per_trip_kg": round(total_co2_tons * 1000 / total_trips, 2),
        "sustainability_score": round((MOBILITY_DATA_MOCK["public_transport_share"] + MOBILITY_DATA_MOCK["active_mobility_share"]) * 100, 1),
        "potential_improvements": {
            "co2_reduction_tons": round(potential_co2_reduction, 2),
            "percentage_reduction": round((potential_co2_reduction / total_co2_tons) * 100, 1),
            "scenario": "Transferir 25% de viajes en auto particular a transporte público",
        },
        "benchmarks": {
            "current_vs_goal": "Medellín está 15% por debajo de la meta de sostenibilidad 2030",
            "regional_comparison": "Mejor que Bogotá (48% TP) pero inferior a Curitiba (75% TP)",
        },
        "recommendations": [
            "Incentivar uso de metro y metrocable con tarifas preferenciales",
            "Restricción vehicular ampliada en zonas críticas",
            "Subsidios para conversión a vehículos eléctricos",
        ],
    }


def generate_comparative_report(
    zone_a: str,
    zone_b: str,
    metric: str = "congestion"
) -> Dict[str, Any]:
    """
    Genera reporte comparativo entre dos zonas o períodos.
    
    Args:
        zone_a: Primera zona a comparar
        zone_b: Segunda zona a comparar
        metric: Métrica a comparar (congestion, trips, speed)
    
    Returns:
        Reporte comparativo
    """
    if zone_a not in ZONE_STATISTICS_MOCK or zone_b not in ZONE_STATISTICS_MOCK:
        return {"error": "Una o ambas zonas no encontradas"}
    
    data_a = ZONE_STATISTICS_MOCK[zone_a]
    data_b = ZONE_STATISTICS_MOCK[zone_b]
    
    comparison = {
        "zone_a": {"id": zone_a, "name": zone_a.replace("_", " ").title()},
        "zone_b": {"id": zone_b, "name": zone_b.replace("_", " ").title()},
        "metric": metric,
    }
    
    if metric == "congestion":
        comparison["results"] = {
            "zone_a_avg": round(data_a["avg_congestion"] * 100, 1),
            "zone_b_avg": round(data_b["avg_congestion"] * 100, 1),
            "difference_pct": round((data_a["avg_congestion"] - data_b["avg_congestion"]) * 100, 1),
            "winner": zone_a if data_a["avg_congestion"] < data_b["avg_congestion"] else zone_b,
        }
    elif metric == "trips":
        comparison["results"] = {
            "zone_a_trips": data_a["daily_trips"],
            "zone_b_trips": data_b["daily_trips"],
            "difference": data_a["daily_trips"] - data_b["daily_trips"],
            "percentage_diff": round(((data_a["daily_trips"] - data_b["daily_trips"]) / data_b["daily_trips"]) * 100, 1),
        }
    elif metric == "speed":
        comparison["results"] = {
            "zone_a_speed_kmh": data_a["avg_speed_kmh"],
            "zone_b_speed_kmh": data_b["avg_speed_kmh"],
            "difference_kmh": data_a["avg_speed_kmh"] - data_b["avg_speed_kmh"],
            "faster_zone": zone_a if data_a["avg_speed_kmh"] > data_b["avg_speed_kmh"] else zone_b,
        }
    
    return comparison


def detect_anomalies(zone: Optional[str] = None, threshold: float = 0.3) -> List[Dict[str, Any]]:
    """
    Detecta patrones anómalos en los datos de movilidad.
    
    Args:
        zone: Zona específica o None para toda la ciudad
        threshold: Umbral de desviación para considerar anomalía (0-1)
    
    Returns:
        Lista de anomalías detectadas
    """
    # Mock de anomalías detectadas
    anomalies = [
        {
            "type": "congestion_spike",
            "zone": "poblado",
            "timestamp": "2025-10-29T14:30:00",
            "severity": "high",
            "description": "Congestión 45% superior a la media para esta hora",
            "possible_cause": "Evento especial no reportado o accidente",
        },
        {
            "type": "low_public_transport_usage",
            "zone": "centro",
            "timestamp": "2025-10-29T08:00:00",
            "severity": "medium",
            "description": "Uso de metro 20% inferior al esperado",
            "possible_cause": "Falla técnica o retrasos no reportados",
        },
        {
            "type": "unusual_pattern",
            "zone": "autopista_norte",
            "timestamp": "2025-10-29T03:00:00",
            "severity": "low",
            "description": "Tráfico nocturno inusualmente alto",
            "possible_cause": "Transporte de carga o evento nocturno",
        },
    ]
    
    if zone:
        anomalies = [a for a in anomalies if a["zone"] == zone]
    
    return anomalies
