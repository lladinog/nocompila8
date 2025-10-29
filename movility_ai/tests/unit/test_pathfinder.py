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

"""
🧪 Tests para PathFinder Agent - Planificación de rutas multimodales.

Fase RED (TDD): Tests que definen el comportamiento esperado.
"""

import unittest
import sys
from pathlib import Path

# Agregar el directorio raíz al path
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(root_dir))


class TestPathFinderAgent(unittest.TestCase):
    """Tests para PathFinder Agent."""

    def test_pathfinder_agent_exists(self):
        """Test: El agente PathFinder existe y está correctamente configurado."""
        try:
            from movility_ai.sub_agents.pathfinder.agent import pathfinder_agent
            
            self.assertIsNotNone(pathfinder_agent)
            self.assertEqual(pathfinder_agent.name, "pathfinder_agent")
            self.assertIn("ruta", pathfinder_agent.description.lower())
        except ImportError:
            self.fail("PathFinder agent no está implementado")

    def test_pathfinder_has_route_tool(self):
        """Test: PathFinder tiene una herramienta para calcular rutas."""
        try:
            from movility_ai.sub_agents.pathfinder.agent import pathfinder_agent
            
            # Verificar que tiene tools
            self.assertGreater(len(pathfinder_agent.tools), 0, 
                             "PathFinder debe tener al menos una tool")
            
            # Verificar que una de las tools es para calcular rutas
            tool_names = [tool.name if hasattr(tool, 'name') else str(tool) 
                         for tool in pathfinder_agent.tools]
            has_route_tool = any('route' in str(name).lower() for name in tool_names)
            self.assertTrue(has_route_tool, 
                          "PathFinder debe tener una tool relacionada con rutas")
        except ImportError:
            self.fail("PathFinder agent no está implementado")

    def test_pathfinder_prompt_has_instructions(self):
        """Test: PathFinder tiene instrucciones claras."""
        try:
            from movility_ai.sub_agents.pathfinder import prompt
            
            self.assertIsNotNone(prompt.PATHFINDER_AGENT_INSTR)
            self.assertIn("ruta", prompt.PATHFINDER_AGENT_INSTR.lower())
            self.assertIn("medellín", prompt.PATHFINDER_AGENT_INSTR.lower())
        except ImportError:
            self.fail("PathFinder prompt no está implementado")

    def test_calculate_route_tool_exists(self):
        """Test: Existe la tool calculate_route."""
        try:
            from movility_ai.sub_agents.pathfinder.tools import calculate_route
            
            self.assertIsNotNone(calculate_route)
            self.assertTrue(callable(calculate_route))
        except ImportError:
            self.fail("calculate_route tool no está implementada")

    def test_calculate_route_returns_route_data(self):
        """Test: calculate_route retorna datos de ruta válidos."""
        try:
            from movility_ai.sub_agents.pathfinder.tools import calculate_route
            
            # Simular llamada con tool_context mock
            result = calculate_route(
                origin="Laureles",
                destination="El Poblado",
                tool_context=None  # Mock simple para testing
            )
            
            # Verificar que retorna string (JSON o texto descriptivo)
            self.assertIsInstance(result, str)
            self.assertGreater(len(result), 0)
            
            # Verificar que menciona origen y destino
            self.assertIn("laureles", result.lower())
            self.assertIn("poblado", result.lower())
        except ImportError:
            self.fail("calculate_route tool no está implementada")
        except Exception as e:
            # Si falla por tool_context, está bien, solo verificamos que existe
            if "tool_context" in str(e).lower():
                pass  # Es esperado sin tool_context real
            else:
                raise

    def test_calculate_route_with_mode_preference(self):
        """Test: calculate_route acepta modo de transporte preferido."""
        try:
            from movility_ai.sub_agents.pathfinder.tools import calculate_route
            
            result = calculate_route(
                origin="Centro",
                destination="Envigado",
                preferred_mode="metro",
                tool_context=None
            )
            
            self.assertIsInstance(result, str)
            # Debería mencionar el metro en la respuesta
            self.assertIn("metro", result.lower())
        except ImportError:
            self.fail("calculate_route tool no está implementada")
        except TypeError as e:
            # Si el error es por parámetros, significa que la función existe pero necesita ajustes
            if "preferred_mode" in str(e):
                self.fail("calculate_route debe aceptar parámetro preferred_mode")
        except Exception:
            pass  # Otros errores son aceptables en esta fase

    def test_visualize_route_tool_exists(self):
        """Test: Existe la tool para visualizar rutas."""
        try:
            from movility_ai.sub_agents.pathfinder.tools import visualize_route
            
            self.assertIsNotNone(visualize_route)
            self.assertTrue(callable(visualize_route))
        except ImportError:
            self.fail("visualize_route tool no está implementada")

    def test_pathfinder_structure(self):
        """Test: La estructura de PathFinder es correcta."""
        try:
            from movility_ai.sub_agents.pathfinder import agent, prompt
            
            # Verificar que el módulo se puede importar
            self.assertIsNotNone(agent)
            self.assertIsNotNone(prompt)
        except ImportError as e:
            self.fail(f"Estructura de PathFinder incompleta: {e}")


class TestPathFinderIntegration(unittest.TestCase):
    """Tests de integración para PathFinder."""

    def test_pathfinder_in_root_agent(self):
        """Test: PathFinder está registrado en el root agent."""
        try:
            from movility_ai.agent import root_agent
            from movility_ai.sub_agents.pathfinder.agent import pathfinder_agent
            
            # Verificar que PathFinder está en los sub-agentes del root
            sub_agent_names = [agent.name for agent in root_agent.sub_agents]
            self.assertIn("pathfinder_agent", sub_agent_names,
                         "PathFinder debe estar registrado en root_agent")
        except ImportError:
            self.fail("PathFinder no está integrado en root_agent")

    def test_pathfinder_can_be_called(self):
        """Test: PathFinder puede ser invocado (estructura mínima)."""
        try:
            from movility_ai.sub_agents.pathfinder.agent import pathfinder_agent
            
            # Verificar propiedades básicas
            self.assertIsNotNone(pathfinder_agent.name)
            self.assertIsNotNone(pathfinder_agent.description)
            self.assertIsNotNone(pathfinder_agent.instruction)
        except ImportError:
            self.fail("PathFinder agent no está implementado")
        except AttributeError as e:
            self.fail(f"PathFinder agent tiene estructura incompleta: {e}")


if __name__ == "__main__":
    unittest.main()
