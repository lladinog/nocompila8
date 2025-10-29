"""
Tests para Insight Agent (City Analytics & Trends)
🔴 RED Phase: Estos tests deben fallar hasta implementar el agente
"""

import pytest


class TestInsightAgent:
    """Tests para la estructura y funcionalidad del Insight Agent"""
    
    def test_insight_agent_exists(self):
        """Verificar que el agente Insight existe"""
        from movility_ai.sub_agents.insight.agent import insight_agent
        
        assert insight_agent is not None
        assert insight_agent.name == "insight_agent"
    
    def test_insight_agent_has_tools(self):
        """Verificar que Insight tiene las herramientas necesarias"""
        from movility_ai.sub_agents.insight.agent import insight_agent
        
        assert len(insight_agent.tools) >= 2
        tool_names = [tool.__name__ for tool in insight_agent.tools]
        assert "generate_city_insights_tool" in tool_names
        assert "generate_insight_chart_tool" in tool_names
    
    def test_insight_agent_has_instructions(self):
        """Verificar que Insight tiene instrucciones definidas"""
        from movility_ai.sub_agents.insight.prompt import INSIGHT_AGENT_INSTR
        
        assert INSIGHT_AGENT_INSTR is not None
        assert len(INSIGHT_AGENT_INSTR) > 100
        assert "analítica" in INSIGHT_AGENT_INSTR.lower() or "insight" in INSIGHT_AGENT_INSTR.lower()


class TestGenerateCityInsightsTool:
    """Tests para la herramienta de generación de insights"""
    
    def test_generate_city_insights_returns_data(self, mock_tool_context):
        """Verificar que generate_city_insights devuelve insights"""
        from movility_ai.sub_agents.insight.tools import generate_city_insights
        
        result = generate_city_insights(time_period="week", tool_context=mock_tool_context)
        
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 100
    
    def test_generate_city_insights_includes_patterns(self, mock_tool_context):
        """Verificar que incluye patrones de movilidad"""
        from movility_ai.sub_agents.insight.tools import generate_city_insights
        
        result = generate_city_insights(time_period="month", tool_context=mock_tool_context)
        
        # Debe mencionar patrones o tendencias
        pattern_keywords = ["patrón", "tendencia", "pico", "hora", "zona", "popular"]
        assert any(keyword in result.lower() for keyword in pattern_keywords)
    
    def test_generate_city_insights_includes_statistics(self, mock_tool_context):
        """Verificar que incluye estadísticas numéricas"""
        from movility_ai.sub_agents.insight.tools import generate_city_insights
        
        result = generate_city_insights(time_period="week", tool_context=mock_tool_context)
        
        # Debe incluir números o porcentajes
        has_numbers = any(char.isdigit() for char in result)
        assert has_numbers
    
    def test_generate_city_insights_compares_zones(self, mock_tool_context):
        """Verificar que compara diferentes zonas de la ciudad"""
        from movility_ai.sub_agents.insight.tools import generate_city_insights
        
        result = generate_city_insights(time_period="month", tool_context=mock_tool_context)
        
        # Debe mencionar al menos 2 zonas
        from movility_ai.shared_libraries.constants import MEDELLIN_ZONES
        mentioned_zones = [zone for zone in MEDELLIN_ZONES if zone in result]
        assert len(mentioned_zones) >= 2
    
    def test_generate_city_insights_saves_to_context(self, mock_tool_context):
        """Verificar que guarda insights en el contexto"""
        from movility_ai.sub_agents.insight.tools import generate_city_insights
        
        generate_city_insights(time_period="week", tool_context=mock_tool_context)
        
        assert hasattr(mock_tool_context.state, "last_city_insights")


class TestInsightChartTool:
    """Tests para la herramienta de gráficos"""
    
    def test_generate_insight_chart_returns_visualization(self, mock_tool_context):
        """Verificar que genera visualización de gráfico"""
        from movility_ai.sub_agents.insight.tools import generate_insight_chart
        
        result = generate_insight_chart(
            chart_type="bar",
            data_category="transport_modes",
            tool_context=mock_tool_context
        )
        
        assert result is not None
        assert "{" in result or "**" in result
    
    def test_generate_insight_chart_supports_multiple_types(self, mock_tool_context):
        """Verificar que soporta diferentes tipos de gráficos"""
        from movility_ai.sub_agents.insight.tools import generate_insight_chart
        
        # Probar diferentes tipos
        result_bar = generate_insight_chart("bar", "zones", mock_tool_context)
        result_line = generate_insight_chart("line", "traffic", mock_tool_context)
        
        assert result_bar is not None
        assert result_line is not None
    
    def test_generate_insight_chart_includes_labels(self, mock_tool_context):
        """Verificar que incluye etiquetas y leyendas"""
        from movility_ai.sub_agents.insight.tools import generate_insight_chart
        
        result = generate_insight_chart("pie", "modes", mock_tool_context)
        
        # Debe tener estructura de datos visuales
        visual_indicators = ["label", "data", "color", "legend", "📊"]
        assert any(indicator in result.lower() for indicator in visual_indicators)


class TestInsightIntegration:
    """Tests de integración con el sistema completo"""
    
    def test_insight_registered_in_root_agent(self):
        """Verificar que Insight está registrado en el agente raíz"""
        from movility_ai.agent import root_agent
        
        sub_agent_names = [agent.name for agent in root_agent.sub_agents]
        assert "insight_agent" in sub_agent_names
    
    def test_insight_mock_agent_works(self):
        """Verificar que MockAgent funciona para testing"""
        from movility_ai.sub_agents.insight.agent import MockAgent
        
        mock_agent = MockAgent(name="test_insight", tools=[], model="test")
        
        assert mock_agent.name == "test_insight"
        assert mock_agent.model == "test"
        assert mock_agent.tools == []
