"""
Tests para FlowSense Agent (Traffic Prediction & Heatmaps)
🔴 RED Phase: Estos tests deben fallar hasta implementar el agente
"""

import pytest
from movility_ai.shared_libraries.types import TrafficInfo
from movility_ai.tools.data_mock_tool import generate_mock_traffic


class TestFlowSenseAgent:
    """Tests para la estructura y funcionalidad del FlowSense Agent"""
    
    def test_flowsense_agent_exists(self):
        """Verificar que el agente FlowSense existe"""
        from movility_ai.sub_agents.flowsense.agent import flowsense_agent
        
        assert flowsense_agent is not None
        assert flowsense_agent.name == "flowsense_agent"
    
    def test_flowsense_agent_has_tools(self):
        """Verificar que FlowSense tiene las herramientas necesarias"""
        from movility_ai.sub_agents.flowsense.agent import flowsense_agent
        
        assert len(flowsense_agent.tools) >= 2
        tool_names = [tool.__name__ for tool in flowsense_agent.tools]
        assert "predict_traffic" in tool_names
        assert "generate_traffic_heatmap" in tool_names
    
    def test_flowsense_agent_has_instructions(self):
        """Verificar que FlowSense tiene instrucciones definidas"""
        from movility_ai.sub_agents.flowsense.prompt import FLOWSENSE_AGENT_INSTR
        
        assert FLOWSENSE_AGENT_INSTR is not None
        assert len(FLOWSENSE_AGENT_INSTR) > 100
        assert "tráfico" in FLOWSENSE_AGENT_INSTR.lower()


class TestPredictTrafficTool:
    """Tests para la herramienta de predicción de tráfico"""
    
    def test_predict_traffic_returns_data(self, mock_tool_context):
        """Verificar que predict_traffic devuelve información de tráfico"""
        from movility_ai.sub_agents.flowsense.tools import predict_traffic
        
        result = predict_traffic(zones=["Laureles", "El Poblado"], tool_context=mock_tool_context)
        
        assert result is not None
        assert isinstance(result, str)
        assert "Laureles" in result
        assert "El Poblado" in result
    
    def test_predict_traffic_handles_all_zones(self, mock_tool_context):
        """Verificar que puede predecir tráfico para todas las zonas"""
        from movility_ai.sub_agents.flowsense.tools import predict_traffic
        from movility_ai.shared_libraries.constants import MEDELLIN_ZONES
        
        result = predict_traffic(zones=MEDELLIN_ZONES, tool_context=mock_tool_context)
        
        assert result is not None
        assert len(result) > 500  # Debe ser un reporte extenso
    
    def test_predict_traffic_includes_severity_levels(self, mock_tool_context):
        """Verificar que incluye niveles de severidad"""
        from movility_ai.sub_agents.flowsense.tools import predict_traffic
        
        result = predict_traffic(zones=["Centro"], tool_context=mock_tool_context)
        
        # Debe incluir al menos uno de los niveles
        severity_indicators = ["🟢", "🟡", "🟠", "🔴", "bajo", "medio", "alto", "crítico"]
        assert any(indicator in result.lower() for indicator in severity_indicators)
    
    def test_predict_traffic_saves_to_context(self, mock_tool_context):
        """Verificar que guarda datos en el contexto"""
        from movility_ai.sub_agents.flowsense.tools import predict_traffic
        
        predict_traffic(zones=["Laureles"], tool_context=mock_tool_context)
        
        assert hasattr(mock_tool_context.state, "last_traffic_prediction")


class TestTrafficHeatmapTool:
    """Tests para la herramienta de mapas de calor"""
    
    def test_generate_traffic_heatmap_returns_json(self, mock_tool_context):
        """Verificar que genera JSON válido para visualización"""
        from movility_ai.sub_agents.flowsense.tools import generate_traffic_heatmap
        import json
        
        result = generate_traffic_heatmap(zones=["Laureles"], tool_context=mock_tool_context)
        
        assert result is not None
        # Debe ser JSON válido
        assert "heatmap_data" in result or "{" in result
    
    def test_generate_traffic_heatmap_includes_colors(self, mock_tool_context):
        """Verificar que incluye información de colores para el mapa"""
        from movility_ai.sub_agents.flowsense.tools import generate_traffic_heatmap
        
        result = generate_traffic_heatmap(zones=["Centro", "El Poblado"], tool_context=mock_tool_context)
        
        # Debe incluir indicadores visuales
        color_indicators = ["🟢", "🟡", "🟠", "🔴", "color", "rgb", "#"]
        assert any(indicator in result.lower() for indicator in color_indicators)


class TestFlowSenseIntegration:
    """Tests de integración con el sistema completo"""
    
    def test_flowsense_registered_in_root_agent(self):
        """Verificar que FlowSense está registrado en el agente raíz"""
        from movility_ai.agent import root_agent
        
        sub_agent_names = [agent.name for agent in root_agent.sub_agents]
        assert "flowsense_agent" in sub_agent_names
    
    def test_flowsense_mock_agent_works(self):
        """Verificar que MockAgent funciona para testing"""
        from movility_ai.sub_agents.flowsense.agent import MockAgent
        
        mock_agent = MockAgent(name="test_flowsense", tools=[], model="test")
        
        assert mock_agent.name == "test_flowsense"
        assert mock_agent.model == "test"
        assert mock_agent.tools == []
