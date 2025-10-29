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

"""Tipos de datos compartidos para MovilityAI"""

from typing import Dict, List, Optional
from pydantic import BaseModel


class Location(BaseModel):
    """Representa una ubicación geográfica"""
    latitude: float
    longitude: float
    address: Optional[str] = None
    name: Optional[str] = None


class TrafficData(BaseModel):
    """Datos de tráfico en tiempo real"""
    location: Location
    congestion_level: float  # 0.0 - 1.0
    average_speed: float  # km/h
    timestamp: str
    metadata: Optional[Dict] = None


class Route(BaseModel):
    """Representa una ruta calculada"""
    origin: Location
    destination: Location
    waypoints: List[Location] = []
    distance_km: float
    duration_minutes: float
    transport_mode: str  # car, transit, walking, bicycle
    traffic_conditions: Optional[str] = None


class AnalysisResult(BaseModel):
    """Resultado de análisis de movilidad"""
    analysis_type: str
    timestamp: str
    data: Dict
    insights: List[str] = []
    recommendations: List[str] = []
