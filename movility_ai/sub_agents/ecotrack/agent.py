"""
EcoTrack Agent - Eco Metrics & Sustainability
"""

import os
from .prompt import ECOTRACK_AGENT_INSTR
from .tools import calculate_eco_metrics, generate_eco_dashboard

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
def calculate_eco_metrics_tool(transport_mode: str, distance_km: float, tool_context) -> str:
    """Calcula métricas ecológicas (CO2, calorías, eco score) de un viaje"""
    return calculate_eco_metrics(transport_mode, distance_km, tool_context)


@tool
def generate_eco_dashboard_tool(user_trips: int, tool_context) -> str:
    """Genera dashboard personalizado de sostenibilidad con logros"""
    return generate_eco_dashboard(user_trips, tool_context)


# Crear el agente EcoTrack
ecotrack_agent = Agent(
    name="ecotrack_agent",
    model="gemini-2.5-flash",
    tools=[calculate_eco_metrics_tool, generate_eco_dashboard_tool],
    instructions=ECOTRACK_AGENT_INSTR
)
