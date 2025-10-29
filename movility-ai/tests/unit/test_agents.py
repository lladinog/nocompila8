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

"""Unit tests for all MovilityAI agents - siguiendo TDD."""

import pytest


class TestRootAgent:
    """Tests for the Root Agent (orchestrator)."""
    
    def test_root_agent_exists(self):
        """Verifica que el root_agent está correctamente definido."""
        from movility_ai.agent import root_agent
        
        assert root_agent is not None
        assert root_agent.name == "root_agent"
        assert "mobility" in root_agent.description.lower() or "movility" in root_agent.description.lower()
    
    def test_root_agent_has_all_subagents(self):
        """Verifica que el root_agent tiene todos los sub-agentes configurados."""
        from movility_ai.agent import root_agent
        
        assert len(root_agent.sub_agents) == 4, "Debe tener 4 sub-agentes"
        
        agent_names = [agent.name for agent in root_agent.sub_agents]
        assert "ingest_agent" in agent_names
        assert "clean_agent" in agent_names
        assert "analyze_agent" in agent_names
        assert "report_agent" in agent_names


class TestIngestAgent:
    """Tests for the Ingest Agent."""
    
    def test_ingest_agent_exists(self):
        """Verifica que el IngestAgent está correctamente definido."""
        from movility_ai.sub_agents.ingest.agent import ingest_agent
        
        assert ingest_agent is not None
        assert ingest_agent.name == "ingest_agent"
    
    def test_ingest_agent_description(self):
        """Verifica la descripción del agente."""
        from movility_ai.sub_agents.ingest.agent import ingest_agent
        
        description_lower = ingest_agent.description.lower()
        assert "traffic" in description_lower or "data" in description_lower


class TestCleanAgent:
    """Tests for the Clean Agent."""
    
    def test_clean_agent_exists(self):
        """Verifica que el CleanAgent está correctamente definido."""
        from movility_ai.sub_agents.clean.agent import clean_agent
        
        assert clean_agent is not None
        assert clean_agent.name == "clean_agent"
    
    def test_clean_agent_description(self):
        """Verifica la descripción del agente."""
        from movility_ai.sub_agents.clean.agent import clean_agent
        
        description_lower = clean_agent.description.lower()
        assert "clean" in description_lower or "validat" in description_lower or "standard" in description_lower


class TestAnalyzeAgent:
    """Tests for the Analyze Agent."""
    
    def test_analyze_agent_exists(self):
        """Verifica que el AnalyzeAgent está correctamente definido."""
        from movility_ai.sub_agents.analyze.agent import analyze_agent
        
        assert analyze_agent is not None
        assert analyze_agent.name == "analyze_agent"
    
    def test_analyze_agent_description(self):
        """Verifica la descripción del agente."""
        from movility_ai.sub_agents.analyze.agent import analyze_agent
        
        description_lower = analyze_agent.description.lower()
        assert "analy" in description_lower or "pattern" in description_lower or "insight" in description_lower


class TestReportAgent:
    """Tests for the Report Agent."""
    
    def test_report_agent_exists(self):
        """Verifica que el ReportAgent está correctamente definido."""
        from movility_ai.sub_agents.report.agent import report_agent
        
        assert report_agent is not None
        assert report_agent.name == "report_agent"
    
    def test_report_agent_description(self):
        """Verifica la descripción del agente."""
        from movility_ai.sub_agents.report.agent import report_agent
        
        description_lower = report_agent.description.lower()
        assert "report" in description_lower or "summar" in description_lower or "document" in description_lower


class TestAgentIntegration:
    """Integration tests for agent coordination."""
    
    def test_all_agents_importable(self):
        """Verifica que todos los agentes se pueden importar sin errores."""
        from movility_ai.agent import root_agent
        from movility_ai.sub_agents.ingest.agent import ingest_agent
        from movility_ai.sub_agents.clean.agent import clean_agent
        from movility_ai.sub_agents.analyze.agent import analyze_agent
        from movility_ai.sub_agents.report.agent import report_agent
        
        assert root_agent is not None
        assert ingest_agent is not None
        assert clean_agent is not None
        assert analyze_agent is not None
        assert report_agent is not None
    
    def test_agent_names_are_unique(self):
        """Verifica que todos los agentes tienen nombres únicos."""
        from movility_ai.agent import root_agent
        
        agent_names = [agent.name for agent in root_agent.sub_agents]
        assert len(agent_names) == len(set(agent_names)), "Los nombres de agentes deben ser únicos"


class TestSharedTypes:
    """Tests for shared data types."""
    
    def test_location_type_exists(self):
        """Verifica que el tipo Location está definido."""
        from movility_ai.shared_libraries.types import Location
        
        # Test de creación de Location
        location = Location(latitude=4.6097, longitude=-74.0817, name="Bogotá")
        assert location.latitude == 4.6097
        assert location.longitude == -74.0817
        assert location.name == "Bogotá"
    
    def test_traffic_data_type_exists(self):
        """Verifica que el tipo TrafficData está definido."""
        from movility_ai.shared_libraries.types import TrafficData, Location
        
        location = Location(latitude=4.6097, longitude=-74.0817)
        traffic_data = TrafficData(
            location=location,
            congestion_level=0.5,
            average_speed=30.0,
            timestamp="2025-10-29T10:00:00Z"
        )
        assert traffic_data.congestion_level == 0.5
        assert traffic_data.average_speed == 30.0
    
    def test_route_type_exists(self):
        """Verifica que el tipo Route está definido."""
        from movility_ai.shared_libraries.types import Route, Location
        
        origin = Location(latitude=4.6097, longitude=-74.0817, name="Origin")
        destination = Location(latitude=4.6500, longitude=-74.1000, name="Destination")
        
        route = Route(
            origin=origin,
            destination=destination,
            distance_km=10.5,
            duration_minutes=25,
            transport_mode="car"
        )
        assert route.distance_km == 10.5
        assert route.transport_mode == "car"
    
    def test_analysis_result_type_exists(self):
        """Verifica que el tipo AnalysisResult está definido."""
        from movility_ai.shared_libraries.types import AnalysisResult
        
        analysis = AnalysisResult(
            analysis_type="congestion_analysis",
            timestamp="2025-10-29T10:00:00Z",
            data={"avg_speed": 30.5, "congestion": 0.6},
            insights=["High congestion detected"],
            recommendations=["Use alternative route"]
        )
        assert analysis.analysis_type == "congestion_analysis"
        assert len(analysis.insights) == 1
        assert len(analysis.recommendations) == 1
