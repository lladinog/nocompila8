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

"""CleanAgent: limpia y normaliza datos de tráfico."""

from google.adk.agents import Agent
from movility_ai.sub_agents.clean import prompt


clean_agent = Agent(
    model="gemini-2.5-flash",
    name="clean_agent",
    description="Agent responsible for cleaning, validating, and standardizing raw traffic data",
    instruction=prompt.CLEAN_AGENT_INSTR,
    tools=[
        # Sin herramientas externas por ahora
    ],
)
