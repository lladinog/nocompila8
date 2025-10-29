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

"""
MovilityAI - Sistema Inteligente de Análisis y Optimización de Movilidad Urbana

Punto de entrada principal para ejecutar el sistema.
"""

if __name__ == "__main__":
    from movility_ai.agent import root_agent
    
    print("🚦 MovilityAI - Intelligent Urban Mobility Analysis System")
    print("=" * 60)
    print("\nSistema iniciado correctamente")
    print(f"Root Agent: {root_agent.name}")
    print(f"Sub-agentes configurados: {len(root_agent.sub_agents)}")
    print("\nAgentes disponibles:")
    for agent in root_agent.sub_agents:
        print(f"  - {agent.name}: {agent.description[:60]}...")
    
    print("\n" + "=" * 60)
    print("✅ Sistema listo para recibir consultas")
    print("\nEjemplos de uso:")
    print("  1. 'Analiza el tráfico en Bogotá'")
    print("  2. 'Dame un reporte de congestión'")
    print("  3. 'Qué patrones de tráfico hay en la zona?'")
    print("\nNota: Las APIs externas se integrarán en la siguiente fase")
    print("=" * 60)
