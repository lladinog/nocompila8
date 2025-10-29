"""
Tests para Pulse Agent (Urban Context & Events)
🔴 RED Phase: Estos tests deben fallar hasta implementar el agente
"""

import pytest
from movility_ai.shared_libraries.types import UrbanEvent


class TestPulseAgent:
    """Tests para la estructura y funcionalidad del Pulse Agent"""
    
    def test_pulse_agent_exists(self):
        """Verificar que el agente Pulse existe"""
        from movility_ai.sub_agents.pulse.agent import pulse_agent
        
        assert pulse_agent is not None
        assert pulse_agent.name == "pulse_agent"
    
    def test_pulse_agent_has_tools(self):
        """Verificar que Pulse tiene las herramientas necesarias"""
        from movility_ai.sub_agents.pulse.agent import pulse_agent
        
        assert len(pulse_agent.tools) >= 2
        tool_names = [tool.__name__ for tool in pulse_agent.tools]
        assert "detect_urban_events_tool" in tool_names
        assert "generate_event_alerts_tool" in tool_names
    
    def test_pulse_agent_has_instructions(self):
        """Verificar que Pulse tiene instrucciones definidas"""
        from movility_ai.sub_agents.pulse.prompt import PULSE_AGENT_INSTR
        
        assert PULSE_AGENT_INSTR is not None
        assert len(PULSE_AGENT_INSTR) > 100
        assert "eventos" in PULSE_AGENT_INSTR.lower() or "urbano" in PULSE_AGENT_INSTR.lower()


class TestDetectUrbanEventsTool:
    """Tests para la herramienta de detección de eventos urbanos"""
    
    def test_detect_urban_events_returns_data(self, mock_tool_context):
        """Verificar que detect_urban_events devuelve información de eventos"""
        from movility_ai.sub_agents.pulse.tools import detect_urban_events
        
        result = detect_urban_events(zones=["Laureles", "Centro"], tool_context=mock_tool_context)
        
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 50
    
    def test_detect_urban_events_includes_event_types(self, mock_tool_context):
        """Verificar que detecta diferentes tipos de eventos"""
        from movility_ai.sub_agents.pulse.tools import detect_urban_events
        
        result = detect_urban_events(zones=["Centro"], tool_context=mock_tool_context)
        
        # Debe mencionar al menos un tipo de evento
        event_keywords = ["protesta", "accidente", "obra", "concierto", "clima", "evento"]
        assert any(keyword in result.lower() for keyword in event_keywords)
    
    def test_detect_urban_events_includes_severity(self, mock_tool_context):
        """Verificar que incluye niveles de severidad"""
        from movility_ai.sub_agents.pulse.tools import detect_urban_events
        
        result = detect_urban_events(zones=["El Poblado"], tool_context=mock_tool_context)
        
        # Debe incluir indicadores de severidad
        severity_indicators = ["🔴", "🟠", "🟡", "🟢", "crítico", "alto", "medio", "bajo"]
        assert any(indicator in result.lower() for indicator in severity_indicators)
    
    def test_detect_urban_events_saves_to_context(self, mock_tool_context):
        """Verificar que guarda eventos en el contexto"""
        from movility_ai.sub_agents.pulse.tools import detect_urban_events
        
        detect_urban_events(zones=["Centro"], tool_context=mock_tool_context)
        
        assert hasattr(mock_tool_context.state, "last_urban_events")
    
    def test_detect_urban_events_handles_multiple_zones(self, mock_tool_context):
        """Verificar que puede detectar eventos en múltiples zonas"""
        from movility_ai.sub_agents.pulse.tools import detect_urban_events
        from movility_ai.shared_libraries.constants import MEDELLIN_ZONES
        
        # Probar con 5 zonas
        zones_to_test = MEDELLIN_ZONES[:5]
        result = detect_urban_events(zones=zones_to_test, tool_context=mock_tool_context)
        
        assert result is not None
        assert len(result) > 200  # Debe ser un reporte extenso


class TestEventAlertsTool:
    """Tests para la herramienta de generación de alertas"""
    
    def test_generate_event_alerts_returns_json(self, mock_tool_context):
        """Verificar que genera JSON válido para visualización"""
        from movility_ai.sub_agents.pulse.tools import generate_event_alerts
        
        result = generate_event_alerts(zones=["Centro"], tool_context=mock_tool_context)
        
        assert result is not None
        # Debe contener estructura JSON o formato visual
        assert "{" in result or "**" in result
    
    def test_generate_event_alerts_includes_icons(self, mock_tool_context):
        """Verificar que incluye iconos visuales"""
        from movility_ai.sub_agents.pulse.tools import generate_event_alerts
        
        result = generate_event_alerts(zones=["Laureles", "El Poblado"], tool_context=mock_tool_context)
        
        # Debe incluir emojis o iconos
        visual_indicators = ["⚠️", "🚨", "🎉", "🌧️", "🚧", "🚗"]
        assert any(indicator in result for indicator in visual_indicators)
    
    def test_generate_event_alerts_groups_by_severity(self, mock_tool_context):
        """Verificar que agrupa alertas por severidad"""
        from movility_ai.sub_agents.pulse.tools import generate_event_alerts
        
        result = generate_event_alerts(zones=["Centro"], tool_context=mock_tool_context)
        
        # Debe tener alguna estructura de priorización
        assert "crítico" in result.lower() or "🔴" in result or "alto" in result.lower()


class TestPulseIntegration:
    """Tests de integración con el sistema completo"""
    
    def test_pulse_registered_in_root_agent(self):
        """Verificar que Pulse está registrado en el agente raíz"""
        from movility_ai.agent import root_agent
        
        sub_agent_names = [agent.name for agent in root_agent.sub_agents]
        assert "pulse_agent" in sub_agent_names
    
    def test_pulse_mock_agent_works(self):
        """Verificar que MockAgent funciona para testing"""
        from movility_ai.sub_agents.pulse.agent import MockAgent
        
        mock_agent = MockAgent(name="test_pulse", tools=[], model="test")
        
        assert mock_agent.name == "test_pulse"
        assert mock_agent.model == "test"
        assert mock_agent.tools == []
