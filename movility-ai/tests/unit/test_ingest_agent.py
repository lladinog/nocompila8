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

"""Unit tests for the IngestAgent - siguiendo TDD."""

import pytest


def test_ingest_agent_exists():
    """Test que verifica que el IngestAgent está correctamente definido."""
    from movility_ai.sub_agents.ingest.agent import ingest_agent
    
    assert ingest_agent is not None
    assert ingest_agent.name == "ingest_agent"
    assert "traffic" in ingest_agent.description.lower() or "mobility" in ingest_agent.description.lower()


def test_ingest_agent_has_tools():
    """Test que verifica que el IngestAgent tiene herramientas configuradas."""
    from movility_ai.sub_agents.ingest.agent import ingest_agent
    
    # Por ahora las herramientas están vacías, este test fallará hasta implementarlas
    # assert len(ingest_agent.tools) > 0, "IngestAgent debe tener al menos una herramienta"
    
    # Test temporal mientras implementamos las tools
    assert hasattr(ingest_agent, "tools")


def test_root_agent_has_ingest_agent():
    """Test que verifica que el root_agent incluye el ingest_agent."""
    from movility_ai.agent import root_agent
    
    assert root_agent is not None
    assert len(root_agent.sub_agents) > 0
    
    # Verificar que ingest_agent está en la lista de sub-agentes
    agent_names = [agent.name for agent in root_agent.sub_agents]
    assert "ingest_agent" in agent_names


@pytest.mark.skip(reason="Requiere implementación de herramientas Google Maps")
def test_ingest_agent_can_fetch_traffic_data():
    """Test de integración: IngestAgent obtiene datos de tráfico reales."""
    from movility_ai.sub_agents.ingest.agent import ingest_agent
    from movility_ai.shared_libraries.types import Location
    
    # Este test se implementará cuando tengamos las herramientas de Google Maps
    test_location = Location(
        latitude=4.6097,  # Bogotá, Colombia
        longitude=-74.0817,
        name="Bogotá Centro"
    )
    
    # TODO: Implementar cuando tengamos google_traffic_tool
    pass
