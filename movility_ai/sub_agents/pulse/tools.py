"""
Herramientas para Pulse Agent
"""

from movility_ai.tools.data_mock_tool import generate_mock_events
from movility_ai.tools.visualizer_tool import generate_event_alerts as viz_event_alerts


def _get_event_icon(event_type: str) -> str:
    """Devuelve el emoji correspondiente al tipo de evento"""
    icons = {
        "protesta": "🚨",
        "accidente": "🚗",
        "obra": "🚧",
        "concierto": "🎉",
        "partido": "⚽",
        "clima": "🌧️",
        "metro": "🚇",
        "festival": "🎭",
        "emergencia": "🚑"
    }
    return icons.get(event_type.lower(), "📍")


def _get_severity_icon(severity: str) -> str:
    """Devuelve el emoji de severidad"""
    severity_icons = {
        "crítico": "🔴",
        "alto": "🟠",
        "medio": "🟡",
        "bajo": "🟢"
    }
    return severity_icons.get(severity.lower(), "⚪")


def detect_urban_events(zones: list[str], tool_context) -> str:
    """
    Detecta eventos urbanos activos en las zonas especificadas
    
    Args:
        zones: Lista de zonas de Medellín a monitorear
        tool_context: Contexto de la herramienta ADK
        
    Returns:
        Reporte formateado con eventos urbanos detectados
    """
    # Generar eventos urbanos simulados
    events_data = generate_mock_events()
    
    # Filtrar eventos por zonas si se especifica
    if zones:
        filtered_events = [e for e in events_data if e.get("location", {}).get("zone") in zones]
        # Si no hay eventos en esas zonas, usar todos pero mencionar que son de otras zonas
        if not filtered_events:
            filtered_events = events_data[:3]  # Mostrar algunos eventos de ejemplo
    else:
        filtered_events = events_data
    
    # Guardar en contexto
    if hasattr(tool_context, 'state'):
        tool_context.state.last_urban_events = filtered_events
    
    # Formatear reporte visual
    report_lines = [
        "👂 **PULSE - MONITOR DE CONTEXTO URBANO**",
        "━" * 50,
        ""
    ]
    
    # Agrupar por severidad
    critical_events = [e for e in filtered_events if e.get("severity") == "crítico"]
    high_events = [e for e in filtered_events if e.get("severity") == "alto"]
    medium_events = [e for e in filtered_events if e.get("severity") == "medio"]
    low_events = [e for e in filtered_events if e.get("severity") == "bajo"]
    
    # Mostrar eventos críticos primero
    if critical_events:
        report_lines.append("🔴 **EVENTOS CRÍTICOS:**")
        for event in critical_events:
            event_icon = _get_event_icon(event.get("event_type", ""))
            location = event.get("location", {})
            zone = location.get("zone", "Desconocida")
            
            report_lines.extend([
                f"{event_icon} **{event.get('description', 'Sin descripción')}**",
                f"   📍 Ubicación: {zone}",
                f"   🕒 Horario: Activo ahora",
                f"   ⚠️ Impacto: {event.get('severity', 'medio').upper()}",
                ""
            ])
    
    # Eventos de alto impacto
    if high_events:
        report_lines.append("🟠 **EVENTOS DE ALTO IMPACTO:**")
        for event in high_events:
            event_icon = _get_event_icon(event.get("event_type", ""))
            location = event.get("location", {})
            zone = location.get("zone", "Desconocida")
            
            report_lines.extend([
                f"{event_icon} {event.get('description', 'Sin descripción')}",
                f"   📍 {zone}",
                ""
            ])
    
    # Resumen de eventos medios y bajos
    if medium_events or low_events:
        report_lines.extend([
            "━" * 50,
            "📊 **OTROS EVENTOS:**",
            f"🟡 {len(medium_events)} eventos de impacto medio",
            f"🟢 {len(low_events)} eventos de bajo impacto",
            ""
        ])
    
    # Agregar resumen
    report_lines.extend([
        "━" * 50,
        f"📌 **TOTAL DE EVENTOS DETECTADOS:** {len(filtered_events)}",
        f"🔴 Críticos: {len(critical_events)} | 🟠 Alto: {len(high_events)} | 🟡 Medio: {len(medium_events)} | 🟢 Bajo: {len(low_events)}",
        "",
        "💡 **TIP:** Usa `generate_event_alerts()` para ver alertas visuales priorizadas"
    ])
    
    return "\n".join(report_lines)


def generate_event_alerts(zones: list[str], tool_context) -> str:
    """
    Genera alertas visuales priorizadas de eventos urbanos
    
    Args:
        zones: Lista de zonas para generar alertas
        tool_context: Contexto de la herramienta ADK
        
    Returns:
        Alertas visuales en formato JSON para visualización
    """
    # Verificar si hay eventos guardados
    events_data = None
    if hasattr(tool_context, 'state') and hasattr(tool_context.state, 'last_urban_events'):
        events_data = tool_context.state.last_urban_events
    else:
        # Generar nuevos eventos si no existen
        events_data = generate_mock_events()
        if zones:
            events_data = [e for e in events_data if e.get("location", {}).get("zone") in zones]
    
    # Generar visualización usando la herramienta de visualización
    alerts_json = viz_event_alerts(events_data)
    
    # Agregar contexto adicional
    result_lines = [
        "🚨 **ALERTAS DE EVENTOS URBANOS - MEDELLÍN**",
        "━" * 50,
        "",
        alerts_json,
        "",
        "━" * 50,
        "📌 **LEYENDA DE PRIORIDADES:**",
        "🔴 CRÍTICO: Acción inmediata requerida",
        "🟠 ALTO: Planificar ruta alternativa",
        "🟡 MEDIO: Considerar en planificación",
        "🟢 BAJO: Información preventiva",
        "",
        "💡 Alertas actualizadas en tiempo real"
    ]
    
    return "\n".join(result_lines)
