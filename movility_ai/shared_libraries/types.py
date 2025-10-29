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

"""Common data schema and types for MovilityAI agents."""

from typing import Optional, List
from google.genai import types
from pydantic import BaseModel, Field


# Convenient declaration for controlled generation.
json_response_config = types.GenerateContentConfig(
    response_mime_type="application/json"
)


class Location(BaseModel):
    """A geographic location in Medellín."""
    name: str = Field(description="Nombre del lugar, ej: Laureles, El Poblado")
    lat: float = Field(description="Latitud")
    lng: float = Field(description="Longitud")
    zone: Optional[str] = Field(default=None, description="Comuna o zona de Medellín")


class RouteSegment(BaseModel):
    """A segment of a route."""
    mode: str = Field(description="Modo de transporte: metro, bus, bicicleta, etc.")
    from_location: str = Field(description="Punto de inicio del segmento")
    to_location: str = Field(description="Punto final del segmento")
    duration_minutes: int = Field(description="Duración estimada en minutos")
    distance_km: float = Field(description="Distancia en kilómetros")
    cost_cop: int = Field(description="Costo en pesos colombianos")
    instructions: List[str] = Field(description="Instrucciones paso a paso")


class Route(BaseModel):
    """A complete route with multiple segments."""
    origin: Location
    destination: Location
    segments: List[RouteSegment]
    total_duration_minutes: int = Field(description="Duración total del viaje")
    total_distance_km: float = Field(description="Distancia total")
    total_cost_cop: int = Field(description="Costo total")
    eco_score: int = Field(description="Puntuación ecológica (0-100)")


class TrafficInfo(BaseModel):
    """Traffic information for a zone or route."""
    zone: str = Field(description="Zona o corredor vial")
    level: str = Field(description="Nivel de tráfico: low, medium, high, critical")
    average_speed_kmh: float = Field(description="Velocidad promedio en km/h")
    incidents: List[str] = Field(default=[], description="Incidentes reportados")
    last_updated: str = Field(description="Última actualización (timestamp)")


class UrbanEvent(BaseModel):
    """An urban event affecting mobility."""
    event_type: str = Field(description="Tipo de evento: protesta, accidente, obra_vial, etc.")
    location: Location
    description: str = Field(description="Descripción del evento")
    severity: str = Field(description="Severidad: low, medium, high")
    start_time: str = Field(description="Hora de inicio")
    end_time: Optional[str] = Field(default=None, description="Hora estimada de finalización")
    affected_zones: List[str] = Field(description="Zonas afectadas")


class EcoMetrics(BaseModel):
    """Environmental impact metrics."""
    co2_saved_kg: float = Field(description="CO2 ahorrado en kilogramos")
    calories_burned: int = Field(description="Calorías quemadas (si aplica)")
    trees_equivalent: float = Field(description="Equivalente en árboles plantados")
    eco_score: int = Field(description="Puntuación ecológica acumulada (0-100)")
    sustainable_trips: int = Field(description="Número de viajes sostenibles realizados")


class RouteRecommendation(BaseModel):
    """A route recommendation with alternatives."""
    recommended_route: Route
    alternative_routes: List[Route] = Field(default=[], description="Rutas alternativas")
    reasoning: str = Field(description="Razón de la recomendación")


class UserProfile(BaseModel):
    """User profile with preferences."""
    name: str = Field(description="Nombre del usuario")
    preferred_modes: List[str] = Field(description="Modos de transporte preferidos")
    eco_conscious: bool = Field(default=False, description="Si prefiere opciones ecológicas")
    budget_sensitive: bool = Field(default=False, description="Si es sensible al presupuesto")
    favorite_zones: List[str] = Field(default=[], description="Zonas frecuentadas")
