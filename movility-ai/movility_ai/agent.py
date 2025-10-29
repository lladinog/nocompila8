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

"""MovilityAI Root Agent - Sistema Inteligente de Análisis de Movilidad Urbana"""

from google.adk.agents import Agent

from movility_ai import prompt
from movility_ai.sub_agents.ingest.agent import ingest_agent
from movility_ai.sub_agents.clean.agent import clean_agent
from movility_ai.sub_agents.analyze.agent import analyze_agent
from movility_ai.sub_agents.report.agent import report_agent
from movility_ai.sub_agents.route_planner.agent import route_planner_agent

root_agent = Agent(
    model="gemini-2.5-flash",
    name="root_agent",
    description="MovilityAI - Intelligent Urban Mobility Analysis System coordinating multiple specialized sub-agents",
    instruction=prompt.ROOT_AGENT_INSTR,
    sub_agents=[
        ingest_agent,
        clean_agent,
        analyze_agent,
        report_agent,
        route_planner_agent,
    ],
)
