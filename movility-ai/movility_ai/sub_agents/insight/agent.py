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

"""Insight Agent - Analista de movilidad urbana"""

from google.adk.agents import Agent
from movility_ai.sub_agents.insight import prompt
from movility_ai.sub_agents.insight import analytics


insight_agent = Agent(
    model="gemini-2.0-flash-exp",
    name="insight_agent",
    description="Agente analista especializado en generar insights y visualizaciones sobre movilidad urbana de Medellín, identificando patrones, zonas críticas, tendencias y oportunidades de mejora para ciudadanos y planeadores",
    instruction=prompt.INSIGHT_AGENT_INSTR,
    tools=[
        analytics.generate_mobility_dashboard,
        analytics.analyze_critical_zones,
        analytics.generate_temporal_analysis,
        analytics.calculate_sustainability_metrics,
        analytics.generate_comparative_report,
        analytics.detect_anomalies,
    ],
)
