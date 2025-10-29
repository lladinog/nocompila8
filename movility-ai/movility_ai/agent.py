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

"""MovilityAI Root Agent - Sistema Inteligente de Movilidad Urbana para Medellín"""

from google.adk.agents import Agent

from movility_ai import prompt
from movility_ai.sub_agents.pathfinder.agent import pathfinder_agent
from movility_ai.sub_agents.flowsense.agent import flowsense_agent
from movility_ai.sub_agents.insight.agent import insight_agent
from movility_ai.sub_agents.alertas.agent import alertas_agent


root_agent = Agent(
    model="gemini-2.0-flash-exp",
    name="root_agent",
    description="MovilityAI - Sistema inteligente de movilidad urbana para Medellín que coordina 4 agentes especializados: planificación de rutas multimodales, predicción de tráfico, gestión de contingencias y análisis de datos urbanos",
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[
        pathfinder_agent,
        flowsense_agent,
        insight_agent,
        alertas_agent,
    ],
)
