"""
Configuración de servidor ADK para MovilityAI

Este archivo configura el servidor de desarrollo de Google ADK
"""

from movility_ai.agent import root_agent

# Exportar el agente para que ADK lo pueda usar
agent = root_agent

# Configuración del servidor
config = {
    "agent": root_agent,
    "port": 8000,
    "host": "localhost",
    "reload": True,
}
