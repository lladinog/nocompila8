"""
Insight Agent - City Analytics & Trends
"""

import os
from .prompt import INSIGHT_AGENT_INSTR
from .tools import generate_city_insights, generate_insight_chart

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
def generate_city_insights_tool(time_period: str, tool_context) -> str:
    """Genera insights agregados de movilidad urbana (patrones, tendencias, estadísticas)"""
    return generate_city_insights(time_period, tool_context)


@tool
def generate_insight_chart_tool(chart_type: str, data_category: str, tool_context) -> str:
    """Genera gráficos analíticos personalizados (bar, line, pie)"""
    return generate_insight_chart(chart_type, data_category, tool_context)


# Crear el agente Insight
insight_agent = Agent(
    name="insight_agent",
    model="gemini-2.5-flash",
    tools=[generate_city_insights_tool, generate_insight_chart_tool],
    instructions=INSIGHT_AGENT_INSTR
)
