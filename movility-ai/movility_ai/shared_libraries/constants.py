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

"""Constantes compartidas del sistema MovilityAI"""

# Configuración de APIs
GOOGLE_MAPS_API_VERSION = "v1"
MOOVIT_API_VERSION = "v1"

# Configuración de modelos
DEFAULT_MODEL = "gemini-2.5-flash"

# Límites y umbrales
MAX_ROUTE_ALTERNATIVES = 5
CONGESTION_THRESHOLD_HIGH = 0.7
CONGESTION_THRESHOLD_MEDIUM = 0.4

# Estados del sistema
STATUS_ACTIVE = "active"
STATUS_ERROR = "error"
STATUS_COMPLETED = "completed"
