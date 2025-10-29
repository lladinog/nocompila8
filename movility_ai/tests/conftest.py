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
Configuración de pytest para MovilityAI.
"""

import sys
import os
from pathlib import Path

import pytest

# Agregar el directorio raíz al path para imports
root_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(root_dir))

# Configurar ambiente de testing
os.environ["TESTING"] = "true"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"


@pytest.fixture(scope="session")
def test_data_dir():
    """Directorio para datos de test."""
    return Path(__file__).parent / "data"


@pytest.fixture
def sample_route_data():
    """Datos de ejemplo para tests de rutas."""
    return {
        "origin": "Laureles",
        "destination": "El Poblado",
        "preferred_mode": "metro"
    }


@pytest.fixture
def sample_traffic_data():
    """Datos de ejemplo para tests de tráfico."""
    return {
        "zone": "Laureles",
        "level": "medium",
        "average_speed_kmh": 35.5
    }


@pytest.fixture
def sample_user_profile():
    """Perfil de usuario de ejemplo."""
    return {
        "name": "Test User",
        "preferred_modes": ["metro", "bicicleta"],
        "eco_conscious": True,
        "favorite_zones": ["Laureles", "El Poblado"]
    }


@pytest.fixture
def mock_tool_context():
    """Mock del contexto de herramientas ADK."""
    class MockState:
        """Mock del estado del contexto."""
        pass
    
    class MockToolContext:
        """Mock del contexto de herramientas."""
        def __init__(self):
            self.state = MockState()
    
    return MockToolContext()
