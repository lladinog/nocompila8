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
Tools para PathFinder Agent - Planificación de rutas multimodales.
"""

from typing import Optional
from movility_ai.tools import data_mock_tool, visualizer_tool


def calculate_route(
    origin: str,
    destination: str,
    preferred_mode: Optional[str] = None,
    tool_context=None
) -> str:
    """
    Calcula una ruta multimodal entre dos puntos en Medellín.
    
    Args:
        origin: Punto de origen (zona de Medellín)
        destination: Punto de destino (zona de Medellín)
        preferred_mode: Modo de transporte preferido (opcional)
        tool_context: Contexto del ADK (opcional para testing)
        
    Returns:
        String con descripción de la ruta calculada
    """
    # Generar ruta simulada usando data_mock_tool
    route_data = data_mock_tool.generate_mock_route(
        origin=origin,
        destination=destination,
        preferred_mode=preferred_mode
    )
    
    # Formatear respuesta
    response = f"✅ Ruta calculada de {origin} a {destination}\n\n"
    
    # Información general
    response += f"📊 **Resumen:**\n"
    response += f"⏱️ Tiempo total: {route_data['total_duration_minutes']} minutos\n"
    response += f"📏 Distancia: {route_data['total_distance_km']} km\n"
    response += f"💰 Costo total: ${route_data['total_cost_cop']:,} COP\n"
    response += f"🌱 Eco Score: {route_data['eco_score']}/100\n\n"
    
    # Segmentos de la ruta
    response += f"🗺️ **Segmentos de ruta:**\n"
    for i, segment in enumerate(route_data['segments'], 1):
        mode_icon = _get_mode_icon(segment['mode'])
        response += f"{i}. {mode_icon} **{segment['mode'].title()}**\n"
        response += f"   📍 {segment['from_location']} → {segment['to_location']}\n"
        response += f"   ⏱️ {segment['duration_minutes']} min | "
        response += f"💰 ${segment['cost_cop']:,} COP\n\n"
    
    # Guardar en contexto si está disponible
    if tool_context:
        try:
            tool_context.state['last_route'] = route_data
            tool_context.state['route_context'] = {
                'origin': origin,
                'destination': destination,
                'timestamp': 'now'
            }
        except:
            pass  # Ignorar si tool_context no está disponible
    
    return response


def visualize_route(
    origin: Optional[str] = None,
    destination: Optional[str] = None,
    tool_context=None
) -> str:
    """
    Genera una visualización de la ruta calculada con mapa visual e imagen.
    
    Args:
        origin: Origen de la ruta (opcional, usa el del contexto)
        destination: Destino de la ruta (opcional, usa el del contexto)
        tool_context: Contexto del ADK
        
    Returns:
        String con visualización enriquecida (imagen + link)
    """
    # Obtener datos de ruta del contexto o usar parámetros
    route_data = None
    actual_origin = origin
    actual_destination = destination
    
    if tool_context:
        try:
            route_data = tool_context.state.get('last_route')
            if route_data and not actual_origin:
                actual_origin = route_data['origin']['name']
                actual_destination = route_data['destination']['name']
        except:
            pass
    
    # Si no hay ruta en contexto ni parámetros, error
    if not actual_origin or not actual_destination:
        return "❌ Error: Debes especificar origen y destino o calcular una ruta primero"
    
    # Generar URL de Google Maps con direcciones
    origin_encoded = actual_origin.replace(" ", "+")
    destination_encoded = actual_destination.replace(" ", "+")
    
    google_maps_url = (
        f"https://www.google.com/maps/dir/{origin_encoded},+Medellín,+Colombia/"
        f"{destination_encoded},+Medellín,+Colombia"
    )
    
    # Imagen ilustrativa de Medellín desde Unsplash (ciudad, transporte)
    # Usamos diferentes imágenes según el modo predominante
    image_url = "https://images.unsplash.com/photo-1589981942335-c7f30747c0d4?w=800&q=80"  # Medellín ciudad
    
    # Generar respuesta visual con imagen embebida
    response = f"## 🗺️ Mapa Interactivo de Ruta\n\n"
    
    # Imagen visual de Medellín
    response += f"![Mapa de Ruta - {actual_origin} a {actual_destination}]({image_url})\n\n"
    
    response += f"### � Detalles de la Ruta\n\n"
    response += f"- **Origen:** {actual_origin}\n"
    response += f"- **Destino:** {actual_destination}\n\n"
    
    # Si hay datos de segmentos, mostrar resumen visual con badges
    if route_data:
        response += f"### 🛤️ Segmentos de la Ruta\n\n"
        for i, segment in enumerate(route_data['segments'], 1):
            mode_icon = _get_mode_icon(segment['mode'])
            response += f"{i}. {mode_icon} **{segment['mode'].title()}** - {segment['duration_minutes']} min\n"
        response += f"\n"
    
    response += f"### 🔗 Ver en Google Maps\n\n"
    response += f"👉 [**Abrir mapa interactivo en Google Maps**]({google_maps_url})\n\n"
    response += f"💡 *Haz clic en el link para ver la ruta completa con opciones de transporte en tiempo real.*\n"
    
    return response


def _get_mode_icon(mode: str) -> str:
    """Retorna el icono apropiado para cada modo de transporte."""
    icons = {
        "metro": "🚇",
        "metrocable": "🚠",
        "bus": "🚌",
        "bicicleta": "🚴",
        "caminando": "🚶",
        "carro": "🚗",
        "moto": "🏍️",
        "tranvia": "🚊"
    }
    return icons.get(mode.lower(), "🚶")
