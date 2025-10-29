"""
EcoTrack Agent - Eco Metrics & Sustainability
"""

from google.adk.agents import Agent

from movility_ai.sub_agents.ecotrack.prompt import ECOTRACK_AGENT_INSTR
from movility_ai.sub_agents.ecotrack.tools import calculate_eco_metrics, generate_eco_dashboard


# Crear el agente EcoTrack
ecotrack_agent = Agent(
    model="gemini-2.5-flash",
    name="ecotrack_agent",
    description="🌱 Agente especializado en métricas ecológicas y sostenibilidad",
    instruction=ECOTRACK_AGENT_INSTR,
    tools=[calculate_eco_metrics, generate_eco_dashboard]
)
