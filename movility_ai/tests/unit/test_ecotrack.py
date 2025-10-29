"""
Tests para EcoTrack Agent (Eco Metrics & Sustainability)
🔴 RED Phase: Estos tests deben fallar hasta implementar el agente
"""

import pytest


class TestEcoTrackAgent:
    """Tests para la estructura y funcionalidad del EcoTrack Agent"""
    
    def test_ecotrack_agent_exists(self):
        """Verificar que el agente EcoTrack existe"""
        from movility_ai.sub_agents.ecotrack.agent import ecotrack_agent
        
        assert ecotrack_agent is not None
        assert ecotrack_agent.name == "ecotrack_agent"
    
    def test_ecotrack_agent_has_tools(self):
        """Verificar que EcoTrack tiene las herramientas necesarias"""
        from movility_ai.sub_agents.ecotrack.agent import ecotrack_agent
        
        assert len(ecotrack_agent.tools) >= 2
        tool_names = [tool.__name__ for tool in ecotrack_agent.tools]
        assert "calculate_eco_metrics_tool" in tool_names
        assert "generate_eco_dashboard_tool" in tool_names
    
    def test_ecotrack_agent_has_instructions(self):
        """Verificar que EcoTrack tiene instrucciones definidas"""
        from movility_ai.sub_agents.ecotrack.prompt import ECOTRACK_AGENT_INSTR
        
        assert ECOTRACK_AGENT_INSTR is not None
        assert len(ECOTRACK_AGENT_INSTR) > 100
        assert "eco" in ECOTRACK_AGENT_INSTR.lower() or "sostenib" in ECOTRACK_AGENT_INSTR.lower()


class TestCalculateEcoMetricsTool:
    """Tests para la herramienta de cálculo de métricas ecológicas"""
    
    def test_calculate_eco_metrics_returns_data(self, mock_tool_context):
        """Verificar que calculate_eco_metrics devuelve métricas"""
        from movility_ai.sub_agents.ecotrack.tools import calculate_eco_metrics
        
        result = calculate_eco_metrics(
            transport_mode="bicicleta",
            distance_km=5.0,
            tool_context=mock_tool_context
        )
        
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 50
    
    def test_calculate_eco_metrics_includes_co2(self, mock_tool_context):
        """Verificar que incluye datos de CO2"""
        from movility_ai.sub_agents.ecotrack.tools import calculate_eco_metrics
        
        result = calculate_eco_metrics(
            transport_mode="metro",
            distance_km=10.0,
            tool_context=mock_tool_context
        )
        
        assert "co2" in result.lower() or "carbono" in result.lower()
    
    def test_calculate_eco_metrics_includes_calories(self, mock_tool_context):
        """Verificar que incluye calorías para modos activos"""
        from movility_ai.sub_agents.ecotrack.tools import calculate_eco_metrics
        
        result = calculate_eco_metrics(
            transport_mode="bicicleta",
            distance_km=5.0,
            tool_context=mock_tool_context
        )
        
        assert "calor" in result.lower() or "ejercicio" in result.lower()
    
    def test_calculate_eco_metrics_compares_modes(self, mock_tool_context):
        """Verificar que compara diferentes modos de transporte"""
        from movility_ai.sub_agents.ecotrack.tools import calculate_eco_metrics
        
        result = calculate_eco_metrics(
            transport_mode="carro",
            distance_km=10.0,
            tool_context=mock_tool_context
        )
        
        # Debe sugerir alternativas más ecológicas
        eco_modes = ["metro", "bicicleta", "caminando", "transporte público"]
        assert any(mode in result.lower() for mode in eco_modes)
    
    def test_calculate_eco_metrics_saves_to_context(self, mock_tool_context):
        """Verificar que guarda métricas en el contexto"""
        from movility_ai.sub_agents.ecotrack.tools import calculate_eco_metrics
        
        calculate_eco_metrics(
            transport_mode="bicicleta",
            distance_km=5.0,
            tool_context=mock_tool_context
        )
        
        assert hasattr(mock_tool_context.state, "last_eco_metrics")


class TestEcoDashboardTool:
    """Tests para la herramienta de dashboard ecológico"""
    
    def test_generate_eco_dashboard_returns_visualization(self, mock_tool_context):
        """Verificar que genera visualización del dashboard"""
        from movility_ai.sub_agents.ecotrack.tools import generate_eco_dashboard
        
        result = generate_eco_dashboard(user_trips=5, tool_context=mock_tool_context)
        
        assert result is not None
        assert "{" in result or "**" in result
    
    def test_generate_eco_dashboard_includes_icons(self, mock_tool_context):
        """Verificar que incluye iconos visuales"""
        from movility_ai.sub_agents.ecotrack.tools import generate_eco_dashboard
        
        result = generate_eco_dashboard(user_trips=10, tool_context=mock_tool_context)
        
        # Debe incluir emojis ecológicos
        eco_icons = ["🌱", "🌳", "♻️", "🚴", "🌍", "💚"]
        assert any(icon in result for icon in eco_icons)
    
    def test_generate_eco_dashboard_shows_progress(self, mock_tool_context):
        """Verificar que muestra progreso del usuario"""
        from movility_ai.sub_agents.ecotrack.tools import generate_eco_dashboard
        
        result = generate_eco_dashboard(user_trips=15, tool_context=mock_tool_context)
        
        # Debe mostrar algún tipo de progreso o logros
        progress_indicators = ["logro", "meta", "progreso", "impacto", "ahorro"]
        assert any(indicator in result.lower() for indicator in progress_indicators)


class TestEcoTrackIntegration:
    """Tests de integración con el sistema completo"""
    
    def test_ecotrack_registered_in_root_agent(self):
        """Verificar que EcoTrack está registrado en el agente raíz"""
        from movility_ai.agent import root_agent
        
        sub_agent_names = [agent.name for agent in root_agent.sub_agents]
        assert "ecotrack_agent" in sub_agent_names
    
    def test_ecotrack_mock_agent_works(self):
        """Verificar que MockAgent funciona para testing"""
        from movility_ai.sub_agents.ecotrack.agent import MockAgent
        
        mock_agent = MockAgent(name="test_ecotrack", tools=[], model="test")
        
        assert mock_agent.name == "test_ecotrack"
        assert mock_agent.model == "test"
        assert mock_agent.tools == []
