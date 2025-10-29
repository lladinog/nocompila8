"""
Pulse Agent - Urban Context & Events
"""

from google.adk.agents import Agent

from movility_ai.sub_agents.pulse.prompt import PULSE_AGENT_INSTR
from movility_ai.sub_agents.pulse.tools import detect_urban_events, generate_event_alerts


# Crear el agente Pulse
pulse_agent = Agent(
    model="gemini-2.5-flash",
    name="pulse_agent",
    description="📡 Agente especializado en contexto urbano y eventos en tiempo real",
    instruction=PULSE_AGENT_INSTR,
    tools=[detect_urban_events, generate_event_alerts]
)
