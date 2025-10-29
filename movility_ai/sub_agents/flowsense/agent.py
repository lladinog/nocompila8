"""
FlowSense Agent - Traffic Prediction & Heatmaps
"""

import os
from .prompt import FLOWSENSE_AGENT_INSTR
from .tools import predict_traffic, generate_traffic_heatmap

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
def predict_traffic_tool(zones: list[str], tool_context) -> str:
    """Predice el estado del tráfico para zonas específicas de Medellín"""
    return predict_traffic(zones, tool_context)


@tool
def generate_traffic_heatmap_tool(zones: list[str], tool_context) -> str:
    """Genera un mapa de calor visual del tráfico urbano"""
    return generate_traffic_heatmap(zones, tool_context)


# Crear el agente FlowSense
flowsense_agent = Agent(
    name="flowsense_agent",
    model="gemini-2.5-flash",
    tools=[predict_traffic_tool, generate_traffic_heatmap_tool],
    instructions=FLOWSENSE_AGENT_INSTR
)
