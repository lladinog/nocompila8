# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""PathFinder Agent - Planificador de rutas multimodales para Medellín."""

try:
    from google.adk.agents import Agent
    from google.adk.tools import tool
    ADK_AVAILABLE = True
except ImportError:
    # Para testing sin ADK
    ADK_AVAILABLE = False
    Agent = None
    def tool(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

from movility_ai.sub_agents.pathfinder import prompt
from movility_ai.sub_agents.pathfinder.tools import calculate_route, visualize_route


# Convertir las funciones en ADK tools
calculate_route_tool = tool(calculate_route) if ADK_AVAILABLE else calculate_route
visualize_route_tool = tool(visualize_route) if ADK_AVAILABLE else visualize_route


# Crear el agente PathFinder
if ADK_AVAILABLE:
    pathfinder_agent = Agent(
        model="gemini-2.5-flash",
        name="pathfinder_agent",
        description="🗺️ Agente especializado en planificación de rutas multimodales para Medellín. Calcula rutas óptimas considerando metro, bus, bicicleta, y otros modos de transporte.",
        instruction=prompt.PATHFINDER_AGENT_INSTR,
        tools=[calculate_route_tool, visualize_route_tool],
    )
else:
    # Mock para testing
    class MockAgent:
        name = "pathfinder_agent"
        description = "🗺️ Agente especializado en planificación de rutas multimodales para Medellín."
        instruction = prompt.PATHFINDER_AGENT_INSTR
        tools = [calculate_route, visualize_route]
    
    pathfinder_agent = MockAgent()
