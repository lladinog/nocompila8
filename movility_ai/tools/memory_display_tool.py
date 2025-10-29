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
🧠 Memory Display Tool - Muestra el estado y memoria del sistema.

Esta herramienta permite visualizar:
- Información recordada por los agentes
- Contexto compartido entre sub-agentes
- Historial de interacciones
- Estado actual del sistema

Útil para demostrar cómo el sistema mantiene contexto y aprende.
"""

import json
from typing import Dict, Any
from datetime import datetime


def display_memory_state(state: Dict[str, Any]) -> str:
    """
    Genera una visualización del estado de memoria del sistema.
    
    Args:
        state: Diccionario con el estado actual del sistema
        
    Returns:
        JSON string con la visualización de la memoria
    """
    memory_viz = {
        "type": "memory_display",
        "title": "🧠 Estado de Memoria del Sistema",
        "timestamp": datetime.now().isoformat(),
        "sections": []
    }
    
    # Sección de perfil de usuario
    if "user_profile" in state:
        memory_viz["sections"].append({
            "title": "👤 Perfil de Usuario",
            "icon": "👤",
            "data": state["user_profile"],
            "color": "#2196F3"
        })
    
    # Sección de ubicación actual
    if "user_location" in state:
        memory_viz["sections"].append({
            "title": "📍 Ubicación Actual",
            "icon": "📍",
            "data": state["user_location"],
            "color": "#4CAF50"
        })
    
    # Sección de contexto de ruta
    if "route_context" in state:
        memory_viz["sections"].append({
            "title": "🗺️ Contexto de Ruta",
            "icon": "🗺️",
            "data": state["route_context"],
            "color": "#FF9800"
        })
    
    # Sección de datos de tráfico
    if "traffic_data" in state:
        memory_viz["sections"].append({
            "title": "🚦 Datos de Tráfico",
            "icon": "🚦",
            "data": state["traffic_data"],
            "color": "#F44336"
        })
    
    # Sección de eventos urbanos
    if "urban_events" in state:
        memory_viz["sections"].append({
            "title": "⚠️ Eventos Urbanos",
            "icon": "⚠️",
            "data": state["urban_events"],
            "color": "#FFC107"
        })
    
    # Sección de métricas ecológicas
    if "eco_metrics" in state:
        memory_viz["sections"].append({
            "title": "🌱 Métricas Ecológicas",
            "icon": "🌱",
            "data": state["eco_metrics"],
            "color": "#8BC34A"
        })
    
    # Resumen de interacciones
    memory_viz["interaction_summary"] = {
        "total_queries": state.get("_interaction_count", 0),
        "agents_used": state.get("_agents_history", []),
        "session_start": state.get("_session_start", datetime.now().isoformat())
    }
    
    return json.dumps(memory_viz, indent=2, ensure_ascii=False)


def display_agent_activity(agent_name: str, action: str, result: Any) -> str:
    """
    Muestra la actividad de un agente específico.
    
    Args:
        agent_name: Nombre del agente
        action: Acción realizada
        result: Resultado de la acción
        
    Returns:
        JSON string con la visualización de la actividad
    """
    activity = {
        "type": "agent_activity",
        "agent": agent_name,
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "result": result,
        "icon": _get_agent_icon(agent_name),
        "color": _get_agent_color(agent_name)
    }
    
    return json.dumps(activity, indent=2, ensure_ascii=False)


def display_agent_transfer(from_agent: str, to_agent: str, context: str) -> str:
    """
    Visualiza la transferencia de control entre agentes.
    
    Args:
        from_agent: Agente que transfiere
        to_agent: Agente que recibe
        context: Contexto de la transferencia
        
    Returns:
        JSON string con la visualización de la transferencia
    """
    transfer = {
        "type": "agent_transfer",
        "title": "🔄 Transferencia de Agente",
        "from": {
            "name": from_agent,
            "icon": _get_agent_icon(from_agent)
        },
        "to": {
            "name": to_agent,
            "icon": _get_agent_icon(to_agent)
        },
        "context": context,
        "timestamp": datetime.now().isoformat(),
        "animation": "arrow_flow"
    }
    
    return json.dumps(transfer, indent=2, ensure_ascii=False)


def display_session_summary(state: Dict[str, Any]) -> str:
    """
    Genera un resumen de la sesión actual.
    
    Args:
        state: Estado completo del sistema
        
    Returns:
        JSON string con el resumen de la sesión
    """
    summary = {
        "type": "session_summary",
        "title": "📊 Resumen de Sesión",
        "stats": {
            "total_interactions": state.get("_interaction_count", 0),
            "agents_consulted": len(set(state.get("_agents_history", []))),
            "routes_calculated": state.get("_routes_count", 0),
            "traffic_checks": state.get("_traffic_checks", 0),
            "eco_score": state.get("eco_metrics", {}).get("eco_score", 0)
        },
        "most_used_agent": _get_most_used_agent(state.get("_agents_history", [])),
        "user_preferences": state.get("user_profile", {}),
        "session_duration": _calculate_session_duration(state.get("_session_start"))
    }
    
    return json.dumps(summary, indent=2, ensure_ascii=False)


# Helper functions

def _get_agent_icon(agent_name: str) -> str:
    """Retorna el icono apropiado para cada agente."""
    icons = {
        "pathfinder_agent": "🗺️",
        "flowsense_agent": "🚦",
        "pulse_agent": "📡",
        "navimind_root_agent": "🧭",
        "ecotrack_agent": "🌱",
        "insight_agent": "📊"
    }
    return icons.get(agent_name, "🤖")


def _get_agent_color(agent_name: str) -> str:
    """Retorna el color apropiado para cada agente."""
    colors = {
        "pathfinder_agent": "#2196F3",
        "flowsense_agent": "#F44336",
        "pulse_agent": "#FFC107",
        "navimind_root_agent": "#4CAF50",
        "ecotrack_agent": "#8BC34A",
        "insight_agent": "#9C27B0"
    }
    return colors.get(agent_name, "#757575")


def _get_most_used_agent(agents_history: list) -> str:
    """Determina el agente más utilizado en la sesión."""
    if not agents_history:
        return "Ninguno"
    
    from collections import Counter
    counter = Counter(agents_history)
    most_common = counter.most_common(1)
    return most_common[0][0] if most_common else "Ninguno"


def _calculate_session_duration(session_start: str) -> str:
    """Calcula la duración de la sesión."""
    if not session_start:
        return "Desconocida"
    
    try:
        start = datetime.fromisoformat(session_start)
        duration = datetime.now() - start
        minutes = int(duration.total_seconds() / 60)
        return f"{minutes} minutos"
    except:
        return "Desconocida"
