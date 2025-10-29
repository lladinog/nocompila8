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

"""FlowSense Agent - Predicción de congestión vial anticipada"""

from google.adk.agents import Agent
from movility_ai.sub_agents.flowsense import prompt
from movility_ai.sub_agents.flowsense import predictor


flowsense_agent = Agent(
    model="gemini-2.0-flash-exp",
    name="flowsense_agent",
    description="Agente especializado en predicción de congestión vial a corto plazo (30-60 min) para Medellín, analizando patrones históricos, clima, eventos y condiciones en tiempo real",
    instruction=prompt.FLOWSENSE_AGENT_INSTR,
    tools=[
        predictor.predict_traffic_congestion,
        predictor.get_traffic_events,
        predictor.get_historical_patterns,
        predictor.analyze_weather_impact,
    ],
)
