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

"""Constants used in MovilityAI system."""

# Session state keys
SYSTEM_TIME = "_time"
USER_LOCATION = "user_location"
USER_PROFILE = "user_profile"
ROUTE_CONTEXT = "route_context"
TRAFFIC_DATA = "traffic_data"
URBAN_EVENTS = "urban_events"
ECO_METRICS = "eco_metrics"

# Medellín zones and landmarks
MEDELLIN_ZONES = [
    "Laureles",
    "El Poblado",
    "Envigado",
    "Belén",
    "Centro",
    "Estadio",
    "Aranjuez",
    "Castilla",
    "Robledo",
    "Buenos Aires",
    "La Candelaria",
    "Guayabal",
    "Itagüí",
    "Sabaneta",
    "La Estrella",
    "Caldas",
]

# Transport modes
TRANSPORT_MODES = [
    "metro",
    "metrocable",
    "bus",
    "bicicleta",
    "caminando",
    "carro",
    "moto",
    "tranvia",
]

# Traffic levels (for visualization)
TRAFFIC_LEVELS = {
    "low": {"color": "green", "label": "Fluido"},
    "medium": {"color": "yellow", "label": "Moderado"},
    "high": {"color": "orange", "label": "Congestionado"},
    "critical": {"color": "red", "label": "Crítico"},
}

# Event types
EVENT_TYPES = [
    "protesta",
    "accidente",
    "obra_vial",
    "evento_masivo",
    "clima_adverso",
    "cierre_vial",
    "metro_fuera_servicio",
]
