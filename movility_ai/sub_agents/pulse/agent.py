"""
Pulse Agent - Urban Context & Events
"""

import os
from .prompt import PULSE_AGENT_INSTR
from .tools import detect_urban_events, generate_event_alerts

# Intentar importar Google ADK
ADK_AVAILABLE = False
try:
    if os.getenv("TESTING") != "true":
        from google.genai.adk import Agent, tool
        ADK_AVAILABLE = True
except ImportError:
    pass

# Si ADK no está disponible, usar mocks para testing
if not ADK_AVAILABLE:
    class MockAgent:
        """Mock Agent para testing sin ADK"""
        def __init__(self, name, model=None, tools=None, instructions=None, sub_agents=None):
            self.name = name
            self.model = model
            self.tools = tools or []
            self.instructions = instructions
            self.sub_agents = sub_agents or []
    
    def tool(func):
        """Mock tool decorator"""
        return func
    
    Agent = MockAgent


# Decorar las herramientas
@tool
def detect_urban_events_tool(zones: list[str], tool_context) -> str:
    """Detecta eventos urbanos activos (protestas, accidentes, obras, clima, eventos masivos)"""
    return detect_urban_events(zones, tool_context)


@tool
def generate_event_alerts_tool(zones: list[str], tool_context) -> str:
    """Genera alertas visuales priorizadas de eventos urbanos"""
    return generate_event_alerts(zones, tool_context)


# Crear el agente Pulse
pulse_agent = Agent(
    name="pulse_agent",
    model="gemini-2.5-flash",
    tools=[detect_urban_events_tool, generate_event_alerts_tool],
    instructions=PULSE_AGENT_INSTR
)
