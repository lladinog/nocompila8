"""
FlowSense Agent - Traffic Prediction & Heatmaps
"""

from google.adk.agents import Agent

from movility_ai.sub_agents.flowsense.prompt import FLOWSENSE_AGENT_INSTR
from movility_ai.sub_agents.flowsense.tools import predict_traffic, generate_traffic_heatmap


# Crear el agente FlowSense
flowsense_agent = Agent(
    model="gemini-2.5-flash",
    name="flowsense_agent",
    description="🚦 Agente especializado en predicción de tráfico y congestión",
    instruction=FLOWSENSE_AGENT_INSTR,
    tools=[predict_traffic, generate_traffic_heatmap]
)
