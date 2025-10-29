# Copyright 2025 MovilityAI
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

"""PathFinder Agent - Planificador de rutas multimodal inteligente"""

from google.adk.agents import Agent
from movility_ai.sub_agents.pathfinder import prompt
from movility_ai.sub_agents.pathfinder import tools


pathfinder_agent = Agent(
    model="gemini-2.0-flash-exp",
    name="pathfinder_agent",
    description="Agente especializado en planificación de rutas multimodales óptimas para Medellín, combinando transporte público, bicicleta y caminata, con análisis de tráfico y clima en tiempo real",
    instruction=prompt.PATHFINDER_AGENT_INSTR,
    tools=[
        tools.get_route_google_maps,
        tools.get_weather_conditions,
        tools.get_encicla_stations,
        tools.calculate_multimodal_route,
    ],
)
