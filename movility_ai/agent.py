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

"""MovilityAI Root Agent - Sistema multiagente de movilidad urbana inteligente."""

from google.adk.agents import Agent

from movility_ai import prompt
from movility_ai.sub_agents.pathfinder.agent import pathfinder_agent
from movility_ai.sub_agents.flowsense.agent import flowsense_agent
from movility_ai.sub_agents.pulse.agent import pulse_agent
from movility_ai.sub_agents.ecotrack.agent import ecotrack_agent
from movility_ai.sub_agents.insight.agent import insight_agent


root_agent = Agent(
    model="gemini-2.5-flash",
    name="navimind_root_agent",
    description="🧭 NaviMind - Asistente inteligente de movilidad urbana para Medellín",
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[
        pathfinder_agent,
        flowsense_agent,
        pulse_agent,
        ecotrack_agent,
        insight_agent,
    ],
    # before_agent_callback=_initialize_user_context,  # TODO: Create this callback
)
