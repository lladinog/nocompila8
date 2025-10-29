"""
Insight Agent - City Analytics & Trends
"""

from google.adk.agents import Agent

from movility_ai.sub_agents.insight.prompt import INSIGHT_AGENT_INSTR
from movility_ai.sub_agents.insight.tools import generate_city_insights, generate_insight_chart


# Crear el agente Insight
insight_agent = Agent(
    model="gemini-2.5-flash",
    name="insight_agent",
    description="📊 Agente especializado en analítica urbana y tendencias de movilidad",
    instruction=INSIGHT_AGENT_INSTR,
    tools=[generate_city_insights, generate_insight_chart]
)
