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

"""Agente Gestor de Contingencias para MovilityAI"""

from google.adk.agents import Agent

from movility_ai.sub_agents.alertas import prompt
from movility_ai.sub_agents.alertas.monitor import (
    monitorear_redes_sociales,
    detectar_incidentes_activos,
    consultar_estado_metro,
    generar_rutas_alternativas,
    consultar_eventos_masivos,
)

alertas_agent = Agent(
    model="gemini-2.0-flash-exp",
    name="alertas_agent",
    description="Agente Gestor de Contingencias - Monitorea incidentes, accidentes, cierres viales y contingencias del Metro en tiempo real. Genera alertas proactivas y sugiere rutas alternativas.",
    instruction=prompt.ALERTAS_AGENT_INSTR,
    tools=[
        monitorear_redes_sociales,
        detectar_incidentes_activos,
        consultar_estado_metro,
        generar_rutas_alternativas,
        consultar_eventos_masivos,
    ],
)
