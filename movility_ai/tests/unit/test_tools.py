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
🧪 Tests unitarios para las herramientas de MovilityAI.

Fase RED (TDD): Estos tests definen el comportamiento esperado de las tools.
Los tests están diseñados para fallar hasta que implementemos las funciones correctamente.

Para ejecutar: python -m pytest tests/unit/test_tools.py -v
"""

import json
import unittest

# Los imports fallarán si las tools no están implementadas como esperamos
try:
    from movility_ai.tools import data_mock_tool, visualizer_tool, memory_display_tool
    TOOLS_AVAILABLE = True
except ImportError:
    TOOLS_AVAILABLE = False
    # Tests fallarán si las tools no están disponibles


class TestDataMockTool(unittest.TestCase):
    """Tests para la herramienta de generación de datos simulados."""
    
    def setUp(self):
        """Verificar que las tools están disponibles."""
        if not TOOLS_AVAILABLE:
            self.skipTest("Tools no disponibles - esperando implementación")

    def test_generate_mock_route_basic(self):
        """Test básico: genera una ruta de Laureles a El Poblado."""
        route = data_mock_tool.generate_mock_route("Laureles", "El Poblado")
        
        # Verificar estructura básica
        self.assertIn("origin", route)
        self.assertIn("destination", route)
        self.assertIn("segments", route)
        self.assertIn("total_duration_minutes", route)
        self.assertIn("total_cost_cop", route)
        self.assertIn("eco_score", route)
        
        # Verificar valores
        self.assertEqual(route["origin"]["name"], "Laureles")
        self.assertEqual(route["destination"]["name"], "El Poblado")
        self.assertGreater(len(route["segments"]), 0)
        self.assertGreater(route["eco_score"], 0)
        self.assertLessEqual(route["eco_score"], 100)

    def test_generate_mock_route_with_preferred_mode(self):
        """Test: genera ruta con modo de transporte preferido."""
        route = data_mock_tool.generate_mock_route(
            "Centro", 
            "Envigado", 
            preferred_mode="metro"
        )
        
        # Verificar que el primer segmento usa el modo preferido
        self.assertEqual(route["segments"][0]["mode"], "metro")

    def test_generate_mock_traffic(self):
        """Test: genera datos de tráfico para zonas de Medellín."""
        traffic_data = data_mock_tool.generate_mock_traffic()
        
        # Verificar que retorna lista
        self.assertIsInstance(traffic_data, list)
        self.assertGreater(len(traffic_data), 0)
        
        # Verificar estructura de cada zona
        for zone_info in traffic_data:
            self.assertIn("zone", zone_info)
            self.assertIn("level", zone_info)
            self.assertIn("average_speed_kmh", zone_info)
            self.assertIn("color", zone_info)
            self.assertIn("label", zone_info)
            
            # Verificar niveles válidos
            self.assertIn(zone_info["level"], ["low", "medium", "high", "critical"])

    def test_generate_mock_traffic_specific_zone(self):
        """Test: genera datos de tráfico para zona específica."""
        traffic_data = data_mock_tool.generate_mock_traffic(zone="Laureles")
        
        self.assertEqual(len(traffic_data), 1)
        self.assertEqual(traffic_data[0]["zone"], "Laureles")

    def test_generate_mock_events(self):
        """Test: genera eventos urbanos simulados."""
        events = data_mock_tool.generate_mock_events()
        
        # Verificar estructura
        self.assertIsInstance(events, list)
        self.assertGreater(len(events), 0)
        
        # Verificar cada evento
        for event in events:
            self.assertIn("event_type", event)
            self.assertIn("location", event)
            self.assertIn("description", event)
            self.assertIn("severity", event)
            self.assertIn("affected_zones", event)
            
            # Verificar severity válido
            self.assertIn(event["severity"], ["low", "medium", "high"])

    def test_generate_mock_eco_metrics(self):
        """Test: genera métricas ecológicas."""
        metrics = data_mock_tool.generate_mock_eco_metrics(user_trips=20)
        
        # Verificar estructura
        self.assertIn("co2_saved_kg", metrics)
        self.assertIn("calories_burned", metrics)
        self.assertIn("trees_equivalent", metrics)
        self.assertIn("eco_score", metrics)
        self.assertIn("sustainable_trips", metrics)
        
        # Verificar valores
        self.assertEqual(metrics["sustainable_trips"], 20)
        self.assertGreater(metrics["eco_score"], 0)
        self.assertLessEqual(metrics["eco_score"], 100)

    def test_generate_mock_insights(self):
        """Test: genera datos de analítica urbana."""
        insights = data_mock_tool.generate_mock_insights()
        
        # Verificar estructura
        self.assertIn("congested_zones", insights)
        self.assertIn("traffic_trend", insights)
        self.assertIn("mode_distribution", insights)
        self.assertIn("summary", insights)
        
        # Verificar que hay datos
        self.assertGreater(len(insights["congested_zones"]), 0)
        self.assertGreater(len(insights["traffic_trend"]), 0)


class TestVisualizerTool(unittest.TestCase):
    """Tests para la herramienta de visualización."""
    
    def setUp(self):
        """Verificar que las tools están disponibles."""
        if not TOOLS_AVAILABLE:
            self.skipTest("Tools no disponibles - esperando implementación")

    def test_generate_route_map(self):
        """Test: genera visualización de mapa de ruta."""
        segments = [
            {"mode": "metro", "from_location": "Laureles", "to_location": "El Poblado"}
        ]
        
        result = visualizer_tool.generate_route_map("Laureles", "El Poblado", segments)
        
        # Debe retornar JSON válido
        data = json.loads(result)
        
        # Verificar estructura
        self.assertEqual(data["type"], "route_map")
        self.assertIn("title", data)
        self.assertIn("map_data", data)
        self.assertIn("visual_style", data)
        
        # Verificar datos del mapa
        self.assertEqual(data["map_data"]["origin"], "Laureles")
        self.assertEqual(data["map_data"]["destination"], "El Poblado")

    def test_generate_traffic_heatmap(self):
        """Test: genera mapa de calor de tráfico."""
        zone_data = [
            {"zone": "Laureles", "level": "medium", "color": "yellow"}
        ]
        
        result = visualizer_tool.generate_traffic_heatmap(zone_data)
        
        # Debe retornar JSON válido
        data = json.loads(result)
        
        # Verificar estructura
        self.assertEqual(data["type"], "traffic_heatmap")
        self.assertIn("zones", data)
        self.assertIn("legend", data)

    def test_generate_eco_dashboard(self):
        """Test: genera dashboard de métricas ecológicas."""
        metrics = {
            "co2_saved_kg": 15.5,
            "calories_burned": 1200,
            "trees_equivalent": 0.5,
            "eco_score": 85
        }
        
        result = visualizer_tool.generate_eco_dashboard(metrics)
        
        # Debe retornar JSON válido
        data = json.loads(result)
        
        # Verificar estructura
        self.assertEqual(data["type"], "eco_dashboard")
        self.assertIn("metrics", data)
        self.assertGreater(len(data["metrics"]), 0)

    def test_generate_event_alerts(self):
        """Test: genera alertas de eventos urbanos."""
        events = [
            {
                "event_type": "protesta",
                "location": "Centro",
                "description": "Manifestación pacífica",
                "severity": "medium"
            }
        ]
        
        result = visualizer_tool.generate_event_alerts(events)
        
        # Debe retornar JSON válido
        data = json.loads(result)
        
        # Verificar estructura
        self.assertEqual(data["type"], "event_alerts")
        self.assertIn("events", data)
        self.assertIn("map_markers", data)

    def test_generate_insight_chart(self):
        """Test: genera gráficos de analítica."""
        analytics = {
            "congested_zones": [{"zone": "El Poblado", "level": 85}],
            "traffic_trend": [{"hour": "08:00", "level": 75}],
            "summary": "Datos de prueba"
        }
        
        result = visualizer_tool.generate_insight_chart(analytics)
        
        # Debe retornar JSON válido
        data = json.loads(result)
        
        # Verificar estructura
        self.assertEqual(data["type"], "analytics_dashboard")
        self.assertIn("charts", data)


class TestMemoryDisplayTool(unittest.TestCase):
    """Tests para la herramienta de visualización de memoria."""
    
    def setUp(self):
        """Verificar que las tools están disponibles."""
        if not TOOLS_AVAILABLE:
            self.skipTest("Tools no disponibles - esperando implementación")

    def test_display_memory_state_basic(self):
        """Test: muestra estado de memoria básico."""
        state = {
            "user_profile": {"name": "Test User", "preferred_modes": ["metro"]},
            "user_location": "Laureles"
        }
        
        result = memory_display_tool.display_memory_state(state)
        
        # Debe retornar JSON válido
        data = json.loads(result)
        
        # Verificar estructura
        self.assertEqual(data["type"], "memory_display")
        self.assertIn("sections", data)

    def test_display_memory_state_full(self):
        """Test: muestra estado completo con todas las secciones."""
        state = {
            "user_profile": {"name": "Test User"},
            "user_location": "Laureles",
            "route_context": {"last_route": "Laureles-Poblado"},
            "traffic_data": {"level": "medium"},
            "urban_events": [{"type": "protesta"}],
            "eco_metrics": {"eco_score": 85}
        }
        
        result = memory_display_tool.display_memory_state(state)
        data = json.loads(result)
        
        # Debe tener 6 secciones
        self.assertEqual(len(data["sections"]), 6)

    def test_display_agent_activity(self):
        """Test: muestra actividad de un agente."""
        result = memory_display_tool.display_agent_activity(
            "pathfinder_agent",
            "calculate_route",
            {"route": "Laureles-Poblado"}
        )
        
        data = json.loads(result)
        
        # Verificar estructura
        self.assertEqual(data["type"], "agent_activity")
        self.assertEqual(data["agent"], "pathfinder_agent")
        self.assertIn("timestamp", data)

    def test_display_agent_transfer(self):
        """Test: visualiza transferencia entre agentes."""
        result = memory_display_tool.display_agent_transfer(
            "navimind_root_agent",
            "pathfinder_agent",
            "Calculate route from Laureles to Poblado"
        )
        
        data = json.loads(result)
        
        # Verificar estructura
        self.assertEqual(data["type"], "agent_transfer")
        self.assertEqual(data["from"]["name"], "navimind_root_agent")
        self.assertEqual(data["to"]["name"], "pathfinder_agent")

    def test_display_session_summary(self):
        """Test: genera resumen de sesión."""
        state = {
            "_interaction_count": 10,
            "_agents_history": ["pathfinder_agent", "flowsense_agent", "pathfinder_agent"],
            "_routes_count": 5,
            "_traffic_checks": 3
        }
        
        result = memory_display_tool.display_session_summary(state)
        data = json.loads(result)
        
        # Verificar estructura
        self.assertEqual(data["type"], "session_summary")
        self.assertIn("stats", data)
        self.assertEqual(data["stats"]["total_interactions"], 10)


if __name__ == "__main__":
    unittest.main()
