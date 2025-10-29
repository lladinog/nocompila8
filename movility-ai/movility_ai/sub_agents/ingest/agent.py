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

"""IngestAgent: obtiene datos de tráfico desde APIs externas."""

from google.adk.agents import Agent
from movility_ai.sub_agents.ingest import prompt

# Las herramientas se importarán cuando estén implementadas
# from movility_ai.tools.google_traffic import google_traffic_tool
# from movility_ai.tools.moovit import moovit_transit_tool


ingest_agent = Agent(
    model="gemini-2.5-flash",
    name="ingest_agent",
    description="Agent responsible for fetching traffic and mobility data from external APIs (Google Maps, Moovit, etc.)",
    instruction=prompt.INGEST_AGENT_INSTR,
    tools=[
        # Herramientas se agregarán progresivamente
        # google_traffic_tool,
        # moovit_transit_tool,
    ],
)
